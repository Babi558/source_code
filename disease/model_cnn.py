# Some part of the code was referenced by https://www.kaggle.com/emmarex/plant-disease-detection-using-keras
import tensorflow as tf
from tflearn.layers.estimator import regression
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
import tflearn
import cv2
import numpy as np
import os
from random import shuffle
from tqdm import tqdm

TRAIN_DIR = 'dataset'
TEST_DIR = 'test/test'
SIZE_IMG = 50
LR = 1e-4
MODEL_NAME = 'trained-{}-{}.model'.format(LR, 'cnn')


def label_im(label):
    if label == 'Healthy':
        return [1, 0, 0, 0]
    elif label == 'EarlyBblight':
        return [0, 1, 0, 0]
    elif label == 'LateBlight':
        return [0, 0, 1, 0]
    elif label == 'LeafBlast':
        return [0, 0, 0, 1]


def train_data():
    train_data = []

    for folder in tqdm(os.listdir(TRAIN_DIR)):
        if folder == '.DS_Store':
            break
        for img in tqdm(os.listdir(TRAIN_DIR+"/"+folder)):
            path = os.path.join(TRAIN_DIR+"/"+folder, img)

            try:
                label = label_im(folder)
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (SIZE_IMG, SIZE_IMG))
                train_data.append([np.array(img), np.array(label)])

            except:
                print(path)

    shuffle(train_data)
    np.save('train_data.npy', train_data)
    return train_data


def process_data():
    testing_data = []
    for img in tqdm(os.listdir(TEST_DIR)):
        path = os.path.join(TEST_DIR, img)
        img_num = img.split('.')[0]
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (SIZE_IMG, SIZE_IMG))
        testing_data.append([np.array(img), img_num])

    shuffle(testing_data)
    np.save('test_data.npy', testing_data)
    return testing_data


train_data = train_data()


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

train = train_data[:-500]
test = train_data[-500:]

X = np.array([i[0] for i in train]).reshape(-1, SIZE_IMG, SIZE_IMG, 3)
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1, SIZE_IMG, SIZE_IMG, 3)
test_y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=11, validation_set=({'input': test_x}, {'targets': test_y}),
          snapshot_step=40, show_metric=True, run_id=MODEL_NAME)

model.save(MODEL_NAME)
