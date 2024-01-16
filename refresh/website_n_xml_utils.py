import os
import requests
import time

# from models import add_record, update_record, read_records_2, read_records
from models.models import *
# from vectorisation.vector_store_n_query import *
from xml_filtration.format_artist_xml import *
from xml_filtration.format_critic_xml import *
from xml_filtration.format_definition_xml import *
from xml_filtration.format_influencer_xml import *
from xml_filtration.format_movement_xml import *


def download_xml_by_id(xml_id, type):
    xml_url = f"https://www.theartstory.org/data/content/{type}/{xml_id}.xml"
    output_folder = f"data/raw_xmls/{type}s"
    output_file = f"data/raw_xmls/{type}s/{xml_id}.xml"
    try:
        # Make a GET request to the XML URL
        response = requests.get(xml_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the output file in binary write mode and write the XML content
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            if os.path.exists(output_file):
                # If it exists, delete the file
                os.remove(output_file)
                print(f"Deleted existing file: {output_file}")
            else:
                print("File Doesn't Exists")
            
            with open(output_file, 'wb') as file:
                file.write(response.content)
            
            print(f"XML downloaded successfully and saved at {output_file}")
            return True
        else:
            print(f"Error: Unable to download XML. Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error: {e}")



import re
import json

import re
import json

def convert_to_underscore(input_string):
    # Using regex to replace hyphens with underscores
    result_string = re.sub(r'[-]', '_', input_string)
    return result_string



def convert_link(input_link):
    # Extract type and id using regex
    match = re.match(r'https://www.theartstory.org/(?P<type>[a-zA-Z]+)/(?P<id>[a-zA-Z-]+)/', input_link)
    
    if match:
        type = match.group('type')
        id = match.group('id')
        
        # Convert id using regex
        id = re.sub(r'-', r'_', id)
        
        # Create the new link
        new_link = f'https://www.theartstory.org/data/content/{type}/{id}.xml'
        
        # Store the information in JSON format
        result_json = {
            "website_link": input_link,
            "type": type,
            "id": id,
            "xml_link": new_link
        }
        
        return json.dumps(result_json, indent=2)
    else:
        return json.dumps({"error": "Invalid input link format"}, indent=2)


import xml.etree.ElementTree as ET

def are_xml_files_equal(xml_id, type):

    online_url = f"https://www.theartstory.org/data/content/{type}/{xml_id}.xml"

    local_path = f"data/raw_xmls/{type}s/{xml_id}.xml"
    
    # Fetch online XML
    online_response = requests.get(online_url)
    online_tree = ET.ElementTree(ET.fromstring(online_response.content))

    # Read locally stored XML
    with open(local_path, 'rb') as local_file:
        local_tree = ET.ElementTree(ET.fromstring(local_file.read()))
    
    similarity_response = ET.tostring(online_tree.getroot()) == ET.tostring(local_tree.getroot())
    
    if similarity_response == True:
        print(f"{xml_id} --> Files are Same")
    else:
        print(f"{xml_id} --> Files are Different")

    # Compare the XML structures
    return similarity_response



# # ------------ Use of convert_link() and returning JSON ------------------

# # Example usage:
# website_link = "https://www.theartstory.org/artist/picasso-pablo/"
# result = convert_link(website_link)
# json_variable = result
# print(result)

# # Load the JSON string into a dictionary
# data = json.loads(json_variable)

# # Access individual objects
# website_link = data["website_link"]
# artist_type = data["type"]
# artist_id = data["id"]
# xml_link = data["xml_link"]

# # Print the values
# print("Website Link:", website_link)
# print("Artist Type:", artist_type)
# print("Artist ID:", artist_id)
# print("XML Link:", xml_link)

# # ------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def filter_and_store_paths():
    url = "https://www.theartstory.org/sitemap.htm"
    # output_file="paths2.txt"
    count = 0
    try:
        # Fetch the HTML content of the page
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Define paths to filter
        filter_paths = ["/artist/", "/critic/", "/definition/", "/influencer/", "/movement/"]

        # Extract and filter paths from the links
        paths = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            path = urlparse(full_url).path
            if any(filter_path in path for filter_path in filter_paths):
                paths.add(path)

        for path in paths:
            count += 1
            if (count >= 6): # limit and checker
                print("\n\n Starting File No. ----------> ", count, " out of 1000.")
                # Splitting the string using "/" as the delimiter
                segments = path.split("/")

                # Extracting the first and second portions
                extracted_type = segments[1]
                extracted_id = segments[2]
                extracted_xml_id = convert_to_underscore(extracted_id)
                print(f"\nType : {extracted_type} ; ID : {extracted_xml_id}")
                if (is_value_in_csv(extracted_id) == False):
                    print(f"\nValue : \"{extracted_xml_id}\" not Found in DB")
                    # update_record(extracted_id, str(datetime.now()), column_index)
                    if (download_xml_by_id(extracted_xml_id, extracted_type) == False):
                        print("\nDownload Failed, Going to the Next One...")
                        continue
                    record_to_add = [extracted_type, extracted_xml_id, str(datetime.now()), " - ", " - ", "not-merged"]
                    add_record(record_to_add)
                    print(f"\nAdded New Record for {extracted_xml_id}")
                    if extracted_type == "artist":
                        artist_xml(extracted_xml_id)
                    if extracted_type == "critic":
                        critic_xml(extracted_xml_id)
                    if extracted_type == "definition":
                        definition_xml(extracted_xml_id)
                    if extracted_type == "movement":
                        movement_xml(extracted_xml_id)
                    if extracted_type == "influencer":
                        influencer_xml(extracted_xml_id)
                    update_record(extracted_xml_id, str(datetime.now()), 3)
                    print(f"\nUpdated Exisitng Record for {extracted_xml_id}")
                    # vectorise(extracted_xml_id, extracted_type)
                    # update_record(extracted_xml_id, str(datetime.now()), 4)
                if (are_xml_files_equal(extracted_xml_id, extracted_type) ==  False):
                    download_xml_by_id(extracted_xml_id, extracted_type)
                    if extracted_type == "artist":
                        artist_xml(extracted_xml_id)
                    if extracted_type == "critic":
                        critic_xml(extracted_xml_id)
                    if extracted_type == "definition":
                        definition_xml(extracted_xml_id)
                    if extracted_type == "movement":
                        movement_xml(extracted_xml_id)
                    if extracted_type == "influencer":
                        influencer_xml(extracted_xml_id)
                    update_record(extracted_xml_id, str(datetime.now()), 3)
                    update_record(extracted_xml_id, str(datetime.now()), 2)
                    # vectorise(extracted_xml_id, extracted_type)
                    # update_record(extracted_xml_id, str(datetime.now()), 4)
                else:
                    update_record(extracted_xml_id, str(datetime.now()), 2)
        # merge_db()


        # # Store filtered paths in a .txt file
        # with open(output_file, 'w') as file:
        #     for path in paths:
        #         file.write(path + '\n')

        print(f"Filtered paths extracted and stored in database.csv and Required Folder")
        return "Success"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return "Failure"

# Example usage:
filter_and_store_paths()
# merge_db()