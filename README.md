# PythonPatentChallenge
Intermedia IT Challenge Patents

# PythonPatentChallenge
Intermedia IT Challenge about Patents using provided data

# Solución
Se realizó el reto según instrucciones del enunciado. Tomar en cuenta las siguientes consideraciones.

-Con el fin de generalizar, en la carpeta Data se ha almacenado originalNames.json. De modo que se pueda cambiar en cualquier momento el listado de nombres originales.
-El archivo functions.py solo tiene funciones y no requiere de ejecución.
-El archivo dataExploring.py genera una inspección inicial de los datos que permita validar o no el enfoque de la solución. Se generan nubes de caracteres y nubes de palabras como referencia visual que es de ayuda a la hora de generar la limpieza básica que se indica en el enunciado. También arroja información sobre la existencia de coincidencias exactas con los nombres originales, qué porcentaje del dataset y cuantas clases están presentes. El resultado de este script se almacena con la etiqueta "-exploration", en formato pdf.
-El archivo namesCleaner.py ejecuta una etapa inicial de limpieza básica, luego realiza un etiquetado de los datos basándose en las coincidencias exactas, para este caso es más del 99% de datos etiquetados debido a coincidencia exacta. Con estas etiquetas se entrena un algoritmo Support Vector Machine, que permite tomar en cuenta la información adicional de país y ciudad, a la vez que la similitud respecto a los nombres "oficiales". El resultado de este archivo genera un archivo con la etiqueta "-fixed", con la columna de nombre normalizada.


#Consideraciones de desempeño y diseño

-Se pudo comprobar una asignación adecuada del nombre corregido al hacer una inspección aleatoria de la columna de datos corregidos (columna "fixed"). SVM tiene buen desempeño con alta dimensionalidad, lo que lo hace adecuado para este enfoque, principalmente después de aplicar codificación OneHoteEncoding a las características 'country' y 'city'.
-El pdf de exploración de los datos puede ayudar a identificar situaciones donde el enfoque de la solución puediera no ser la mejor opción, casos como los siguientes:
-Un gran desbalance de clases.
-Cero coincidencias en el conjunto de datos con alguna categoría de nombres "originales".
-Es necesario modificar originalNames.json en caso se requiere aplicar una nueva solución con un conjunto de nombres originales distinto.
-Según lo indicado en el enunciado, se asumió que las abreviaturas propias de una empresa corresponden con las que estaban en el conjunto particular de datos. De igual forma se procedió a adquirirlas con expresión regular y se detallan en el pdf de la exploración de datos.
-Al hacer uso de SVM se elimina la dependencia solo de la similitud ortográfica y se permite que los campos de país y ciudad también sean tomados en cuenta para la asignación del nombre corregido.

#Oportunidades de mejora a solución

 -Encontrar métodos distintos de inferencia de los nombres originales sin que se indiquen de manera explícita. (El grado de incertidumbre aumenta considerablemente).
-Establecer validaciones que levanten alarma cuando se ejecute el código sobre un conjunto de datos que infrinja las principales consideraciones al momento de ejcutar la solución basada en SVM. Por ejemplo:
        -Desbalance de clases.
        -Ausencia de clase en conjunto de datos original, incluso después de limpieza básica.
    -Considerar validaciones ante archivos defectuosos o con estructura distinta.
    -Robustecer ante eventuales ubicaciones nuevas para nombres de compañía, de modo que también se aproveche la similitud ortográfica aunque no existan ejemplos de la combinación país ciudad compañía, en el conjunto de datos.

#Sobre el uso de los scripts
    -Es necesario ejecutar desde consola cualquiera de los dos scripts (namesCleaner.py y dataExploring.py).
    -El archivo de salida se guardará en la misma ubicación del archivo de entrada. En ambos casos existirá una etiqueta que lo diferencie del archivo oficial: "-fixed" y "-exploration".
