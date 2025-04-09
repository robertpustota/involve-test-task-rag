# 🩺 Test Task – Medical RAG Agent for Involve

This repository contains the implementation of a **technical test task** for the company **Involve**. The goal is to design and implement a complete **Retrieval-Augmented Generation (RAG)** system for answering user questions based on **official medical guidelines** from the Ministry of Health of Ukraine.

---

## 📌 Solution Overview

The task was divided into four key stages:

### 1. 🧾 Automatic PDF Collection
- **Goal**: Download all documents from the *Cardiology* section at [guidelines.moz.gov.ua](https://guidelines.moz.gov.ua/documents).
- **Challenge**: The website is protected by **Cloudflare** and renders documents via JavaScript.
- **Solution**:  
  - Used `undetected_chromedriver` + `selenium` to simulate browser interaction.
  - Navigated the page and parsed HTML with `BeautifulSoup`.
  - Enabled headless PDF downloads with Chrome DevTools Protocol.
  - Saved metadata: document title, download URL, page numbers.
  - Initially, using a real Chrome user profile was also considered to improve bypass reliability. However, this approach was not chosen in order to maintain transparency and reproducibility of the solution for demonstration purposes.


---

### 2. 🧠 Vector Indexing for Semantic Search
- **Goal**: Transform PDFs into searchable knowledge using vector embeddings.
- **Steps**:
  - Performed **page-based chunking** for optimal granularity.
  - Used the **OpenAI API** to generate semantic embeddings.
  - Stored embeddings and metadata in **Qdrant** (local Docker container).

---

### 3. 🤖 Question Answering with DSPy
- **Goal**: Build a QA agent that returns fact-based answers from the documents.
- **Framework**: Implemented using **DSPy**, a modern library for building composable reasoning pipelines.
- **Behavior**:
  - Agent retrieves most relevant document chunks via vector similarity.
  - Generates grounded answers using OpenAI with clear **source citation** (document + page).
  - Ensures faithfulness and avoids hallucination by guiding the prompt.

---

### 4. 📊 Automated Evaluation
- **Goal**: Automatically assess the quality of agent answers using reference data.
- **Library**: Used `DeepEval` and custom `GEval` to benchmark factuality, relevance, and source attribution.
- **Metrics**:
  - `ContextualPrecisionMetric`
  - `ContextualRecallMetric`
  - `ContextualRelevancyMetric`
  - `AnswerRelevancyMetric`
  - `FaithfulnessMetric`
  - `GEval` for checking if the cited source matches the claim.

---

## 🧰 Technology Stack

| Purpose              | Tools / Libraries                                |
|----------------------|--------------------------------------------------|
| Web scraping         | `undetected-chromedriver`, `selenium`, `bs4`     |
| PDF chunking         | `PyMuPDF`                                        |
| Embedding generation | `OpenAI API`                                     |
| Vector search        | `Qdrant` (Docker)                                |
| QA system            | `DSPy`, `OpenAI`                                 |
| Evaluation           | `DeepEval`, `matplotlib`, custom `GEval`         |

---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/robertpustota/involve-test-task-rag.git
cd involve-test-task-rag
```

### 2. Create Environment File

```env
# .env
# OpenAI API Key
OPENAI_API_KEY=sk-...

# Qdrant base URL
QDRANT_URL=http://localhost:6333
```

### 4. Start Qdrant in Docker
```bash
docker run -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

```bash
jupyter notebook InvolveTestTask.ipynb
```
Follow each step in the notebook to:

1. Download PDF files.

2. Build and store vector embeddings.

3. Answer user queries.

4. Evaluate the quality of responses.

### ⚠️ CAPTCHA Notice

When running the notebook, especially during the **PDF scraping step**, you will see a **browser window open via `undetected-chromedriver`**.

This is expected — the script simulates a real user to **bypass Cloudflare protection**.

If Cloudflare presents a **CAPTCHA**, you'll need to **solve it manually in the browser window**. After that, the script will continue automatically.

✅ Most of the time, the bypass works **without manual intervention**, but in some cases (especially on the first run or from a new IP), a CAPTCHA might appear.

❗ You might need to solve the CAPTCHA **more than once**, depending on the website's security behavior.


## 👤 Author
Submitted by: Artem Sydorenko
For: Involve – Technical Test Task
[kradworkmail@gmail.com]
