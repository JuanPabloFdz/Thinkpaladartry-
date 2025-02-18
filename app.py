import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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


col1, col2= st.columns(2)


with col1: 
    # 📊 **Gráfico de barras: Macronutrientes medios por categoría**
    st.subheader("📊 Macronutrientes Medios por Categoría")
    df_nutrition = df_filtered.groupby("Categoría")[["Grasas (100g)", "Proteínas (100g)", "Carbohidratos (100g)"]].mean().reset_index()

    fig = px.bar(
    df_nutrition, 
    x="Categoría", 
    y=["Grasas (100g)", "Proteínas (100g)", "Carbohidratos (100g)"],
    title="Distribución de Macronutrientes por Categoría",
    labels={"value": "Cantidad (100g)", "variable": "Macronutriente"},
    barmode="group")
    st.plotly_chart(fig)


with col2: 
    # 📊 **Gráfico de barras: Calorías Medias por Categoría**
    st.subheader("🔥 Calorías Medias por Categoría")
    df_calories = df_filtered.groupby("Categoría")["Calorías (100g)"].mean().reset_index()

    fig = px.bar(
    df_calories, 
    x="Categoría", 
    y="Calorías (100g)",
    title="Calorías Medias por Categoría",
    labels={"Calorías (100g)": "Calorías por 100g"})
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

# 🔥 **Top 5 Recetas Más Rápidas**
st.subheader("⏩ Top 5 Recetas Más Rápidas")
fastest_recipes = df_filtered[df_filtered["Tiempo (min)"] < 600].nsmallest(5, "Tiempo (min)")
st.dataframe(fastest_recipes[["Título", "Categoría", "Tiempo (min)", "Dificultad", "Calorías (100g)"]])

# 🔢 **Top 5 Recetas con Más Pasos**
st.subheader("📜 Top 5 Recetas con Más Pasos")
most_steps_recipes = df_filtered.nlargest(5, "Número de Pasos")
st.dataframe(most_steps_recipes[["Título", "Categoría", "Número de Pasos", "Dificultad", "Calorías (100g)"]])




# 🛒 **Sugeridor de Recetas**
st.subheader("🤖 Sugeridor de Recetas")
quieres_sugerencia = st.checkbox("¿Quieres una sugerencia de receta?")

if quieres_sugerencia:
    categoria_sugerida = st.selectbox("Selecciona una categoría para la sugerencia:", df["Categoría"].unique())
    df_sugerencias = df[df["Categoría"] == categoria_sugerida]
    
    if not df_sugerencias.empty:
        receta_sugerida = df_sugerencias.sample(1).iloc[0]  # Elegimos una receta aleatoria
        
        st.write(f"### 🥘 Receta Sugerida: {receta_sugerida['Título']}")
        st.write(f"- ⏳ Tiempo de preparación: {receta_sugerida['Tiempo (min)']} minutos")
        st.write(f"- 🔥 Calorías por 100g: {receta_sugerida['Calorías (100g)']}")
        st.write(f"- 🍗 Proteínas: {receta_sugerida['Proteínas (100g)']}g")
        st.write(f"- 🍞 Carbohidratos: {receta_sugerida['Carbohidratos (100g)']}g")
        st.write(f"- 🛢 Grasas: {receta_sugerida['Grasas (100g)']}g")
        
        st.write("### 🛒 Lista de la compra")
        st.write(f"{receta_sugerida['Ingredientes con Cantidad']}")
    else:
        st.warning("No hay recetas en esta categoría.")



# Crear gráfico de dispersión
df_filtered = df[df["Tiempo (min)"] <= 600]
fig_steps_time = px.scatter(df_filtered, 
                            x="Número de Pasos", 
                            y="Tiempo (min)", 
                            color="Dificultad",  # Colorear por dificultad
                            size="Tiempo (min)",  # Tamaño de los puntos según el tiempo
                            hover_data=["Título", "Categoría"],  # Mostrar detalles al pasar el mouse
                            title="Relación entre el Número de Pasos y el Tiempo de Preparación")

# Mostrar en Streamlit
st.plotly_chart(fig_steps_time)
