from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import glob
import math
import os
from os import listdir, path

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
from IPython import display

import PIL.Image
import PIL.ImageOps
import PIL.ImageFont
import PIL.ImageDraw
import textwrap
from io import BytesIO

from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import caption_generator
from im2txt.inference_utils import vocabulary


# Get a list of all the file paths that ends with .txt from in specified directory
fileList = glob.glob('./content/model.ckpt-2000000.*')
# Iterate over the list of filepaths & remove each file.
for filePath in fileList:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)

# Choose the trained model --> current is 2
model_number = "2"
model_path = "./content/model.ckpt-"+model_number+"000000"   # Give model path
vocab_path = "./content/word_counts"+model_number+".txt"     # Give word_counts file path
tf.logging.set_verbosity(tf.logging.INFO)

# Build the inference graph.
g = tf.Graph()
with g.as_default():
    model = inference_wrapper.InferenceWrapper()
    restore_fn = model.build_graph_from_config(configuration.ModelConfig(), model_path)
g.finalize()

# Create the vocabulary.
vocab = vocabulary.Vocabulary(vocab_path)

#######################################################
### if tensorflow version is <1.13.2 then you have to check variables name as per tensorflow version

OLD_CHECKPOINT_FILE = "./content/model.ckpt-2000000"
NEW_CHECKPOINT_FILE = "./content/model.ckpt-2000000"

import tensorflow as tf
vars_to_rename = {
    "lstm/BasicLSTMCell/Linear/Matrix": "lstm/basic_lstm_cell/kernel",
    "lstm/BasicLSTMCell/Linear/Bias": "lstm/basic_lstm_cell/bias",
}
new_checkpoint_vars = {}
reader = tf.train.NewCheckpointReader(OLD_CHECKPOINT_FILE)
for old_name in reader.get_variable_to_shape_map():
  if old_name in vars_to_rename:
    new_name = vars_to_rename[old_name]
  else:
    new_name = old_name
  new_checkpoint_vars[new_name] = tf.Variable(reader.get_tensor(old_name))

init = tf.global_variables_initializer()
saver = tf.train.Saver(new_checkpoint_vars)

with tf.Session() as sess:
  sess.run(init)
  saver.save(sess, NEW_CHECKPOINT_FILE)

#######################################################

sess = tf.Session(graph=g)
# Load the model from checkpoint.
restore_fn(sess)

# Prepare the caption generator. Here we are implicitly using the default
# beam search parameters. See caption_generator.py for a description of the
# available beam search parameters.
generator = caption_generator.CaptionGenerator(model, vocab, beam_size=5)
#%%



image_path = "./photos/"    #### provide path where image is stored
filename = listdir(image_path)
filenames = [f for f in filename if '.jpg' in f or '.png' in f or '.jpeg' in f]
resultsFile = input("Name of output file: ")
store = open('./content/results/' + resultsFile,'w')   #### directory to store captions file

for i, file in enumerate(filenames):
    try:
        img = PIL.Image.open(image_path+file).convert('RGBA')
        box = PIL.Image.new('RGBA', img.size, (255,255,255,0))
        draw = PIL.ImageDraw.Draw(box)
        image = open(image_path+file,'rb').read() # Read the image as bytes
        captions = generator.beam_search(sess, image)
        syntheticText = ""
        for caption in captions:
            # Ignore begin and end words.
            sentence = [vocab.id_to_word(w) for w in caption.sentence[1:-1]]
            sentence = " ".join(sentence)
            syntheticText = syntheticText + sentence + " "
        syntheticText = syntheticText.replace(".", " ")
        syntheticText = syntheticText.replace("   ", " ").replace("  ", " ").lower()
        file = file.split(".")[0]
        print(file+":%s" % (syntheticText))
        store.write(file+":" + syntheticText + "\n")
    except KeyboardInterrupt:
        store.close()
        break
store.close()