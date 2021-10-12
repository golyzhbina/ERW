from PIL import Image
import numpy as np
import os


way_to_images = r"C:\Users\Lenovo\Desktop\UIR\Void microCT dataset_Mehdikhani et al\Voids microCT dataset\Tomographic images\[0,90]4s"
lst_of_names = os.listdir(way_to_images)
lst_of_names.sort()
lst_of_names = [lst_of_names[200]]

way_to_edit_images = r"C:\Users\Lenovo\Desktop\UIR"

for name in lst_of_names:
    img = Image.open(os.path.join(way_to_images, name))
    img_as_array = np.asarray(img)
    new_img = []
    for i in range(205, 1432):
        new_img_i = np.array(img_as_array[i][315: 457])
        # for j in range(len(new_img_i)):
            # new_img_i[j] = 60 if new_img_i[j] == 255 else new_img_i[j]

        new_img.append(new_img_i)

    new_img = np.array(new_img)
    new_img = Image.fromarray(new_img)

    new_name = name
    new_img.save(os.path.join(way_to_edit_images, new_name))


