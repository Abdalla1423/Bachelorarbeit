from prompt_frameworks.corag import corag
from prompt_frameworks.hiss import hiss
from prompt_frameworks.rarr import rarr
from prompt_frameworks.baseline import base
from prompt_frameworks.keywords import keyword
from enum import Enum


class PF(Enum):
    CORAG = 'CORAG'
    HISS = 'HISS'
    RARR = 'RARR'
    BASELINE = 'BASELINE'
    KEYWORD = 'KEYWORD'


prompt_frameworks_fn = {
    PF.CORAG.value: corag,
    PF.HISS.value: hiss,
    PF.RARR.value: rarr,
    PF.BASELINE.value: base,
    PF.KEYWORD.value: keyword
}

prompt_frameworks_map = {
    "baseline": PF.BASELINE.value,
    "keyword": PF.KEYWORD.value,
    "rarr": PF.RARR.value,
    "corag": PF.CORAG.value,
    "hiss": PF.HISS.value,
}


class MODELS(Enum):
    GPT_4 = 'GPT_4'
    LLAMA_8B = 'LLAMA_8B'


model_map = {
    "gpt4": MODELS.GPT_4.value,
    "llama8b": MODELS.LLAMA_8B.value,
}


class RETRIEVER(Enum):
    SERPER_WEBSEARCH = 'SERPER_WEBSEARCH'


retriever_map = {
    "serper": RETRIEVER.SERPER_WEBSEARCH.value
}
