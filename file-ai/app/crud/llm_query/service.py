from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from app.core.utils.utils import extract_text


class LLMQueryService:
    def __init__(self, llm_model : OllamaLLM):
        self.llm_model = llm_model
        self.prompt = ChatPromptTemplate.from_template("""
You are an assistant for business document summarization.
ONLY use the information provided in the documents below to answer the question.
If the answer is not present in the documents, reply: "I don't know based on the provided documents."
Be concise and structured.

Question: {question}

Documents:
{documents}

Answer:
""")
        self.chain = self.prompt | self.llm_model

    
    '''
    get docs after file vector search 
    '''
    async def async_structured_answer(self, query: str, docs: list):
        # Extract text from MongoDB docs (customize field as needed)
        documents_str = "\n\n".join([extract_text(doc) for doc in docs])

        response = await self.chain.ainvoke({
            "question": query,
            "documents": documents_str
        })

        return response
