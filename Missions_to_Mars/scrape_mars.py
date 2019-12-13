from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


def init_browser():

    executable_path = {"executable_path": '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html

    soup = bs(html, 'html.parser')
    news_title = soup.body.find("div", class_="content_title").text
    news_p = soup.body.find("div", class_="article_teaser_body").text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text("FULL IMAGE")
    i = 0
    while True:
        try:
            i += 1
            if i == 50:
                return 1
            browser.click_link_by_partial_text("more info")
        except:
            continue
        else:
            break

    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = "https://www.jpl.nasa.gov" + soup.figure.find("a")["href"]

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find_all("p", class_="TweetTextSize")[0].text.replace("\n", " ").replace("\xa0", " ").replace("pic.twitter", " pic.twitter")

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemi_names = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced",
                "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
    hemi_dicts = []
    i = 0
    for hemi in hemi_names:
        while True:
            try:
                i += 1
                if i == 50:
                    return 1
                browser.click_link_by_partial_text(hemi)
            except:
                continue
            else:
                break
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.find("a", target="_blank")["href"]
        title = hemi
        
        hemi_dicts.append({"title": title, "img_url": img_url})
        browser.visit(url)



    final_dict = {}

    final_dict["news_title"] = news_title
    final_dict["news_p"] = news_p
    final_dict["featured_image_url"] = featured_image_url
    final_dict["mars_weather"] = mars_weather
    final_dict["tables"] = tables
    final_dict["hemi_dicts"] = hemi_dicts


    return final_dict



