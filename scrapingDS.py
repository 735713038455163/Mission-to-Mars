# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#Add function called scrape_all to do the following:
# 1) Initialize the browser.
# 2) Create a data dictionary.
# 3) End the WebDriver and return the scraped data.


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #hemisphere_image_urls = mars_hemispheres(browser)
    news_title, news_paragraph = mars_news(browser)
    

    # Run all scraping functions and store results in a dictionary
    #Deliverable 2-step2:  In the def scrape_all() function in your scraping.py file,
    # create a new dictionary in the data dictionary to hold a list of dictionaries with the URL string and title of each hemisphere image
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text() 
        #print(news_title)
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #print(news_p)

    except AttributeError:
        return None, None

    return news_title, news_p

#JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

# Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-hover table-dark table-bordered thead thead-dark")

#Deliverable 2 - Step 3 create a function that will scrape the hemisphere data by using your code 
#from the Mission_to_Mars_Challenge.py file. At the end of the function, return the scraped data 
#as a list of dictionaries with the URL string and title of each hemisphere image.

def mars_hemispheres(browser):
    # 1. Open the browser and visit the URL with thumbnails of the images
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Optional delay for loading the page
    # browser.is_element_present_by_css('div.list_text', wait_time=1)

    # 2. Create a list of dictionaries to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #tip1 Find the HTML tag that holds all the links to the full-resolution images,
    #or find a common CSS element for the full-resolution image

    #tip2: Using a for loop, iterate through the tags or CSS element.
    for x in range(4):
        # Get a list of hemispheres by browsing through each article
        #tip3: Create an empty diction, hemisphere={}, inside the for loop
        hemisphere = {} 

        browser.find_by_css('a.product-item h3')[x].click()
        element=browser.links.find_by_text('Sample').first
        
        #Get image
        #img_url = browser.find_by_css('a.itemLink.product-item img')[0]['href']
        img_url=element['href']            
          
        # Get Hemisphere Title
        title = browser.find_by_css('h2.title').text
        
        # Append Hemisphere Object to List
        hemisphere['img_url'] = img_url
        hemisphere['title'] = title
        hemisphere_image_urls.append(hemisphere)
        # Browse back to repeat
        # print(hemisphere)
        browser.back()
    return hemisphere_image_urls
            
           
#end of scrape all


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())