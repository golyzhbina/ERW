from PIL import Image
import os


way_to_images = way = r"C:\Users\Lenovo\Desktop\UIR\Void microCT dataset_Mehdikhani et al\Voids microCT dataset\Tomographic images\[0,90]2s"
lst_of_names = os.listdir(way_to_images)
lst_of_names = lst_of_names[100: 2026]
lst_of_names = sorted(lst_of_names, key=lambda name: int(name[9:-4]))

way_to_edit_images = r"C:\Users\Lenovo\Desktop\UIR"

for name in lst_of_names:
    img = Image.open(os.path.join(way_to_images, name))
    img = img.crop((175, 270, 355, 1420))
    new_name = f"{lst_of_names.index(name) + 1}.tif"    # TODO: поменять число в имени
    img.save(os.path.join(way_to_edit_images, new_name))
