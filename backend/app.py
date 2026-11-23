
import re

from flask import Flask, jsonify, request
from flask_cors import CORS

from database import get_connection
from rag.source_retriever import search_chunks_with_sources
from rag.embeddings import model

app = Flask(__name__)
CORS(app)


DISCLAIMER = (
    "Disclaimer: CampusAI_Assistant is an automated basic AI system "
    "and may make errors. Please verify critical information directly "
    "with the relevant institutional department or official administration."
)

def create_focused_answer(question, results):
    """Answer using relevant sentences and retain their original sources."""

    not_found = (
        "The requested information was not found in "
        "the available institutional documents."
    )

    if not results:
        return not_found, []

    stop_words = {
        "what", "where", "when", "who", "why", "which",
        "how", "much", "many", "does", "do", "did",
        "is", "are", "was", "were", "the", "a", "an",
        "to", "for", "of", "in", "on", "at", "from",
        "and", "or", "with", "by", "be", "can", "could",
        "would", "should", "i", "we", "you", "me",
        "my", "your", "their", "it", "this", "that",
        "please", "tell", "give", "provide", "available",
        "information", "university", "maseno", "student",
        "students", "procedure"
    }

    def normalize_word(word):
        word = word.lower()

        if len(word) > 4 and word.endswith("ies"):
            return word[:-3] + "y"

        if len(word) > 4 and word.endswith("s"):
            return word[:-1]

        return word

    question_terms = {
        normalize_word(word)
        for word in re.findall(r"[a-zA-Z]+", question)
        if normalize_word(word) not in stop_words
    }

    if not question_terms:
        return not_found, []

    candidates = []

    for result in results:
        source = result.get("source")

        if not source:
            continue

        text = re.sub(r"\s+", " ", result["chunk_text"])

        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", text)
            if len(sentence.split()) >= 5
        ]

        for sentence in sentences:
            sentence_terms = {
                normalize_word(word)
                for word in re.findall(r"[a-zA-Z]+", sentence)
            }

            overlap = question_terms.intersection(sentence_terms)

            required_matches = min(2, len(question_terms))

            if len(overlap) < required_matches:
                continue

            candidates.append({
                "sentence": sentence,
                "source": source,
                "overlap": len(overlap)
            })

    if not candidates:
        return not_found, []

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    sentence_embeddings = model.encode(
        [item["sentence"] for item in candidates],
        normalize_embeddings=True
    )

    similarities = sentence_embeddings @ question_embedding

    ranked = sorted(
        zip(similarities, candidates),
        key=lambda item: item[0],
        reverse=True
    )

    best_score = float(ranked[0][0])

    if best_score < 0.30:
        return not_found, []

    selected = [
        item
        for score, item in ranked
        if float(score) >= max(0.30, best_score - 0.08)
    ][:3]

    answer_sentences = []
    selected_sources = []
    seen_sources = set()

    for item in selected:
        answer_sentences.append(
            item["sentence"].replace("Kshs ", "Kshs. ")
        )

        source = item["source"]

        source_key = (
            source.get("title"),
            source.get("version"),
            source.get("page_number"),
            source.get("section_heading"),
            source.get("paragraph_reference")
        )

        if source_key not in seen_sources:
            seen_sources.add(source_key)

            clean_source = dict(source)

            if clean_source.get("section_heading"):
                clean_source["section_heading"] = re.sub(
                    r"\s+", " ",
                    clean_source["section_heading"]
                ).strip()

            selected_sources.append(clean_source)

    return "\n".join(answer_sentences), selected_sources



@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "system": "Cam"
        "pusAI_Assistant",
        "message": "Welcome to CampusAI_Assistant",
        "status": "running"
    })


@app.route("/api/health", methods=["GET"])
def health():
    try:
        connection = get_connection()
        connection.close()
        database_status = "connected"
    except Exception:
        database_status = "not_connected"

    return jsonify({
        "system": "CampusAI_Assistant",
        "backend": "operational",
        "database": database_status,
        "status": "healthy"
    })


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Please enter a question."
        }), 400

    try:
        results = search_chunks_with_sources(question, limit=3)

        if not results:
            return jsonify({
                "answer": (
                    "The requested information was not found in "
                    "the available institutional documents."
                ),
                "sources": [],
                "disclaimer": DISCLAIMER
            })
        answer, selected_sources = create_focused_answer(
            question,
            results
        )

        sources = []

        for source in selected_sources:
            sources.append({
                "document_title": source.get("title"),
                "document_type": source.get("document_type"),
                "version": source.get("version"),
                "effective_date": (
                    str(source["effective_date"])
                    if source.get("effective_date") else None
                ),
                "section_heading": source.get("section_heading"),
                "paragraph_reference": source.get("paragraph_reference"),
                "page_number": source.get("page_number")
            })

        return jsonify({
            "question": question,
            "answer": answer,
            "sources": sources,
            "disclaimer": DISCLAIMER
        })

    except Exception as error:
        return jsonify({
            "error": str(error),
            "answer": (
                "An error occurred while processing your question."
            ),
            "sources": []
        }), 500   

       
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )
