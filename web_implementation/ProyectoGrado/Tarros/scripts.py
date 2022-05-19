from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def test_dataset(test_image_front, test_image_back, test_image_up):

    #LOAD ALL THREE DATASETS
    model1 = load_model('Tarros/ai_models/tarros_1.hdf5')
    model2 = load_model('Tarros/ai_models/tarros_2.hdf5')
    model3 = load_model('Tarros/ai_models/tarros_3.hdf5')

    #NORMALIZES THE DATA
    test_image_front = np.array(test_image_front) / 255
    test_image_back = np.array(test_image_back) / 255
    test_image_up = np.array(test_image_up) / 255

    #PREDICT EVERY MODEL
    q = model1.predict(np.array( [test_image_front,]))
    q = (100 - (q[0][0]*100)).round(2)
    print(f'Tarro frontal: Chance: {q}%')
    
    q2 = model2.predict(np.array( [test_image_back,]))
    q2 = (100 - (q2[0][0]*100)).round(2)
    print(f'Tarro trasero: Chance: {q2}%')

    q3 = model3.predict(np.array( [test_image_up,]))
    q3 = (100 - (q3[0][0]*100)).round(2)
    print(f'Tarro arriba: Chance: {q3}%')

    #IF ALL 3 MODELS ARE UP TO 50% THEN THE OUTPUT IS TRUE

    return {
        'result': True, 
        'front':q, 
        'back': q2, 
        'up': q3
    } if q > 50 and q2 > 50 and q3 > 50 else {
        'result': False, 
        'front':q, 
        'back': q2, 
        'up': q3
    }


def change_size(i):
    reducida = i.resize((180, 256))
    return reducida

def process_image(i1, i2, i3):
    return test_dataset(
        change_size(Image.open(i1).convert('RGB')), 
        change_size(Image.open(i2).convert('RGB')), 
        change_size(Image.open(i3).convert('RGB'))
    )