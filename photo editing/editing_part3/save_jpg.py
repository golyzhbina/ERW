from PIL import Image
import os


def save_as_jpg(way_to_images: str, way_to_save: str) -> None:

    lst_of_names = os.listdir(way_to_images)
    lst_of_names = sorted(lst_of_names, key=lambda name: int(name[:-4]))

    for name in lst_of_names:
        img = Image.open(os.path.join(way_to_images, name))
        new_name = f"{name[:-4]}.jpg"
        img.save(os.path.join(way_to_save, new_name))

save_as_jpg(r"E:\folder_J\images\images_edited_tif", r"E:\folder_J\images\images_edited_jpg")
