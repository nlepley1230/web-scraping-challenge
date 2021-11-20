# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    Mars_News_dict = Mars_News()
    Mars_Featured_Image_dict = Mars_Featured_Image()
    Mars_Fact_dict = Mars_Fact()
    Mars_Hemispheres_dict = Mars_Hemispheres()

    mars_dict = {**Mars_News_dict, **Mars_Featured_Image_dict, **Mars_Fact_dict, **Mars_Hemispheres_dict}

    return mars_dict



def Mars_News():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get a list of all news division and pick out the latest one
    status = True
    while status:
        try:
            results = soup.find_all('div', class_='list_text')
            result = results[0]
            status = False
        except:
            pass

    # Identify and return title and article
    news_title = result.find('div', class_='content_title').a.text.strip()
    news_article = result.find('div', class_='article_teaser_body').text.strip()

    browser.quit()

    Mars_News_dict = {}
    Mars_News_dict['news_title'] = news_title
    Mars_News_dict['news_article'] = news_article

    return Mars_News_dict



def Mars_Featured_Image():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Open up full image
    status = True
    while status:
        try:
            browser.links.find_by_partial_text('FULL IMAGE').click()

            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')

            image_box = soup.find('div', class_='fancybox-inner')
            featured_image_url = image_url.replace('index.html', '') + image_box.img['src']
            status = False
        except:
            pass
    

    browser.quit()

    Mars_Featured_Image_dict = {}
    Mars_Featured_Image_dict['featured_image_url'] = featured_image_url

    return Mars_Featured_Image_dict



def Mars_Fact():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html

    tables = pd.read_html(facts_url)
    table = tables[0]
    table.columns = ['Description', 'Mars']
    
    table_html = table.to_html(index=False, classes = "table table-striped")
    Mars_Fact_dict= {'table_html': table_html}

    browser.quit()

    return Mars_Fact_dict



def Mars_Hemispheres():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

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
        original = download.find_all('li')[0].a['href']
        image_dict['img_url'] = original
        image_list.append(image_dict)
        
        browser.back()

    browser.quit()

    Mars_Hemispheres_dict = {}
    Mars_Hemispheres_dict['image_urls'] = image_list
    
    return Mars_Hemispheres_dict 