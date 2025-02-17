import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


def get_answer(query):
    
    #Define the persistent directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persistent_dir = os.path.join(current_dir, "db", "chroma_db")
        
    #Define the embedding model.
    embeddings = OllamaEmbeddings(
            model="llama3.1:8b"
        )

    db = Chroma(
            embedding_function=embeddings, persist_directory=persistent_dir
    )

    #Retrieve relevant documents based on query

    retriever = db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "score_threshold": 0.5}, 
        )

    relevant_docs = retriever.invoke(query)
    
    combine_input = (
        "Here is a document that might help answer this question:"
        + query
        + "\n\nRelevant Document:\n"
        + "\n\n".join([doc.page_content for doc in relevant_docs])
        + "\n\nPlease provide a rough answer based only on the provided document. If the answer is not found in the documents, respond with 'I'm not sure.'"
    )

    model = ChatOllama(model="llama3.1:8b")

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=combine_input),
    ]

    result = model.invoke(messages)
    
    return result.content

