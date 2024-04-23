import numpy as np
import pandas as pd
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
import re
from webdriver_manager.chrome import ChromeDriverManager
import datetime

#CWD. Include / at the end.
PATH = ''
kmovie_df = pd.read_excel(PATH + 'kmovieIMDB.xlsx')
kdrama_df = pd.read_excel(PATH + 'kdramaIMDB.xlsx')


def scrape_reviews(url, days_threshold=31):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    service = webdriver.chrome.service.Service(executable_path= PATH + 'chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    '''
    #Linux
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
    '''
    try:
        time.sleep(1)
        driver.get(url)
        time.sleep(1)

        body = driver.find_element(By.CSS_SELECTOR, 'body')
        for _ in range(3):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        sel = Selector(text=driver.page_source)
        review_counts = sel.css('.lister .header span::text').extract_first()

        if review_counts:
            review_counts = review_counts.replace(',', '').split(' ')[0]
            more_review_pages = int(int(review_counts) / 25)
        else:
            more_review_pages = 0  # Set a default value when review_counts is None


        for _ in tqdm(range(more_review_pages)):
            try:
                css_selector = 'load-more-trigger'
                driver.find_element(By.ID, css_selector).click()
                time.sleep(2)
            except:
                pass

        review_date_list = []
        review_list = []
        review_url_list = []
        error_url_list = []
        error_msg_list = []
        helpfulness_list = []
        reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')
        threshold_date = datetime.datetime.now() - datetime.timedelta(days=days_threshold)
        for d in tqdm(reviews):
                try:
                    sel2 = Selector(text=d.get_attribute('innerHTML'))

                    try:
                        review = sel2.css('.text.show-more__control::text').extract_first()
                    except:
                        review = np.NaN
                    try:
                        review_date_str = sel2.css('.review-date::text').extract_first()
                        review_date = datetime.datetime.strptime(review_date_str, '%d %B %Y')  # Adjust format accordingly
                        review_date = review_date.replace(hour=0, minute=0, second=1)  # Set time to 00:00:01
                        review_date_str = review_date.strftime('%Y-%m-%d %H:%M:%S')  # Convert to desired format
                    except:
                        review_date_str = None
                    
                    # Check if the review date is within the threshold
                    if review_date and review_date >= threshold_date:
                        try:
                            helpfulness_text = sel2.css('.text-muted::text').extract_first()
                            match = re.search(r'\d+', helpfulness_text)

                            # Check if a match is found
                            if match:
                                # Get the matched digits
                                helpfulness_text = match.group()
                            else:
                                helpfulness_text = 0
                        except:
                            helpfulness_text = 0

                        review_date_list.append(review_date_str)
                        review_list.append(review)
                        review_url_list.append(url)
                        helpfulness_list.append(helpfulness_text)
                except Exception as e:
                    error_url_list.append(url)
                    error_msg_list.append(e)

        review_df = pd.DataFrame({
            'post_created_time': review_date_list,
            'post_detail': review_list,
            'post_source': review_url_list,
            'post_like': helpfulness_list,
        })

        return review_df

    finally:
        driver.quit()

kdrama_urls = kdrama_df['url']
kdresult_df = pd.concat([scrape_reviews(url) for url in kdrama_urls], ignore_index=True)

kmovie_urls = kmovie_df['url']
kmresult_df = pd.concat([scrape_reviews(url) for url in kmovie_urls], ignore_index=True)
kdresult_df['platform'] = 'IMDB'
kmresult_df['platform'] = 'IMDB'
kdresult_df['genre'] = 'Drama'
kmresult_df['genre'] = 'Movie' 

result_df = pd.concat([kmresult_df, kdresult_df], ignore_index=True)

result_df.to_excel(PATH + 'IMDBNewResult.xlsx')