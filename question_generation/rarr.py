from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages = [ 
    {"role": "user", "content": '''
I will check things you said and ask questions.
(1) You said: Your nose switches back and forth between nostrils. When you sleep, you switch about every 45 minutes. This
is to prevent a buildup of mucus. It's called the nasal cycle.
To verify it,
a) I googled: Does your nose switch between nostrils?
b) I googled: How often does your nostrils switch?
c) I googled: Why does your nostril switch?
d) I googled: What is nasal cycle?
(2) You said: The Stanford Prison Experiment was conducted in the basement of Encina Hall, Stanford's psychology building.
To verify it,
a) I googled: Where was Stanford Prison Experiment was conducted?
(3) You said: The Havel-Hakimi algorithm is an algorithm for converting the adjacency matrix of a graph into its adjacency
list. It is named after Vaclav Havel and Samih Hakimi.
To verify it,
a) I googled: What does Havel-Hakimi algorithm do?
b) I googled: Who are Havel-Hakimi algorithm named after?
(4) You said: "Time of My Life" is a song, by American singer-songwriter Bill Medley from the soundtrack of the 1987 film
Dirty Dancing. The song was produced by Michael Lloyd.
To verify it,
a) I googled: Who sings "Time of My Life"?
b) I googled: Who produced me some ty of tea
(5) You said: Kelvin Hopins was suspended from the Labor Party due to his membership in the Conservative Party.
To verify it,
a) I googled: Why was Kelvin Hopins suspended from Labor Party?
(6) You said: Social work is a profession that is based in the philosophical tradition of humanism. It is an intellectual
discipline that has its roots in the 1800s.
To verify it,
a) I googled: What philosophical tradition is social work based on?
b) I googled: what year does social work has its root in?
(7) You said: Half a million sharks could be killed to make the COVID-19 vaccine
To verify it:
     '''}
  ]
)

print(completion.choices[0].message)