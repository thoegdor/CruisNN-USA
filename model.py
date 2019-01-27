import glob
import os

from PIL import Image

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.layers.normalization import BatchNormalization
from keras import optimizers
from keras import backend as K
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

# plotting
import matplotlib.pyplot as plt

# some augmentation

#datagen = ImageDataGenerator(rescale=1./255)
'''
img = load_img('cap/run_1/1.png')  # this is a PIL image
x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

i = 0
for batch in datagen.flow(x, batch_size=1,
                          save_to_dir='preview', 
						  save_prefix='test', 
						  save_format='jpeg'):
    i += 1
    if i > 20:
        break 
'''
# vars

out_shape = 1

input_width = 200
input_height = 66
input_channels = 3

def create_model(keep_prob=0.6):
    
	model = Sequential()

	# NVIDIA's model
	model.add(BatchNormalization(input_shape=(input_height, input_width, input_channels)))
	model.add(Conv2D(24, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
	model.add(BatchNormalization())
	model.add(Conv2D(36, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
	model.add(BatchNormalization())
	model.add(Conv2D(48, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
	model.add(BatchNormalization())
	model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
	model.add(BatchNormalization())
	model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
	model.add(Flatten())
	model.add(Dense(1164, activation='relu'))
	drop_out = 1 - keep_prob
	model.add(Dropout(drop_out))
	model.add(Dense(100, activation='relu'))
	model.add(Dropout(drop_out))
	model.add(Dense(50, activation='relu'))
	model.add(Dropout(drop_out))
	model.add(Dense(10, activation='relu'))
	#model.add(Dropout(drop_out))
	#model.add(Dense(out_shape, activation='softsign', name="predictions"))

	return model

def customized_loss(y_true, y_pred, loss='euclidean'):
	# MSE
	if loss == 'L2':
		
		L2_norm_cost = 0.001
		val = K.mean(K.square((y_pred - y_true)), axis=-1) \
			+ K.sum(K.square(y_pred), axis=-1) / 2 * L2_norm_cost

	# euclidean distance loss
	elif loss == 'euclidean':
		
		val = K.sqrt(K.sum(K.square(y_pred - y_true), axis=-1))
		
	return val

def load_training_data():

	X, y = [], []
	X_train, y_train = [], []
	X_val, y_val = [], []

	recordings = glob.iglob("cap/*")
	
	for R in recordings:
		
		filenames = list(glob.iglob('{}/*.png'.format(R)))
		steering = [float(line) for line in open(("{}/steering.txt").format(R)).read().splitlines()]
		#print(len(filenames))
		#print(len(steering))
		#assert len(filenames) == len(steering), "For recording {}, the number of steering values does not match the number of images.".format(R)
	
		for file, steer in zip(filenames, steering):
			
			assert steer >= -128 and steer <= 128
			
			# split to valid

			im = Image.open(file)
			im = im/255 # augmentation
			im_arr = im_arr.reshape((input_height, input_width, input_channels))
			
			X.append(im_arr)
			y.append(steer)
		
	i_X = round(len(X)*.8)
	i_y = round(len(y)*.8)
		
	X_train = X[:i_X]
	X_val = X[i_X:]
	y_train = y[:i_y]
	y_val = y[i_y:]

	assert len(X_train) == len(y_train)
	assert len(X_val) == len(y_val)

	return np.asarray(X_train), \
	np.asarray(y_train).reshape((len(y_train), 1)), \
	np.asarray(X_val), \
	np.asarray(y_val).reshape((len(y_val), 1))


if __name__ == '__main__':

	# Load Training Data
	X_train, y_train, X_val, y_val = load_training_data()

	print(X_train.shape[0], 'training samples.')
	print(X_val.shape[0], 'validation samples.')

	# Training loop variables
	epochs = 100
	batch_size = 32

	model = create_model()

	weights_file = "weights_dir/the_weights.hdf5"
	if os.path.isfile(weights_file):
		model.load_weights(weights_file)

	model.compile(loss=customized_loss, optimizer=optimizers.adam(lr=0.0001))

	checkpointer = ModelCheckpoint(monitor='val_loss',filepath=weights_file,verbose=1, save_best_only=True,mode='min')
		
	earlystopping = EarlyStopping(monitor='val_loss', patience=20)

	model.fit(
		X_train, 
		y_train, 
		batch_size=batch_size, 
		epochs=epochs,
		shuffle=True, 
		validation_data=(X_val, y_val), 
		callbacks=[checkpointer, earlystopping],
		verbose=1
		)

	#need to add a plotting piece
