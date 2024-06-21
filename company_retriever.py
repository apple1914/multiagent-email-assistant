from langchain_community.document_loaders import JSONLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.tools.retriever import create_retriever_tool


embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
loader = JSONLoader(file_path="../data/companies.json", jq_schema=".[]", text_content=False)
documents = loader.load()

db = Chroma.from_documents(documents, embedding_function)
retriever = db.as_retriever()

from langchain.tools.retriever import create_retriever_tool

company_retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_movie_tool",
    "Based on the query, find best company that fits the criteria.",
)

# @tool
# def company_retriever_tool(query: str) -> str:
#     """Consult the company docs and answer question based on the context"""
#     docs = retriever.query(query, k=1)
#     return "\n\n".join([doc["page_content"] for doc in docs])