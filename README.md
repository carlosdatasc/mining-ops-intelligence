# MINE-OS: Operational Intelligence System

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/AI-Scikit%20Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Viz-Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

> **An Artificial Intelligence suite for operational risk monitoring in mining, transforming unstructured text logs into real-time decision dashboards.**

---

## Operational Log Analyzer: From WhatsApp to Insights with NLP

### The Problem
In the current operational environment, companies suffer from **information overload**. Daily activity reports (often sent via WhatsApp or informal chats) generate thousands of lines of unstructured text. This causes managers to waste hours reading irrelevant messages instead of making strategic decisions.

### The Solution
An **End-to-End** solution that ingests raw text logs, processes them using **Natural Language Processing (NLP)** to classify events, and visualizes them in an Executive Dashboard. The goal is to transform "textual noise" into structured and actionable data.

---

## Privacy Notice & Synthetic Data
**Important:** Due to the sensitive nature of real operational information, this project was developed using **Synthetic Data**.

A data generation logic was implemented that replicates:
* Human writing patterns found in quick reports.
* Logical relationships between timestamps, vehicles, and incident types.

This ensures business confidentiality without sacrificing the technical validity of the **Proof of Concept**.

---

## Workflow (Pipeline)

1.  **Data Ingestion:** Extraction of logs from `.txt` files (simulating WhatsApp exports).
2.  **Pre-processing (Cleaning):**
    * Text normalization (lowercase, removal of accents).
    * Removal of stopwords and special characters.
    * Deduplication of redundant messages.
3.  **Feature Engineering:** Creation of structured DataFrames based on keywords and tags from the "Additional Details" (DA) column.
4.  **Modeling (NLP):** Event classification using `CountVectorizer` as the base vectorizer.
5.  **Visualization:** Dashboard generation for temporal analysis.

---

## Model Results

The base model achieved solid performance for operational incident classification:

| Metric | Result | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | **83%** | The model correctly classifies 8 out of 10 reports. |
| **Precision** | **90%** | When the model predicts a category, it is highly reliable. |
| **Recall** | **75%** | The model is able to recover the majority of relevant events. |

---

##Future Improvements & Scalability

To take this project to a production environment (**Enterprise Level**), the following updates are proposed:

* **Model:** Migrate from CountVectorizer to **TF-IDF** or neural Embeddings (**Word2Vec/BERT**) to better capture semantic context.
* **NER (Named Entity Recognition):** Implement entity recognition to automatically extract vehicle plates, driver names, and geographic locations.
* **Real Data:** Retrain the model with a real historical dataset to capture business-specific jargon.

---

## Tech Stack

This project uses a modern **End-to-End** architecture:

* **Frontend & UI:** Streamlit with **Custom CSS injection** (Glassmorphism design system).
* **AI Core:** Natural Language Processing (NLP) using **Scikit-Learn** (CountVectorizer).
* **Data Processing:** **Pandas** for log manipulation and temporal feature extraction (Feature Engineering).
* **Visualization:** **Plotly Express & Graph Objects** for interactive charts (Sunburst Charts, Stacked Areas).

---


