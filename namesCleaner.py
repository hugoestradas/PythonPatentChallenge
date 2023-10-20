
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from wordcloud import WordCloud
from fuzzywuzzy import fuzz
from sklearn.svm import SVC
from functions import *
import pandas as pd
import argparse
import json
import os


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

#Almacenando orden de patent_id
outDf = df.copy()

#Limpieza básica - Justificada por exploración y en solution.txt
df['organization'] = df['organization'].apply(cleanWS)
df['organization'] = df['organization'].apply(cleanSC)
df['organization'] = df['organization'].apply(lambda x: cleanLegalStid(x, legalStid))

#Condiciones enunciado
df['country'] = df['country'].str.strip() #Country no require validación
#Validando city de manera básica
df['city'] = df['city'].str.strip()#Unica validación


#Evaluando similitud ortográfica
for i in range(len(rcn)):
    df['similarity'+str(i)] = df['organization'].apply(lambda x: fuzz.ratio(x, rcn[i])/100)

#Asignando clasificación
df['y'] = df.apply(lambda x: labeler(x['organization'], rcn), axis=1)

###Entrenando modelo

#Haciendo OneHotEncoding a columnas categoricas
#País
encoder = OneHotEncoder()
country_encoded = encoder.fit_transform(df[['country']])
ohe_country = pd.DataFrame(country_encoded.toarray(), columns=encoder.get_feature_names_out())
#Ciudad
encoder2 = OneHotEncoder()
city_encoded = encoder2.fit_transform(df[['city']])
ohe_city = pd.DataFrame(city_encoded.toarray(), columns=encoder2.get_feature_names_out())

#Agregando columnas
df = pd.concat([df, ohe_country, ohe_city], axis=1)
#Separando filas asignadas de filas sin asignación
missing = df[df['y'].isna()]
df = df[~df['y'].isna()]

Xtrain, Xtest, ytrain, ytest = train_test_split(df.drop(['y','organization','patent_id','city','country'], axis = 1), df['y'],\
                test_size=0.2, random_state=1010)

#Usando Support Vector Machine
#Permite tomar en cuenta las otras variables, no solo la similitud ortográfica
model = SVC()
model.fit(Xtrain, ytrain)
ypred = model.predict(Xtest)

#Prediciendo missing
missing.drop('y', axis=1, inplace=True)
missing['y'] = model.predict(missing.drop(['organization','patent_id','city','country'], axis = 1))

#Agregando a df principal
#df.update(missing['y'])
df = pd.concat([df, missing])
df.rename(columns={'y':'fixed'}, inplace=True)

#Devolviendo a orden original
outDf = outDf.merge(df[['patent_id','fixed']], on='patent_id', how='left')

#Mapeo final
mapDic = {i:rcn[i] for i in range(len(rcn))}
outDf['fixed'] = outDf['fixed'].map(mapDic)

#Guardando csv
outDf.to_csv(re.sub(".csv","-fixed.csv",fPath), index=False)
