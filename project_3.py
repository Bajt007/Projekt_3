"""
project_3.py: third project in Engeto Online Python Academy, started in January 23, 2025
author: Richard Ryzí
email: ryzi.richard@gmail.com
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def retrieve_html_content(url: str) -> str:
    """Retrieves HTML content from the given URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error retrieving URL: {url} --> Status code {response.status_code}")
            print(f"Please check whether the provided URL is valid")
            return ""
    except Exception as error:
        print(error)
        return ""

def get_municipality_links(html_content: str) -> dict[str, str]:
    """Analyzes HTML content and extracts links to municipalities."""
    soup = BeautifulSoup(html_content, 'html.parser')
    municipality_links = {}
    tables = soup.find_all('table', class_='table')
    for table in tables:
        for row in table.find_all('tr'):
            municipality_code_td = row.find('td', class_='cislo')
            if municipality_code_td:
                link_tag = municipality_code_td.find('a')
                if link_tag and 'href' in link_tag.attrs:
                    municipality_code = link_tag.text
                    relative_url = link_tag['href']
                    municipality_links[municipality_code] = relative_url
    return municipality_links

def extract_municipality_data(html_content: str, municipality_code: str) -> dict[str, str]:
    """Extracts relevant data for each municipality from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Code
    municipality_data = {"code": municipality_code}

    # Location
    location_elements = soup.find_all('h3')
    for h3_element in location_elements:
        if "Obec:" in h3_element.text:
            location = h3_element.text.replace("Obec:", "").strip()
            municipality_data["location"] = location
            break
    
    # Registered votes
    registered_element = soup.find('td', headers='sa2')
    municipality_data["registered"] = registered_element.text.replace("\xa0", " ") if registered_element else None
   
    # Issued envelopes
    envelopes_element = soup.find('td', headers='sa5')
    municipality_data["envelopes"] = envelopes_element.text if envelopes_element else None

    # Valid votes
    valid_element = soup.find('td', headers='sa6')
    municipality_data["valid"] = valid_element.text if valid_element else None

    # Political party data
    table_rows = soup.find_all('tr')
    for row in table_rows:
        party_name_element = row.find('td', class_='overflow_name')
        if party_name_element:
            party_name = party_name_element.text.strip()
            votes_element = party_name_element.find_next_sibling('td')
            if votes_element:
                votes = votes_element.text.strip()
                municipality_data[party_name] = votes
    return municipality_data


def export_results_to_csv(results: dict[str, dict[str, str]], output_file: str):
    """Exports the extracted results to CSV file."""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if results:
                first_row_keys = list(list(results.values())[0].keys())
                writer.writerow(first_row_keys)
                for municipality_data in results.values():
                    row_values = [municipality_data.get(key, '') for key in first_row_keys]
                    # for key in first_row_keys:
                    #   value = municipality_data.get(key, '')
                    #   row_values.append(value)
                    writer.writerow(row_values)      
    except Exception as e:
        print(f"Error while exporting into CSV: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python project_3.py "url" output_filename')
        sys.exit()

    base_url = sys.argv[1]
    output_filename = sys.argv[2] + ".csv"
   
    main_page_html = retrieve_html_content(base_url)
    if not main_page_html:
        sys.exit()
  
    print(f"DOWNLOADING DATA FROM THE SELECTED URL: {base_url}")
    municipality_links = get_municipality_links(main_page_html)
   
    base_detail_url = "https://www.volby.cz/pls/ps2017nss/"
    all_results = {}

    for code, relative_url in municipality_links.items():
        complete_url = base_detail_url + relative_url
        try:
            municipality_html = retrieve_html_content(complete_url)
            if municipality_html:
                municipality_data = extract_municipality_data(municipality_html, code)
                all_results[code] = municipality_data
        except Exception as e:
            print(f"Error processing municipality {code} from {complete_url}: {e}")

    # pprint(all_results)
    print(f"SAVING TO CSV FILE: {output_filename}")
    export_results_to_csv(all_results, output_filename)
    print("TERMINATING PROGRAM")