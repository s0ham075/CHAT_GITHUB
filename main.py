import os
import shutil
import re
import git
from urllib.parse import urlparse

local_dir = os.getcwd()
branch = None

def get_repo_name(url):
    parsed_url = urlparse(url)
    repo_name = os.path.basename(parsed_url.path) # Extract the base name from the path (which is usually the repository name)
    # Remove the ".git" extension if it exists
    repo_name = repo_name[:-4]
    clean_string = re.sub(r'[^a-zA-Z]', '', repo_name) # remove non alphabetic characters
    return clean_string


def clone_repo(url):
   try:
        path = os.path.join(local_dir,"staging",get_repo_name(url))
        # Check if the repository already exists in the specified path
        if os.path.exists(path):
           print(f"{get_repo_name(url)} already added in db")
           return False
    
        repo = git.Repo.clone_from(url,path)
        global branch 
        branch = repo.head.reference
        print(f"{get_repo_name(url)} cloned succesfully")
        return True
   except Exception as e : 
       print(f"Error cloning the git repository: {e}")
       return False
   
def delete_cloned_repo(url):
    local_path = os.path.join(local_dir,"staging",get_repo_name(url))
    try:
        # Check if the local path exists
        if os.path.exists(local_path):
            # Use shutil.rmtree to remove the entire directory
            shutil.rmtree(local_path,ignore_errors=True)
            print(f"Repository at {local_path} successfully deleted.")
        else:
            print(f"Repository at {local_path} does not exist.")
    except Exception as e:
        print(f"Error deleting repository: {e}")

from langchain_community.document_loaders import GitLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import AstraDB
from astrapy.db import AstraDB as astra

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 3000,
    chunk_overlap  = 20,
)

from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = None


def load_repo(url):
    db = astra(token="AstraCS:BATxwaoHbsDRWctjGxgGFzvj:2fd4e930e73f98b42ee4c976a6deee5425ef3e73552d498adf7e628a15bc6fca",
        api_endpoint="https://39e4f0bb-6b50-45b2-bcc6-4d0dd1360f1c-us-east-2.apps.astra.datastax.com"
    )
    new_collection = db.create_collection(
    get_repo_name(url),
    dimension=384,
    )
    vectorstore = AstraDB(
    embedding=embeddings,
    collection_name=get_repo_name(url),
    api_endpoint= os.environ.get('ASTRA_DB_API_ENDPOINT'),
    token=os.environ.get('ASTRA_DB_TOKEN'),
    )
  
    print("collection created")
    try:
        loader = GitLoader(repo_path=os.path.join(local_dir,"staging",get_repo_name(url)), branch=branch, file_filter=lambda file_path: not file_path.endswith("package-lock.json"),)
        data = loader.load()
        chunks = text_splitter.split_documents(data)
        print("chunks created")
        vectorstore.add_documents(chunks)
        return True
    except Exception as e:
        print(f"Error loading and indexing repository: {e}") 
        return False

def repository_loader(url):
    result = False
    if(clone_repo(url)):
        result = load_repo(url)
    if result :
        delete_cloned_repo(url)



print('HELLO FROM CONTAINER')