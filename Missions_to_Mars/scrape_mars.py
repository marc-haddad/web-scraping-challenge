#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


# In[2]:


get_ipython().system('which chromedriver')


# In[3]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


url = "https://mars.nasa.gov/news/"
browser.visit(url)


# In[5]:


html = browser.html


# In[6]:


while True:
    try:
        soup = bs(html, 'html.parser')
        news_title = soup.body.find("div", class_="content_title").text
        news_p = soup.body.find("div", class_="article_teaser_body").text
    except:
        continue
    else:
        break


# In[7]:


url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[8]:


browser.click_link_by_partial_text("FULL IMAGE")


# In[9]:


while True:
    try:
        browser.click_link_by_partial_text("more info")
    except:
        continue
    else:
        break


# In[10]:


html = browser.html
soup = bs(html, 'html.parser')


# In[11]:


featured_image_url = "https://www.jpl.nasa.gov" + soup.figure.find("a")["href"]


# In[12]:


featured_image_url


# In[13]:


url = "https://twitter.com/marswxreport?lang=en"
browser.visit(url)


# In[14]:


html = browser.html
soup = bs(html, 'html.parser')


# In[15]:


mars_weather = soup.find_all("p", class_="TweetTextSize")[0].text.replace("\n", " ").replace("\xa0", " ").replace("pic.twitter", " pic.twitter")
mars_weather


# In[16]:


url = "https://space-facts.com/mars/"
tables = pd.read_html(url)
tables


# In[17]:


url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)


# In[18]:


hemi_names = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced",
             "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
hemi_dicts = []
for hemi in hemi_names:
    while True:
        try:
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


# In[19]:


hemi_dicts


# In[20]:





# In[ ]:





# In[ ]:




