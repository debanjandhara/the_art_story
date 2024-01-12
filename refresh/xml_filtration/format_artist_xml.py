def artist_xml(id_artist):
    import xml.etree.ElementTree as ET
    import re
    import sys
    import os
    import textwrap
    
    output_file = f"data/filtered_txts/artists/{id_artist}.txt"

    output_variable = ""

    if os.path.exists(output_file):
        # If the file exists, delete it
        os.remove(output_file)

    # Specify the path to your XML file
    xml_file_path = f"data/raw_xmls/artists/{id_artist}.xml"

    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Now you can access elements in the XML file using ElementTree methods
    for main_element in root.iter('main'):
        # Extract data from specific tags
        artist_id = main_element.find('id').text
        name = main_element.find('name').text
        years_worked = main_element.find('years').text
        description = main_element.find('description').text
        # art_description = main_element.find('art_description').text
        nationality = main_element.find('nationality').text
        occupation = main_element.find('occupation').text
        birthDate = main_element.find('birthDate').text
        birthPlace = main_element.find('birthPlace').text
        deathDate = main_element.find('deathDate').text
        deathPlace = main_element.find('deathPlace').text
        publish_date = main_element.find('pub_time').text

# {name}'s Art Description : {art_description}

    output_variable += f'''Id : {artist_id}
Source Link : https://www.theartstory.org/artist/{re.sub('_', '-', artist_id)}/
Dynamic Card Iframe Link : https://www.theartstory.org/data/content/dynamic_content/ai-card/artist/{re.sub('_', '-', artist_id)}
Name : {name}
{name} Years Worked : {years_worked}
{name}'s Description : {description}

{name}'s Nationality : {nationality}
{name}'s Occupation : {occupation}
{name}'s BirthDate : {birthDate}
{name}'s BirthPlace : {birthPlace}
{name}'s DeathDate : {deathDate}
{name}'s DeathPlace : {deathPlace}
{name} Content Publish Date: {publish_date}'''

    output_variable += "\n\nQuotes : "

    for quotes in root.iter('quotes'):
        for quote in quotes.findall('q'):
            output_variable += f'{quote.text}, '

    for article in root.iter('article'):
        synopsys = article.find('synopsys').text
        cleaned_synopsys = re.sub(r'<.*?>', '', synopsys)
        output_variable += f"\n\nSynopsis : {cleaned_synopsys}"

    output_variable += "\n\nKey Ideas : "
    for idea in root.iter('idea'):
        cleaned_key_ideas = re.sub(r'<.*?>', '', idea.text)
        output_variable += f"\"{cleaned_key_ideas}\", "

    for section in root.iter('section'):
        section_title = section.get('title')
        output_variable += f"\n\n{section_title} :"

        for subsection in section.iter('subsection'):
            subsection_title = subsection.get('title')
            output_variable += f"\n\n{subsection_title} : "
            for p_element in subsection.iter('p'):
                if p_element.get('type') == 'p':
                    p_text = ' '.join(p_element.itertext())
                    cleaned_p_text = re.sub(r'<.*?>', '', p_text.strip())
                    output_variable += f"{cleaned_p_text}"

    output_variable += "\n\nArtwork : "

    for artworks in root.iter('artworks'):
        for artwork in artworks.iter('artwork'):
            artwork_title = artwork.find('title').text
            output_variable += f"\n\nTitle : {artwork_title}"
            artwork_year = artwork.find('year').text
            output_variable += f"\n\nProduced in the year : {artwork_year}"
            artwork_materials = artwork.find('materials').text
            output_variable += f"\n\nMaterial Used : {artwork_materials}"
            artwork_desc = artwork.find('desc').text
            output_variable += f"\n\nDescription  : {re.sub(r'<.*?>', '', textwrap.dedent(artwork_desc))}"
            artwork_collection = artwork.find('collection').text
            output_variable += f"\n\nFound in Collection : {artwork_collection}"

    output_variable += "\n\nRecommended Books:\n\n"

    for category in root.iter('category'):
        for subcategory in category.iter('subcategory'):
            if subcategory.get('name') == 'not_to_show':
                for entry in subcategory.iter('entry'):
                        title = entry.find('title').text
                        info = entry.find('info').text
                        link = entry.find('link').text
                        amazon_link = f"https://www.amazon.com/gp/product/{link}?tag=tharst-20"
                        output_variable += f"Title : {title}\nLink : {amazon_link}\n\n"

    output_variable += "\n\nExtra Links (Websites) : \n"
    for category in root.iter('category'):
        if category.get('name') == ('web resources'):
            for subcategory in category.iter('subcategory'):
                    for entry in subcategory.iter('entry'):
                            title = entry.find('title').text
                            info = entry.find('info').text
                            link = entry.find('link').text
                            output_variable += f"Title : {title}\nLink : {link}\n\n"

    # output_variable = ""

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(output_variable)

    print(f"Output has been written to {output_file}")