import csv


parent_filename = '/Users/bell/Desktop/parent_export.csv'
# child_filename  = '/Users/bell/Desktop/thea_full_no_duplicate.csv'
child_filename  = '/Users/bell/Desktop/New_nat_original_db.csv'
# feature_image_filename = '/Users/bell/Desktop/nat_image3.csv'
# feature_image_filename = '/Users/bell/Desktop/Thea_db_image_clean.csv'
feature_image_filename = '/Users/bell/Desktop/Thea_db_image_clean_classifly_duplicate.csv'

parents = []
childs = []
parent_and_child = []

#Get Parent and Child
with open(parent_filename, newline='') as f:
    products = csv.reader(f)
    
    for product in products:
        
        data_parent = {
            'Type': 'variable',
            'Name': product[1],
            'Published': '1',
            'Is featured?': '1',
            'Short description': product[4],
            'Categories': product[5],
            'Regular price': product[6],
            'In stock?': '1',
            'Parent': '',
            'Tag': product[9],
            'Attribute 1 name': 'size name',
            'Attribute 1 value(s)': product[11],
            'Attribute 1 visible': '0',
            'Attribute 1 global': '0',
            # 'Attribute 2 name': 'color id',
            # 'Attribute 2 value(s)': product[14],
            # 'Attribute 2 visible': '0',
            # 'Attribute 2 global': '0',
            'Attribute 2 name': 'color name',
            'Attribute 2 value(s)': product[15],
            'Attribute 2 visible': '0',
            'Attribute 2 global': '0',
            # 'Attribute 4 name': 'color code',
            # 'Attribute 4 value(s)': product[22],
            # 'Attribute 4 visible': '0',
            # 'Attribute 4 global': '0',
        }

        parents.append(data_parent)

with open(child_filename, newline='') as f:
    products = csv.reader(f)
    
    for product in products:
        
        data_child = {
            'Name': product[1],
            'Short description': product[2],
            'Categories': product[3],
            'Size name': product[4],
            'Regular price': product[5],
            'Stock': product[8],
            'Color id': product[9],
            'Color name': product[10],
            'Color code': product[11]
        }

        childs.append(data_child)

feature_images = []
with open(feature_image_filename, newline='') as f:
    products = csv.reader(f)

    for product in products:
        if product[0] != 'Product ID':
            feature_image = product[5]
            # array_of_feature_image = product[3]
            # first_image_of_array = array_of_feature_image.split(',')[0]

            data_feature_image = {
                'id': product[0],
                'Name': product[1],
                'Color Name': product[3],
                'Feature Image': feature_image
            }

            # print (data_feature_image)

            feature_images.append(data_feature_image)

#-----------------------------------------------------------------------
product_id = 0

for parent in parents:
    if parent['Name'] != 'Name':
        product_id = product_id + 1
        child_id = 'id:'+str(product_id)

        feature_image_jpg = ''
        for feature_image in feature_images:
            if feature_image['Name'] == parent['Name']:
                feature_image_jpg = feature_image['Feature Image']

        data_parent_and_child = {
            'ID': product_id,
            'Type': 'variable',
            'Name': parent['Name'],
            'Published': '1',
            'Is featured?': '1',
            'Short description': parent['Short description'],
            'Categories': parent['Categories'],
            'Regular price': parent['Regular price'],
            'In stock?': '1',
            'Stock': '',
            'Parent': '',
            'Attribute 1 name': 'Size',
            'Attribute 1 value(s)': parent['Attribute 1 value(s)'],
            'Attribute 1 visible': '0',
            'Attribute 1 global': '0',
            # 'Attribute 2 name': 'color id',
            # 'Attribute 2 value(s)': parent['Attribute 2 value(s)'],
            # 'Attribute 2 visible': '0',
            # 'Attribute 2 global': '0',
            'Attribute 2 name': 'Color',
            'Attribute 2 value(s)': parent['Attribute 2 value(s)'],
            'Attribute 2 visible': '0',
            'Attribute 2 global': '0',
            # 'Attribute 4 name': 'color code',
            # 'Attribute 4 value(s)': parent['Attribute 4 value(s)'],
            # 'Attribute 4 visible': '0',
            # 'Attribute 4 global': '0',
            'Images': feature_image_jpg,
            'Tag': parent['Tag'],
        }

        parent_and_child.append(data_parent_and_child)

        for child in childs:
            if child['Name'] == parent['Name']:
                parent_id = product_id
                product_id = product_id + 1

                if child['Color name'] == 'NULL':
                    color_name = 'One Color'
                else:
                    color_name = child['Color name']

                feature_image_jpg = ''
                # for feature_image in feature_images:
                    # if feature_image['id'] == child['Color id'] and feature_image['Name'] == child['Name'] and feature_image['Color Name'] == child['Color name']:
                        # feature_image_jpg = feature_image['Feature Image']

                data_parent_and_child = {
                    'ID': product_id,
                    'Type': 'variation',
                    'Name': parent['Name'],
                    'Published': '1',
                    'Is featured?': '1',
                    'Short description': child['Short description'],
                    'Categories': child['Categories'],
                    'Regular price': child['Regular price'],
                    'In stock?': '1',
                    'Stock': child['Stock'],
                    'Parent': child_id,
                    'Attribute 1 name': 'Size',
                    'Attribute 1 value(s)': child['Size name'],
                    'Attribute 1 visible': '0',
                    'Attribute 1 global': '0',
                    # 'Attribute 2 name': 'color id',
                    # 'Attribute 2 value(s)': child['Color id'],
                    # 'Attribute 2 visible': '0',
                    # 'Attribute 2 global': '0',
                    'Attribute 2 name': 'Color',
                    'Attribute 2 value(s)': color_name,
                    'Attribute 2 visible': '0',
                    'Attribute 2 global': '0',
                    # 'Attribute 4 name': 'color code',
                    # 'Attribute 4 value(s)': child['Color code'],
                    # 'Attribute 4 visible': '0',
                    # 'Attribute 4 global': '0',
                    'Images': feature_image_jpg,
                    'Tag': parent['Tag'],
                }

                parent_and_child.append(data_parent_and_child)

keys = parent_and_child[0].keys()
with open('/Users/bell/Desktop/child_export_new.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, keys)
    writer.writeheader()
    writer.writerows(parent_and_child)
