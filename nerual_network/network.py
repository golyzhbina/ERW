import matplotlib.pyplot as plt
from keras.layers import UpSampling2D, concatenate
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D
from tensorflow.keras.metrics import MeanIoU
from tensorflow.keras import Model
from numpy import array, asarray
from os import listdir
from os.path import join


# preparing data
way_to_original_train = r"E:\folder_J\images\jpg\train\images_jpg"
way_to_edited_train = r"E:\folder_J\images\jpg\train\images_edited_jpg"


def load_images(way: str, lst_of_name: list) -> array:

    images = []
    for name in lst_of_name:
        image = load_img(join(way, name),
                         color_mode="grayscale",
                         target_size=(1150, 180))
        image = img_to_array(image) / 255
        images.append(image)

    return array(images)


images_name_train = listdir(way_to_original_train)

x_train = load_images(way_to_original_train, images_name_train)
y_train = load_images(way_to_edited_train, images_name_train)

input_layer = Input(shape=(1150, 180, 1), batch_size=7804)
conv1 = Conv2D(64, (3, 3), padding="same", activation="relu")(input_layer)      # 1150 * 180 * 64
conv1_2 = Conv2D(32, (3, 3), padding="same", activation="relu")(conv1)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1_2)                                   # 575 * 90 * 64

conv2 = Conv2D(32, (3, 3), padding="same", activation="relu")(pool1)            # 575 * 90 * 32
pool2 = MaxPooling2D(pool_size=(5, 2))(conv2)                                   # 115 * 45 * 32
up2 = UpSampling2D(size=(5, 2))(pool2)

conc3 = concatenate([pool1, up2])
up3 = UpSampling2D(size=(2, 2))(conc3)
conv3 = Conv2D(16, (3, 3), padding="same", activation="relu")(up3)            # 115 * 45 * 16
pool3 = MaxPooling2D(pool_size=(5, 3))(conv3)                                   # 23 * 15 * 16

conv4 = Conv2D(1, (1, 1), padding="same", activation="sigmoid")(conv3)

model = Model(inputs=[input_layer], outputs=[conv4])
print(model.summary())

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=[MeanIoU(num_classes=50)])
his = model.fit(x_train, y_train,batch_size=30, epochs=5, validation_split=0.1)

plt.plot(his.history['loss'])
plt.show()

images_name_test = listdir(way_to_original_train)

x_test = load_images(way_to_original_train, images_name_test)
y_test = load_images(way_to_edited_train, images_name_test)

model.evaluate(x_test, y_test)





