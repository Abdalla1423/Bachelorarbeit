from langchain_community.retrievers.you import YouRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

# set up runnable
runnable = RunnablePassthrough

# set up retriever, limit sources to one
retriever = YouRetriever(num_web_results=1)

# set up model
model = ChatOpenAI(model="gpt-3.5-turbo-16k")

# set up output parser
output_parser = StrOutputParser()

# set up prompt that expects one question
prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)

# set up chain
chain = (
    runnable.assign(context=(lambda x: x["question"]) | retriever)
    | prompt
    | model
    | output_parser
)

output = chain.invoke({"question": "what is the weather in NY today"})

print(output)