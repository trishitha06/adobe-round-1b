import os
import json
import time
from datetime import datetime
from utils.text_extractors import extract_relevant_sections

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
PERSONA_FILE = "/app/persona.json"

def load_persona(path: str):
    try:
        with open(path, "r") as f:
            data = json.load(f)
        persona = data.get("persona", "").strip()
        job = data.get("job_to_be_done", "").strip()
        if not persona or not job:
            raise ValueError("persona.json missing required keys.")
        return persona, job
    except Exception as e:
        raise RuntimeError(f"Failed to load persona file '{path}': {e}") from e

def main():
    start_time = time.time()
    persona, job = load_persona(PERSONA_FILE)

    document_files = sorted(f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf"))
    extracted_sections = []
    subsection_analysis = []

    for filename in document_files:
        path = os.path.join(INPUT_DIR, filename)
        sections, subsections = extract_relevant_sections(path, persona, job)

        for i, s in enumerate(sections):
            s_out = dict(s)
            s_out["document"] = filename
            s_out["importance_rank"] = i + 1
            extracted_sections.append(s_out)

        for i, sub in enumerate(subsections):
            sub_out = dict(sub)
            sub_out["document"] = filename
            sub_out["importance_rank"] = i + 1
            subsection_analysis.append(sub_out)

    output = {
        "metadata": {
            "input_documents": document_files,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "output.json"), "w") as f:
        json.dump(output, f, indent=2)

    end_time = time.time()
    print(f"✅ Output generated in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()