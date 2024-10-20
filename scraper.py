'''
Tutorial:
https://www.youtube.com/watch?v=DqtlR0y0suo
'''

import requests
from bs4 import BeautifulSoup
import json
import time
from lxml import etree

def scrape_page(page: int):

    url = "https://ingredientbrothers.com/bulk-products/"

    payload = json.dumps({
    "action": "facetwp_refresh",
    "data": {
        "facets": {
        "product_search": "",
        "product_categories": [],
        "product_tags": [],
        "product_category_dropdown": [],
        "product_pager": []
        },
        "frozen_facets": {},
        "http_params": {
        "get": [],
        "uri": "bulk-products",
        "url_vars": []
        },
        "template": "wp",
        "extras": {
        "sort": "default"
        },
        "soft_refresh": 1,
        "is_bfcache": 1,
        "first_load": 0,
        "paged": page # page number
    }
    })
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': 'sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2024-10-11%2009%3A37%3A02%7C%7C%7Cep%3Dhttps%3A%2F%2Fingredientbrothers.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2024-10-11%2009%3A37%3A02%7C%7C%7Cep%3Dhttps%3A%2F%2Fingredientbrothers.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; _ga=GA1.1.593389484.1728639422; _gcl_au=1.1.724200144.1728639422; _reb2buid=b4bf1b4c-ade4-4a24-aaa2-ec4d323897d0-1728639422534; _reb2bgeo=%7B%22city%22%3A%22Kaohsiung%22%2C%22country%22%3A%22Taiwan%22%2C%22countryCode%22%3A%22TW%22%2C%22hosting%22%3Afalse%2C%22isp%22%3A%22Chunghwa%20Telecom%20Co.%2C%20Ltd.%22%2C%22lat%22%3A22.6148%2C%22proxy%22%3Afalse%2C%22region%22%3A%22KHH%22%2C%22regionName%22%3A%22Kaohsiung%22%2C%22status%22%3A%22success%22%2C%22timezone%22%3A%22Asia%2FTaipei%22%2C%22zip%22%3A%22%22%7D; pum-1198=true; _reb2bref=https://ingredientbrothers.com/bulk-product-category/bulk-nuts-seeds/; sbjs_udata=vst%3D3%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F129.0.0.0%20Safari%2F537.36; __cf_bm=4DXnPKixeTdY1YxSm_dI_hwFeVSvYjY0_1oYUWRkdXA-1729258894-1.0.1.1-vI0K7.1WkqGyHezOzQXiil02WikAagrBWh4D_l5mSl6UWnR.LWFCmF0Wwtmp2HTzLOrRz15_cFlITjhisRyUQA; sbjs_session=pgs%3D39%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fingredientbrothers.com%2Fbulk-products%2F; _ga_X3LD3T6B41=GS1.1.1729255005.3.1.1729259401.60.0.2071050812; __cf_bm=ys2GsWMcbGHqI_T7m_QXzSS9MRlljLQI7.lsCJw1ITw-1729261193-1.0.1.1-S1d5ntkM8Oo8eYypunn3vAHANtooO5BJ9JFb73ZMkDRXIIasd0Qq37Jx5u70yOM8omCv7LL.mnAhgPOOP.nVzA',
    'origin': 'https://ingredientbrothers.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://ingredientbrothers.com/bulk-products/',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response

def scrape_origins(url: str):
    # Fetch the page content
    response = requests.get(url)
    html_content = response.content

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Use the CSS selector to find the specific element
    element = soup.find('tr', class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_origin-countries')

    # If the element exists, print its text content
    if element:
        # Now, find the 'p' tag within that 'tr' element
        country_text = element.find('p').text
        # Replace ' and ' with ', ' to standardize the separation
        country_text = country_text.replace(', and ', ' and ') # fix: United States, Canada, China, and Russia
        standardized_text = country_text.replace(' and ', ', ')

        # Split the text into a list using ', ' as the separator
        countries = [country.strip() for country in standardized_text.split(',')]

        return countries
    else:
        print("Element not found")
    
    
def main():
    products = []
    page = 1

    while True:

        response = scrape_page(page)   

        data = json.loads(response.text)
        html_content = data['template']
        soup = BeautifulSoup(html_content, 'html.parser')
        product_links = soup.find_all('a', class_='woocommerce-LoopProduct-link') # <a class="woocommerce-LoopProduct-link woocommerce-loop-product__link" ...</a>

        # Step 3: Extract product information
        for link in product_links:
            title = link.h2.text.strip()
            title = ' '.join(title.split())
            url = link['href']
            img = link.img['src']
            
            # Create a product dictionary
            product_info = {
                "title": title,
                "url": url,
                "img": img
            }
            products.append(product_info)
        # save to json file
        print(f"Page {page} scraped")
        print(f"Total items scraped: {len(products)}")
        print(f"Items on this page: {len(product_links)}")
        if len(product_links) < 18:
            break
        
        page += 1
        time.sleep(1)
        

    with open('products.json', 'w') as f:
            json.dump(products, f)

# if __name__ == '__main__':
    # main()
    # print("Scraping completed!")
    # scrape_origins('https://ingredientbrothers.com/bulk-products/bulk-acai-freeze-dried-powder-organic/')