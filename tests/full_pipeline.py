from prompt_frameworks.ragar import multiCoRAG
from prompt_frameworks.hiss import hiss
from prompt_frameworks.rarr import rarr
from enum import Enum
import ast

class PF_ENUM(Enum):
    RAGAR = 'RAGAR'
    HISS = 'HISS'
    RARR = 'RARR'

pf_dict = {PF_ENUM.RAGAR: multiCoRAG, PF_ENUM.HISS: hiss, PF_ENUM.RARR: rarr}

def getVerdict(pf, claim):
    verdict_str = pf_dict[pf](claim)
    verdict = ast.literal_eval(verdict_str)
    veracity = verdict["rating"]
    return veracity

print(getVerdict(PF_ENUM.RARR, "Today Biden died"))