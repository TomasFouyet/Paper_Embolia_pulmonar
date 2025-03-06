import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar y renombrar columnas del Excel
def load_data(file):
    # Lee el Excel sin cabecera (header=None) ya que asumimos que el archivo no tiene nombres de columnas
    df = pd.read_excel(file, header=None)
    # Asignar nombres de columnas de acuerdo a la descripción:
    # 1. Año, 2. Fecha, 3. Sexo, 4,5,6 se mantienen igual,
    # 7. Comuna, 8. Región, 9 y 10 se mantienen igual,
    # 11. Tipo de enfermedad, 12 se mantiene,
    # 13. Enfermedad Específica, 14 se mantiene,
    # 15. Causa de muerte, 16 se mantiene,
    # 17. Especificaciones, columnas 18 a 26 vacías, 27. Hospital o clínica
    columnas = [
        "Año", "Fecha", "Sexo", "Col4", "Col5", "Col6",
        "Comuna", "Region", "Col9", "Col10", "Tipo de enfermedad", "Col12",
        "Enfermedad Especifica", "Col14", "Causa de muerte", "Col16",
        "Especificaciones", "Empty18", "Empty19", "Empty20", "Empty21",
        "Empty22", "Empty23", "Empty24", "Empty25", "Empty26", "Hospital o clinica"
    ]
    df.columns = columnas
    return df

# Título de la aplicación
st.title("Análisis de Datos de Excel")

# Cargar archivos Excel (acepta múltiples archivos)
uploaded_files = st.file_uploader("Selecciona uno o más archivos Excel", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    # Cargar y concatenar los archivos en un solo DataFrame
    df_list = [load_data(file) for file in uploaded_files]
    df = pd.concat(df_list, ignore_index=True)
    
    st.write("Datos cargados:")
    st.dataframe(df.head())

    # Barra lateral para filtros
    st.sidebar.header("Filtros")
    
    # Filtro por Año
    year_options = sorted(df["Año"].dropna().unique())
    selected_years = st.sidebar.multiselect("Año", year_options, default=year_options)
    
    # Filtro por Sexo
    sexo_options = sorted(df["Sexo"].dropna().unique())
    selected_sexo = st.sidebar.multiselect("Sexo", sexo_options, default=sexo_options)
    
    # Filtro por Región
    region_options = sorted(df["Region"].dropna().unique())
    selected_region = st.sidebar.multiselect("Región", region_options, default=region_options)
    
    # Filtro por Comuna
    comuna_options = sorted(df["Comuna"].dropna().unique())
    selected_comuna = st.sidebar.multiselect("Comuna", comuna_options, default=comuna_options)
    
    # Aplicar los filtros
    filtered_df = df[
        df["Año"].isin(selected_years) &
        df["Sexo"].isin(selected_sexo) &
        df["Region"].isin(selected_region) &
        df["Comuna"].isin(selected_comuna)
    ]
    
    st.write(f"Datos filtrados: {filtered_df.shape[0]} registros")
    st.dataframe(filtered_df)
    
    # Estadísticas descriptivas
    st.subheader("Estadísticas Descriptivas")
    st.write(filtered_df.describe(include='all'))
    
    # Gráfico: Distribución por Sexo
    st.subheader("Distribución por Sexo")
    sexo_counts = filtered_df["Sexo"].value_counts()
    fig, ax = plt.subplots()
    sexo_counts.plot(kind="bar", ax=ax)
    ax.set_ylabel("Cantidad")
    ax.set_title("Número de registros por Sexo")
    st.pyplot(fig)
    
    # Gráfico: Número de registros por Año
    st.subheader("Número de Registros por Año")
    year_counts = filtered_df["Año"].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    year_counts.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("Cantidad")
    ax2.set_title("Número de registros por Año")
    st.pyplot(fig2)
else:
    st.write("Por favor, carga uno o más archivos Excel para continuar.")
