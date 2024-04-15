# Importar las bibliotecas necesarias
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("Current Working Directory:", os.getcwd())

df = pd.read_excel("../../data/raw/cancer_hbv.xlsx", engine='openpyxl')

col_drop_file = '../../data/raw/columnas_drop'

# Leer el archivo con las columnas a eliminar
with open(col_drop_file, 'r') as file:
    columnas_a_eliminar = [line.strip() for line in file.readlines()]

#  Eliminar las columnas especificadas
df = df.drop(columns=columnas_a_eliminar, errors='ignore')

# Filtramos el DataFrame para obtener solo las filas donde 'NOM_TOPOLOGIA' es igual a 'Prostata'
df = df[df['NOM_TOPOLOGIA'] == 'Prostata']

# Guardar el DataFrame filtrado especificando el delimitador, sin índice y con codificación UTF-8
df.to_csv('../../data/processed/df_cancer_prostata.csv', index=False, encoding='utf-8')

# Reemplazar 'S/A' por NaN en la columna 'FECHA_COMITE'
df['FECHA_COMITE'] = df['FECHA_COMITE'].replace('S/A', np.nan)
df['FEC_NACIMIENTO'] = pd.to_datetime(df['FEC_NACIMIENTO'], format='%d/%m/%Y',errors='coerce')
df['FECHA_CANCER_PREVIO_1'] = pd.to_datetime(df['FECHA_CANCER_PREVIO_1'], format='%Y',errors='coerce')
df['FECHA_CANCER_PREVIO_2'] = pd.to_datetime(df['FECHA_CANCER_PREVIO_2'], format='%Y',errors='coerce')
df['FECHA_COMITE'] = pd.to_datetime(df['FECHA_COMITE'], format='%d/%m/%Y',errors='coerce')
df['FEC_INGRESO_CASO'] = pd.to_datetime(df['FEC_INGRESO_CASO'], format='%d/%m/%Y',errors='coerce')
df['FEC_DIAGNO'] = pd.to_datetime(df['FEC_DIAGNO'],format='%d/%m/%Y')
df['FEC_TOM_MUESTRA'] = pd.to_datetime(df['FEC_TOM_MUESTRA'], format='%d/%m/%Y',errors='coerce')
df['FECHA_FALLECIMIENTO'] = pd.to_datetime(df['FECHA_FALLECIMIENTO'], format='%d/%m/%Y',errors='coerce')

# Columnas Fecha de Tratamiento tienen formato distinto. 
columnas_fecha_tratamiento = [col for col in df.columns if 'FECHA_INICIO_TRATAMIENTO' in col or 'FECHA_TERMINO_TRATAMIENTO' in col]

# Convertir las columnas identificadas a datetime
for col in columnas_fecha_tratamiento:
    df[col] = pd.to_datetime(df[col], errors='coerce')
    
# Eliminar filas donde 'FECHA_INICIO_TRATAMIENTO_1' es nula (No se realizaron tratamientos a estos pacientes)
df = df.dropna(subset=['FECHA_INICIO_TRATAMIENTO_1'])

# Cálculo de la diferencia en días entre la fecha de diagnóstico y la fecha de inicio del primer tratamiento
df['DIAS_HASTA_INICIO_TRATAMIENTO'] = (df['FECHA_INICIO_TRATAMIENTO_1'] - df['FEC_DIAGNO']).dt.days

# Filtrar el DataFrame para mantener solo las filas donde 'FECHA_INICIO_TRATAMIENTO_1' <= 'FEC_DIAGNO'
df = df[df['FECHA_INICIO_TRATAMIENTO_1'] >= df['FEC_DIAGNO']]


# Definir los estados para los cuales 'SOBREVIVE' será 1
estados_sobrevive = ['VIVO CON ENFERMEDAD', 'VIVO SIN ENFERMEDAD', 'VIVO EN RECAIDA/RECURRENCIA']

# Crear la columna 'SOBREVIVE' basada en la condición dada
df['SOBREVIVE'] = df['ESTADO_ACTUAL'].apply(lambda x: 1 if x in estados_sobrevive else 0 if x == 'MUERTE' else np.nan)

# Eliminar filas donde 'SOBREVIVE' es nulo
df = df.dropna(subset=['SOBREVIVE'])

# Convertir 'SOBREVIVE' a tipo de dato entero
df['SOBREVIVE'] = df['SOBREVIVE'].astype('int64')

# Split the values in 'TNM_1' column by space and create new columns
df[['Tipo_Tumor', 'T', 'N', 'M']] = df['TNM_1'].str.split(' ', expand=True)


# Guardar el DataFrame filtrado especificando el delimitador, sin índice y con codificación UTF-8
df.to_csv('../../data/processed/df_cancer_prostata_processed.csv', index=False, encoding='utf-8')



df.info()
