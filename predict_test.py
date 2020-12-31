import numpy as np         # dealing with arrays
import os                  # dealing with directories
import ConvolutionalNN
import cv2

""" Some Constants"""
IMG_SIZE = 50 # Resizing the images to 50x50
LR = 1e-3 # Learning Rate 0.001
MODEL_NAME = "cat_for_predict.data-00000-of-00001"
IMAGE_COLOR_SCHEME = cv2.IMREAD_GRAYSCALE


def predict(imgPath, show=False):
    model = ConvolutionalNN.CreateModel()
    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print('model loaded!')


    if os.path.exists(imgPath):
        img = cv2.imread(imgPath, IMAGE_COLOR_SCHEME)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        if show:
            cv2.imshow('image', img)
        cv2.waitKey(0)
        img_data = np.array(img)
        data = img_data.reshape(IMG_SIZE, IMG_SIZE, 1)
        model_out = model.predict([data])[0]
        print(model_out)
        if np.argmax(model_out) == 1:
            str_label = 'Dog'
        else:
            str_label = 'Cat'

        if show:
            print(str_label)
        return str_label
    else:
        print("Invalid Image Path")
        return ''


if __name__ == "__main__":
    predict("cat_for_predict.jpg", show=True)
