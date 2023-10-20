import json
import argparse
import regex as re
import pandas as pd
from fpdf import FPDF
from functions import *
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#Nombres originales
#rcn = ["MICROSOFT TECHNOLOGY LICENSING","MICRON TECHNOLOGY","ELTA SYSTEMS","DELTA SYSTEMS"]

#Leyendo nombres originales
with open('Data/originalNames.json', 'r') as f:
    rcn = json.load(f)
    f.close()

#Leyendo datos
#fPath = 'Data/data.csv'
parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='Path de datos')
fPath = parser.parse_args().path
df = pd.read_csv(fPath)

#Eliminando nans de organization
df = df[~df['organization'].isna()]

#Cambiando tipos
df['organization'] = df['organization'].astype(str)
df['country'] = df['country'].astype(str)
df['city'] = df['city'].astype(str)

#Corpus total
corpus = ' '.join(df['organization'])
allchars = set(corpus)
#Corpus base
bcorpus = ' '.join(rcn)
bchars = set(bcorpus)
#Diferencias
diffChars = allchars.difference(bchars)

allchars = ''.join(allchars)
bchars = ''.join(bchars)

#Preparando para nube de palabras
bfreqs = Counter({letra: 1 for letra in bchars})
freqs = Counter({letra: 1 for letra in allchars})

#Nube de nombres originales
colorDic = {letra: rdColor for letra in diffChars}
color_func = SpecificColorFunc(colorDic)
wordcloudb = WordCloud(width=800, height=400, background_color='white', color_func=color_func, normalize_plurals=False)\
    .generate_from_frequencies(bfreqs)
plt.figure(figsize=(10,5))
plt.imshow(wordcloudb, interpolation='bilinear')
plt.axis('off')
wordcbPath = 'temp/wordcloudb.png'
plt.savefig(wordcbPath)
#plt.show()

#Nube de todo el corpus
wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=color_func, normalize_plurals=False)\
    .generate_from_frequencies(freqs)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
wordcPath = 'temp/wordcloud.png'
plt.savefig(wordcPath)
#plt.show()

#Determinando frecuencia de nombres
df['freq'] = df.groupby('organization')['organization'].transform('count')
namesFreq = dict(zip(df['organization'],df['freq']))

#Nube dataset sin limpiar
colorDic = {letra: rdColor for letra in rcn}
color_func = SpecificColorFunc(colorDic)
wordcloudO = WordCloud(width=1000, height=500, background_color='white', color_func=color_func, normalize_plurals=False)\
    .generate_from_frequencies(namesFreq)
plt.figure(figsize=(10,5))
plt.imshow(wordcloudO, interpolation='bilinear')
plt.axis('off')
wordoPath = 'temp/wordcloud_DfOriginal.png'
plt.savefig(wordoPath)
#plt.show()


###Limpieza básica
df['organization'] = df['organization'].str.upper()
df['organization'] = df['organization'].apply(cleanWS)
df['organization'] = df['organization'].apply(cleanSC)

###Determinando abreviaturas de empresa
lstInd = r'(\s[A-Z]{1,3})$'
df['legalStid'] = df['organization'].str.extract(lstInd)
legalStid = list(df['legalStid'].dropna().unique())

#Eliminando terminaciones de empresa
df['organization'] = df['organization'].apply(lambda x: cleanLegalStid(x, legalStid))

#Nube de nombres luego de limpieza
df['freq'] = df.groupby('organization')['organization'].transform('count')
namesFreq = dict(zip(df['organization'],df['freq']))

#Nombres luego de limpieza inicial
colorDic = {letra: rdColor for letra in rcn}
color_func = SpecificColorFunc(colorDic)
wordcloudLast = WordCloud(width=1000, height=500, background_color='white', color_func=color_func, normalize_plurals=False)\
    .generate_from_frequencies(namesFreq)
plt.figure(figsize=(10,5))
plt.imshow(wordcloudLast, interpolation='bilinear')
plt.axis('off')
lastwordcPath = 'temp/wordcloud_DfCleaned.png'
plt.savefig(lastwordcPath)
#plt.show()

#Calculando datos adicionales
df['official'] = df['organization'].apply(lambda x: checkOfficial(x, rcn))

#Etiquetas existentes en df
labels = df[df['official'] == True]['organization'].unique()
existing = set(rcn).intersection(set(labels))

print("Etiquetas existentes en datos {}/{}".format(len(existing),len(rcn)))

print('Etiquetas existentes en df: {}'.format(labels))

#Porcentaje de etiquetas
labeled = df[df['official'] == True].shape[0]*100/df.shape[0]
print('Porcentaje de etiquetas: {}%'.format(round(labeled,2)))

#Creando pdf de exploración

class PDF(FPDF):
    pass

pdf = PDF()

#Pagina 1
pdf.add_page()

# Añadir un título
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "Caracteres permitidos", ln=True, align='C')
pdf.ln(5)
# Añadir una descripción
pdf.set_font("Arial", size=12)
descripcion = """
Es posible visualizar de color rojo los caracteres discrepantes conmparados con los nombres "oficiales".
El tamaño de las letras no tiene relevancia acá.
"""
pdf.multi_cell(0, 10, descripcion)

pdf.ln(5)
#Añadiendo nubes de caracteres
pdf.image(wordcbPath, x=10, y=80, w=190)
pdf.ln(5)
pdf.image(wordcPath, x=10, y=190, w=190)

#Pagina 2
pdf.add_page()
# Añadir un título
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "Primera limpieza", ln=True, align='C')
pdf.ln(5)
# Añadir una descripción
pdf.set_font("Arial", size=12)  # Cambiamos el tamaño para la descripción
descripcion = """
En rojo se puede ver la coincidencia con los nombres "oficiales", antes y después.
El tamaño de los nombres sí tiene relevancia acá.
"""
pdf.multi_cell(0, 10, descripcion)

#Agregando wordclouds de nombres
pdf.ln(5)
pdf.image(wordoPath, x=10, y=80, w=190)
pdf.ln(5)
pdf.image(lastwordcPath, x=10, y=190, w=190)

#Pagina3
#Agregando datos adicionales
pdf.add_page()
# Añadir un título
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "Datos adicionales", ln=True, align='C')
pdf.ln(5)
# Añadir una descripción
pdf.set_font("Arial", size=12)  # Cambiamos el tamaño para la descripción
descripcion = """
Se muestra la lista de abreviaturas de empresa encontradas en el dataset.
{}
Según enunciado, se asumen estas como las posibles palabras especiales para remover.


Luego de la limpieza básica, el porcentaje de datos coincidentes con un nombre original es de {}%.


La cantidad de etiquetas existentes en el dataset es de {}/{}.
""".format(legalStid, round(labeled,2),len(existing),len(rcn))

pdf.multi_cell(0, 10, descripcion)

# Guardar el PDF con un nombre
pdf.output(re.sub('.csv','-exploration.pdf',fPath))
