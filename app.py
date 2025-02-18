import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos desde el CSV
@st.cache_data
def load_data():
    return pd.read_csv("recetas.csv")

df = load_data()

# Sidebar para seleccionar la categoría de recetas
categoria_seleccionada = st.sidebar.selectbox("Selecciona una categoría", df["Categoría"].unique())

# Filtrar datos por categoría seleccionada
filtered_df = df[df["Categoría"] == categoria_seleccionada]

# Gráfico de barras - Macronutrientes promedio por categoría
st.subheader("Macronutrientes promedio por categoría")
macronutrientes = df.groupby("Categoría")[["Proteínas", "Grasas", "Carbohidratos"]].mean().reset_index()
fig_macros = px.bar(macronutrientes, x="Categoría", y=["Proteínas", "Grasas", "Carbohidratos"],
                     title="Macronutrientes medios por categoría", barmode="group")
st.plotly_chart(fig_macros)

# Gráfico de calorías medias por categoría
st.subheader("Calorías medias por categoría")
calorias_medias = df.groupby("Categoría")["Calorías"].mean().reset_index()
fig_calorias = px.bar(calorias_medias, x="Categoría", y="Calorías", title="Calorías promedio por categoría")
st.plotly_chart(fig_calorias)

# Clasificación de recetas por ingesta calórica
st.subheader("Clasificación de recetas por calorías")
df["Nivel Calórico"] = pd.cut(df["Calorías"], bins=[0, 250, 370, float("inf")], 
                                labels=["Baja (<250 kcal)", "Normal (250-370 kcal)", "Alta (>370 kcal)"])
conteo_niveles = df["Nivel Calórico"].value_counts().reset_index()
fig_niveles = px.bar(conteo_niveles, x="index", y="Nivel Calórico", title="Número de recetas por nivel calórico")
st.plotly_chart(fig_niveles)

# Gráfico de barras de los macronutrientes para la categoría seleccionada
st.subheader(f"Macronutrientes en la categoría {categoria_seleccionada}")
fig_categoria = px.bar(filtered_df, x="Título", y=["Proteínas", "Grasas", "Carbohidratos", "Calorías"],
                       title=f"Macronutrientes y calorías en {categoria_seleccionada}", barmode="group")
st.plotly_chart(fig_categoria)

# Relación entre tiempo medio y dificultad
st.subheader("Tiempo medio de las recetas vs Dificultad")
tiempo_dificultad = df.groupby("Dificultad")["Tiempo (min)"].mean().reset_index()
fig_tiempo = px.bar(tiempo_dificultad, x="Dificultad", y="Tiempo (min)", title="Tiempo medio por dificultad")
st.plotly_chart(fig_tiempo)

# Receta más rápida
st.subheader("Receta más rápida")
receta_mas_rapida = df.loc[df["Tiempo (min)"].idxmin()]
st.write(f"La receta más rápida es **{receta_mas_rapida['Título']}**, con un tiempo de **{receta_mas_rapida['Tiempo (min)']} minutos**.")
