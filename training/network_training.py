import tensorflow as tf
from tensorflow.keras import models, optimizers, regularizers
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model, clone_model
import matplotlib.pyplot as plt 


def generate_model():
    model = tf.keras.Sequential()
    model.add(Conv2D(filters=16,kernel_size=3,padding='same', activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4), input_shape=(256,180,3)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=2))
    model.add(Dropout(0.35))

    model.add(Conv2D(filters=32,kernel_size=3,padding='same', activation='relu', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=2))
    model.add(Dropout(0.35))

    model.add(Conv2D(filters=64,kernel_size=3,padding='same', kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4), activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(BatchNormalization())
    model.add(Dropout(0.35))

    model.add(Flatten())
    model.add(Dense(256))
    model.add(BatchNormalization())
    model.add(Dense(1, activation='sigmoid'))
    model.summary()
    
    return model


def generate_imagedatagen():
    train_datagen = ImageDataGenerator(
        rescale = 1./255,
        rotation_range = 20,
        width_shift_range = 0.2,
        height_shift_range = 0.2,
        shear_range = 0.2,
        zoom_range = 0.3,
        horizontal_flip = False
    )
    
    test_datagen = ImageDataGenerator(rescale = 1./255)
    
    return train_datagen, test_datagen


def generate_datagen(train_datagen, test_datagen):
    train_generator1 = train_datagen.flow_from_directory('../input/tarros-dataset-final-for-real/DATASET_improved/1_front/train',
                                 target_size = (256,180),
                                 batch_size = 4,
                                 class_mode = "binary")

    validation_generator1 = test_datagen.flow_from_directory("../input/tarros-dataset-final-for-real/DATASET_improved/1_front/validation",
                                 target_size = (256,180),
                                 batch_size = 1,
                                 class_mode = "binary")
    
    train_generator2 = train_datagen.flow_from_directory("../input/tarros-dataset-final-for-real/DATASET_improved/2_back/train",
                                 target_size = (256,180),
                                 batch_size = 4,
                                 class_mode = "binary")

    validation_generator2 = test_datagen.flow_from_directory("../input/tarros-dataset-final-for-real/DATASET_improved/2_back/validation",
                                 target_size = (256,180),
                                 batch_size = 1,
                                 class_mode = "binary")
    
    train_generator3 = train_datagen.flow_from_directory("../input/tarros-dataset-final-for-real/DATASET_improved/3_up/train",
                                 target_size = (256,180),
                                 batch_size = 4,
                                 class_mode = "binary")

    validation_generator3 = test_datagen.flow_from_directory("../input/tarros-dataset-final-for-real/DATASET_improved/3_up/validation",
                                 target_size = (256,180),
                                 batch_size = 1,
                                 class_mode = "binary")
    
    return train_generator1, validation_generator1, train_generator2, validation_generator2, train_generator3, validation_generator3


def generate_checkpoints():
    checkpoint1 = ModelCheckpoint('tarros_1.hdf5', monitor = "val_accuracy", verbose = 1, save_best_only = True)
    checkpoint2 = ModelCheckpoint('tarros_2.hdf5', monitor = "val_accuracy", verbose = 1, save_best_only = True)
    checkpoint3 = ModelCheckpoint('tarros_3.hdf5', monitor = "val_accuracy", verbose = 1, save_best_only = True)
    
    return checkpoint1, checkpoint2, checkpoint3


def train_model(model, train_generator, validation_generator, checkpoint, epochs):
    model.compile(loss = "binary_crossentropy",
             optimizer = 'rmsprop',
             metrics = ["accuracy"])
    
    hist = model.fit(train_generator,
                steps_per_epoch = 448//4,
                epochs = epochs,
                validation_data = validation_generator,
                validation_steps = 56//1,
                callbacks = [checkpoint])
    
    return hist


def plot_performance(hist, title):
    plt.plot(hist.history["accuracy"], label = "Train")
    plt.plot(hist.history["val_accuracy"], label = "Validation")
    plt.title(title)
    plt.legend()
    plt.show()
    plt.savefig(title)


def train_network():
    model1 = generate_model()
    model2 = clone_model(model1)
    model3 = clone_model(model1)
    
    train_datagen, test_datagen = generate_imagedatagen()
    
    train_generator1, validation_generator1, train_generator2, validation_generator2, train_generator3, validation_generator3 = generate_datagen(train_datagen, test_datagen)
    
    checkpoint1, checkpoint2, checkpoint3 = generate_checkpoints()
    
    hist1 = train_model(model = model1, 
                        train_generator = train_generator1, 
                        validation_generator = validation_generator1, 
                        checkpoint = checkpoint1, 
                        epochs = 70)
    
    hist2 = train_model(model = model2, 
                        train_generator = train_generator2, 
                        validation_generator = validation_generator2, 
                        checkpoint = checkpoint2, 
                        epochs = 70)
    
    hist3 = train_model(model = model3, 
                        train_generator = train_generator3, 
                        validation_generator = validation_generator3, 
                        checkpoint = checkpoint3, 
                        epochs = 70)
    
    plot_performance(hist1, 'front-side performance')
    
    plot_performance(hist2, 'back-side performance')
    
    plot_performance(hist3, 'up-side performance')


def test_model(model_name, directory):
    test_model = load_model(model_name)
    test_datagen = ImageDataGenerator(rescale = 1./255)
    test_generator = test_datagen.flow_from_directory(directory,
                                 target_size = (256,180),
                                 batch_size = 1,
                                 class_mode = "binary")
    
    test_model.evaluate(test_generator)


if __name__ == '__main__':
    train_network()
    test_model(model_name = './tarros_1.hdf5', 
           directory = '../input/tarros-dataset-final-for-real/DATASET_improved/1_front/test')
    test_model(model_name = './tarros_2.hdf5', 
            directory = '../input/tarros-dataset-final-for-real/DATASET_improved/2_back/test')
    test_model(model_name = './tarros_3.hdf5', 
            directory = '../input/tarros-dataset-final-for-real/DATASET_improved/3_up/test')