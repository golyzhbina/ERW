from PIL import Image
import numpy as np
import os


way_to_images = r"C:\Users\Lenovo\Desktop\UIR"
lst_of_names = os.listdir(way_to_images)
lst_of_names.sort()
lst_of_names = [lst_of_names[1]]

way_to_edit_images = r"C:\Users\Lenovo\Desktop\UIR"

for name in lst_of_names:

        img = Image.open(os.path.join(way_to_images, name))
        image_as_array = np.asarray(img)
        for i in range(len(image_as_array)):
                image_as_array[i] = np.array(list(map(lambda x: 255 if x < 70 else 0, image_as_array[i])))

        from_array_img = Image.fromarray(image_as_array)

        new_name = "0200.tif"
        from_array_img.save(os.path.join(way_to_edit_images, new_name))



