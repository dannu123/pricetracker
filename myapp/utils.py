import importlib
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def flipkart(name):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Provide the full path to chromedriver.exe
        driver = webdriver.Chrome(executable_path=r'C:\Users\raksh\OneDrive\Desktop\DjPriceCompare\chromedriver.exe', options=chrome_options)

        name1 = name.replace(" ", "+")
        flipkart_url = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'

        print("\nSearching on Flipkart....")
        driver.get(flipkart_url)

        # Scroll down to trigger lazy loading
        for _ in range(3):  # Adjust the number of scrolls as needed
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            driver.implicitly_wait(2)  # Add a short delay to allow content to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        flipkart_price, flipkart_name, flipkart_image, flipkart_link = '0', '0', '0', '0'

        product_cards = soup.find_all('div', {'class': '_1AtVbE'})

        for product_card in product_cards:
            flipkart_name_elements = product_card.select('._4rR01T')
            if flipkart_name_elements:
                flipkart_name = flipkart_name_elements[0].getText().strip().upper()
                if name.upper() in flipkart_name:
                    flipkart_price_elements = product_card.select('._30jeq3._1_WHN1')
                    flipkart_image_elements = product_card.select('._396cs4')
                    flipkart_link_elements = product_card.select('a.Zhf2z-')
                    
                    flipkart_price = flipkart_price_elements[0].getText().strip() if flipkart_price_elements else 'N/A'
                    flipkart_image = flipkart_image_elements[0]['src'] if flipkart_image_elements else 'N/A'
                    flipkart_link = 'https://www.flipkart.com' + flipkart_link_elements[0]['href'] if flipkart_link_elements else 'N/A'

                    print(flipkart_image)
                    print("Flipkart:")
                    print(flipkart_name)
                    print(flipkart_price)
                    print(flipkart_link)
                    print("---------------------------------")

                    # Assuming you want information for the first matching product only
                    break

        return flipkart_price, flipkart_name[:50], flipkart_image, flipkart_link
    except Exception as e:
        print(f"Flipkart: Error - {e}")
        print("---------------------------------")
        return '0', '0', '0', '0'


def amazon(name):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Provide the full path to chromedriver.exe
        driver = webdriver.Chrome(executable_path=r'C:\Users\raksh\OneDrive\Desktop\DjPriceCompare\chromedriver.exe', options=chrome_options)

        # Replace spaces with '+' for the URL
        name2 = name.replace(" ", "+")
        amazon_url = f'https://www.amazon.in/s?k={name2}'

        # Open the Amazon URL in the browser
        driver.get(amazon_url)

        # Wait for the page to load
        time.sleep(2)

        print("\nSearching in Amazon...")

        # Extract the page source after waiting
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        amazon_price, amazon_name, amazon_image, amazon_link = '0', '0', '0', '0'

        # Find elements using BeautifulSoup
        amazon_page = soup.select('.a-color-base.a-text-normal')

        for i, item in enumerate(amazon_page):
            amazon_name = item.getText().strip().upper()
            if name.upper() in amazon_name:
                amazon_name = item.getText().strip()
                amazon_images = soup.select('.a-section.aok-relative.s-image-fixed-height')
                amazon_image = amazon_images[i].find('img')['src']

                # Find the parent element of the price
                parent_element = item.find_parent(class_='sg-col-inner')

                # Locate the price within the parent element
                amazon_price_element = parent_element.select_one('.a-offscreen')

                # Extract the price if available
                amazon_price = amazon_price_element.text.strip() if amazon_price_element else '0'

                print("Amazon:")
                print(amazon_name)
                print(amazon_price)
                print("---------------------------------")
                break

        return amazon_price, amazon_name[:50], amazon_image, amazon_url

    except Exception as e:
        print(f"Amazon: Error - {e}")
        print("---------------------------------")
        return '0', '0', '0', '0'


def gadgetsnow(name):
    try:
        name1 = name.replace(" ", "-")
        name2 = name.replace(" ", "+")
        gadgets_now_url = f'https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={name2}'
        res = requests.get(gadgets_now_url, headers=headers)
        print("\nSearching in Gadgets Now...")
        soup = BeautifulSoup(res.text, 'html.parser')
        gadgets_now_price, gadgets_now_name, gadgets_now_image, gadgets_now_link = '0', '0', '0', '0'

        gadgets_now_page = soup.select('.product-name')
        for i, item in enumerate(gadgets_now_page):
            gadgets_now_name = item.getText().strip().upper()
            if name.upper() in gadgets_now_name:
                gadgets_now_name = item.getText().strip()
                images = soup.select('.product-img-align')[i]
                image = images.select('.lazy')[0]
                gadgets_now_image = image['data-original']
                gadgets_now_price = soup.select('.offerprice')[i].getText().strip().upper()
                gadgets_now_price = "₹" + "".join(filter(str.isdigit, gadgets_now_price))
                print("Gadgets Now:")
                print(gadgets_now_name)
                print("---------------------------------")
                break

        return gadgets_now_price, gadgets_now_name[:50], gadgets_now_image, gadgets_now_url
    except Exception as e:
        print(f"Gadgets Now: Error - {e}")
        print("---------------------------------")
        return '0', '0', '0', '0'


def croma(name):
    try:
        name2 = name.replace(" ", "+")
        croma_url = f"https://www.croma.com/search/?q={name2}:relevance:ZAStatusFlag:true:excludeOOSFlag&text={name2}"
        
        # Use the settings module to get the base directory
        chrome_driver_path = str(settings.BASE_DIR)+'\chromedriver.exe'
        print("Driver path:", chrome_driver_path)
        
        wd = webdriver.Chrome(executable_path=chrome_driver_path)
        wd.get(croma_url)
        
        wait = WebDriverWait(wd, 10)

        element_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3.product-title.plp-prod-title")))
        element_price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.amount")))
        image_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-img.plp-card-thumbnail img")))

        croma_name = element_name.text
        croma_price = element_price.text
        croma_image = image_element.get_attribute("src")
        croma_link = wd.current_url  # Added line to capture current URL
        wd.quit()

        return croma_price, croma_name[:50], croma_image, croma_link
    except Exception as e:
        print(f"Croma: Error - Message: {str(e)}")
        print("---------------------------------")
        return '0', '0', '0', '0'


def reliance(name):
    try:
        name1 = name.replace(" ", "-")
        name2 = name.replace(" ", "+")
        reliance_url = f'https://www.reliancedigital.in/search?q={name2}:relevance'
        res = requests.get(reliance_url, headers=headers)
        print("\nSearching in Reliance Digital...")
        soup = BeautifulSoup(res.text, 'html.parser')

        reliance_page = soup.select('.sp__name')
        reliance_data = soup.find('div', class_='slider-text').getText().strip()
        reliance_price = ''.join(filter(lambda char: char.isdigit() or char == '.', reliance_data.split('₹')[1]))
        reliance_image = "https://www.reliancedigital.in/" + soup.find('img', class_='img-responsive')['data-srcset']

        for i, item in enumerate(reliance_page):
            reliance_name = item.getText().strip().upper()
            if name.upper() in reliance_name:
                reliance_name = item.getText().strip()
                print("Reliance Digital:", reliance_price)
                print(reliance_name)
                print(reliance_image)
                print("₹" + reliance_price)
                print("---------------------------------")
                break

        return reliance_price, reliance_name[:50], reliance_image, reliance_url
    except Exception as e:
        print(f"Reliance Digital: Error - {e}")
        print("---------------------------------")
        return '0', '0', '0', '0'


def convert(a):
    b=a.replace(" ",'')
    c=b.replace("INR",'')
    d=c.replace(",",'')
    d=d.replace("`",'')
    f=d.replace("₹",'')
    g=int(float(f))
    try:
        if f:  # Check if the string is not empty
            g = int(float(f))
            return g
        else:
            return 0  # or return a default value when the string is empty
    except ValueError:
        return 0  # Handle any other potential conversion errors
