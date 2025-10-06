import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df.drop_duplicates(inplace=True)

    # Flexible date parsing (fix for error)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df = df.dropna(subset=['date_added'])   # 🚀 Remove rows with missing/invalid dates
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month


    # Fill missing values
    df['country'] = df['country'].fillna("Unknown")
    df['rating'] = df['rating'].fillna("Unknown")
    df['duration'] = df['duration'].fillna("Unknown")

    return df

df = load_data()

# ----------------------------
# Missing Dates Info
# ----------------------------
missing_dates = df['date_added'].isna().sum()
if missing_dates > 0:
    st.warning(f"⚠️ {missing_dates} rows have invalid or missing 'date_added' values. They were skipped in time-based analysis.")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("🔍 Filters")

year_filter = st.sidebar.slider(
    "Select Year Range",
    int(df['year_added'].min(skipna=True)),
    int(df['year_added'].max(skipna=True)),
    (2010, 2020)
)

type_filter = st.sidebar.multiselect(
    "Content Type",
    df['type'].unique(),
    default=df['type'].unique()
)

country_filter = st.sidebar.multiselect(
    "Country",
    df['country'].value_counts().head(15).index,
    default=df['country'].value_counts().head(5).index
)

df_filtered = df[
    (df['year_added'].between(year_filter[0], year_filter[1], inclusive="both")) &
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter))
]

# ----------------------------
# Overview KPIs
# ----------------------------
st.title("🎬 Netflix Movies & TV Shows Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Titles", df_filtered.shape[0])
col2.metric("Movies", df_filtered[df_filtered['type'] == "Movie"].shape[0])
col3.metric("TV Shows", df_filtered[df_filtered['type'] == "TV Show"].shape[0])
col4.metric("Countries", df_filtered['country'].nunique())

st.markdown("---")

# ----------------------------
# Tabs Layout
# ----------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Movies vs TV Shows",
    "📈 Trends Over Time",
    "🌍 Top Countries",
    "⭐ Ratings",
    "🎭 Genres",
    "⏳ Duration"
])

# ----------------------------
# Movies vs TV Shows
# ----------------------------
with tab1:
    st.subheader("🍿 Movies vs TV Shows")
    type_counts = df_filtered['type'].value_counts().reset_index()
    fig = px.pie(
        type_counts,
        values='count',
        names='type',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Content Trends
# ----------------------------
with tab2:
    st.subheader("📈 Content Added Over Time")
    trend = df_filtered.groupby(['year_added', 'type']).size().reset_index(name='count')
    fig = px.line(
        trend,
        x='year_added',
        y='count',
        color='type',
        markers=True,
        labels={'year_added': 'Year', 'count': 'Number of Titles'}
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Top Countries
# ----------------------------
with tab3:
    st.subheader("🌍 Top Countries Contributing Content")
    top_countries = df_filtered['country'].value_counts().head(10).reset_index()
    fig = px.bar(
        top_countries,
        x='count',
        y='country',
        orientation='h',
        color='count',
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Ratings
# ----------------------------
with tab4:
    st.subheader("⭐ Ratings Distribution")
    rating_counts = df_filtered['rating'].value_counts().reset_index()
    fig = px.bar(
        rating_counts,
        x='rating',
        y='count',
        color='count',
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Genres
# ----------------------------
with tab5:
    st.subheader("🎭 Genre Popularity")
    genres = df_filtered['listed_in'].str.split(',').explode().str.strip()
    top_genres = genres.value_counts().head(15).reset_index()

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            top_genres,
            x='count',
            y='listed_in',
            orientation='h',
            color='count',
            color_continuous_scale="magma"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        genre_text = " ".join(genres.dropna())
        wordcloud = WordCloud(width=500, height=400, background_color="black").generate(genre_text)
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

# ----------------------------
# Durations
# ----------------------------
with tab6:
    st.subheader("⏳ Duration Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Movies Duration Distribution")
        movies = df_filtered[df_filtered['type'] == "Movie"].copy()
        movies['minutes'] = (
            movies['duration'].str.replace(" min", "", regex=False)
            .replace("Unknown", 0)
            .astype(int)
        )
        fig = px.histogram(
            movies,
            x='minutes',
            nbins=30,
            color_discrete_sequence=["skyblue"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("TV Show Seasons Distribution")
        tv_shows = df_filtered[df_filtered['type'] == "TV Show"].copy()
        tv_shows['seasons'] = (
            tv_shows['duration'].str.replace(" Season", "", regex=False)
            .str.replace("s", "", regex=False)
            .replace("Unknown", 0)
            .astype(int)
        )
        season_counts = tv_shows['seasons'].value_counts().head(10).reset_index()
        fig = px.bar(
            season_counts,
            x='seasons',
            y='count',
            color='count',
            color_continuous_scale="plasma"
        )
        st.plotly_chart(fig, use_container_width=True)
