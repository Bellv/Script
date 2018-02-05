import csv
import requests


filename_main = '/Users/bell/Desktop/child_export_new.csv'
filename_success = '/Users/bell/Desktop/success_image_export_v2.csv'
# filename_db_image = '/Users/bell/Desktop/Thea_db_image_clean.csv'
filename_db_image = '/Users/bell/Desktop/Thea_db_image_clean_classifly_duplicate.csv'

def get_main_data(filename_main):
    main_table = []
    with open(filename_main, newline='') as f:
        products = csv.reader(f)

        for product in products:
            data_main = {
                'ID': product[0],
                'Type': product[1],
                'Name': product[2],
                'Published': '1',
                'Is featured?': '1',
                'Short description': product[5],
                'Categories': product[6],
                'Regular price': product[7],
                'In stock?': '1',
                'Stock': product[9],
                'Parent': product[10],
                'Attribute 1 name': 'Size',
                'Attribute 1 value(s)': product[12],
                'Attribute 1 visible': '0',
                'Attribute 1 global': '0',
                'Attribute 2 name': 'Color',
                'Attribute 2 value(s)': product[16],
                'Attribute 2 visible': '0',
                'Attribute 2 global': '0',
                'Images': product[19],
                'Tag': product[20]
            }
            main_table.append(data_main)
       
    return main_table

def get_db_image_data(filename_db_image):
    db_image_data = []
    with open(filename_db_image, newline='') as f:
            products = csv.reader(f)

            for product in products:

                data_db = {
                    'product_id': product[0],
                    'product_name': product[1],
                    'product_color_name': product[3],
                    'image_title': product[4],
                    'feature_image_path': product[5],
                    'image_id': product[9]
                }
                
                db_image_data.append(data_db)

    return db_image_data

def map_product_success_with_db_data(image_title, db_images):
    product_id = ''
    product_name = ''
    product_color_name = ''
    db_feature_image = ''

    for db_image in db_images:
        final_temp_image_ids = []
        temp_images_ids = db_image['image_id'].split(',')

        #remove space
        for temp_images_id in temp_images_ids:
            no_space_temp_images_id = temp_images_id.replace(' ', '')
            final_temp_image_ids.append(no_space_temp_images_id)
       
        #map new nat db sheet with success data wp image id
        for final_temp_image_id in final_temp_image_ids:
            if image_title == final_temp_image_id:
                product_id = db_image['product_id']
                product_name = db_image['product_name']
                product_color_name = db_image['product_color_name']
                db_feature_image = db_image['feature_image_path']

    return product_id, product_name, product_color_name, db_feature_image

def get_success_image_data(filename_success, db_image_data):
    success_table = []
    with open(filename_success, newline='') as f:
        products = csv.reader(f)

        for product in products:
            product_id, product_name, product_color_name, db_feature_image = map_product_success_with_db_data(product[3], db_image_data)
            data_success = {
                'product_id': product_id,
                'product_name': product_name,
                'product_color_name': product_color_name,
                'product_image': product[3],
                'wp_id': product[4],
                'wp_title': product[5],
                'wp_path': db_feature_image #product[6]
            }
            success_table.append(data_success)

    return success_table

def extract_product_name(success_datas):
    all_product_names = []

    for success_data in success_datas:
        data_all_product_names = {
            'product_ID': success_data['product_id'],
            'product_name': success_data['product_name'],
            'product_color_name': success_data['product_color_name'],
            'wp_path': success_data['wp_path']
        }
        all_product_names.append(data_all_product_names)

    return all_product_names

def remove_duplicate_all_products(all_products):
    no_duplicate = []
    for i in range(0, len(all_products)):
        if all_products[i] not in all_products[i+1:]:
            no_duplicate.append(all_products[i])

    return no_duplicate

def map_wp_image_id(all_products, success_datas):
    header = {'product_ID': 'Product ID', 'product_name': 'Product Name', 'product_color_name': 'Product Color Name', 'wp_path': 'Wordpress Path'}
    all_product_with_images = []
    for all_product in all_products:
        wordpress_id = []
        if all_product != header:
            for success_data in success_datas:
                data_current_success_data = {
                    'product_ID': success_data['product_id'],
                    'product_name': success_data['product_name'],
                    'product_color_name': success_data['product_color_name'],
                    'product_wp_path': all_product['wp_path'],
                }

                if data_current_success_data != header:
                    if all_product['product_name'] == data_current_success_data['product_name'] and all_product['product_color_name'] == data_current_success_data['product_color_name']:
                        wordpress_id.append(success_data['wp_id'])

            product_wp_id = ','.join(wordpress_id)
            wordpress_id = []
            data_all_product_with_images = {
                'product_ID': all_product['product_ID'],
                'product_name': all_product['product_name'],
                'product_color_name': all_product['product_color_name'],
                'product_wp_path': all_product['wp_path'],
                'product_wp_id': product_wp_id
            }
            all_product_with_images.append(data_all_product_with_images)

    return all_product_with_images

def replace_attribute_size_name_value(raw_size_name):
    #Replace Size Name format
    att_size_name = ''
    if raw_size_name == '6, 2, 0, 4, 8':
        att_size_name = '0, 2, 4, 6, 8'
    elif raw_size_name == '4, 0, 2, 6':
        att_size_name = '0, 2, 4, 6'
    elif raw_size_name == '0, 4, 2, 6':
        att_size_name = '0, 2, 4, 6'
    elif raw_size_name == '0, 6, 4, 2, 8':
        att_size_name = '0, 2, 4, 6, 8'
    elif raw_size_name == '0, 4, 6, 2':
        att_size_name = '0, 2, 4, 6'
    else:
        att_size_name = raw_size_name

    return att_size_name

def replace_feature_image(main_data, child_feature_image):
    #Child feature image
    if child_feature_image != 'variation':
        feature_img = child_feature_image.replace('http://www.theabythara.com/uploads/products/xl/', 'http://theabythara.pi.bypronto.com/2/wp-content/uploads/sites/2/2018/01/')
    else:
        feature_img = main_data['Images']

    return feature_img

def get_additional_variation_image(additional_variation_img):
    #Additional feature image
    variation_img = ''
    if additional_variation_img != '':
        variation_img = additional_variation_img
    else:
        variation_img = ''
    
    return variation_img

def write_data_for_generate_csv_file(main_data, additional_variation_img, child_feature_image):
    feature_img = replace_feature_image(main_data, child_feature_image)
    variation_img = get_additional_variation_image(additional_variation_img)
    att_size_name = replace_attribute_size_name_value(main_data['Attribute 1 value(s)'])

    data_mapping_main_data_with_image = {
        'ID': main_data['ID'],
        'Type': main_data['Type'],
        'Name': main_data['Name'],
        'Published': '1',
        'Is featured?': '1',
        'Short description': main_data['Short description'],
        'Categories': main_data['Categories'],
        'Regular price': main_data['Regular price'],
        'In stock?': '1',
        'Stock': main_data['Stock'],
        'Parent': main_data['Parent'],
        'Attribute 1 name': 'Size',
        'Attribute 1 value(s)': att_size_name,
        'Attribute 1 visible': '0',
        'Attribute 1 global': '0',
        'Attribute 2 name': 'Color',
        'Attribute 2 value(s)': main_data['Attribute 2 value(s)'],
        'Attribute 2 visible': '0',
        'Attribute 2 global': '0',
        'Images': feature_img,
        'Meta: _wc_additional_variation_images': variation_img,
        'Tag': main_data['Tag']
    }

    return data_mapping_main_data_with_image

def mapping_main_table(main_datas, all_products):
    final_main_data_with_image = []
    header = {'ID': 'ID', 'Type': 'Type', 'Name': 'Name', 'Published': '1', 'Is featured?': '1', 'Short description': 'Short description', 'Categories': 'Categories', 'Regular price': 'Regular price', 'In stock?': '1', 'Stock': 'Stock', 'Parent': 'Parent', 'Attribute 1 name': 'Size', 'Attribute 1 value(s)': 'Attribute 1 value(s)', 'Attribute 1 visible': '0', 'Attribute 1 global': '0', 'Attribute 2 name': 'Color', 'Attribute 2 value(s)': 'Attribute 2 value(s)', 'Attribute 2 visible': '0', 'Attribute 2 global': '0', 'Images': 'Images', 'Tag': 'Tag'}
    for main_data in main_datas:
        if main_data != header and main_data['Type'] != 'variable':
            data_current_main_data = {
                'ID': main_data['ID'],
                'product_name': main_data['Name'],
                'product_color_name': main_data['Attribute 2 value(s)']
            }

            additional_variation_img = ''
            child_feature_imgs = []
            child_feature_img = ''
            for all_product in all_products:
                if data_current_main_data['product_name'] == all_product['product_name'] and data_current_main_data['product_color_name'] == all_product['product_color_name']:
                    additional_variation_img = all_product['product_wp_id']
                    child_feature_imgs.append(all_product['product_wp_path'])

            if len(child_feature_imgs) != 0:
                child_feature_img = child_feature_imgs[0]
            else:
                child_feature_img = ''

            data_mapping_main_data_with_image = write_data_for_generate_csv_file(main_data, additional_variation_img, child_feature_img)
            final_main_data_with_image.append(data_mapping_main_data_with_image)
        elif main_data != header and main_data['Type'] != 'variation':
            data_mapping_main_data_with_image = write_data_for_generate_csv_file(main_data, '', 'variation')
            final_main_data_with_image.append(data_mapping_main_data_with_image)
    
    return final_main_data_with_image

def generate_csv_file(complete_main_data):
    keys = complete_main_data[0].keys()
    with open('/Users/bell/Desktop/Temp_Complete_Data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader()
        writer.writerows(complete_main_data)

def main_process():
    #Mapping Image with all image list within success table
    db_image_data = get_db_image_data(filename_db_image)
    success_datas = get_success_image_data(filename_success, db_image_data)
    all_products = extract_product_name(success_datas)
    all_products = remove_duplicate_all_products(all_products)
    all_products = map_wp_image_id(all_products, success_datas)

    #Mapping image with main table
    main_datas = get_main_data(filename_main)
    complete_main_data = mapping_main_table(main_datas, all_products)

    #generate csv file
    generate_csv_file(complete_main_data)

main_process()
