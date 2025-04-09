import dspy
from qdrant_retriever import QdrantRetriever


class CardiologyInfoRetrievalSignature(dspy.Signature):
    """
    Answer the user's question in Ukrainian using only the retrieved content from official cardiology documents of the Ministry of Health of Ukraine.

    Instructions:
    1. Write a clear, medically accurate, and concise answer (max 100 words).
    2. Use only the retrieved content — do not add or assume anything beyond it.
    3. Include specific clinical details (e.g. medication names, timelines, procedures) if available.
    4. Do not simplify or generalize — reflect medical instructions exactly.
    5. At the end, add sources in the format:

       Джерела:
       1. Document Title, page X. [Link](URL)
    6. If no relevant content is found do not include any sources and return this (in Ukrainian):
       "Не знайдено інформації про [TOPIC] у документах розділу 'Кардіологія' Міністерства охорони здоров’я України."
    """
    user_input: str = dspy.InputField(
        desc="User input"
    )
    retrieved_docs: list[dict[str, str]] = dspy.InputField(
        desc="Retrieved cardiology documents from the Ministry of Health of Ukraine, including text and metadata"
    )
    output: str = dspy.OutputField(
        desc="Generated answer based on the retrieved content."
    )


class CardiologyRAGAgent(dspy.Module):
    """
    Specialized agent for searching cardiology information in medical guidelines.
    :param llm_model: str - The model to use for the agent.
    :param llm_model_kwargs: dict - The kwargs to pass to the model.
    :param retriever: QdrantRetriever - The retriever to use for the agent.
    """
    def __init__(self, llm_model: str, llm_model_kwargs: dict, retriever: QdrantRetriever):
        self.llm_model = llm_model
        self.llm_model_kwargs = llm_model_kwargs
        self.retriever = retriever
        self.agent = dspy.Predict(
            signature=CardiologyInfoRetrievalSignature)

    def forward(self, user_input: str):
        related_docs = self.retriever.search_medical_guidelines(user_input)
        result = self.agent(user_input=user_input, retrieved_docs=related_docs)
        return result
    
    def invoke(self, user_input: str):
        with dspy.settings.context(lm=dspy.LM(self.llm_model, **self.llm_model_kwargs)):
            return self.forward(user_input)
