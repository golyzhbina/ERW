from PIL import Image
from numpy import array, asarray
import numpy as np


def draw_img(img):
    print(*img[250])
    img_new = []
    for i in range(1150):
        img_new.append(list(map(list, img[i])))
        img_new[i].insert(0, [0, 0, 0, 0])
        img_new[i].append([0, 0, 0, 0])

    img_new.insert(0, [0, 0, 0, 0] * 180)
    img_new.append([0, 0, 0, 0] * 180)
    print(len(img_new), len(img_new[i]))

    new_layer = [[]] * 1152
    for i in range(1152):
        new_layer[i] = [[255, 255, 255, 0]] * 182

    for i in range(1, 1151):
        for j in range(1, 181):
            coords = [(i - 1, j - 1), (i, j - 1), (i - 1, j), (i, j), (i + 1, j + 1), (i + 1, j), (i, j + 1),
                     (i - 1, j + 1), (i + 1, j - 1)]

            for coord in coords:
                if 250 <= img_new[i][j][0] <= 255:
                    new_layer[coord[0]][coord[1]] = array([225, 0, 0, 150])


    new_layer = new_layer[1:-1]
    new_layer = list(map(lambda x: x[1:-1], new_layer))


    new_layer = array(list(map(array, new_layer)))

    return new_layer

test = Image.open(r"C:\Users\Lenovo\Desktop\UIR\images\images_for_bot\edited\2.jpg")
test = test.convert("RGBA")
arr = asarray(test)
new_arr = draw_img(arr)


new_img = Image.fromarray(new_arr.astype(np.uint8))
new_img.save("img_test.png")

img_back = Image.open(r'C:\Users\Lenovo\Desktop\UIR\images\images_for_bot\original\2.jpg')
img_back = img_back.convert("RGB")
img_fore = Image.open('img_test.png')
img_fore = img_fore.convert("RGB")

res = Image.blend(img_back, img_fore, 0.3)
res.save("img_back.png")
