import regex as re
import numpy as np

#%%Constants
grColor = '#6F8AA1'
rdColor = '#D45D5D'
blColor = '#4A90E2'
legalStid = [' INC', ' LLC', ' LTD', ' LLP', ' PC', ' KKC']

#%%Functions
#Para cambio de color
class SpecificColorFunc(object):
    def __init__(self, color_dict):
        self.color_dict = color_dict
    def __call__(self, word, **kwargs):
        return self.color_dict.get(word, grColor)

#Limpiando espacios en blanco
def cleanWS(x):
    x = x.strip()
    multSpace = r"[\s]{2,}"
    x = re.sub(multSpace," ",x)
    return x

#Filtrando caracteres especiales
def cleanSC(x):
    x = x.strip()
    sc = r"[^A-Z\s]"#No numeros ni minúsculas
    x = re.sub(sc,"",x)
    return x


#Limpiando abreviaturas de empresa
def cleanLegalStid(x, legalwords):
    for w in legalwords:
        tpattern = r'({}$)'.format(w)

        x = re.sub(tpattern,"",x)
    return x

#Chequeando existencia de todas las palabras OFICIALES
def checkOfficial(x, ofWords):
    try:
        index = ofWords.index(x)
        return True
    except ValueError:
        return False

#Obteniendo categoría
def labeler(x, ofWords):
    try:
        index = ofWords.index(x)
        return index
    except ValueError:
        return np.nan