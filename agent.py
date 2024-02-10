from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_together import Together
from main import get_repo_name
import os
import requests 
import json
llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0,
    max_tokens=1024,
    together_api_key=os.environ.get('TOGETHER_API_KEY'),
)

from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain_community.utilities import SerpAPIWrapper
search = SerpAPIWrapper()
search_tool = Tool(
    name = "search",
    func=search.run,
    description="use this tool to get search the web and get information related to things which are not related to the repository. You should ask targeted questions"
)

from langchain_community.utilities import StackExchangeAPIWrapper
stackexchange = StackExchangeAPIWrapper()
stackexchange_tool = Tool(
    name="error-search",
    func=stackexchange.run,
    description="useful for when you need information regarding a programming error. You should pass the error directly"
)


from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")


# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import  tool
from query import answer_query

@tool
def get_repo_issues(url : str)->str:
    """ Use this tool to get the issues about the repo or any information about the issues of the repository """
    # Extract owner and repo names from the URL
    repo_url = os.getenv("collection_name")
    parts = repo_url.rstrip('.git').split('/')
    owner, repo = parts[-2], parts[-1]

    # GitHub API endpoint for issues
    api_url = f'https://api.github.com/repos/{owner}/{repo}/issues'

    try:
        # Make GET request to GitHub API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response and return issues
            result =  response.json()
            return json.dumps(result)
        else:
            return f"Error: Unable to fetch issues. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def retrieve_repo(question: str)->str:
    """" use this to get code from the repository or the project.You should look for file or Folder name or code snippets regarding the query.The input you give to this tool should be detailed
    if the question is a general question regarding the project for ex - "what is the repo about " then try to find the readme file"""

    result = answer_query(question,os.getenv("collection_name"))
    return result


from langchain import hub
from langchain.agents import create_react_agent,AgentExecutor
tools = [retrieve_repo,stackexchange_tool,search_tool,get_repo_issues]


# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/react")
prompt.template = """You are  Coding assistant , who answers questions based on the github repo or project or anything related to the world of tech,
Answer the following questions as best you can , However dont make up anything on your own, always try to look for relevant documents in the repo
. You have access to the following tools:
  {tools}
Use the following format:
Question: the input question you must answer 
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]( if you are going to use retrieve repo tool - 
IT IS VERY IMPORTANT TO ASK A DETAILED AND LENGTHY QUESTION TO GET QUALITY RESPONSE)
Action Input: the input to the action
Observation:  the result of the action,(here it is mandatory to check wether the observation is related to the question or not, if not repeat the process untill you are satisfied)
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer,
Final Answer:(in case of retrieve repo tool , the observation from the tool should be your final answer directly) the final answer to the original input question,You should first explain the concept in a clear and concise manner and  You should try to  provide code snippets for better understanding
Begin!
Question: {input}
Thought:{agent_scratchpad}"""
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)


conversational_agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=prompt
)

agent_executor = AgentExecutor(agent=conversational_agent, tools=tools,handle_parsing_errors=True,verbose=True)
def agent_query(query):
    result = agent_executor.invoke({"input":query});  
    print(result)
    return result["output"]