import os
os.environ["OPENAI_API_KEY"] = "################"
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

pinecone.init(
    api_key="###############",
    environment="gcp-starter"
)

index_name = "langchain-demo"
embeddings= OpenAIEmbeddings(model="text-embedding-ada-002")
index=Pinecone.from_existing_index(index_name, embeddings)

def get_similiar_docs(query, k=2, score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query, k=k)
  else:
    similar_docs = index.similarity_search(query, k=k)
  return similar_docs

# model_name = "text-davinci-003"
model_name = "gpt-3.5-turbo"
# model_name = "gpt-4"
llm = ChatOpenAI(model_name=model_name)

chain = load_qa_chain(llm, chain_type="stuff")

def get_answer(query):
  similar_docs = get_similiar_docs(query)
  answer = chain.run(input_documents=similar_docs, question=query)
  return answer

#print(get_answer("Hola"))