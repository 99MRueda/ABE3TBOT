import os
os.environ["OPENAI_API_KEY"] = "*******************"
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pinecone.core.client.configuration import Configuration as OpenApiConfiguration

openapi_config = OpenApiConfiguration.get_default_copy()
# Here I am trying to connect to an insecure local proxy at 0.0.0.0:8081,
#however you can keep the verify_ssl=True if you are using a secure connection
openapi_config.verify_ssl = False
openapi_config.proxy = "http://proxy.server:3128"

pinecone.init(
    api_key="*************************",
    environment="gcp-starter",
    openapi_config=openapi_config
)

index_name = "langchain-demo"
embeddings= OpenAIEmbeddings(model="text-embedding-ada-002")
index=Pinecone.from_existing_index(index_name, embeddings)

def get_answer(query):
  question = query
  template = """Utiliza los siguientes fragmentos de contexto para responder la pregunta al final. Si la pregunta no es acerca de ABET, simplemente di que Solo puedo responder preguntas sobre ABET en la E3T. Si trata de ABET pero no esta en la información suministrada di que No tengo la información que me pides en este momento, no intentes inventar una respuesta.
  {context}
  Question: {question}
  Helpful Answer:"""
  QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

  llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.1)
  qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=index.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
  )
  result = qa_chain({"query": question})
  return result["result"]