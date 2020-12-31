import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import numpy as np         # dealing with arrays
import os                  # dealing with directories
import tensorflow as tf

from matplotlib import pyplot
from keras.utils import to_categorical
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

LR = 1e-3 # Learning Rate 0.001
IMG_SIZE = 50 # Resizing the images to 50x50
MODEL_NAME = 'dogsvscats-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match

train_data = None #np.load("train_data.npy", allow_pickle=True)
testing_data = None #np.load("test_data.npy", allow_pickle=True)

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

def TrainModel(model):
    """ Training the Convolutional Neural Network"""
    # Check for an existing, trained model
    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print('model loaded!')

    # Splitting the data to check the accuracy and future testing and training
    train = train_data[:-100]
    test = train_data[-100:]

    # Creating our data arrays for training
    X = np.array([i[0] for i in train]).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    Y = [i[1] for i in train]

    # Creating our data arrays for testing
    test_x = np.array([i[0] for i in test]).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    test_y = [i[1] for i in test]

    # Now we train it for 3 consecutive epochs
    model.fit({'input': X}, {'targets': Y}, n_epoch=10, validation_set=({'input': test_x}, {'targets': test_y}),
              snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

    if input("Would you like to save? [y\\n]").lower() == 'y':
        model.save(MODEL_NAME)
        print("Model Saved!")


if __name__ == "__main__":
    TrainModel(CreateModel())