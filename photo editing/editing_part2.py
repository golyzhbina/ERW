from PIL import Image
import numpy as np
import os


way_to_images = r"C:\Users\Lenovo\Desktop\UIR\Void microCT dataset_Mehdikhani et al\Voids microCT dataset\Tomographic images\Edit_part1"
lst_of_names = os.listdir(way_to_images)
lst_of_names.sort()

way_to_edit_images = r"C:\Users\Lenovo\Desktop\UIR\Void microCT dataset_Mehdikhani et al\Voids microCT dataset\Tomographic images\Edit_part2"

for name in lst_of_names:
    img = Image.open(os.path.join(way_to_images, name))
    img_as_array = np.asarray(img)
    new_img = []
    for i in range(115, 1332):
        new_img_i = np.array(img_as_array[i][95: 242])
        for j in range(len(new_img_i)):
            new_img_i[j] = 60 if new_img_i[j] == 255 else new_img_i[j]

        new_img.append(new_img_i)

    new_img = np.array(new_img)
    new_img = Image.fromarray(new_img)

    new_name = name[0: 4] + "e" + name[4:]
    new_img.save(os.path.join(way_to_edit_images, new_name))
    img = Image.close()

