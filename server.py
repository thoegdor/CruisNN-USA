import sys, time, logging, os, argparse

import numpy as np
from PIL import Image, ImageGrab
from socketserver import TCPServer, StreamRequestHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from model import create_model, input_width, input_height, input_channels

def prepare_image(im):
	im = im.resize((input_width, input_height))
	im_arr = np.frombuffer(im.tobytes(), dtype=np.uint8)
	im_arr = im_arr.reshape((input_height, input_width, input_channels))
	im_arr = np.expand_dims(im_arr, axis=0)
	return im_arr

class TCPHandler(StreamRequestHandler):
	
	def handle(self):
		weights_file = 'weights_dir/the_weights.hdf5'
		logger.info("Loading {}...".format(weights_file))
		model.load_weights(weights_file)

		logger.info("Handling a new connection...")
		
		for line in self.rfile:
			message = str(line.strip(),'utf-8')
			logger.debug(message)

			if message.startswith("PREDICTFROMCLIPBOARD"):
				im = ImageGrab.grabclipboard()
				if im != None:
					prediction = model.predict(prepare_image(im), batch_size=1)[0]
					print((str(prediction[0]) + "\n"))
					self.wfile.write((str(prediction[0]) + "\n").encode('utf-8'))
				else:
					self.wfile.write("PREDICTIONERROR\n".encode('utf-8'))
				
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Start a prediction server that other apps will call into.')
	parser.add_argument('-a', '--all', action='store_true', help='Use the combined weights for all tracks, rather than selecting the weights file based off of the course code sent by the Play.lua script.', default=False)
	parser.add_argument('-p', '--port', type=int, help='Port number', default=36296)
	parser.add_argument('-c', '--cpu', action='store_true', help='Force Tensorflow to use the CPU.', default=False)
	args = parser.parse_args()

	logger.info("Loading model...")
	model = create_model(keep_prob=1)

	if args.all:
		model.load_weights('weights_dir/the_weights.hdf5')

	logger.info("Starting server...")
	server = TCPServer(('0.0.0.0', args.port), TCPHandler)

	print("Listening on Port: {}".format(server.server_address[1]))
	sys.stdout.flush()
	server.serve_forever()