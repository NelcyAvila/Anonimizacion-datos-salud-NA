# Anonimizacion-datos-salud-NA
# 1 Creación del dataset simulado
Mediante este dataset se realiza  un ejmplo de la simulación de anonimización que pueden ser aplicados posteriormente a los campos reales de la salud. 
Como primer paso se tiene la creación un DataFrame con información médica simulada de 10 pacientes, con los siguientes campos:

    -ID: Es el identificador único de cada paciente para poder diferenciarlos
    -Edad: Indica la edad del paciente en años, que comprende la edad entre 23 y 54 años.
    -Género: Indica el género mas culino con F y Femenino con M.
    -Código_Postal: Indica el código de la ubicación geográfica 
    -Diagnóstico: Este campo indica el tipo de enefermedad cardíaca diagnosticada a cada paciente.
    
# 2 Preprocesamiento.
   ## 2.1 Limpieza
   
Se verifica si hay valores nulos (NA) usando df.isnull().sum(). El resultado que se muestra en la consola es que no hay valores faltantes o NA.

  ## 2.2 Conversión de cuasi-identificadores 
  
Se identifican los cuasi-identificadores, que son atributos que por sí solos no identifican a una persona, pero combinados pueden revelar su identidad. Se convierten a tipo texto para tratarlos como atributos identificables indirectamente.
Los campos seleccionados como cuasi-identificadores son:

-Edad

 -Género

-Código_Postal
Luego se puede visualizar el dataset ya limpio y listo para aplicar la anonimización.

# 3 Anonimización
## 3.1 k-Anonimato
Este proceso es realizado con el  objetivo es evitar que una persona sea identificable por tener combinaciones únicas de edad, género y zona geográfica.
Se generaliza la edad en rangos de 10 años para reducir especificidad.
Se generaliza el código postal dejando solo los primeros 4 dígitos y ocultando los 2 últimos como se puede ver en los ejemplos, esto con la finalidad de ocultar zonas pequeñas.
Se agrupan los datos por estos tres atributos de la Edad, Género, Código_Postal, con el objetivo de ver si cada grupo tiene al menos 2 registros (k ≥ 2).
Se identifican los grupos con frecuencia menor a 2, es decir los que no cumplen k-anonimato y el resultado fue que tres frupos no cumplen con k-anonimato y por lo tanto se puede decir que estan en riesgo de reidentificación puesto que la combinación de edad, el género y la zona son únicas dentro del dataset.
Estos grupos son:

  -Hombres de 20–29 años en la zona 1901XX

  -Hombres de 30–39 años en la zona 1901XX

  -Hombres de 50–59 años en la zona 1901XX
    
## 3.2 l-Diversidad
Se agrupan los datos por cuasi-identificadores como en k-anonimato. En donde el objetivo es asegurarse de que dentro de cada grupo de  cuasi-identificadores haya al menos 2 diagnósticos distintos con l=2
Esto protege contra el riesgo de saber que una persona con ciertos datos tiene una única enfermedad, aumentando la confidencialidad.
Sin embargo, los tres grupos anteriores analizados en k-anonimato son los mismos grupos que no poseen diversidad. Por ejemplo, el grupo que comprende la edad entre 30 y 39 años de edad tienen solamente arritmia.
Por ello se puede consluir que aunque se cumpla parcialmente k-anonimato, no garantiza la privacidad en su totalidad si no existe diversidad en los datos sensibles, por ello también es necesario apliar l-diversidad.
## 3.3 Privacidad Diferencial
El objetivo de la privacidad diferencial es la protección de la privacidad al responder consultas sobre el dataset mediante la implementación de ruido aleatorio, esto con la finalidad de identificar si el pacienteen específico está presente. 
EL conteo real de los pacientes con diagnóstico de arritmia es de 3. AL plicar el ruido aleatorio Laplaciano al conteo usando la función np.random.laplace, con ruido= 1.0 el resultado es igual a 3.94.
Es decir, el resultado varia de manera leve en cada ejecusión, aumentando la privacidad pero sin modificar el dataset original, esto, precisamente por la aplicación del ruido lo cual es ideal cuando se quiere ver la informacion en general de los pacientes. 

# 4. Visualización de Resultados
## 4.1 Combinaciones únicas
La primera gráfica compara el número de combinaciones únicas de cuasi-identificadores en el dataset original y en el k-anonimizado.
El conjunto de datos original tiene 10 combinaciones únicas de los cuasi-identificadores, lo cual quiere decir que cada persona puede ser identificada con facilidad.
Una vez aplicado el k-anonimato  se puede ver que el número de combinaciones se reduce a 6, lo cual es un indicador de que los registros comparten los mismos valores generalizados y, por ello aumenta la privacidad de los pacientes. 
Mediante la gráfica y tras el análisis se puede concluir que esta técnica es efectiva al momento de reducir el numero de identificadores únicos de los pacientes.
## 4.2 Diversidad por grupo
La segunda gráfica, es un un histograma que representa la cantidad de diagnósticos diferentes únicos que existen por cada grupo de cuasi-identificadores despues de la aplicación de k-anonimato. 
El histograma muestra que 3 grupos tienen un diagnóstico único, es decir no cumplen lo la l-diversidad de l=2. Además, hay 2 grupos que tienen 2 diagnósticos distintos y un grupo que tienen 3 diagnósticos diferentes. 
Con esta información visualizada se puede concluir que aunque k-anonimato agrupa los datos, no es una garantía de que exista diversidad dentro de esos grupos, ya que algunos de ellos siguen siendo vulnerables puesto que comparten el mismo diagnóstico, lo que pone en riesgo la informacion sensible de los pacientes, por ello se complementa con la l-diversidad, la cual asegura que haya al menos l diagnósticos distintos con la finalidad de mejorar la privacidad de los datos. 

## 4.3 Conteo real vs. privacidad diferencial

    La privacidad diferencial se encarga de proteger los datos individuales en estadísticas agregadas.
    En este último gráfico se compara el conteo real de personas diagnostiacadas con Arritmia y el número estimado después de aplicar la privacidad diferencial que añade ruido para proteger la información.
    En esta gráfica se puede ver el conteo real, de 3 casos, pero aplicando la privacidad diferencial el conteo que se muestra es de 3.94. Esta diferencia pequeña se da debido al ruido laplaciano aleatorio que fue agregado para que no sea posible saber con exactitud cuántas personas tienen arritmia, y de esta manera se protege la privacidad de los pacientes.

