# Dependencies
from bs4 import BeautifulSoup
from bs4.element import XMLProcessingInstruction
import requests
import pandas as pd
import datetime as dt
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    print("Starting to scrape")
    News_header, News_article = get_mars_news()
    print(News_header,News_article)

    mars_data = {
        'news_title' : News_header,
        'news_article' : News_article,
        'featured_image' : get_mars_images(browser),
        'mars_facts' : get_mars_facts(),
        'hemispheres' : get_mars_hemispheres(browser),
        'last_modified' : dt.datetime.now()
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data


def get_mars_news():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
  
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_title = soup.find('div', class_='content_title').get_text()
    news_title = news_title.replace('\n', '')

    news_article =  soup.find('div', class_='rollover_description_inner').get_text()
    news_article = news_article.replace('\n', '')

    print(news_title)
    return news_title, news_article 

def get_mars_images(browser):

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain image
    for item in soup.find_all('img', class_='headerimage fade-in'):
        featuredimage = item['src']

    featuredimage = url + featuredimage
    print(featuredimage)
    return featuredimage


def get_mars_facts():

    df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')

    return df.to_html(classes="table table-striped")


def get_mars_hemispheres(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url) 

    html = browser.html

    # Create an empty list to store the dicts for image name and urls
    hemisphere_image_urls = []

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img', class_="thumb")

    print(images)
 
images = soup.find_all('div', class_='description')

image_list = []
for image in images:
    image_dict = {}
    image_title = image.a.h3.text
    image_dict['title'] = image_title
    
    browser.links.find_by_partial_text(image_title).click()
    
    new_html = browser.html
    new_soup = BeautifulSoup(new_html, 'html.parser')
    
    download = new_soup.find('div', class_='downloads')
    original = download.find_all('li')[1].a['href']
    image_dict['img_url'] = original
    image_list.append(image_dict)
    
    browser.back()

image_list 

    browser.quit() 

    return (image_list)
