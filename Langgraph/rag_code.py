from langchain import embeddings
from langchain import vectorstores
from langchain.embeddings import OpenaAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.embeddings.openai import OpenAIEmbeddings

#loading the docs

docs =  ["Company policy text...", "Another document..."]

#create embeddings
embeddings = OpenAIEmbeddings()

#Storing in vector db
vectorstore = FAISS.from_texts(docs, embeddings)

#create retriever
retriever = vectorstore.as_retriever()

#create rag chain
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=retriever
)

#Query
response = qa.run("What is company policy?")
print(response)