import matplotlib.pyplot as plt
from keras.layers import UpSampling2D, Flatten, Dense
from keras.models import Sequential
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.metrics import MeanIoU
from tensorflow.keras import Model
from numpy import array, reshape, shape
from os import listdir
from os.path import join

# preparing data
way_to_original_train = r"E:\folder_J\images\jpg\train\images_jpg"
way_to_edited_train = r"E:\folder_J\images\jpg\train\images_edited_jpg"


def load_images(way: str, lst_of_name: list, flag: bool) -> array:

    images = []
    for name in lst_of_name:
        image = load_img(join(way, name),
                         color_mode="grayscale",
                         target_size=(1150, 180))
        image = img_to_array(image) / 255

        if flag:
            image = reshape(image, (207000, 1))

        images.append(image)

    return array(images)


images_name_train = listdir(way_to_original_train)

x_train = load_images(way_to_original_train, images_name_train, False)
y_train = load_images(way_to_edited_train, images_name_train, True)


model = Sequential([Conv2D(16, kernel_size=(5, 2), padding="same", activation="relu", input_shape=(1150, 180, 1)),
                    MaxPooling2D(pool_size=(2, 2)),
                    Conv2D(32, kernel_size=(3, 3), padding="same", activation="relu"),
                    MaxPooling2D(pool_size=(5, 2)),
                    Conv2D(64, kernel_size=(3, 3), padding="same", activation="relu"),
                    MaxPooling2D(pool_size=(5, 3)),
                    ])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=[MeanIoU(num_classes=50)])
his = model.fit(x_train, y_train, batch_size=30, epochs=2, validation_split=0.1)

plt.plot(his.history['loss'])
plt.plot(his.history['val_loss'])
plt.show()