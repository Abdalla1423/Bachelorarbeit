from datasets import Dataset 
from ragas.metrics import FaithulnesswithHHEM
from ragas import evaluate
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = os.environ.get("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_ENDPOINT"] = os.environ.get("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT")

q = [' Is it true that More than half of all black children live in single-parent households, a number that has doubled — doubled — since we were children.']
a = ['The claim that Barack Obama stated that more than half of all black children live in single-parent households, and that this number has doubled since his childhood, is true. This statement was made by Obama in a 2008 Father’s Day speech, where he emphasized the importance of fathers in the family and the impact of single parenthood on the African American community. He noted that the number of black children living in single-parent households had doubled since his own childhood, highlighting the increasing prevalence of this family structure within the black community. Therefore, the claim is accurate and reflects Obamas statements on this issue.']
con = [  
        [
            "We know that more than half of all black children live in single-parent households, a number that has doubled — doubled — since we were children ...",
            "We know that more than half of all black children live in single-parent households, a number that has doubled—doubled—since we were children… And the foundations of our community are weaker because of it.” –Barack Obama. When it comes to race, one of the most gifted writers on the contemporary American scene is Ta-Nehisi Coates. In a 2008 Father’s Day speech, then-Senator Obama observed, correctly, that fathers are 'critical' to the family, and that the foundations of the African American community are more fragile than they might otherwise be because many black children are growing up in a home without their own father. On this subject, Barack Obama, not Ta-Nehisi Coates, gets it right.",
            "Mr. Obama noted that 'more than half of all black children live in single-parent households,' a number that he said had doubled since his own childhood. Speaking in Texas in February, Mr. Obama told the mostly black audience to take responsibility for the education and nutrition of their children, and lectured them for feeding their children 'cold Popeyes' for breakfast. 'I say this knowing that I have been an imperfect father,' he said, 'Knowing that I have made mistakes and I’ll continue to make more, wishing that I could be home for my girls and my wife more than I am right now.' The Obama campaign added the speech to Mr. Obama’s schedule on Saturday, when he returned to Chicago after a campaign swing through Pennsylvania and Ohio.",
            "We know that more than half of all black children live in single-parent households, a number that has doubled-doubled-since we were children… And the foundations of our community are weaker because of it.” –Barack Obama. When it comes to race, one of the most gifted writers on the contemporary American scene is Ta-Nehisi Coates. In a 2008 Father’s Day speech, then-Senator Obama observed, correctly, that fathers are 'critical' to the family, and that the foundations of the African American community are more fragile than they might otherwise be because many black children are growing up in a home without their own father. The bottom line: Obama was right to say that African American dads matter; clearly, blacks boys and girls are more likely to flourish when they are raised in a home with their biological parents."
        ]
]

# faithfulness_with_hhem = FaithulnesswithHHEM()
# data_samples = {
#     'question': q,
#     'answer': a,
#     'contexts' : con,
# }
# dataset = Dataset.from_dict(data_samples)
# score = evaluate(dataset,metrics=[faithfulness_with_hhem])
# df = score.to_pandas()
# df.to_excel('faithfulnes.xlsx')

# from datasets import Dataset 
# from ragas.metrics import faithfulness
# from ragas import evaluate

# data_samples = {
#     'question': ['When was the first super bowl?', 'Who won the most super bowls?'],
#     'answer': ['The first superbowl was held on Jan 15, 1967', 'The most super bowls have been won by The New England Patriots'],
#     'contexts' : [['The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles,'], 
#     ['The Green Bay Packers...Green Bay, Wisconsin.','The Packers compete...Football Conference']],
# }
# dataset = Dataset.from_dict(data_samples)
# score = evaluate(dataset,metrics=[faithfulness])
# df = score.to_pandas()
# df.to_excel('faithfulnes.xlsx')

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from ragas.metrics import faithfulness
from ragas import evaluate
from datasets import Dataset 
from langchain_openai import ChatOpenAI



langchain_llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
)

langchain_embeddings = OllamaEmbeddings(
    model="llama3.1"
)


data_samples = {
    'question': q,
    'answer': a,
    'contexts' : con,
}
dataset = Dataset.from_dict(data_samples)

results = evaluate(dataset, metrics=[faithfulness], llm=langchain_llm, embeddings=langchain_embeddings)
df = results.to_pandas()
df.to_excel('faithfulnes.xlsx')

