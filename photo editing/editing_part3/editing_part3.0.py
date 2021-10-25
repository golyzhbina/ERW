from PIL import Image
import numpy as np
import os


way_to_images = r"C:\Users\Lenovo\Desktop\UIR"
lst_of_names = os.listdir(way_to_images)
lst_of_names.sort()
lst_of_names = [lst_of_names[1]]

way_to_edit_images = r"C:\Users\Lenovo\Desktop\UIR"
colors = [(57, 0, 3832), (66, 3832, 6742), (55, 6742, 8681)]

for name in lst_of_names:

        img = Image.open(os.path.join(way_to_images, name))
        image_as_array = np.asarray(img)

        if 1 <= int(name[-4]) < 3833:
                k = 57
        elif 3833 <= int(name[-4]) < 6743:
                k = 66
        elif 6743 <= int(name[-4]):
                k = 55

        for i in range(len(image_as_array)):
                image_as_array[i] = np.array(list(map(lambda x: 255 if x < k else 0, image_as_array[i])))

        from_array_img = Image.fromarray(image_as_array)
        from_array_img.save(os.path.join(way_to_edit_images, name))



