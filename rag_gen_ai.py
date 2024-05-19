import json
from typing import Dict
from langchain_community.llms import SagemakerEndpoint
from langchain_community.llms.sagemaker_endpoint import LLMContentHandler
from langchain_community.embeddings import SagemakerEndpointEmbeddings
from langchain_community.embeddings.sagemaker_endpoint import EmbeddingsContentHandler
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        input_str = json.dumps({"inputs": prompt, "parameters": model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]
    
content_handler = ContentHandler()

class EmbeddingsHandler(EmbeddingsContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs={}) -> bytes:
        input_str = json.dumps({"queries": prompt, "mode": "nn_train_data", **model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        embeddings = [[x[0]["score"]] for x in response_json]
        return embeddings

embeddings_handler = EmbeddingsHandler()
    
embeddings = SagemakerEndpointEmbeddings(
    endpoint_name='jumpstart-dft-multilingual-e5-base',
    region_name='us-west-2',
    content_handler=embeddings_handler
)

loader = PyPDFDirectoryLoader('./forex_report/')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=0
)

docs = text_splitter.split_documents(documents)

db = FAISS.from_documents(docs, embeddings)
db.save_local("qa.db")

prompt_template = "Search Content:\n{context}\nQuestion:{question}:\nAnswer:"

PROMPT = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])

chain = load_qa_chain(
    llm = SagemakerEndpoint(
        endpoint_name="jumpstart-dft-meta-textgeneration-llama-2-7b-f",
        region_name="us-west-2",
        content_handler=content_handler
    ),
    prompt=PROMPT
)

query = "美元/日圓"
search_results = db.similarity_search(query, k=3)

result = chain.run(input_documents=search_results, question=query)
print(result)