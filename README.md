# Intelligent File Search

## Overview

This is a demonstration of a **semantic and multi-modal File Search** system built using [Superlinked](https://github.com/superlinked/superlinked) and backed by the Qdrant Vector Database. Inspired by the hotel-search example, it’s tailored for intelligent discovery of files using natural language and metadata filters.

### 🔍 Features

- **Natural Language Queries:** Search files conversationally (e.g., _“recent PDFs about sport or cinema”_).
- **Multi-modal Semantic Search:** Combines content, filename, numeric size, and date metadata.
- **Hard Filters:** File type, tags, size range, and creation/modification dates.

---

## File Schema & Modalities

- **Text:**
  - `Content` – full-text semantic field
  - `Filename` – file name embedding
- **Numbers:**
  - `Size_kB` – size in kilobytes
- **Dates (recency-aware):**
  - `Creation_Date` – when file was created
  - `Last_Modified_Date` – last file modification date
- **Hard filters:**
  - `File_Type` – e.g. `["pdf"]`, `["docx"]`
  - `Tags` – e.g. `["sport", "cinema"]`

---

## Query Examples

- _“recent PDF files about sport or cinema”_
- _“Large Word documents about marketing”_
- _“Old reports tagged as archived”_
- _“text files under 50 KB with budget summary”_

---

## 📝 Notebooks

Explore and experiment with two helpful notebooks:

| Notebook                  | Purpose |
|---------------------------|---------|
| `notebooks/dataset_loading.ipynb`     | Shows loading of `combined_index.jsonl`. Demonstrates how the dataset is split and batched. Highlights the difference between fake/test data and production-ready data. |
| `notebooks/superlinked-queries.ipynb` | Demonstrates natural-language and manual-parameter queries. |

---

## ⚙️ Core Components

- **`superlinked_app/index.py`** – schema, spaces, and index definitions
- **`superlinked_app/query.py`** – query definitions, semantic & filter logic
- **`superlinked_app/nlq.py`** – natural-language-to-parameter conversion
- **`superlinked_app/api.py`** – REST endpoints and Qdrant integration

---

## 📘 Data Format Example

```json
{
  "id": "file_01",
  "Filename": "budget_2024.xlsx",
  "Path": "/data/reports/",
  "Size_kB": 1024.5,
  "File_Type": ["xlsx"],
  "Tags": ["finance", "budget"],
  "Creation_Date": 1672531199,
  "Last_Modified_Date": 1688102399,
  "Content": "Q1 2024 budget breakdown for marketing and operations..."
}


## Query with Simple Query (Without LLM)

This extension supports querying documents using a simplified query interface without relying on Large Language Models (LLMs). This feature enables quick and efficient searching based on straightforward query parameters.

### How It Works

You can pass a dictionary of parameters including a `simple_query` string and optional controls such as `limit` to fetch relevant documents. These parameters are expanded internally using the `expand_simple_query_params` function from the modified `query.py`, which transforms the input into detailed search parameters understood by the retrieval system.

For an example of how to use this feature, refer to the [Query with simple_query without LLM section](https://github.com/tatankam/intelligent-file-search/blob/main/notebooks/superlinked-queries.ipynb#query-with-simple_query-without-llm) in the project notebook.

### Modifications in `query.py`

The `query.py` module was enhanced to include the `expand_simple_query_params` function, which processes the `simple_query` and expands it into detailed search parameters. These changes improve the API usability by allowing natural language-like queries without the complexity of LLM-based parsing.

### Purpose of `nlq_nollm.py`

The `nlq_nollm.py` module was created to provide Natural Language Query (NLQ) functionality **without** using Large Language Models (LLMs). This is intended to improve responsiveness, reduce computational overhead, and enable usage in environments where LLMs are not available or feasible.

`nlq_nollm.py` relies on the enhanced query processing in `query.py` to interpret and execute NLQ using traditional parsing and parameter expansion, offering a balance between usability and system requirements.

