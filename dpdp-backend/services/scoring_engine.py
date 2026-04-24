import matplotlib
matplotlib.use("Agg")

import os
import json
import re
import numpy as np
import matplotlib.pyplot as plt
import time
import logging

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from core.config import settings
from core.config import USE_EXTERNAL_API, EXTERNAL_API_KEY

# ==============================
# Logging Setup
# ==============================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==============================
# Caching
# ==============================
cache = {}

def get_cached_result(policy_text):
    if policy_text in cache:
        logging.info("Returning cached result")
        return cache[policy_text]
    return None

def save_cache(policy_text, result):
    cache[policy_text] = result
    logging.info("Saved result to cache")

# ==============================
# Retry Logic
# ==============================
def call_llm_with_retry(prompt, retries=3):
    import google.generativeai as genai
    genai.configure(api_key=EXTERNAL_API_KEY)
    model = genai.GenerativeModel("gemini-pro")

    for i in range(retries):
        try:
            response = model.generate_content(prompt, generation_config={"temperature": 0.1}, request_options={"timeout": 10})
            return response.text
        except Exception as e:
            logging.warning(f"Retry {i+1} failed: {e}")
            if i < retries - 1:
                time.sleep(2)
    raise Exception("LLM failed after retries")


# ==============================
# Load Semantic Model
# ==============================
model = None
if SentenceTransformer is not None:
    try:
        model = SentenceTransformer(settings.MODEL_NAME)
    except Exception:
        model = None


def simple_encode(texts):
    tokens_list = [re.findall(r"\w+", text.lower()) for text in texts]
    vocab = {}
    for tokens in tokens_list:
        for token in tokens:
            if token not in vocab:
                vocab[token] = len(vocab)

    vectors = np.zeros((len(texts), len(vocab)), dtype=float)
    for i, tokens in enumerate(tokens_list):
        for token in tokens:
            vectors[i, vocab[token]] += 1
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return vectors / norms


def encode_texts(texts):
    if model is not None:
        return model.encode(texts)
    return simple_encode(texts)


def analyze_with_llm(policy_text, clauses):
    prompt = f"""
You are an expert auditor for India's DPDP Act.

TASK:
Evaluate the given privacy policy against DPDP compliance.

INPUT:
Privacy Policy:
{policy_text}

DPDP Clauses:
{json.dumps(clauses, indent=2)}

INSTRUCTIONS:
- Analyze each clause carefully
- Assign a compliance score (0–100)
- Identify risks and missing elements
- Be strict and professional

OUTPUT FORMAT (STRICT JSON ONLY):
{{
    "overall_score": number,
    "risk_level": "Low" | "Medium" | "High",
    "clause_analysis": [
        {{
            "clause": "Clause name",
            "score": number,
            "status": "Compliant" | "Partial" | "Non-Compliant",
            "reason": "Short explanation"
        }}
    ],
    "recommendations": ["..."]
}}
"""

    raw = call_llm_with_retry(prompt)
    return raw


def clean_json(response_text):
    response_text = response_text.strip()

    if response_text.startswith("```"):
        parts = response_text.split("```")
        if len(parts) > 1:
            response_text = parts[1]
        if response_text.startswith("json"):
            response_text = response_text[4:].strip()

    return json.loads(response_text)


def analyze_with_local_model(policy_text):
    clauses = load_clauses()

    results = {}
    missing = []
    total_score = 0
    clause_names = []
    clause_scores = []
    explanations = []

    sentences = [
        s.strip()
        for s in policy_text.split(".")
        if len(s.strip()) > 20
    ]

    if not sentences:
        return {
            "overall_score": 0,
            "risk_level": "High Risk",
            "section_analysis": {},
            "missing_clauses": [],
            "recommendations": [],
            "graph_path": "",
            "explanations": []
        }

    # Encode policy sentences
    sentence_embeddings = encode_texts(sentences)

    for clause in clauses:

        clause_title = clause["title"]
        clause_text = clause["description"]
        clause_section = clause["section"]
        clause_category = clause["category"]

        clause_embedding = encode_texts([clause_text])

        similarities = cosine_similarity(
            clause_embedding,
            sentence_embeddings
        )[0]

        best_index = int(np.argmax(similarities))
        best_sentence = sentences[best_index]

        similarity_score = float(similarities[best_index]) * 100
        final_score = round(similarity_score, 2)

        clause_names.append(clause_title)
        clause_scores.append(final_score)

        total_score += final_score

        explanations.append({
            "clause_title": clause_title,
            "section": clause_section,
            "category": clause_category,
            "policy_sentence": best_sentence,
            "similarity_score": final_score
        })

        if final_score >= settings.SIMILARITY_THRESHOLD:

            results[clause_title] = {
                "section": clause_section,
                "category": clause_category,
                "similarity_score": final_score,
                "status": "Matched"
            }

        else:

            missing.append(clause_title)

            results[clause_title] = {
                "section": clause_section,
                "category": clause_category,
                "similarity_score": final_score,
                "status": "Missing"
            }

    overall_score = round(total_score / len(clauses), 2)

    # ==============================
    # Risk Classification
    # ==============================
    if overall_score >= 75:
        risk = "Low Risk"
    elif overall_score >= 45:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    # ==============================
    # Generate Recommendations
    # ==============================
    recommendations = []

    if missing:
        for clause in missing:
            recommendations.append(
                f"The privacy policy should include a section for '{clause}' to improve DPDP compliance."
            )
    else:
        recommendations.append(
            "The privacy policy appears well aligned with DPDP Act 2023 requirements."
        )

    # ==============================
    # Generate Compliance Graph
    # ==============================
    if not os.path.exists("reports"):
        os.makedirs("reports")

    graph_path = "reports/compliance_chart.png"

    plt.figure(figsize=(10, 5))
    plt.bar(clause_names, clause_scores)
    plt.xlabel("DPDP Clauses")
    plt.ylabel("Similarity Score (%)")
    plt.title("DPDP Compliance Clause Analysis")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()

    return {
        "overall_score": overall_score,
        "risk_level": risk,
        "section_analysis": results,
        "missing_clauses": missing,
        "recommendations": recommendations,
        "graph_path": graph_path,
        "explanations": explanations
    }


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a_norm = np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = np.linalg.norm(b, axis=1, keepdims=True)
    a_norm[a_norm == 0] = 1
    b_norm[b_norm == 0] = 1
    return np.dot(a, b.T) / (a_norm * b_norm.T)


# ==============================
# Load DPDP Clauses
# ==============================
def load_clauses():

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, "data", "dpdp_clauses.json")

    if not os.path.exists(file_path):
        alt_path = os.path.join(os.getcwd(), "data", "dpdp_clauses.json")
        if os.path.exists(alt_path):
            file_path = alt_path

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"DPDP clauses file not found. Checked: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================
# AI Compliance Analysis
# ==============================
def analyze_compliance(policy_text: str):

    # Check cache first
    cached = get_cached_result(policy_text)
    if cached:
        return cached

    clauses = load_clauses()

    if USE_EXTERNAL_API:
        logging.info("Using external API for analysis")
        try:
            llm_response = analyze_with_llm(policy_text, clauses)
            result = clean_json(llm_response)
            # Add missing fields for compatibility
            result.setdefault("section_analysis", {})
            result.setdefault("missing_clauses", [])
            result.setdefault("graph_path", "")
            result.setdefault("explanations", [])
            save_cache(policy_text, result)
            return result
        except Exception as e:
            logging.error(f"LLM parsing failed, fallback to local model: {e}")
            # Fall through to local logic

    # Local model logic
    logging.info("Using local model for analysis")
    result = analyze_with_local_model(policy_text)
    save_cache(policy_text, result)
    return result