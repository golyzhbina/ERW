from shutil import move
from os import listdir
from os.path import join


def move_files(way_from: (str, str), way_to: (str, str), step: int) -> None:

    lst_of_names = listdir(way_from[1])
    lst_of_names.sort(key=lambda name: int(name[:-4]))
    lst_of_names = lst_of_names[::step]

    for name in lst_of_names:
        file1 = join(way_from[0], name)
        file2 = join(way_from[1], name)

        move(file1, way_to[0])
        move(file2, way_to[1])

    return


move_files((r"E:\folder_J\images\jpg\train\images_jpg",
            r"E:\folder_J\images\jpg\train\images_edited_jpg"),
           (r"E:\folder_J\images\images_for_bot\original",
            r"E:\folder_J\images\images_for_bot\edited"), 1000)






