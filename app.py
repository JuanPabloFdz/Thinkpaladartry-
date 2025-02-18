import streamlit as st
import pandas as pd
import plotly.express as px

# 📌 Configuración de la Página
st.set_page_config(page_title="Dashboard de Recetas", page_icon="🍽️", layout="wide")

# 📂 Cargar el CSV con los datos de recetas
@st.cache_data
def load_data():
    return pd.read_csv("recetas.csv")

df = load_data()

# 🎨 Estilo
st.title("🍽️ Dashboard de Recetas")
st.markdown("Analiza las recetas según su contenido nutricional, dificultad y tiempo de preparación.")

# 📌 Filtros
st.sidebar.header("📊 Filtros")
categorias = st.sidebar.multiselect("Selecciona Categorías", df["Categoría"].unique(), default=df["Categoría"].unique())

# Filtrar por categorías seleccionadas
df_filtered = df[df["Categoría"].isin(categorias)]

# 📌 Gráfico 1: Comparación de Grasas, Proteínas y Carbohidratos por Categoría
st.subheader("📊 Comparación de Macronutrientes por Categoría")
df_nutrition = df_filtered.groupby("Categoría")[["Grasas (100g)", "Proteínas (100g)", "Carbohidratos (100g)"]].mean().reset_index()
fig1 = px.bar(df_nutrition, x="Categoría", y=["Grasas (100g)", "Proteínas (100g)", "Carbohidratos (100g)"], 
              barmode="group", title="Grasas, Proteínas y Carbohidratos Medios por Categoría")
st.plotly_chart(fig1)

# 📌 Gráfico 2: Calorías Medias por Categoría
st.subheader("🔥 Calorías Medias por Categoría")
df_calories = df_filtered.groupby("Categoría")["Calorías (100g)"].mean().reset_index()
fig2 = px.bar(df_calories, x="Categoría", y="Calorías (100g)", title="Calorías Medias por Categoría", color="Calorías (100g)")
st.plotly_chart(fig2)

# 📌 Gráfico 3: Clasificación de Recetas por Calorías
st.subheader("🍏 Clasificación de Recetas por Calorías")
df_filtered["Caloría Nivel"] = pd.cut(df_filtered["Calorías (100g)"], bins=[0, 250, 370, 1000], 
                                       labels=["Baja", "Normal", "Alta"])
df_calorie_count = df_filtered.groupby(["Categoría", "Caloría Nivel"]).size().reset_index(name="Conteo")
fig3 = px.bar(df_calorie_count, x="Categoría", y="Conteo", color="Caloría Nivel", 
              title="Número de Recetas por Nivel de Calorías")
st.plotly_chart(fig3)

# 📌 Gráfico 4: Comparación de Macronutrientes por Categoría Seleccionada
st.sidebar.subheader("🔍 Detalle por Categoría")
categoria_seleccionada = st.sidebar.selectbox("Selecciona una Categoría", df["Categoría"].unique())

df_categoria = df_filtered[df_filtered["Categoría"] == categoria_seleccionada]
fig4 = px.bar(df_categoria, x=["Proteínas (100g)", "Grasas (100g)", "Carbohidratos (100g)"], 
              title=f"Macronutrientes de {categoria_seleccionada}")
st.plotly_chart(fig4)

# 📌 Gráfico 5: Relación Tiempo vs Dificultad
st.subheader("⏳ Tiempo vs Dificultad")
fig5 = px.scatter(df_filtered, x="Tiempo (min)", y="Dificultad", color="Categoría", 
                  title="Relación entre Tiempo de Preparación y Dificultad")
st.plotly_chart(fig5)

# 📌 Mostrar la Receta Más Rápida
st.subheader("⚡ Receta Más Rápida")
fastest_recipe = df_filtered[df_filtered["Tiempo (min)"] == df_filtered["Tiempo (min)"].min()]
st.write(f"🥇 La receta más rápida es: **{fastest_recipe.iloc[0]['Título']}** con **{fastest_recipe.iloc[0]['Tiempo (min)']} min** de preparación.")

