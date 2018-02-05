import csv


parent = []
temp = []

filename = '/Users/bell/Desktop/New_nat_original_db.csv'

def generate_attribute(product_name, short_description, category, regular_price, collection, product):
    #Generate different Attribute 1
    att_size_name = []
    att_color_id = []
    att_color_name = []
    att_color_code = []
            
    for each_temp in temp:
        att_size_name.append(each_temp[2])
        att_color_id.append(each_temp[3])
        att_color_name.append(each_temp[4])
        att_color_code.append(each_temp[5])

    att_size_name = list(set(att_size_name))
    att_size_name_value = ", ".join(att_size_name)

    att_color_id = list(set(att_color_id))
    att_color_id_value = ", ".join(att_color_id)

    att_color_names = list(set(att_color_name))
    att_color_name_no_null = []
    for att_color_name in att_color_names:
        if att_color_name == 'NULL':
            att_color_name = 'One Color'
            att_color_name_no_null.append(att_color_name)
        else:
            att_color_name_no_null.append(att_color_name)

    att_color_name_value = ", ".join(att_color_name_no_null)

    att_color_code = list(set(att_color_code))
    att_color_code_value = ", ".join(att_color_code)

    #Creating product object
    data_product = {
        'Type': 'variable',
        'Name': product_name,
        'Published': '1',
        'Is featured?': '1',
        'Short description': short_description,
        'Categories': category,
        'Regular price': '',
        'In stock?': '0',
        # 'Stock': ,
        'Parent': '',
        'Tag': collection,
        'Attribute 1 name': 'Size',
        'Attribute 1 value(s)': att_size_name_value,
        'Attribute 1 visible': '0',
        'Attribute 1 global': '0',
        # 'Attribute 2 name': 'color id',
        # 'Attribute 2 value(s)': att_color_id_value,
        # 'Attribute 2 visible': '0',
        # 'Attribute 2 global': '0',
        'Attribute 2 name': 'Name',
        'Attribute 2 value(s)': att_color_name_value,
        'Attribute 2 visible': '0',
        'Attribute 2 global': '0',
        # 'Attribute 4 name': 'color code',
        # 'Attribute 4 value(s)': att_color_code_value,
        # 'Attribute 4 visible': '0',
        # 'Attribute 4 global': '0',
    }

    return data_product

#main
max_num_lines = sum(1 for line in open(filename, newline=''))
with open(filename, newline='') as f:
    products = csv.reader(f)
    current_num_lines = 0

    for product in products:
        current_num_lines = current_num_lines + 1

        # product_id, product_name, attribute_1_size_name, attribute_2_color_id, attribute_3_color_name, attribute_4_color_code
        # short description, Categories(type), Regular price(price), stock, collection, status
        temp_data = [product[0] ,product[1], product[4], product[9], product[10], product[11], product[2], product[3], product[5], product[13], product[12]]
        first_temp = ''
        if len(temp) > 0:
            first_temp = temp[0]

        #Compare and Select Case
        header_text = [
            'icweb_cms_products_ID', 
            'icweb_cms_products_Name', 
            'icweb_cms_products_size_Name', 
            'icweb_cms_products_size_colorID', 
            'icweb_cms_products_color_Name', 
            'icweb_cms_products_color_Code',
            'icweb_cms_products_Description',
            'icweb_cms_products_Type',
            'icweb_cms_products_size_PriceTHB',
            'icweb_cms_products_collection_Name',
            'icweb_cms_products_Status'
        ]
        if temp_data[10] == 'Enable':
            if temp_data == header_text:
                None

            elif len(temp) == 0 and temp_data != header_text:
                temp.append(temp_data)

            elif temp_data[0] == first_temp[0] and temp_data[1] == first_temp[1]:
                temp.append(temp_data)

                #print last line out (in case duplicate last line only)
                if current_num_lines == max_num_lines:
                    product_name = first_temp[1]
                    short_description = first_temp[6]
                    category = first_temp[7]
                    regular_price = first_temp[8]
                    collection = first_temp[9]
                    data_product = generate_attribute(product_name, short_description, category, regular_price, collection, product)
                    parent.append(data_product)

            elif temp_data[0] != first_temp[0] and temp_data[1] != first_temp[1]:
                #Mapping Value from temp
                product_name = first_temp[1]
                short_description = first_temp[6]
                category = first_temp[7]
                regular_price = first_temp[8]
                collection = first_temp[9]
                data_product = generate_attribute(product_name, short_description, category, regular_price, collection, product)
                parent.append(data_product)

                temp = []
                temp.append(temp_data)

#Generate Parent Product CSV File
keys = parent[0].keys()
with open('/Users/bell/Desktop/parent_export.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, keys)
    writer.writeheader()
    writer.writerows(parent)

