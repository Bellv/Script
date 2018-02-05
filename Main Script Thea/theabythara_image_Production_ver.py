import os
import requests
import csv

authname = ''
authpass = ''

# imgPath = '/Users/bell/Downloads/testimage.jpg'
url_path='http://2-beta.pi.bypronto.com/wp-json/wp/v2/media'

def get_image_list():
    list_of_import_image = []
    filename = '/Users/bell/Desktop/nat_image3.csv'
    with open(filename, newline='') as f:
        products = csv.reader(f)
        
        for product in products:
            if product[1] != 'Name':
                data_list_images = {
                    'ID': product[0],
                    'Name': product[1],
                    'Color name': product[2],
                    'Image': product[4]
                } 
            
                list_of_import_image.append(data_list_images)

    return list_of_import_image

def get_import_image(image_lists):
    import_image = []
    for image_list in image_lists:
        product_id = image_list['ID']
        product_name = image_list['Name']
        product_color_name = image_list['Color name']
        product_images = image_list['Image'].split(',')

        for product_image in product_images:
            data_import_image = {
                'ID': product_id,
                'Name': product_name,
                'Color name': product_color_name,
                'Image': product_image
            }
            
            import_image.append(data_import_image) 

    return import_image

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

def restImgUL(import_images):
    success_image_files_for_write_csv = []
    fail_image_files_for_write_csv = []
    for import_image in import_images:
        product_id = import_image['ID']
        product_name = import_image['Name']
        product_color_name = import_image['Color name']
        product_image = import_image['Image']

        print (f'Name: {product_name} - Image: {product_image}')
        try:
            img_path = '/Users/bell/Desktop/'+product_image
            data = open(img_path, 'rb').read()
            fileName = os.path.basename(img_path)
            res = requests.post(url=url_path,
                                data=data,
                                headers={ 'Content-Type': 'image/jpg','Content-Disposition' : 'attachment; filename=%s'% fileName},
                                auth=(authname, authpass))

            newDict=res.json()
            title = newDict.get('title').get('rendered')
            newID = newDict.get('id')
            file_path = newDict.get('guid').get('rendered')

            data_image_file = {
                'Wordpress ID': newID,
                'Wordpress Title': title,
                'WordPress Path': file_path,
                'Product ID': product_id,
                'Product Name': product_name,
                'Product Color Name': product_color_name,
                'Product Image': product_image
            }
            
            success_image_files_for_write_csv.append(data_image_file)
            print (f'WP ID: {newID} - WP Title: {title} - WP File Path: {file_path}')
        except:
            fail_image_files_for_write_csv.append(import_image)
            print ('FAIL upload image --------------------')

    return success_image_files_for_write_csv, fail_image_files_for_write_csv

def write_csv_file_success(image_files_for_write_csv):
    keys = image_files_for_write_csv[0].keys()
    with open('/Users/bell/Desktop/import_images_set/success_image_export.csv', 'w') as csvfile: #use 'a' for add more row
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader() 
        writer.writerows(image_files_for_write_csv)

def write_csv_file_fail(image_files_for_write_csv):
    keys = image_files_for_write_csv[0].keys()
    with open('/Users/bell/Desktop/import_images_set/fail_image_export.csv', 'w') as csvfile: #use 'a' for add more row
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader() 
        writer.writerows(image_files_for_write_csv)


image_lists = get_image_list()
raw_images = get_import_image(image_lists)
import_images = split(raw_images, 3)

# for i in import_images[19]:
#     print (i)
#     print (len(import_images[19]))
#0 -> 19
success_list, fail_list = restImgUL(import_images[0])
write_csv_file_success(success_list)
write_csv_file_fail(fail_list)
