import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def load_pdf_data():

    #Define the directory containing the text file and the persistent directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "document")
    persistent_dir = os.path.join(current_dir, "db", "chroma_db")

    #Check if the Chroma vector store already exists.
    if not os.path.exists(persistent_dir):
        print("Persistent directory deos not exists. Initializing vector store")
        
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"The directory named {data_dir}, does not exists."
            )
            
        #Loads the pdf files.
        loader = PyPDFDirectoryLoader(data_dir)
        documents = loader.load()
        
        #Split documents into chunks.
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents=documents)
        
        #Create vector embeddings
        embeddings = OllamaEmbeddings(
            model="llama3.1:8b"
        )
        
        #Create the vector store and persist it automatically
        db = Chroma.from_documents(
                documents=docs, embedding=embeddings, persist_directory=persistent_dir
            )