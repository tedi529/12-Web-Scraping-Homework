# Dependencies and Setup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# Initialize browser 
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Initialize empty dictionary to be used to store scraped data in Mongo
mars_data = {}

# Define scrape functions and store data into dictionary created above
#################################

# NASA Mars News
def scrape_news():
    browser = init_browser()

    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url) 
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('div', class_='content_title')
    mars_data['news_title'] = title.find('a').text

    paragraph = soup.find('div', class_='article_teaser_body')
    mars_data['news_p'] = paragraph.text

    return mars_data

    time.sleep(10)
    browser.quit()

# JPL Mars Space Featured Image
def scrape_feat_image():
    browser = init_browser()

    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_url = soup.find('article')["style"].split("('")[1].split("')")[0]
    site_url = "https://www.jpl.nasa.gov"
    mars_data['featured_image_url'] = site_url + image_url

    return mars_data

    time.sleep(10)
    browser.quit()

# Twitter Latest Mars Weather 
def scrape_weather():
    driver = webdriver.Chrome()

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    driver.get(twitter_url)
    time.sleep(5)

    body = driver.find_element_by_tag_name('body')
    body.send_keys(Keys.PAGE_DOWN)
    
    mars_twitter_html = driver.page_source
    soup = BeautifulSoup(mars_twitter_html, 'html.parser')

    weather = soup.find_all(class_ = 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')

    for item in weather:
        if item.text.split(" ")[0] =='InSight':
            weather = item.text
            break

    time.sleep(5)

    mars_data['weather'] = weather

    return mars_data

    time.sleep(10)
    driver.quit()

# Mars Facts 
def scrape_facts():
    facts_url = "https://space-facts.com/mars/"
    
    # Scrape tabular data in website using pandas
    mars_facts = pd.read_html(facts_url)
    mars_df = pd.DataFrame(mars_facts[0]).rename(columns={0: "Attribute", 1: "Value"})
    
    #Convert to html table
    html_table_mars = mars_df.to_html(index=False)
    html_table_mars.replace('\n', '')
    mars_data["mars_facts_table"] = html_table_mars

    return mars_data

    time.sleep(10)
    browser.quit()

# Mars Facts 
def scrape_hemispheres():
    browser = init_browser()

    landing_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"
    browser.visit(landing_url)

    hemisphere_image_urls = []

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    container = soup.find_all('div', class_='item')
    for hemi in container:
        titles = hemi.find('h3').text
    
    # Find URL of each hemisphere page 
        partial_hemi_url = hemi.find('a')['href']
        hemi_url = base_url + partial_hemi_url
    
    # Visit each URL and extract image URL
        browser.visit(hemi_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser') 
        wrapper = soup.find('div', class_='downloads')
        images = wrapper.find('a')['href']
    
        hemi_dict = dict({"title": titles, "img_url": images})
        hemisphere_image_urls.append(hemi_dict)

    mars_data['hemisphere_titles'] = [k['title'] for k in hemisphere_image_urls]
    mars_data['hemisphere_images'] = [v['img_url'] for v in hemisphere_image_urls]

    return mars_data

    time.sleep(10)
    browser.quit()
