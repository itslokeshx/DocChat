def build_prompt(context, question):
    return f"""You are a helpful AI assistant that answers questions strictly based on a provided document.

Instructions:
- Read the context carefully and answer the question based on it.
- Synthesize the information naturally — do not copy chunks verbatim.
- If the context genuinely does not contain enough information to answer, say exactly:
  "I couldn't find relevant information about that in the document."
- Do NOT refuse if the context clearly addresses the question.

Context:
------------------------
{context}
------------------------

Question: {question}

Answer:"""