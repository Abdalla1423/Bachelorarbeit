# 1000 Request per month
from langchain_community.retrievers import TavilySearchAPIRetriever
from dotenv import load_dotenv 

load_dotenv()
retriever = TavilySearchAPIRetriever(k=3)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from models.models import GPT_3

prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)
chain = (
    RunnablePassthrough.assign(context=(lambda x: x["question"]) | retriever)
    | prompt
    | GPT_3
    | StrOutputParser()
)

result = chain.invoke({"question": "how many units did bretch of the wild sell in 2020"})

print(result)