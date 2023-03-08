import pandas as pd
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

#INITIALISE DATAFRAMES
df_movies = pd.DataFrame(columns=['movie_title','movie_info','genres','directors','authors','actors', 'release_date'])
df_reviews = pd.DataFrame(columns=['movie_title','critic_name','top_critic','publisher_name','review_type','review_score', 'review_date','review_content'])


driver = webdriver.Chrome('chromedriver')

#NAVIGATE TO TOP 100 MOVIES TAB
driver.get("https://www.rottentomatoes.com/browse/movies_at_home/sort:popular")
movie_we = driver.find_elements(By.XPATH, '//a[@class = "js-tile-link"]')
print(len(movie_we))

driver.get(movie_we[0].get_attribute("href"))
movie_we = driver.find_elements(By.XPATH, '//div[@class="links-wrap"]//a')
driver.get(movie_we[0].get_attribute("href"))


review_rows = driver.find_elements(By.XPATH, '//div[@class = "review-row"]')


display_name = driver.find_elements(By.XPATH, '//a[@class = "display-name"]')
publication = driver.find_elements(By.XPATH, '//a[@class = "publication"]')
review_type = driver.find_elements(By.XPATH, '//div[@class = "review-data"]//score-icon-critic')

review = driver.find_elements(By.XPATH, '//div[@class = "review-text-container"]//p[@class = "review-text"]')
score = driver.find_elements(By.XPATH, '//div[@class = "review-text-container"]//p[@class = "original-score-and-url"]')
isCritic = driver.find_elements(By.XPATH, '//div[@class = "reviewer-name-and-publication"]//rt-icon-top-critic[@class = "small"]//div[@class = "wrap"]//span')

next_button = driver.find_element(By.XPATH, '//rt-button[@class = "js-prev-next-paging-next"]')
next_button.click()

print(display_name[0].text)
print(publication[0].text)
print(review_type[0].get_attribute("state"))
print(review[0].text)
if("Original" in score[0].text.split('|')[1]):
    date = score[0].text.split('|')[2].strip()
    score = score[0].text.split('|')[1].split(':')[1].strip()
    
else:
    date = score[0].text.split('|')[1].strip()
    score = ""
print(score)

if(len(isCritic)==0):
    print("Nothing")
else:
    print("TOP CRITIC")


time.sleep(1)
display_name = driver.find_elements(By.XPATH, '//a[@class = "display-name"]')
publication = driver.find_elements(By.XPATH, '//a[@class = "publication"]')
review_type = driver.find_elements(By.XPATH, '//div[@class = "review-data"]//score-icon-critic')

review = driver.find_elements(By.XPATH, '//div[@class = "review-text-container"]//p[@class = "review-text"]')
score = driver.find_elements(By.XPATH, '//div[@class = "review-text-container"]//p[@class = "original-score-and-url"]')
isCritic = driver.find_elements(By.XPATH, '//div[@class = "reviewer-name-and-publication"]//rt-icon-top-critic[@class = "small"]//div[@class = "wrap"]//span')

print(display_name[0].text)
print(publication[0].text)
print(review_type[0].get_attribute("state"))
print(review[0].text)

if("Original" in score[0].text.split('|')[1]):
    date = score[0].text.split('|')[2].strip()
    score = score[0].text.split('|')[1].split(':')[1].strip()
    
else:
    date = score[0].text.split('|')[1].strip()
    score = ""
    

print(score)
if(len(isCritic)==0):
    print("Nothing")
else:
    print("TOP CRITIC")


next_button = driver.find_element(By.XPATH, '//rt-button[@class = "js-prev-next-paging-next"]')
next_button.click()