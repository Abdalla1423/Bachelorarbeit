from models.gpt import askGPT4
from models.llama import askLlamaOllama, askLlamaKISS

current_model = "GPT_4"


def setModel(model):
    global current_model
    current_model = model


def askModel(prompt, stop=None):
    if current_model == "GPT_4":
        return askGPT4(prompt, stop)
    else:
        return askLlamaKISS(prompt, stop)
