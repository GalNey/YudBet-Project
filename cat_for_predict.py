import numpy as np         # dealing with arrays
import os                  # dealing with directories
import cv2
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tensorflow as tf

""" Some Constants"""
IMG_SIZE = 50 # Resizing the images to 50x50
LR = 1e-3 # Learning Rate 0.001
MODEL_NAME = 'dogsvscats-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match
IMAGE_COLOR_SCHEME = cv2.IMREAD_GRAYSCALE


def predict(imgPath, show=False, loaded_model=None):
    if not loaded_model:
        model = CreateModel()
        if os.path.exists('{}.meta'.format(MODEL_NAME)):
            model.load(MODEL_NAME)
            print('model loaded!')
    else:
        model = loaded_model

    if os.path.exists(imgPath):
        img = cv2.imread(imgPath, IMAGE_COLOR_SCHEME)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        if show:
            cv2.imshow('image', img)
        cv2.waitKey(0)
        img_data = np.array(img)
        data = img_data.reshape(IMG_SIZE, IMG_SIZE, 1)
        model_out = model.predict([data])[0]

        print (model_out)
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


def CreateModel():
    """ Configuring the Convolutional Neural Network"""
    tf.reset_default_graph()
    convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name='input')

    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 128, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 2, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')  # Windows doesn't log to tmp folder
    return model


if __name__ == "__main__":
    model = CreateModel()
    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print('model loaded!')

    while 1:

        print(predict("cat.jpg", loaded_model=model))

        input("test")
