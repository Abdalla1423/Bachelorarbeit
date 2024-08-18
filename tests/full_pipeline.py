from prompt_frameworks.ragar import multiCoRAG
from prompt_frameworks.hiss import hiss
from prompt_frameworks.rarr import rarr
from enum import Enum

class PF_ENUM(Enum):
    RAGAR = 'RAGAR'
    HISS = 'HISS'
    RARR = 'RARR'

pf_dict = {PF_ENUM.RAGAR: multiCoRAG, PF_ENUM.HISS: hiss, PF_ENUM.RARR: rarr}

def getVerdict(pf, claim):
    return pf_dict[pf](claim)

print(getVerdict(PF_ENUM.RAGAR, "Today Biden died"))