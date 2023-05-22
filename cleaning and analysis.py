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

#import

## CLEANING

data = pd.read_excel('MilanoIndeed.xlsx')
dati = data.copy()
print(dati.head(10))
print(dati.info())


# See the most used words for job descriptions

# Create a text file with only short description for every company
descrizioni = dati['Description']
with open('descrizioni.txt', 'w') as file:
    for desc in dati['Description']:
        file.write(desc + '\n')
        
# This is for replacing special characters with an empty string
def strip_puntuactions(line):
    """Function for replacing special characters %^&* to empty string"""
    for character in string.punctuation:
        line = line.replace(character, "")
    return line  

# Exclude special characters and stop words in English and Italian
# Get italian and English stop words
filepath = "descrizioni.txt"

stop_words_it = stopwords.words('italian')
stop_words_eng = stopwords.words('english')

stop_words = stop_words_it.copy()
stop_words.extend(stop_words_eng)

filtered_list = []

with open(filepath, 'r') as fi:
    #exclude special characters
    for line in fi:
        line = strip_puntuactions(line)
        words = line.split()
        
        # exclude stop words
        for word in words:
            word = word.lower()
            if word.lower() not in stop_words:
                filtered_list.append(word)
                
### ANALYSIS
         
# Word Count and Frequencies
word_count = {}

for line in filtered_list:
    line = strip_puntuactions(line)
    words = line.split()
    
    for word in words:
        word = word.lower()
        if word not in word_count:
            word_count[word] = 0
        word_count[word] += 1
            
print(f"...{list(word_count.keys())[:30]}")

# Plot most used words in  a word plot
def create_word_cloud(word_count):
    wordcloud = WordCloud(width=800, height=800, background_color='white', colormap='inferno').generate_from_frequencies(word_count)
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# word_count is the dictionary of word frequency
create_word_cloud(word_count)


#########################

# Search up for programming languages

# opening the file in read mode
my_file = open("programming_visualiz_tools.txt", "r")
  
# reading the file
data = my_file.read()
  
# replacing end splitting the text 
# when newline ('\n') is seen.
programming_languages = data.split("\n")
# print(programming_languages)
my_file.close()

filtered_list = []

with open(filepath, 'r') as fi:
    #exclude special characters
    for line in fi:
        line = strip_puntuactions(line)
        words = line.split()
        
        # exclude stop words
        for word in words:
            word = word.lower()
            if word.lower() in programming_languages:
                filtered_list.append(word)



# Word Count and Frequencies
word_count = {}


for line in filtered_list:
    line = strip_puntuactions(line)
    words = line.split()
    
    for word in words:
        word = word.lower()
        if word not in word_count:
            word_count[word] = 0
        word_count[word] += 1
            
            
print(f"...{list(word_count.keys())[:30]}")


######### Analysis on Ratings

# Change data types for analysis
dati['Ratings'] =  dati['Ratings'].str.replace(',', '.').astype(float)
dati['JobTitle'] = dati['JobTitle'].str.lower()

# Count per Job title or Company
#jobtitles = dati.groupby('JobTitle').count().reset_index()
companies = dati.groupby('Company').count().reset_index()

zero_ratings = companies.loc[companies['Ratings'] == 0]
company_names = zero_ratings.iloc[:, 0].values
print(f"Companies without rating: {company_names}")

# Ratings x company
plot_ratings = dati.fillna('')
plot_ratings = plot_ratings.loc[plot_ratings['Ratings'] != '']
sorted_plot_ratings = plot_ratings.sort_values(by='Ratings')

fig = px.bar(sorted_plot_ratings, 
             x='Company', 
             y='Ratings',
             hover_data=['Location', 'Job_types'], 
             color='Ratings',
             labels={'Salario':'Salary'}, 
             height=400)

# fig.update_layout(xaxis={'categoryorder':'category ascending'})

fig.show()

