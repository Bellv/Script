import csv
import json
import lxml.html
import requests
import cssselect

from django.http import HttpResponse

# import urllib2
from bs4 import BeautifulSoup, NavigableString

#------- Get Pages --------
# #find all page
response = requests.get('http://glpworldwide.com/river/')
data = response.text
soup = BeautifulSoup(data)

raw_pages = []
all_product = soup.find('div', id='home-featured-itineraries-list')
for tag_a in all_product.find_all('a', href=True):
    url_link = str(tag_a['href'])
    raw_pages.append(url_link)

#remove duplicate url_link
no_duplicate_pages = []
for page in raw_pages:
    if page not in no_duplicate_pages:
        no_duplicate_pages.append(page)

#remove redirect page
no_duplicate_pages.remove('http://glpworldwide.com/login-2/?redirect_to=http%3A%2F%2Fglpworldwide.com%2Findex.php')
pages = no_duplicate_pages

# print (pages)
#------ print region -------
# region_csv = []
# all_product_names = soup.find_all('h3')
# region_names = soup.find_all('div', class_='continent')

# for x in range (len(all_product_names)):

#     data_region_csv = {
#         'product_name': all_product_names[x].text,
#         'region': region_names[x].text,
#         'url': no_duplicate_pages[x]

#     }
#     region_csv.append(data_region_csv)

# print (region_csv)

#-------- Hard code pages -------
# pages = [
    # 'http://glpworldwide.com/itinerary/classic-mekong/'
    # 'http://glpworldwide.com/itinerary/classic-voyage-south/'
    # 'http://glpworldwide.com/itinerary/frozen-land-penguins/'
# ]

#------ Bs4 ---------
#Beatiful Soup part
product_csv = []
product_json = []

for page in pages:
    print (page)

    response = requests.get(page)
    data = response.text
    soup = BeautifulSoup(data)

    product_name = soup.find('h1', class_='post-title entry-title').text.replace('\xa0', ' ')
    price = soup.find('span', class_='price').text.replace('From ', '').replace('\xa0', ' ').replace('$', '')
    duration = soup.find('span', class_='duration').text.replace('\xa0', ' ')
    description = soup.find('div', class_='intro').text.replace('\xa0', ' ')
    
    soup_product_map = soup.find('img', id='itin-map')
    product_map = soup_product_map['src']

    # daily_overview_table = soup.find_all('table')[0]
    soup_daily_overview = soup.find('div', id='tab1')
    pf_content_daily_overview = soup_daily_overview.find(class_='pf-content')
    daily_overview = str(pf_content_daily_overview.find('table'))
    replaced_daily_overview = daily_overview.replace(
        '<table>', '<h2>Daily Overview</h2> \n[row] \n[column span="8"] \n<div class="table-responsive"> \n<table class="table table-bordered"> \n<thead>'
    ).replace(
        '<td>Day</td>', '<th class="text-center">Day</th>'
    ).replace(
        '<td>Destination</td>', '<th class="text-center">Destination</th>'
    ).replace(
        '<td>Activities</td>', '<th class="text-center">Activities</th>'
    ).replace(
        '<tbody>', '', 1
    ).replace(
        '</tr>', '</tr> \n</thead> \n<tbody>', 1
    ).replace(
        '</table>', '</table> \n</div> \n[/column] \n[/row]'
    )

    gallery_daily_overview = []

    soup_header_image = soup.find('div', class_='lefty threequarter')
    soup_img_header_image = soup_header_image.find('img', src=True)
    header_image = soup_img_header_image['src']
    gallery_daily_overview.append(header_image)

    try:
        soup_gallery_daily_overview = pf_content_daily_overview.find('div', id='gallery-1')
        src_gallery_daily_overview = soup_gallery_daily_overview.find_all('img')
        for src in src_gallery_daily_overview:
            gallery_daily_overview.append(src['src'])
    except:
        None

    replaced_gallery_daily_overview = str(gallery_daily_overview).replace('[', '').replace(']', '').replace('\'', '').replace(',', '|').replace(' ', '')

    soup_detailed_itinerary = soup.find('div', id='tab2')
    detailed_itinerary = soup_detailed_itinerary.find(class_='pf-content')
    replaced_detailed_itinerary = str(detailed_itinerary).replace(
        '<div class="pf-content">', ''
    ).replace(
        '</div>', ''
    )

    soup_date_and_price = soup.find('div', id='tab3')
    soup_date_and_price_table = soup_date_and_price.find('div', class_='pf-content')
    date_and_price = soup_date_and_price_table
    date_and_price = str(soup_date_and_price_table).split('</table>')[0] + '</table>'
    replaced_date_and_price = date_and_price.replace(
        '<div class="pf-content"><table>' , '<div class="table-responsive"> \n<table class="table table-bordered"> \n<thead> \n</thead>'
    ).replace(
        '</table>', '</table> \n</div>'
    )
    
    soup_ship_details = soup.find('div', id='tab5')
    ship_details = soup_ship_details.find_all('div', id='conveyance-tables')
    replace_ship_details = str(ship_details).replace(
        '[<div id="conveyance-tables">', ''
    ).replace(
        ' <h3>Ship Details</h3>', '[row] \n[column span="10"]'
    ).replace(
        '<table class="deets-table">', '\n<div class="table-responsive"> \n<table class="table table-bordered text-center"> \n<thead>'
    ).replace(
        '<td>Built</td>', '<th>Built</th>'
    ).replace(
        '<td>Length</td>', '<th>Length</th>'
    ).replace(
        '<td>Decks</td>', '<th>Decks</th>'   
    ).replace(
        '<td>Cabins</td>', '<th>Cabins</th>'
    ).replace(
        '<td>Passengers</td>', '<th>Passengers</th>'
    ).replace(
        '<td>Cabin Size</td><td></td></tr>', '<th>Cabin Size</th></tr></thead>\n<tbody>\n'
    ).replace(
        '<p></p>', ''
    ).replace(
        '</table>', '\n</tbody> \n</table> \n</div> \n[/column] \n[column span="10"] \n'
    ).replace(
        '\n</table> \n</div> \n[/column] \n[column span="10"] \n </div>]', '\n</table> \n</div> \n[/column] \n[/row]'
    )

    soup_travel_tips = soup.find('div', id='tab6')
    travel_tips = str(soup_travel_tips.find(class_='pf-content'))
    replace_travel_tips = travel_tips.replace(
        '<div class="pf-content">', ''
    ).replace(
        '</div>', '', -1
    )

    #------- Replace or Reformat of code structure for WP team copy paste  ---------
    mapping_daily_overview = replaced_daily_overview.replace(
        '<thead>\n\n<tr>', '<thead>\n<tr>'
    ).replace(
        '<tr>\n<td></td>\n<td></td>\n<td></td>\n</tr>', ''
    ).replace(
        '<tbody>\n\n<tr>', '<tbody>\n<tr>'
    )
    mapping_detailed_itinerary = replaced_detailed_itinerary.replace(
        '<div class="pf-content"><table>', ''
    ).replace(
        '</div>', ''
    ).replace(
        '</p>\n<p> </p>\n<p>', '<\p>\n<p>'
    )
    mapping_date_and_price = replaced_date_and_price.replace(
        '<div class="pf-content"><table>', ''
    ).replace(
        '</div>', ''
    )
    mapping_date_and_price = mapping_date_and_price + '</div>'

    mapping_ship_details = replace_ship_details.replace(
        '</h3><h2>', '</h3>\n<h2>'
    ).replace(
        '<thead><tr><th>', '<thead>\n<tr>\n<th>'
    ).replace(
        '</th><th>', '</th>\n<th>'
    ).replace(
        '/th></tr></thead>', '/th>\n</tr>\n</thead>'
    ).replace(
        '<tr><td>', '<tr>\n<td>'
    ).replace(
        '</td><td>', '</td>\n<td>'
    ).replace(
        '</td></tr>', '</td>\n</tr>'
    )
    mapping_travel_tips = replace_travel_tips.replace(
        '<p><strong> </strong></p>', ''
    ).replace(
        '<p><strong>            </strong></p>', ''
    ).replace(
        '</p>\n\n<p>', '<\p>\n</p>'
    ).replace(
        '</ul>\n\n<p>', '</ul>\n<p>'
    )

    #------- Mapping data to csv and json
    data_csv = {
        'Product_Name': product_name,
        'Regular_Price': price,
        'Attribute_1_name': 'Days',
        'Attribute_1_value(s)': duration,
        'Short_description': description,
        'Map': product_map,
        'Images': replaced_gallery_daily_overview,
        'Daily_overview': mapping_daily_overview,
        'Detailed_itinerary': mapping_detailed_itinerary,
        'Date_and_price': mapping_date_and_price,
        'Ship_details': mapping_ship_details,
        'Travel_tips': mapping_travel_tips
    }
    product_csv.append(data_csv)

    # data_json = {
    #     'Product_Name': product_name,
    #     'Map': product_map,
    #     'Daily_overview': mapping_daily_overview,
    #     'Detailed_itinerary': mapping_detailed_itinerary,
    #     'Date_and_price': mapping_date_and_price,
    #     'Ship_details': mapping_ship_details,
    #     'Travel_tips': mapping_travel_tips
    # }
    # product_json.append(data_json)

keys = product_csv[0].keys()
with open('Desktop/product_river_v3.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, keys)
    writer.writeheader()
    writer.writerows(product_csv)

json.dumps(product_json)

# with open('Desktop/product_makong.json', 'w') as f:
#     json.dump(product_json, f)
