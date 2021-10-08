from PIL import Image
import os.path
import numpy as np

way_to_sample = r"C:\Users\Lenovo\Desktop\уир\Void microCT dataset_Mehdikhani et al\Voids microCT dataset\Tomographic images\Edit1"
name_of_sample = "0040e.tif"
sample = Image.open(os.path.join(way_to_sample, name_of_sample))
sample_as_array = np.asarray(sample)

way_to_images = r"C:\Users\Lenovo\Desktop\уир\Void microCT dataset_Mehdikhani et al\Voids microCT dataset\Tomographic images\[+-45]2s"
file_name = "0041.tif"
image = Image.open(os.path.join(way_to_images, "0041.tif"))
image_as_array = np.asarray(image)
for i in range(len(image_as_array)):
    image_as_array[i] = np.array(list(map(lambda x, y: y if y == 255 else x,
                                          image_as_array[i], sample_as_array[i])))

file_name = file_name[:4] + "e" + file_name[4:]
image_from_array = Image.fromarray(image_as_array)
image_from_array.save(os.path.join(way_to_images, file_name))
image.close()
sample.close()
