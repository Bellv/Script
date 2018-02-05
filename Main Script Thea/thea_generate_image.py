import csv

image_files = []
def get_image_list():
    list_of_import_image = []
    filename = '/Users/bell/Desktop/nat_image.csv'
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


image_lists = get_image_list()
raw_images = get_import_image(image_lists)

import_images = split(raw_images, 200)

for i in import_images[0]:
    print (i)
    print (len(import_images[0]))




# print (import_images)


# keys = import_images[0].keys()
# with open('Desktop/import_images/import_images.csv', 'w') as csvfile: #use 'a' for add more row
#     writer = csv.DictWriter(csvfile, keys)
#     writer.writeheader() 
#     writer.writerows(import_images)
