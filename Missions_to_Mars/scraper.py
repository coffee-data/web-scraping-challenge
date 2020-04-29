from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	return "HELLO PLEASE"

def scraper():
	browser = init_browser()

	# Visit NASA
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)

	# Pause, continue
	time.sleep(2)

	# HTML object
	html = browser.html
	# Parse HTML with Beautiful Soup
	soup = BeautifulSoup(html, 'html.parser')
	# Retrieve all elements that contain book information
	articles = soup.find_all('li', class_='slide')

	for article in articles:
	    # Retrieve specific div with class
	    div = article.find('div', class_='content_title')
	    # Funnel to 'a'
	    title = div.find('a')
	    # Only grab text
	    news_title = title.text
	    # Retrieve specific div with class
	    div = article.find('div', class_='article_teaser_body')
	    # Only grab text
	    news_p = div.text
	    
	# Put results in dict
	NASA_NEWS = [{
	    "news_title":news_title,
	    "news_p":news_p
	}]


	# Visit NASA images
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url)

	# Pause, continue
	time.sleep(2)

	# HTML object
	html = browser.html
	# Parse HTML with Beautiful Soup
	soup = BeautifulSoup(html, 'html.parser')
	# Retrieve all elements that contain book information
	articles = soup.find_all('article', class_='carousel_item')

	for article in articles:
	    # Retrieve a to find href
	    a = article.find('a')
	    # Concatenate with base url
	    featured_image_url = 'https://www.jpl.nasa.gov/' + a['data-fancybox-href']
	
	# Put results in dict
	FEAT_IMG = [{
	"FEAT_IMG":featured_image_url
	}]


	# Visit Mars Twitter
	url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(url)

	# Pause, continue
	time.sleep(2)

	# HTML object
	html = browser.html
	# Parse HTML with Beautiful Soup
	soup = BeautifulSoup(html, 'html.parser')
	# Retrieve all elements that contain book information
	tweets = soup.find('div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o')

	div = tweets.find('div', class_='css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
	span = div.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
	mars_weather = span.text

	MARS_WEATHER = [{
	"MARS_WEATHER":mars_weather
	}]


	# Visit Spcae Facts
	url = 'https://space-facts.com/mars/'
	browser.visit(url)

	# Pause, continue
	time.sleep(2)

	# Read url into html tables and view
	tables = pd.read_html(url)
	tables

	# Slice out the table of choice
	df = tables[0]
	# Name columns
	df.columns = [
	    'Data_Type',
	    'Data_Value'
	]
	# Preview
	df.head()
	# Replace colons
	df['Data_Type'] = df.Data_Type.str.replace(':',"")

	df.set_index('Data_Type', inplace=True)

	# Convert to html table string
	html_table = df.to_html()
	html_table

	# Remove new line text
	html_table.replace('\n', '')

	# Save to file
	df.to_html('table.html')

	SPACE_TABLE = [{
	"SPACE_TABLE":df
	}]


	# Visit Astrology
	url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url)

	# Pause, continue
	time.sleep(2)

	# Iterate through all pages

	# HTML object
	html = browser.html
	# Parse HTML with Beautiful Soup
	soup = BeautifulSoup(html, 'html.parser')
	# Retrieve all elements that contain book information
	photos = soup.find_all('div', class_='description')

	hemisphere_image_urls = []

	# Iterate through each book
	for photo in photos:
	    
	    section = photo.find('a', class_='itemLink product-item')
	    href_text = section.find('h3').text
	    
	    # Assign for dict
	    title = href_text
	    
	    try:
	        browser.click_link_by_partial_text(href_text)
	        
	        # HTML object
	        html = browser.html
	        # Parse HTML with Beautiful Soup
	        soup = BeautifulSoup(html, 'html.parser')
	        # Retrieve all elements that contain book information
	        
	        divs = soup.find('div', class_='downloads')
	        a_href = divs.find('a')
	        href = a_href['href']
	        
	        # Assign for dict
	        img_url = href
	        
	        # Create a dictionary with elements
	        dict = ({
	            'title':title,
	            'img_url':img_url
	        })
	        
	        # Append to outside list
	        hemisphere_image_urls.append(dict)
	        
	        # Return to previous page
	        browser.back()
	    
	    except:
	        print('Whoops')

	MARS_IMGS = [{
	"MARS_IMGS":hemisphere_image_urls
	}]

	final_dict = {
	"NASA_NEWS":NASA_NEWS,
	"FEAT_IMG":FEAT_IMG,
	"MARS_WEATHER":MARS_WEATHER,
	"SPACE_TABLE":SPACE_TABLE,
	"MARS_IMGS":MARS_IMGS
	}

	return final_dict