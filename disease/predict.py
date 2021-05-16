import cv2
import numpy as np
import os
from random import shuffle
from tqdm import \
    tqdm
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tensorflow as tf
import argparse
import imutils
from keras.models import load_model


def predict(path):

    img = path
    SIZE_IMG = 50
    LR = 1e-4
    MODEL_NAME = 'trained-{}-{}.model'.format(LR, 'cnn')

    def verify_data(img):
        verifying_data = []
        # for img in tqdm(os.listdir(verify_dir)):
        path = img
        img_num = img.split('.')[0]
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (SIZE_IMG, SIZE_IMG))
        verifying_data.append([np.array(img), img_num])
        np.save('verify_data.npy', verifying_data)
        return verifying_data

    verify_data = verify_data(img)
    # verify_data = np.load('verify_data.npy')

    tf.compat.v1.reset_default_graph()

    convnet = input_data(shape=[None, SIZE_IMG, SIZE_IMG, 3], name='input')

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 128, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 4, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=LR,
                         loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')

    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print('model loaded success!')

    import matplotlib.pyplot as plt
    fig = plt.figure()

    for num, data in enumerate(verify_data):

        img_num = data[1]
        img_data = data[0]

        orig = img_data
        data = img_data.reshape(SIZE_IMG, SIZE_IMG, 3)

        model_out = model.predict([data])[0]

        if np.argmax(model_out) == 0:
            label = 'Healthy'
        elif np.argmax(model_out) == 1:
            label = 'EarlyBblight'
        elif np.argmax(model_out) == 2:
            label = 'Healthy'
        elif np.argmax(model_out) == 3:
            label = 'LeafBlast'

        print('Result: '+label)


parser = argparse.ArgumentParser(description='Pass the path to test the image')
parser.add_argument("image", help="Image path")
args = parser.parse_args()
if args.image:
    predict(args.image)
