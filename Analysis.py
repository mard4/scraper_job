import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import string
import numpy as np
import string
import nltk
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

from scrapers.ScraperWikipedia import scrape_programming_languages
from scrapers.ScraperIndeed import scrape_indeed


programming_languages0 = scrape_programming_languages()
work = "Data Analyst"
location = "Milano"
df_indeed = scrape_indeed(work, location)
#df_indeed = scrape_indeed()


print('.. WEB Scraper is done')

# Importing Data and Data Exploration
# df_indeed = pd.read_excel('MilanoIndeed.xlsx')
dati = df_indeed.copy()
print(dati.head(10))
print(dati.info())

# Plot companies ratings

def plot_ratings_companies(dati):
    """Apply all operations to plot data"""
    dataset = dati.copy()
    dataset['Ratings'] =  dataset['Ratings'].str.replace(',', '.').astype(float)     # Change data types for analysis
    dataset['JobTitle'] = dataset['JobTitle'].str.lower()

    # Count per Job title or Company
    #jobtitles = dati.groupby('JobTitle').count().reset_index()
    companies = dataset.groupby('Company').count().reset_index()

    zero_ratings = companies.loc[companies['Ratings'] == 0]
    company_names = zero_ratings.iloc[:, 0].values
    print(f"Companies without rating: {company_names}")

    # Ratings x company
    plot_ratings = dataset.fillna('')
    plot_ratings = plot_ratings.loc[plot_ratings['Ratings'] != '']
    sorted_plot_ratings = plot_ratings.sort_values(by='Ratings').drop_duplicates(subset='Company')
    return sorted_plot_ratings

sorted_plot_ratings = plot_ratings_companies(dati)
fig = px.bar(sorted_plot_ratings, 
             x='Company', 
             y='Ratings',
             hover_data=['Location', 'Job_types'], 
             color='Ratings',
             labels={'Salario':'Salary'}, 
             height=400)

fig.show()

# See the most used words for job descriptions
descrizioni = dati['Description']
descriptions = []

for desc in descrizioni:
    descriptions.append(desc)

# Cleaning
def strip_puntuactions(line):
    """Function for replacing special characters %^&* to empty string"""
    for character in string.punctuation:
        line = line.replace(character, "")
    return line  

def exclude_stop_words(descriptions):
    stop_words_it = stopwords.words('italian')
    stop_words_eng = stopwords.words('english')
    stop_words = stop_words_it.copy()
    stop_words.extend(stop_words_eng)
    filtered_list = []
    
    for line in descriptions:
        #"""Exclude special characters"""
        line = strip_puntuactions(line)
        words = line.split()

    for word in words:
        #"""Exclude stop words"""
        if word.lower() not in stop_words:
            filtered_list.append(word)
    return filtered_list

# Analysis
def wordCount_Freq(filtered_list):
    word_count = {}

    for line in filtered_list:
        line = strip_puntuactions(line)
        words = line.split()

        for word in words:
            word = word.lower()
            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1

    print(f"...{list(word_count.keys())[:10]}")
    return word_count


def indeed_programming_languages(descriptions):
    """Open file with all programming languages to match with descriptions"""
    programming_languages = programming_languages0[0].to_list()
    languages_inDescriptions = []

    for language in programming_languages:
        #language = strip_punctuation(language)
        for description in filtered_list:
            if language.lower() in description.lower():
                languages_inDescriptions.append(language)
                break
    
    # Count the occurrences of each language
    language_counts = Counter(languages_inDescriptions)
    
    # Create a DataFrame from the language counts
    df = pd.DataFrame(list(language_counts.items()), columns=['Language', 'Occurrences'])
    
    return df


# def main():
filtered_list = exclude_stop_words(descriptions)
word_count = wordCount_Freq(filtered_list)
languages_inDescriptions = indeed_programming_languages(filtered_list)
    
# main()

##### PLOTS 
# Plot most used words in  a word plot
def create_word_cloud(word_count):
    wordcloud = WordCloud(width=800, height=800, background_color='white', colormap='inferno').generate_from_frequencies(word_count)
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# word_count is the dictionary of word frequency
create_word_cloud(word_count)

print(languages_inDescriptions)