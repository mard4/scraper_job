# Import necessary libraries, Selenium and Beautiful soup for scraping
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import string


# Get url by criteria in current_url below
def get_current_url(url, job_title, location):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="text-input-what"]').send_keys(job_title)
    time.sleep(2)    
    
#     driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(location)
    input_element = driver.find_element(By.XPATH, '//*[@id="text-input-where"]')
    input_element.send_keys(Keys.CONTROL, "a") # select all content
    input_element.send_keys(Keys.DELETE) # delete the content
#     time.sleep(1)
    input_element.send_keys(location)
        
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div').click()
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@id="jobsearch"]/button').click()
    except:
        driver.find_element(By.XPATH, '//*[@id="whatWhereFormId"]/div[3]/button').click()
    current_url = driver.current_url

    return current_url 

current_url = get_current_url('https://it.indeed.com/','Data Analyst',"Milano")   # insert job position and location
print(f"..url for scraping: {len(current_url)}")

# Opens Chrome to search for jobs in previous url
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("window-size=1400,1400")
#PATH = "C://Program Files (x86)//chromedriver.exe"
#driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome(options=chrome_options)

for i in range(0,1, 1):
#     driver.get('https://it.indeed.com/jobs?q=Data%20Analyst&l=Torino%20Piemonte&start='+str(i))
    driver.get(current_url+str(i))
    driver.implicitly_wait(5)

    jobtitles = []
    companies = []
    locations = []
    descriptions = []
    ratings = []
    job_types = []
    salaries = []
    dates = []

    jobs = driver.find_elements(By.CLASS_NAME, "slider_container")

    for job in jobs:

            jobtitle = job.find_element(By.CLASS_NAME, 'jobTitle').text.replace("new", "").strip()
            jobtitles.append(jobtitle)
            company = job.find_element(By.CLASS_NAME, 'companyName').text.replace("new", "").strip()
            companies.append(company)
            location = job.find_element(By.CLASS_NAME, 'companyLocation').text.replace("new", "").strip()
            locations.append(location)
            description = job.find_element(By.CLASS_NAME, 'job-snippet').text.replace("new", "").strip()
            descriptions.append(description)

            # RATING            
            try:
                rating_element = job.find_element(By.CLASS_NAME, 'ratingNumber')
                rating = rating_element.find_element(By.TAG_NAME, 'span').text
                ratings.append(rating)
            except:
                #print(f"No rating found for company: {company}")
                ratings.append(np.nan)

            # JOB TYPE                
            try:
                job_type_element = job.find_element(By.CLASS_NAME, 'attribute_snippet')
                job_type_aria = job_type_element.find_element(By.CSS_SELECTOR, '[aria-label="Job type"]')
                job_type_text = job_type_element.text.replace(job_type_aria.get_attribute('aria-label'), '').strip()
                job_types.append(job_type_text)
            except:
                job_types.append(np.nan)
                
            # SALARY                
            try:
                salary_element = job.find_element(By.CLASS_NAME, 'attribute_snippet')
                salary_aria = salary_element.find_element(By.CSS_SELECTOR, '[aria-label="Salary"]')
                salary_text = salary_element.text.replace(salary_aria.get_attribute('aria-label'), '').strip()
                salaries.append(salary_text)
            except:
                salaries.append(np.nan)
            
            #  PUBBLICATION DATE               
            try:
                date = job.find_element(By.CLASS_NAME, 'date').text.split('\n')[1]
                dates.append(date)
            except:
                dates.append(np.nan)

            
# close              
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.popover-x-button-close.icl-CloseButton"))).click()
            except:
                pass

    df_da=pd.DataFrame()
    df_da['JobTitle']=jobtitles
    df_da['Company']=companies
    df_da['Location']=locations
    df_da['Description']=descriptions
    df_da['Ratings']= ratings
    df_da['Job_types']= job_types
    df_da['Salary']= salaries
    df_da['Pubblication_Date']= dates
#     print(df_da)

print(f"..number of jobs scraped: {len(df_da)}")



# export
df_da.to_excel('{}/data/MilanoIndeed.xlsx', index=False)


