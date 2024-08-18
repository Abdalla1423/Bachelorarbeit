# 1000 Request per month
from langchain_community.retrievers import TavilySearchAPIRetriever
from dotenv import load_dotenv 

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from models.models import GPT_3

def tavily_qa_retriever(query):
    load_dotenv()
    retriever = TavilySearchAPIRetriever(k=3)

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

    result = chain.invoke({"question": query})
    
    return result

# print(tavily_qa_retriever("Is there free healthcare in the US"))