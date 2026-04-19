import os
import json
from groq import Groq
from core.services.rag_service import RAGService
from apps.documents.models import Document


class QuestionService:

    @staticmethod
    def generate_questions(document_id, num_questions, difficulty, topic=None):

        client = Groq(api_key=os.environ["GROQ_API_KEY"])

        # ---------------- Get Document ----------------
        doc = Document.objects.get(id=document_id)

        query = topic if topic else "important concepts"

        # ---------------- Retrieve Context ----------------
        chunks = RAGService.retrieve_relevant_chunks(query, doc)

        if not chunks:
            raise Exception("No relevant content found")

        context = "\n".join(chunks)

        # ---------------- Strong Prompt ----------------
        prompt = f"""
You are an academic question generator.

STRICT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- No extra text
- Ensure JSON is parsable

FORMAT:
{{
  "mcqs": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "answer": "string"
    }}
  ],
  "descriptive": [
    {{
      "question": "string",
      "answer": "string"
    }}
  ]
}}

Generate EXACTLY {num_questions} questions.
Split reasonably between MCQs and descriptive.

Difficulty: {difficulty}

Context:
{context}
"""

        # ---------------- Call LLM ----------------
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You output strictly valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        raw_output = response.choices[0].message.content.strip()

        # ---------------- Parse JSON Safely ----------------
        try:
            parsed_output = json.loads(raw_output)
        except json.JSONDecodeError:
            # fallback if model messes up
            parsed_output = {
                "error": "Invalid JSON from model",
                "raw_output": raw_output
            }

        return parsed_output