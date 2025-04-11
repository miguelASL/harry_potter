import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ydata_profiling import ProfileReport
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Rutas de los archivos desde el .env
CHARACTERS_PATH = os.getenv("CHARACTERS_PATH")
BOOKS_PATH = os.getenv("BOOKS_PATH")
MOVIES_PATH = os.getenv("MOVIES_PATH")
SPELLS_PATH = os.getenv("SPELLS_PATH")

# Carga de datos
df_characters = pd.read_csv(
    r"harry_potter\data\books.csv")
df_books = pd.read_csv(r"C:\Users\msarm\Desktop\harry potter\books.csv")
df_movies = pd.read_csv(r"C:\Users\msarm\Desktop\harry potter\movies.csv")
df_spells = pd.read_csv(r"C:\Users\msarm\Desktop\harry potter\hechizos.csv")

# Limpieza (ETL)
for df in [df_characters, df_books, df_movies, df_spells]:
    for col in ['gender', 'house', 'species']:
        if col in df.columns:
            df[col] = df[col].fillna("Desconocido")

# Gráficos

# Personajes por casa
house_counts = df_characters[df_characters['house'] !=
                             "Desconocido"]['house'].value_counts().reset_index()
house_counts.columns = ['Casa', 'Cantidad']
fig1 = px.bar(house_counts, x="Casa", y="Cantidad", color="Casa",
              title="🎓 Personajes por Casa", text_auto=True, template="plotly_dark")
fig1.show()

# Género
gender_counts = df_characters['gender'].value_counts().reset_index()
gender_counts.columns = ['Género', 'Cantidad']
fig2 = px.pie(gender_counts, names='Género', values='Cantidad',
              hole=0.4, title="⚖️ Género de Personajes", template="plotly_white")
fig2.show()

# Línea de tiempo libros vs películas

book_dates = ["1997-06-26", "1998-07-02", "1999-07-08",
              "2000-07-08", "2003-06-21", "2005-07-16", "2007-07-21"]
movie_dates = ["2001-11-16", "2002-11-15", "2004-05-31", "2005-11-18",
               "2007-07-11", "2009-07-15", "2010-11-19", "2011-07-15"]

book_titles = ["The Philosopher's Stone", "The Chamber of Secrets", "The Prisoner of Azkaban",
               "The Goblet of Fire", "The Order of the Phoenix", "The Half-Blood Prince", "The Deathly Hallows"]
movie_titles = ["The Philosopher's Stone", "The Chamber of Secrets", "The Prisoner of Azkaban", "The Goblet of Fire",
                "The Order of the Phoenix", "The Half-Blood Prince", "The Deathly Hallows Part 1", "The Deathly Hallows Part 2"]

books_timeline = pd.DataFrame(
    {"Evento": book_titles, "Tipo": "Libro", "Fecha": pd.to_datetime(book_dates)})
movies_timeline = pd.DataFrame(
    {"Evento": movie_titles, "Tipo": "Película", "Fecha": pd.to_datetime(movie_dates)})

timeline_df = pd.concat([books_timeline, movies_timeline]).sort_values("Fecha")

fig5 = px.scatter(timeline_df, x="Fecha", y="Tipo", color="Tipo", text="Evento",
                  symbol="Tipo", title="📚🎬 Línea de Tiempo de Libros y Películas", template="plotly_dark")
fig5.update_traces(marker=dict(size=14), textposition='top center')
fig5.update_layout(height=500)
fig5.show()

# Casa vs Género
house_gender = df_characters.groupby(
    ["house", "gender"]).size().reset_index(name="count")
house_gender = house_gender[house_gender["house"] != "Desconocido"]

fig_gender_house = px.bar(
    house_gender,
    x="house",
    y="count",
    color="gender",
    title="Distribución de Género por Casa",
    template="plotly_dark",
    labels={"count": "Cantidad de personajes",
            "house": "Casa", "gender": "Género"}
)
fig_gender_house.update_layout(barmode='stack')
fig_gender_house.show()

# Casa vs Especie
house_species = df_characters.groupby(
    ["house", "species"]).size().reset_index(name="count")
house_species = house_species[house_species["house"] != "Desconocido"]

fig_species_house = px.treemap(
    house_species,
    path=["house", "species"],
    values="count",
    title="🌳 Diversidad de Especies por Casa",
    color="count",
    color_continuous_scale="Tealgrn"
)
fig_species_house.show()

# Filtrar valores válidos
df_species_valid = df_characters[(df_characters["species"] != "Desconocido") & (
    df_characters["house"] != "Desconocido")].copy()

# Agrupar por casa y especie
species_counts_by_house = df_species_valid.groupby(
    ["house", "species"]).size().reset_index(name="count")

#  Sunburst Chart (Casa -> Especie)
fig_species_sunburst = px.sunburst(
    species_counts_by_house,
    path=["house", "species"],
    values="count",
    title="🌳 Diversidad de Especies por Casa",
    color="count",
    color_continuous_scale="Tealgrn"
)
fig_species_sunburst.show()
