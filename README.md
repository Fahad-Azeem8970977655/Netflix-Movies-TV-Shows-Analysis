# Netflix Movies & TV Shows Analysis 

## 📌 Project Overview
This project analyzes the **Netflix Movies & TV Shows dataset** to explore content trends, genres, ratings, and contributions by different countries.  
A professional **Streamlit dashboard** is built to provide interactive insights using advanced data visualizations.

## 🔍 Features
- 📊 **Content Trends** → Movies vs TV Shows over the years  
- 🌍 **Country Contributions** → Which countries contribute most content  
- 🎭 **Genre Distribution** → Most popular genres on Netflix  
- ⭐ **Ratings Analysis** → Distribution of audience ratings  
- 🗓️ **Time-based Analysis** → Yearly and monthly release trends  
- 📈 **Correlation Heatmap** → Relationships among numerical features  

## 🗂️ Dataset
- Source: [Netflix Movies & TV Shows Dataset (Kaggle)](https://www.kaggle.com/shivamb/netflix-shows)  
- Shape: ~8,800 rows, 12 columns  
- Columns include: `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description`.

⚠️ Rows with invalid or missing **`date_added`** were dropped to ensure clean time-based analysis.

## 🚀 How to Run
1. Clone or download this project folder:  
   ```bash
   git clone <your-repo-url>
   cd "Netflix Movies & TV Shows Analysis"
