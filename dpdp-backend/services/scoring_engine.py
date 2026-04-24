import matplotlib
matplotlib.use("Agg")

import os
import json
import re
import numpy as np
import matplotlib.pyplot as plt

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from core.config import settings
from core.config import USE_EXTERNAL_API, EXTERNAL_API_KEY


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
    import google.generativeai as genai

    genai.configure(api_key=EXTERNAL_API_KEY)

    prompt = f"""
You are an expert Indian DPDP Act auditor.

Analyze the following privacy policy:

{policy_text}

Against these clauses:
{json.dumps(clauses, indent=2)}

Return ONLY JSON:
{{
    "overall_score": number,
    "risk_level": "Low/Medium/High",
    "explanations": ["..."]
}}
"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text


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

    clauses = load_clauses()

    if USE_EXTERNAL_API:
        try:
            llm_response = analyze_with_llm(policy_text, clauses)
            result = json.loads(llm_response)
            # Add missing fields for compatibility
            result.setdefault("section_analysis", {})
            result.setdefault("missing_clauses", [])
            result.setdefault("recommendations", [])
            result.setdefault("graph_path", "")
            return result
        except Exception as e:
            print(f"API failed, fallback to local model: {e}")
            # Fall through to local logic

    # Local model logic continues

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