# %%

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# %%
# Base URL of the site
# base_url = "https://www.thedieselshop.us/INDEXLSRS.html"
base_url = "http://www.thedieselshop.us/INDEXLSRS.html"
master_url = "http://www.thedieselshop.us/"

# Function to get all links from the main page
def get_all_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.endswith(".HTML") and "thedieselshop.us" not in href:
        #if href.endswith(".html") and "thedieselshop.us" in href:
            links.append(master_url + href)
    
    return links

# Function to scrape table data from a given page
def scrape_table_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    
    data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols = [col.text.strip() for col in cols]
            if cols:  # Ensure it's not an empty row
                data.append(cols)
    return data

# Main function to scrape all pages
def main():
    links = get_all_links(base_url)
    #! #################################################################################
    print(links)
    #return(links)
    #! #################################################################################
    all_data = []
    headers = None
    
    for link in links:
        print(f"Scraping: {link}")
        table_data = scrape_table_data(link)
        table_data = pd.DataFrame(table_data[3:],index=None)
        link_name = link.rsplit("/",1)[1]
        link_name = link_name.rsplit(".",1)[0]
        csv_name = link_name + ".csv"
        table_data.to_csv(csv_name, index=False)
        print(table_data)
    #     if table_data:
    #         if headers is None:
    #             headers = table_data[0]  # Assume first row as header
    #         all_data.extend(table_data[1:])
        
    #     time.sleep(1)  # Respectful delay to avoid being blocked
    
    # if all_data:
    #     df = pd.DataFrame(all_data, columns=headers)
    #     df.to_csv("diesel_data.csv", index=False)
    #     print("Data saved to diesel_data.csv")
    # else:
    #     print("No data scraped.")



# %%

links = main()

print(links)
# %%


response = requests.get(base_url, verify= False)
soup = BeautifulSoup(response.text, 'html.parser')



# %%



if __name__ == "__main__":
    main()


