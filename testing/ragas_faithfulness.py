from datasets import Dataset 
from ragas.metrics import FaithulnesswithHHEM
from ragas import evaluate

faithfulness_with_hhem = FaithulnesswithHHEM()
data_samples = {
    'question': ['When was the first super bowl?', 'Who won the most super bowls?'],
    'answer': ['The first superbowl was held on Jan 15, 1967', 'The most super bowls have been won by The New England Patriots'],
    'contexts' : [['The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles,'], 
    ['The Green Bay Packers...Green Bay, Wisconsin.','The Packers compete...Football Conference']],
}
dataset = Dataset.from_dict(data_samples)
score = evaluate(dataset,metrics=[faithfulness_with_hhem])
df = score.to_pandas()
df.to_excel('faithfulnes.xlsx')

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
