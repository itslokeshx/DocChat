def build_prompt(context, question):
    return f"""
You are a helpful AI assistant.

Answer ONLY using the context below.

Rules:
- Do not use outside knowledge.
- If the answer is not present, say:
  "I couldn't find that information in the document."

Context:
------------------------
{context}
------------------------

Question:
{question}

Answer:
"""