from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate

from tensorflow.keras import Model

input_layer = Input(shape=(1150, 180, 1), batch_size=7804)
conv1_1 = Conv2D(64, (3, 3), padding="same", activation="relu")(input_layer)
conv1_2 = Conv2D(1, (3, 3), padding="same", activation="relu")(conv1_1)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1_2)

conv2_1 = Conv2D(128, (3, 3), padding="same", activation="relu")(pool1)
conv2_2 = Conv2D(1, (3, 3), padding="same", activation="relu")(conv2_1)
pool2 = MaxPooling2D(pool_size=(5, 2))(conv2_2)

conv3_1 = Conv2D(512, (3, 3), padding="same", activation="relu")(pool2)
conv3_2 = Conv2D(1, (3, 3), padding= "same", activation="relu")(conv3_1)
# pool3 = MaxPooling2D(pool_size=(5, 3))(conv3_2)

conc4 = concatenate([UpSampling2D(size=(5, 2))(conv3_2), conv2_2])
conv4_1 = Conv2D(512, kernel_size=(3, 3), padding="same", activation="relu")(conc4)
conv4_2 = Conv2D(256, kernel_size=(3, 3), padding="same", activation="relu")(conv4_1)

conc5 = concatenate([UpSampling2D(size=(2, 2))(conv4_2), conv1_2])
conv5_1 = Conv2D(128, kernel_size=(3, 3), padding="same", activation="relu")(conc5)
conv5_2 = Conv2D(1, kernel_size=(3, 3), padding="same", activation="relu")(conv5_1)

conv4 = Conv2D(1, (1, 1), padding="same", activation="sigmoid")(conv5_1)

model = Model(inputs=[input_layer], outputs=[conv4])
print(model.summary())
