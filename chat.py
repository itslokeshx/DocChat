from langchain_groq import ChatGroq
question="what is attachment theory"
results = Vector_DB.similarity_search(query="what is attachment theory")
context = ""
for result in results:
    context += result.page_content
prompt = f"""
You are a helpful AI assistant.

Your task is to answer the user's question using ONLY the information provided in the context below.

Rules:
1. Answer only from the provided context.
2. Do not make up facts or use outside knowledge.
3. If the answer is not present in the context, reply:
   "I couldn't find that information in the provided document."
4. Keep the answer clear and concise.

==================== CONTEXT ====================

{context}

=================================================

Question:
{question}

Answer:
"""
llm = ChatGroq(model="llama-3.1-8b-instant",temperature=0.1,max_tokens=1024,api_key=GROQ_API)
response=llm.invoke(prompt)
response.content