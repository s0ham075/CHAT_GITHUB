from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_together import Together

from langchain_community.vectorstores import AstraDB
from main import get_repo_name
import os 

from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

def get_prompt(instruction, new_system_prompt ):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template

sys_prompt = """You are a helpful, smart and intelligent coding assistant. Always answer as helpfully as possible using the context code provided. Your answers should only answer the question once, you can provide code snippets but make sure you explain them thoroughly

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. """

instruction = """CONTEXT CODE:/n/n {context}/n

Question: {question}"""


prompt_template = get_prompt(instruction, sys_prompt)
llama_prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

llama2_llm = Together(
    model="togethercomputer/llama-2-70b-chat",
    temperature=0.7,
    max_tokens=1024,
    together_api_key=os.environ.get('TOGETHER_API_KEY')
)


def process_llm_response(llm_response):
  response = " "
  response += llm_response['result'] + "\n\nSources\n"
  for source in llm_response['source_documents']:
     response +="Source - "+source.metadata['source'] +"\n"

  return response

def answer_query(query,url):
    vectorstore = AstraDB(
    embedding=embeddings,
    collection_name=get_repo_name(url),
    api_endpoint= os.environ.get('ASTRA_DB_API_ENDPOINT'),
    token=os.environ.get('ASTRA_DB_TOKEN'),
    )
    retriever = vectorstore.as_retriever(search_type='mmr')
    qa_chain = RetrievalQA.from_chain_type(llm= llama2_llm, chain_type_kwargs = {"prompt": llama_prompt},chain_type="stuff",retriever=retriever,return_source_documents = True)
    return process_llm_response(qa_chain(query))