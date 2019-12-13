from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():

    executable_path = {"executable_path": '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


# Define func to scrape various data sources
def scrape():
    browser = init_browser()

    # Get latest news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

        # Give browser some time to load
    time.sleep(1)

        # Gather and parse html data
    html = browser.html
    soup = bs(html, 'html.parser')

        # Save headline and blurb
    news_title = soup.body.find("div", class_="content_title").text
    news_p = soup.body.find("div", class_="article_teaser_body").text

    # Get featured img url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

        # Navigate to full-res img
    browser.click_link_by_partial_text("FULL IMAGE")    
    
    time.sleep(1)
    
    browser.click_link_by_partial_text("more info")

        # Store relevant html info
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = "https://www.jpl.nasa.gov" + soup.figure.find("a")["href"]

    # Get the latest weather from official twitter
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

        # Store relevant html info
    mars_weather = soup.find_all("p", class_="TweetTextSize")[0].text.replace("\n", " ").replace("\xa0", " ").replace("pic.twitter", " pic.twitter")

    # Get Mars facts
    url = "https://space-facts.com/mars/"
        # Use Pandas to convert html to df; No Splinter navigation needed
    tables_df = pd.read_html(url)[0]
        # Alter column names
    tables_df = tables_df.rename(columns={0: "Description", 1: "Value"})
        # Transform back to html
    tables = tables_df.to_html()
    
    # Get Mars Hemisphere images
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
        # List names
    hemi_names = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced",
                "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
        # Initialize empty list
    hemi_dicts = []

        # Iterate over names to gather img urls
    for hemi in hemi_names:

        browser.click_link_by_partial_text(hemi)

        time.sleep(0.5)

        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.find("a", target="_blank")["href"]
        title = hemi
        # Append dict to initialized list
        hemi_dicts.append({"title": title, "img_url": img_url})
        browser.visit(url)


    # Final dict to be exported to Mongo
        # Initialize
    final_dict = {}

        # Define key-val pairs that contain all data gathered
    final_dict["news_title"] = news_title
    final_dict["news_p"] = news_p
    final_dict["featured_image_url"] = featured_image_url
    final_dict["mars_weather"] = mars_weather
    final_dict["tables"] = tables
    final_dict["hemi_dicts"] = hemi_dicts

        # Export when called
    return final_dict



