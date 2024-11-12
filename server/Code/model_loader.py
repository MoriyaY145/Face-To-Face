import os
import pickle
from keras.src.saving.saving_api import load_model

# Get the absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths to the model files
model_cnn_path = os.path.join(BASE_DIR, '..', 'models', 'cnnModel.h5')
model_eyebrow_path = os.path.join(BASE_DIR, '..', 'models', 'eyebrowModel.pkl')
scaler_eyebrow_path = os.path.join(BASE_DIR, '..', 'models', 'scalerEyebrow.pkl')
model_jaw_path = os.path.join(BASE_DIR, '..', 'models', 'jawModel.h5')
scaler_jaw_path = os.path.join(BASE_DIR, '..', 'models', 'scalerJaw.pkl')

# Load the models
model_cnn = load_model(model_cnn_path)
model_eyebrow = pickle.load(open(model_eyebrow_path, 'rb'))
scaler_eyebrow = pickle.load(open(scaler_eyebrow_path, 'rb'))
model_jaw = load_model(model_jaw_path)
scaler_jaw = pickle.load(open(scaler_jaw_path, 'rb'))
