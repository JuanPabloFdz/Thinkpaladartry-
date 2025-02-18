import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cargamos el data set
@st.cache_data
def load_data():
    return pd.read_csv("recetas.csv", encoding="utf-8")

df = load_data()

# Definimos el título de la app 
st.title("🥐 Análisis de Recetas - ThinkPaladar🥑")
st.write("A continiuación se presenta los datos mas relevantes relativos a las recetas, sus valores nutricionales y sus características.")

# Mostramos la estructura del df
st.subheader("📋 Estructura de los Datos")
st.write(df.head())  # Muestra los primeros registros del DataFrame

# FILTRO DEBBUGING - quitar 
if "Tiene Nutrición" in df.columns:
    df_filtered = df[df["Tiene Nutrición"] == 1]
else:
    st.write("La columna 'Tiene Nutrición' no está presente en el CSV.")
    df_filtered = df 

# Gráfico 1: 
# 📊 **Gráfico de barras: Macronutrientes medios por categoría**
st.subheader("📊 Macronutrientes Medios por Categoría") #Titulo del gráfico
df_nutrition = df_filtered.groupby("Categoría")[["Grasas (100g)", "Proteínas (100g)", "Carbohidratos (100g)"]].mean().reset_index()

fig = px.bar(
df_nutrition, 
x="Categoría", 
y=["Grasas (100g)", "Proteínas (100g)", "Carbohidratos (100g)"],
title="Distribución de Macronutrientes por Categoría",
labels={"value": "Cantidad (100g)", "variable": "Macronutriente"},
barmode="group")
st.plotly_chart(fig)

#Gráfico 2: 
# 📊 **Tiempo Medio de Recetas vs Dificultad**
st.subheader("⏳ Tiempo Medio de Recetas por Dificultad") #Titulo del gráfico
df_difficulty = df_filtered.groupby("Dificultad")["Tiempo (min)"].mean().reset_index() #agrupamos por dificultad

fig = px.bar(
df_difficulty,
x="Dificultad",
y="Tiempo (min)",
title="Tiempo Medio de Recetas vs Dificultad",
labels={"Tiempo (min)": "Tiempo Promedio (min)"})
st.plotly_chart(fig)


#Gráfico 3:     
# 📊 **Gráfico de barras: Calorías Medias por Categoría**
st.subheader("🔥 Calorías Medias por Categoría") #Titulo del gráfico
df_calories = df_filtered.groupby("Categoría")["Calorías (100g)"].mean().reset_index()

fig = px.bar(
    df_calories, 
    x="Categoría", 
    y="Calorías (100g)",
    title="Calorías Medias por Categoría",
    labels={"Calorías (100g)": "Calorías por 100g"})
st.plotly_chart(fig)

# Gráfico 4
# 📊 **Clasificación de recetas por calorías**
st.subheader("🍽️ Clasificación de Recetas por Calorías") #Titulo del gráfico
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
st.subheader("📌 Selecciona una Categoría para Ver sus Detalles") #Titulo del gráfico
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

########## Top recetas 
# 🔥 **Top 5 Recetas Más Rápidas**
st.subheader("⏩ Top 5 Recetas Más Rápidas")
fastest_recipes = df_filtered[df_filtered["Tiempo (min)"] < 600].nsmallest(5, "Tiempo (min)")
st.dataframe(fastest_recipes[["Título", "Categoría", "Tiempo (min)", "Dificultad", "Calorías (100g)"]])


#Receta con más pasos. 
# 🔢 **Top 5 Recetas con Más Pasos**
st.subheader("📜 Top 5 Recetas con Más Pasos")
most_steps_recipes = df_filtered.nlargest(5, "Número de Pasos")
st.dataframe(most_steps_recipes[["Título", "Categoría", "Número de Pasos", "Dificultad", "Calorías (100g)"]])

#######################
# 
st.sidebar.header("🎯 Filtros de Recetas")

# Selección de Categoría
categoria_seleccionada = st.sidebar.selectbox("Selecciona una categoría:", df["Categoría"].unique(), key= "categoria_sugerencia")

# Aplicar filtro por categoría
df_categoria = df[df["Categoría"] == categoria_seleccionada]

# 📌 **Métricas y Ranking de Recetas**
st.subheader(f"📌 Ranking de Recetas en {categoria_seleccionada}")

col1, col2, col3 = st.columns(3)

# Recetas con más pasos
with col1:
    st.subheader("🔢 Más Pasos")
    top_pasos = df_categoria.nlargest(5, "Número de Pasos")
    st.table(top_pasos[["Título", "Número de Pasos"]])

# Recetas con menor tiempo
with col2:
    st.subheader("⏳ Menos Tiempo")
    top_rapidas = df_categoria.nsmallest(5, "Tiempo (min)")
    st.table(top_rapidas[["Título", "Tiempo (min)"]])

# Recetas con más ingredientes
with col3:
    st.subheader("🥦 Más Ingredientes")
    df_categoria["Número de Ingredientes"] = df_categoria["Ingredientes"].apply(lambda x: len(str(x).split(", ")))
    top_ingredientes = df_categoria.nlargest(5, "Número de Ingredientes")
    st.table(top_ingredientes[["Título", "Número de Ingredientes"]])
#####################
# Hacemos un sugeridor de recetas 

# 🛒 **Sugeridor de Recetas**
st.subheader("🤖 Sugeridor de Recetas")
quieres_sugerencia = st.checkbox("¿Quieres una sugerencia de receta?") # Boton para saber si quiere sugerencia o no

if quieres_sugerencia:
    categoria_sugerida = st.selectbox("Selecciona una categoría para la sugerencia:", df["Categoría"].unique(), key= "sugerencia") # Hacemos que se deba selecionar una categoria. 
    df_sugerencias = df[df["Categoría"] == categoria_sugerida]
    
    if not df_sugerencias.empty:
        receta_sugerida = df_sugerencias.sample(1).iloc[0]  # Elegimos una receta aleatoria
        #Y visualizamos 
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
df_filtered = df[df["Tiempo (min)"] <= 600] #Hacemos un filtrado porque hay recetas muy extensas y distorsionan la  visualización. 
fig_pasos = px.scatter(df_filtered, 
                            x="Número de Pasos", 
                            y="Tiempo (min)", 
                            color="Dificultad",  # Coloreamos por dificultad 
                            size="Tiempo (min)",  # DEfinimos el tamño según el tiempo
                            hover_data=["Título", "Categoría"],  # Esto es un elemento dinamico qu enos ayuda a ver mejor los datos al masar el mouse. 
                            title="Relación entre el Número de Pasos y el Tiempo de Preparación")

# mostramos
st.plotly_chart(fig_pasos)
