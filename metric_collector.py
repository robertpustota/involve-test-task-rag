import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm
from collections import defaultdict
from deepeval.test_case import LLMTestCase
from deepeval.metrics import BaseMetric
from deepeval import evaluate
from deepeval.evaluate import aggregate_metric_pass_rates

class VisualMetricCollector:
    def __init__(self, 
                 metrics: list[BaseMetric],
                 retriever: BaseMetric,
                 agent):
        self.metrics = metrics
        self.retriever = retriever
        self.agent = agent
        self.test_cases = []
        self.metric_scores = pd.DataFrame()

    def collect_test_cases(self, questions: list[str], answers: list[str] | None = None):
        if answers is not None and len(questions) != len(answers):
            raise ValueError("Questions and answers must have the same length")

        self.test_cases = []

        for question in tqdm(questions, total=len(questions), desc="Creating test cases"):
            retrieved_docs = [str(doc["text"]) for doc in self.retriever.search_medical_guidelines(question)]
            result = self.agent.invoke(question)

            # If answers are not provided, use None for expected_output
            expected_output = answers[questions.index(question)] if answers else None
            
            # Create test case
            test_case = LLMTestCase(
                input=question,
                actual_output=result.output,
                expected_output=expected_output,
                retrieval_context=retrieved_docs
            )
            self.test_cases.append(test_case)

        return self.test_cases

    def collect_metric_results(self):
        if not self.test_cases:
            raise ValueError("Test cases not collected. Run collect_test_cases first.")

        # Run DeepEval evaluation
        evaluation_result = evaluate(self.test_cases, metrics=self.metrics, print_results=False)
        aggregate_metric_pass_rates(evaluation_result.test_results)
        # Prepare a score dictionary per test case
        data = defaultdict(list)
        for result in evaluation_result.test_results:
            data["Input"].append(result.input)

            for metric_data in result.metrics_data or []:
                data[metric_data.name].append(metric_data.score)

        # Store as DataFrame
        self.metric_scores = pd.DataFrame(data)
        return self.metric_scores

    def visualize(self):
        if self.metric_scores.empty:
            raise ValueError("No metric results to visualize. Run collect_metric_results_async() first.")

        self.metric_scores.set_index("Input").plot(kind="bar", figsize=(12, 6))
        plt.title("LLM Evaluation Metric Scores")
        plt.ylabel("Score")
        plt.ylim(0, 1.1)
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()
