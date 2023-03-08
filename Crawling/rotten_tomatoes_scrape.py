import pandas as pd
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By

#INITIALISE DATAFRAMES
df_movies = pd.DataFrame(columns=['movie_title','movie_info','genres','directors','authors','actors', 'release_date'])
df_reviews = pd.DataFrame(columns=['movie_title','critic_name','top_critic','publisher_name','review_type','review_score', 'review_date','review_content'])

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)



#NAVIGATE TO TOP 100 MOVIES TAB
driver.get("https://www.rottentomatoes.com/browse/movies_at_home/sort:popular")

time.sleep(10)  
#retrieves movie name
movie_name = driver.find_elements(By.XPATH, '//a[@slot = "caption"]//span[@class = "p--small"]')
noOfMovies = len(movie_name)

for l in range(0,noOfMovies):
    
    movie_title = movie_name[l].text
    print(movie_title)
    
    #NAVIGATE TO DESCRIPTION OF A MOVIE
    selected_movie = driver.find_elements(By.XPATH, '//tile-dynamic[@isvideo = "true"]//a[@slot = "caption"]')
    driver.get(selected_movie[l].get_attribute("href"))

    # #retrieves synopsis
    synopsis = driver.find_elements(By.XPATH, '//div[@id = "movieSynopsis"]')
    synopsis = synopsis[0].text

    labels = driver.find_elements(By.XPATH, '//ul[@class = "content-meta info"]//li[@class = "meta-row clearfix"]//*[starts-with(@class, "meta-label")]')
    descriptions = driver.find_elements(By.XPATH, '//ul[@class = "content-meta info"]//li[@class = "meta-row clearfix"]//*[starts-with(@class, "meta-value")]')
    rating = ""
    genre = ""
    directors = "" 
    authors = "" 
    release_date = "" 

    for k in range(0,len(labels)):
        if("Rating" in labels[k].text):
            rating = descriptions[k].text.split("|")[0]
        
        if("Genre" in labels[k].text):
            genre = descriptions[k].text
        
        if("Director" in labels[k].text):
            directors = descriptions[k].text
        
        if("Writer" in labels[k].text):
            authors = descriptions[k].text

        if("Release Date (Theaters)" in labels[k].text):
            release_date = descriptions[k].text.replace("Wide","").strip()
            release_date = release_date.replace("Limited","").strip()

    #retrieves actor names
    actors = driver.find_elements(By.XPATH, '//div[@class = "castSection "]//*[starts-with(@class, "cast-item media")]//div[@class = "media-body"]//span')
    actors_names = ""
    for i in range(0,len(actors)):
        if(len(actors[i].text) !=0):
            actors_names = actors_names + actors[i].text + ", "
    actors_names = actors_names[:-2]

    row = pd.Series([movie_title,synopsis,genre,directors,authors,actors_names,release_date], index=df_movies.columns)
    df_movies = df_movies.append(row,ignore_index=True) 

    #NAVIGATE TO ALL CRITICS REVIEW SECTION
    all_critics_link = driver.find_elements(By.XPATH, '//div[@class="links-wrap"]//a')
    driver.get(all_critics_link[0].get_attribute("href"))

    count = 0
    while count <= 50:
        review_rows = driver.find_elements(By.XPATH, '//div[@class = "review-row"]')
        display_name_elements = driver.find_elements(By.XPATH, '//a[@class = "display-name"]')
        publication_elements = driver.find_elements(By.XPATH, '//a[@class = "publication"]')
        review_type_elements = driver.find_elements(By.XPATH, '//div[@class = "review-data"]//score-icon-critic')

        review_elements = driver.find_elements(By.XPATH, '//div[@class = "review-text-container"]//p[@class = "review-text"]')
        score_elements = driver.find_elements(By.XPATH, '//div[@class = "review-text-container"]//p[@class = "original-score-and-url"]')
        
        for r in range(0,len(review_rows)):
            display_name = "" 
            publication = "" 
            review_type = "" 
            review = ""
            date = ""
            score = "" 
            isCritic = ""

            count = count + 1
            display_name = display_name_elements[r].text
            print(display_name)
            publication = publication_elements[r].text
            review_type = review_type_elements[r].get_attribute("state")
            review = review_elements[r].text
            if("Original" in score_elements[r].text.split('|')[1]):
                date = score_elements[r].text.split('|')[2].strip()
                score = score_elements[r].text.split('|')[1].split(':')[1]
                
            else:
                date = score_elements[r].text.split('|')[1].strip()
                score = ""

            isCritic = driver.find_elements(By.XPATH, '//div[@class = "reviewer-name-and-publication"]//rt-icon-top-critic[@class = "small"]//div[@class = "wrap"]//span')
            if(len(isCritic)==0):
                isCritic = "False"
            else:
                isCritic = "True"

            row = pd.Series([movie_title,display_name,isCritic,publication,review_type,score,date,review], index=df_reviews.columns)
            df_reviews = df_reviews.append(row,ignore_index=True)

        try: 
            time.sleep(10)
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//nav[@class = "prev-next-paging__wrapper"]//rt-button[@data-direction = "next"]')))
            # next_button = driver.find_element(By.XPATH, '//nav[@class = "prev-next-paging__wrapper"]//rt-button[@data-direction = "next"]')
            next_button.click()
            time.sleep(10)  
        except NoSuchElementException:
            break
        except TimeoutException:
            break

      
        

    driver.get("https://www.rottentomatoes.com/browse/movies_at_home/sort:popular")

    time.sleep(10)
    movie_name = driver.find_elements(By.XPATH, '//a[@slot = "caption"]//span[@class = "p--small"]')
    # movie_name = driver.find_elements(By.XPATH, '//a[@class = "js-tile-link"]//img')

df_reviews.to_csv('movie_reviews.csv',index=False)
df_movies.to_csv('movies.csv',index=False)