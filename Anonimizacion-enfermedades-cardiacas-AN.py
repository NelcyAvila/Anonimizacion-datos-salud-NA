
import pandas as pd

#1. Creamos un DataFrame simulado
### El dataFrame contiene diagnósticos de enfermedades cardíacas en hombres y mujeres entre 23 a 54 años de edad.
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Edad": [34, 45, 23, 54, 31, 29, 40, 33, 27, 38],
    "Género": ["F", "M", "F", "M", "F", "M", "M", "F", "F", "M"],
    "Código_Postal": ["190101", "190102", "190103", "190101", "190102", "190103", "190101", "190102", "190103", "190101"],
    "Diagnóstico": [
        "Arritmia",
        "Cardiopatía isquémica",
        "Insuficiencia cardíaca",
        "Arritmia",
        "Miocardiopatía",
        "Cardiopatía isquémica",
        "Cardiopatía congénita",
        "Insuficiencia cardíaca",
        "Miocardiopatía",
        "Arritmia"
    ]
}

df = pd.DataFrame(data)
df
# 2. Preprocesamiento:
## Limpieza de valores nulos
### Verificamos si hay valores nulos
print("NA por columna:")
print(df.isnull().sum())

### Convertimos Edad, Género y Código_Postal a tipo string para tratarlos como cuasi-identificadores
df["Edad"] = df["Edad"].astype(str)
df["Género"] = df["Género"].astype(str)
df["Código_Postal"] = df["Código_Postal"].astype(str)

### Marcamos los cuasi-identificadores
quasi_identificadores = ["Edad", "Género", "Código_Postal"]

### Mostramos el dataset ya limpio y preparado
print("\nDataset preparado:")
print(df)

# 3. Anonimización
import numpy as np
## 3.1 k-Anonimato con agrupación generalizada
### Copiamos el dataset original para no modificarlo directamente
df_k = df.copy()

### Generalizamos la edad en rangos de 10 años
def generalizar_edad(edad_str):
    edad = int(edad_str)
    rango_inferior = (edad // 10) * 10
    rango_superior = rango_inferior + 9
    return f"{rango_inferior}-{rango_superior}"

df_k['Edad'] = df_k['Edad'].apply(generalizar_edad)

### Generalizamos Código Postal manteniendo solo los primeros 4 dígitos
df_k['Código_Postal'] = df_k['Código_Postal'].str[:4] + "XX"

### Verificamos que cada grupo de cuasi-identificadores aparezca al menos 2 veces
quasi_identificadores = ['Edad', 'Género', 'Código_Postal']

### Contamos las combinaciones únicas
grupos = df_k.groupby(quasi_identificadores).size().reset_index(name='counts')
print("Frecuencia de los grupos:")
print(grupos)

### Filtramos grupos con frecuencia menor a k=2
grupos_bajos = grupos[grupos['counts'] < 2]
print("\nGrupos con frecuencia menor a 2 (no anónimos):")
print(grupos_bajos)

### Mostramos el dataset anonimizado
print("\nDataset k-anonimizado:")
print(df_k)

## 3.2 l-Diversidad asegurando diversidad de diagnósticos.

l = 2

### Agrupamos por cuasi-identificadores
grupos_ldiversidad = df_k.groupby(quasi_identificadores)['Diagnóstico'].nunique().reset_index(name='diagnosticos_unicos')

print("\nDiversidad de diagnósticos por grupo:")
print(grupos_ldiversidad)

### Filtramos grupos que no cumplen con l-diversidad
grupos_no_ldiversos = grupos_ldiversidad[grupos_ldiversidad['diagnosticos_unicos'] < l]
print("\nGrupos que no cumplen con l-diversidad (menos de 2 diagnósticos distintos):")
print(grupos_no_ldiversos)

## 3.3 Privacidad diferencial agregando ruido Laplaciano a las consultas

### Contamos casos de Arritmia
count_arritmia = (df['Diagnóstico'] == 'Arritmia').sum()

### Parámetro de privacidad (epsilon)
epsilon = 1.0

### Función para generar ruido laplaciano
def ruido_laplaciano(scale):
    return np.random.laplace(0, scale)

### Sensibilidad (en conteos es 1)
sensibilidad = 1

### Agregamos ruido al conteo
ruido = ruido_laplaciano(sensibilidad / epsilon)
count_arritmia_dp = count_arritmia + ruido

print(f"Conteo real de Arritmia: {count_arritmia}")
print(f"Conteo con privacidad diferencial (ruido Laplaciano): {count_arritmia_dp:.2f}")

# 4.Visualización:
## 4.1 Comparacion del DataFrame Original con el K-Anonimato
import matplotlib.pyplot as plt

### Conteo de combinaciones únicas de cuasi-identificadores
original_uniques = df.groupby(['Edad', 'Género', 'Código_Postal']).size().shape[0]
anonimizado_uniques = df_k.groupby(['Edad', 'Género', 'Código_Postal']).size().shape[0]

### Gráfico de barras comparando combinaciones únicas
plt.figure(figsize=(6, 4))
plt.bar(['Original', 'k-Anonimato'], [original_uniques, anonimizado_uniques], color=['skyblue', 'orange'])
plt.title('Comparación de combinaciones únicas')
plt.ylabel('Número de combinaciones únicas')
plt.show()

## 4.2 Diversidad de diagnósticos por grupo (l-diversidad)
### Histograma de número de diagnósticos únicos por grupo
plt.figure(figsize=(6, 4))
plt.hist(grupos_ldiversidad['diagnosticos_unicos'], bins=range(1, grupos_ldiversidad['diagnosticos_unicos'].max()+2), edgecolor='black')
plt.title('Diversidad de Diagnósticos por Grupo (l-diversidad)')
plt.xlabel('Número de diagnósticos únicos por grupo')
plt.ylabel('Frecuencia')
plt.xticks(range(1, grupos_ldiversidad['diagnosticos_unicos'].max()+1))
plt.show()
## 4.3 Conteo real vs privacidad diferencial
plt.figure(figsize=(6, 4))
plt.bar(['Real', 'Privacidad diferencial'], [count_arritmia, count_arritmia_dp], color=['brown', 'pink'])
plt.title('Casos de Arritmia')
plt.ylabel('Número de casos')
plt.show()
