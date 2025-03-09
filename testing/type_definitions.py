from prompt_frameworks.ragar import multiCoRAG
from prompt_frameworks.hiss import hiss
from prompt_frameworks.rarr import rarr
from prompt_frameworks.baseline import base
from prompt_frameworks.keywords import keyword
from enum import Enum

class PF_ENUM(Enum):
    RAGAR = 'RAGAR'
    HISS = 'HISS'
    RARR = 'RARR'
    BASELINE = 'BASELINE'
    KEYWORD = 'KEYWORD'


pf_dict = {
    PF_ENUM.RAGAR.value: multiCoRAG, 
    PF_ENUM.HISS.value: hiss, 
    PF_ENUM.RARR.value: rarr, 
    PF_ENUM.BASELINE.value: base, 
    PF_ENUM.KEYWORD.value: keyword
}

class MODELS(Enum):
    GPT_4 = 'GPT_4'
    GPT_4_mini = 'GPT_4_mini'
    LLAMA_8B = 'LLAMA_8B'

class DATASETS(Enum):
    POLITIFACT = 'POLITIFACT'
    AVERITEC = 'AVERITEC'