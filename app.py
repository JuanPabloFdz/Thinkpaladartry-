import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el dataset
@st.cache_data
def load_data():
    return pd.read_csv("recetas.csv", encoding="utf-8")

df = load_data()

# Título de la App
st.title("📊 Análisis de Recetas - ThinkPaladar")
st.write("Visualización y análisis de recetas en base a sus valores nutricionales.")

# Verificar las columnas del DataFrame
st.subheader("📋 Estructura de los Datos")
st.write(df.head())  # Muestra los primeros registros del DataFrame

# 📌 Filtro de recetas que tienen información nutricional
if "Tiene Nutrición" in df.columns:
    df_filtered = df[df["Tiene Nutrición"] == 1]
else:
    st.write("⚠️ Advertencia: La columna 'Tiene Nutrición' no está presente en el CSV.")
    df_filtered = df  # Usamos todo el dataset si la columna no está

# 📊 **Gráfico de barras: Macronutrientes medios por categoría**
st.subheader("📊 Macronutrientes Medios por Categoría")
df_nutrition = df_filtered.groupby("Categoría")[["Grasas (100g)", "Proteínas (100g)", "Carbohidratos (100g)"]].mean().reset_index()

fig = px.bar(
    df_nutrition, 
    x="Categoría", 
    y=["Grasas (100g)", "Proteínas (100g)", "Carbohidratos (100g)"],
    title="Distribución de Macronutrientes por Categoría",
    labels={"value": "Cantidad (100g)", "variable": "Macronutriente"},
    barmode="group"
)
st.plotly_chart(fig)

# 📊 **Gráfico de barras: Calorías Medias por Categoría**
st.subheader("🔥 Calorías Medias por Categoría")
df_calories = df_filtered.groupby("Categoría")["Calorías (100g)"].mean().reset_index()

fig = px.bar(
    df_calories, 
    x="Categoría", 
    y="Calorías (100g)",
    title="Calorías Medias por Categoría",
    labels={"Calorías (100g)": "Calorías por 100g"}
)
st.plotly_chart(fig)

# 📊 **Clasificación de recetas por calorías**
st.subheader("🍽️ Clasificación de Recetas por Calorías")
df_filtered["Clasificación Calórica"] = pd.cut(
    df_filtered["Calorías (100g)"],
    bins=[0, 250, 370, df_filtered["Calorías (100g)"].max()],
    labels=["Baja en Calorías (<250 kcal)", "Ingesta Normal (250-370 kcal)", "Alta en Calorías (>370 kcal)"]
)

df_calories_class = df_filtered.groupby(["Categoría", "Clasificación Calórica"]).size().reset_index(name="Cantidad")

fig = px.bar(
    df_calories_class,
    x="Categoría",
    y="Cantidad",
    color="Clasificación Calórica",
    title="Distribución de Recetas por Calorías",
    labels={"Cantidad": "Número de Recetas"},
    barmode="stack"
)
st.plotly_chart(fig)

# 📌 **Selección de una categoría para ver detalles nutricionales**
st.subheader("📌 Selecciona una Categoría para Ver sus Detalles")
categorias = df_filtered["Categoría"].unique()
selected_category = st.selectbox("Selecciona una categoría:", categorias)

df_category = df_filtered[df_filtered["Categoría"] == selected_category]

# 📊 **Gráfico de nutrientes de la categoría seleccionada**
fig = px.bar(
    df_category, 
    x="Título",
    y=["Proteínas (100g)", "Grasas (100g)", "Carbohidratos (100g)", "Calorías (100g)"],
    title=f"Nutrientes de Recetas en la Categoría: {selected_category}",
    labels={"value": "Cantidad", "variable": "Nutriente"},
    barmode="group"
)
st.plotly_chart(fig)

# 📊 **Tiempo Medio de Recetas vs Dificultad**
st.subheader("⏳ Tiempo Medio de Recetas por Dificultad")
df_difficulty = df_filtered.groupby("Dificultad")["Tiempo (min)"].mean().reset_index()

fig = px.bar(
    df_difficulty,
    x="Dificultad",
    y="Tiempo (min)",
    title="Tiempo Medio de Recetas vs Dificultad",
    labels={"Tiempo (min)": "Tiempo Promedio (min)"}
)
st.plotly_chart(fig)

# 🔥 **Receta más rápida**
st.subheader("⏩ Receta Más Rápida")
fastest_recipe = df_filtered.loc[df_filtered["Tiempo (min)"].idxmin()]

st.write(f"🥇 **{fastest_recipe['Título']}** (Tiempo: {fastest_recipe['Tiempo (min)']} min)")

