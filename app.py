

import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos desde el CSV
@st.cache_data
def load_data():
    return pd.read_csv("recetas.csv")

df = load_data()

# Título de la aplicación
st.title("📊 Análisis de Recetas - ThinkPaladar")

# Filtrar recetas que tienen información nutricional
###################################################################################
st.write("Columnas disponibles en el DataFrame:", df.columns.tolist())
print(df.head())
df["Tiene Nutrición"] = pd.to_numeric(df["Tiene Nutrición"], errors="coerce")
df_filtered = df[df["Tiene Nutrición"] == 1]
######################################################
# 1️⃣ **Gráfico de Barras: Grasas, Proteínas e Hidratos por Categoría**
st.subheader("🔹 Promedio de Grasas, Proteínas y Carbohidratos por Categoría")
df_nutrition = df_filtered.groupby("Categoría")[["Grasas", "Proteínas", "Carbohidratos"]].mean().reset_index()

fig1 = px.bar(df_nutrition, 
              x="Categoría", 
              y=["Grasas", "Proteínas", "Carbohidratos"],
              title="Macronutrientes promedio por Categoría",
              labels={"value": "Gramos por 100g", "variable": "Macronutriente"},
              barmode="group")
st.plotly_chart(fig1)

# 2️⃣ **Gráfico de Barras: Calorías Medias por Categoría**
st.subheader("🔹 Calorías promedio por Categoría")
df_calories = df_filtered.groupby("Categoría")["Calorías"].mean().reset_index()

fig2 = px.bar(df_calories, 
              x="Categoría", 
              y="Calorías",
              title="Calorías promedio por Categoría",
              labels={"Calorías": "Kcal por 100g"},
              color="Calorías")
st.plotly_chart(fig2)

# 3️⃣ **Clasificación de recetas según calorías**
st.subheader("🔹 Clasificación de Recetas según Calorías")
df_filtered["Clasificación Calórica"] = pd.cut(df_filtered["Calorías"], 
                                               bins=[0, 250, 370, float("inf")], 
                                               labels=["Baja (<250 kcal)", "Normal (250-370 kcal)", "Alta (>370 kcal)"])

df_caloric_distribution = df_filtered.groupby("Categoría")["Clasificación Calórica"].value_counts().unstack()

fig3 = px.bar(df_caloric_distribution, 
              title="Clasificación de Recetas según Calorías",
              labels={"value": "Número de Recetas", "variable": "Clasificación Calórica"},
              barmode="stack")
st.plotly_chart(fig3)

# 4️⃣ **Selección de Categoría para detalle nutricional**
st.subheader("🔹 Selecciona una Categoría para ver su detalle nutricional")
categoria_seleccionada = st.selectbox("Selecciona una categoría", df_filtered["Categoría"].unique())

df_categoria = df_filtered[df_filtered["Categoría"] == categoria_seleccionada]

fig4 = px.bar(df_categoria, 
              x="Título", 
              y=["Grasas", "Proteínas", "Carbohidratos", "Calorías"],
              title=f"Macronutrientes y Calorías en {categoria_seleccionada}",
              labels={"value": "Cantidad por 100g", "variable": "Macronutriente"},
              barmode="group")
st.plotly_chart(fig4)

# 5️⃣ **Comparación Tiempo vs Dificultad**
st.subheader("🔹 Comparación entre Tiempo de preparación y Dificultad")
fig5 = px.scatter(df_filtered, 
                  x="Tiempo (min)", 
                  y="Dificultad",
                  color="Categoría",
                  size="Calorías",
                  title="Tiempo de preparación vs Dificultad",
                  labels={"Tiempo (min)": "Tiempo en minutos", "Dificultad": "Nivel de dificultad"})
st.plotly_chart(fig5)

# 6️⃣ **Receta Más Rápida**
st.subheader("🔹 Receta más rápida")
receta_mas_rapida = df_filtered[df_filtered["Tiempo (min)"] == df_filtered["Tiempo (min)"].min()]
st.write("**La receta más rápida es:**", receta_mas_rapida.iloc[0]["Título"])
st.write("🕒 **Tiempo:**", receta_mas_rapida.iloc[0]["Tiempo (min)"], "minutos")
st.write("🔥 **Calorías:**", receta_mas_rapida.iloc[0]["Calorías"], "Kcal por 100g")

# **Botón para mostrar datos en tabla**
st.subheader("📋 Datos de Recetas")
if st.button("Mostrar datos en tabla"):
    st.dataframe(df_filtered)



