# %%

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# %%
# Base URL of the site
# base_url = "https://www.thedieselshop.us/INDEXLSRS.html"
base_url = "https://www.rrpicturearchives.net/locoList.aspx?id="

# Function to get all links from the main page
def get_all_links():
    ArchiveList = pd.read_excel("RR Picture Archives List.xlsx")
    links = []
    Companies = ArchiveList["Reporting Marks"].to_list()
    for company in Companies:
        print(company)
        links.append(company)
    
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
    links = get_all_links()
    #! #################################################################################
    print(links)
    #return(links)
    #! #################################################################################
    all_data = []
    headers = None
    
    for link in links:
        link_url = base_url + link
        print(f"Scraping: {link}")
        table_data = scrape_table_data(link_url)
        table_data = pd.DataFrame(table_data[20:])
        table_data = table_data.iloc[:, [0,1,2,3]]
        table_data.columns = ['Unit Number', 'Notes', 'Model','Serial Number']
        cutoffrow = table_data[table_data['Unit Number'].str.startswith("Page")].index.min()
        table_data = table_data.loc[0:cutoffrow-1]
        for i in ["&Page=2","&Page=3"]:
            try:
                response = requests.head(link_url+i, allow_redirects=True, timeout=5)
                if response.status_code == 200:
                    print("URL exists!")
                    additional_data = scrape_table_data(link_url+i)
                    additional_data = pd.DataFrame(additional_data[20:])
                    additional_data = additional_data.iloc[:, [0,1,2,3]]
                    additional_data.columns = ['Unit Number', 'Notes', 'Model','Serial Number']
                    cutoffrow = additional_data[additional_data['Unit Number'].str.startswith("Page")].index.min()
                    additional_data = additional_data.loc[0:cutoffrow-1]
                    table_data = pd.concat([table_data,additional_data],axis=0)
                else:
                    print(f"URL returned status code {response.status_code}")
            except requests.RequestException as e:
                print("URL does not exist or could not be reached:", e)
        csv_name = link + ".csv"
        table_data = table_data.replace({'Â ': '_'}, regex=True)
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


# response = requests.get(base_url, verify= False)
# soup = BeautifulSoup(response.text, 'html.parser')



# # %%



# if __name__ == "__main__":
#     main()


