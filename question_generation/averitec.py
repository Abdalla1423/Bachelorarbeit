from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages = [ 
    {"role": "user", "content": '''
Outrageously, United We Win claimed that "As mayor, Cory Booker, US Democratic
presidential candidate and US New Jersey Senator, passed criminal justice reform in a US
Republican Senate.". Criticism includes questions like: Did U.S. Sen. Cory Booker pass
criminal justice reform? What was the Republicans’ majority in the Senate when the bill was
signed into law?

Outrageously, Mokwele Kholofelo Banny claimed that "A married couple in Florida, Tito
and Amanda Watts, was arrested for selling fake golden tickets to heaven to hundreds of
people.". Criticism includes questions like: Did married couple Tito and Amanda Watts from
Florida get arrested for selling fake golden tickets to heaven?

Outrageously, Muhammadu Buhari claimed that "It makes no sense for oil to be cheaper in
Nigeria than in Saudi Arabia.". Criticism includes questions like: What was the price of
petrol in Nigeria in Oct 2020? What was the price of petrol in Saudi Arabia in Oct 2020?

Outrageously, Tea talk and gossip claimed that "Microsoft cofounder Bill Gates said Be nice
to nerds. Chances are you’ll end up working for one.". Criticism includes questions like: Is
Bill Gates quoted as saying "Be nice to nerds, chances are you'll end up working for one"?

Outrageously, Sen. Amy Klobuchar claimed that "US President Trump called for reduced
funding for the Centre for Disease Control and Prevention.". Criticism includes questions
like: Did US President Trump propose budget cuts in the funding for the Centre for Disease
Control and Prevention?

Outrageously, Paul Renner claimed that "For health risk exceptions in Florida's abortion amendment, “You're not even talking to a doctor to make that determination.”Criticism includes questions
like:
     '''}
  ]
)

print(completion.choices[0].message)