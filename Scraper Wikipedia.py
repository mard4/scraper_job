# Import necessary libraries, Selenium and Beautiful soup for scraping
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
import string


# Scrape all programming languages for text key analysis with job description

r = requests.get("https://en.wikipedia.org/wiki/Timeline_of_programming_languages")
# Convert to a beautiful soup object
soup = bs(r.text, 'html.parser')

# table = soup.find_all("table", attrs={"class":"wikitable sortable"})
tables = soup.find_all("table", class_="wikitable sortable")

all_languages = pd.DataFrame()

# Iterate through each table and append it to dataframe
for table in tables:
    df = pd.read_html(str(table))[0]
    all_languages = all_languages.append(df)
    
# Drop the rows where column names are repeated
all_languages = all_languages[~all_languages.iloc[:, 0].str.contains('Programming language|Year', na=False)]
all_languages.reset_index(drop=True, inplace=True)

print(f"..number of languages scraped: {len(all_languages)}")

# Visualization Tools
r = requests.get("https://hevodata.com/learn/data-analysis-tools/")
soup = bs(r.text, 'html.parser')

a_elements = soup.find_all("a", class_="rank-math-link")
viz_tools = []
for a in a_elements:
    viz_tools.append(a.text)
    
viz_tools = viz_tools[11:]

# Merge into single dataframe
viz_tools = pd.Series(viz_tools)
all_languages['Visualization Tools'] = viz_tools

print("..executed")

# export

# export
#all_languages.to_excel('{}/data/MilanoIndeed.xlsx', index=False)
