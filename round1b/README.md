# Approach Explanation – Round 1B
## Adobe India Hackathon 2025: Connecting the Dots

---

## 🔍 Problem Statement

The task is to analyze a collection of PDF documents and extract the most relevant **sections** and **subsections**, tailored to a given **persona** and their **job-to-be-done**. The output must be a structured JSON file, ranking these sections in order of importance.

---

� Technologies Used (Round 1B) 
--------------------------------
• PyMuPDF (fitz): PDF parsing and layout understanding 

• difflib: For fuzzy keyword matching 

• regex (re): Token extraction from job descriptions 

• json, os, time: File handling and metadata recording

## 🧠 High-Level Approach

Our solution simulates the behavior of an intelligent reader who:

1. Understands the **intent** of a user (persona + job).
2. **Scans documents** to identify candidate headings.
3. Matches and **ranks content** based on semantic relevance.
4. Extracts **refined paragraphs** under key headings for deeper insight.

---

## 🏗️ Key Components

### 1. **PDF Parsing with PyMuPDF**

We use the PyMuPDF library to extract:
- Text blocks
- Font size and formatting (bold, all-caps)
- Positioning (Y-axis, alignment)

This enables us to infer likely **section headings**.

---

### 2. **Heuristic Heading Detection**

We apply a combination of rules to identify meaningful headings:
- Font size relative to body text
- Bold or uppercase formatting
- Appears centered or top-aligned
- Matches known section keywords (e.g., “Introduction”, “Results”)

---

### 3. **Keyword Matching and Scoring**

We extract keywords from the `job_to_be_done` using regex and lowercase tokenization. For each detected heading, we compute a **relevance score** based on:

| Feature               | Score |
|------------------------|-------|
| Bold formatting        | +1    |
| All-caps heading       | +0.5  |
| Fuzzy keyword match    | +1.5  |

Fuzzy matching uses Python’s `difflib` to handle variations (e.g., “tree” vs “trees”).

---

### 4. **Refined Text Extraction**

For every matched heading, we extract the **nearby paragraph** (next block on the same page). This text provides richer context for the subsection analysis.

---

### 5. **Ranking and Output**

All matched sections and subsections are sorted by their scores. We assign an `importance_rank` and format the result in the required JSON schema.

---

## ✅ Highlights of Our Approach

- ✅ Lightweight and **offline**
- ✅ CPU-only, **no external models** used
- ✅ Modular design reused from Round 1A
- ✅ Generic scoring that **generalizes to any persona or document type**

---
� Docker Commands (Round 1B) 
------------------------------
Build Docker Image :
cd round1b docker build --no-cache --platform linux/amd64 -t mysolution:round1b . 

Run Docker Container: 
docker run --rm -v ${PWD}/../input:/app/input -v ${PWD}/../output:/app/output --network 
none mysolution:round1b 

## 🔒 Assumptions & Limitations

- Works best when headings are visually distinct (size or style)
- Does not perform deep semantic summarization (no LLMs used)
- Future improvements could include paragraph-level embedding similarity

---

## 🧪 Testing

Tested using:
- Academic PDFs (CS, Math)
- Technical reports and whitepapers
- Varying formatting styles (multi-column, justified)

Execution time is consistently under 60s for 3–5 PDFs.

---

## 📁 Output Example

```json
{
  "section_title": "Binary Search Trees",
  "page_number": 3,
  "refined_text": "Binary search trees are hierarchical data structures...",
  "importance_rank": 1
}
