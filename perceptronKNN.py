


## This code attempts to identify the handwritten numbers using both the simple perceptron and KNN alogrithm
## Instead of using Pycharm and Scikit-Learn libraries, we will try to write the code from scratch for learning purposes
## We assume two different files, one where the images are given, another where the actual number is given
## Everything else should be self-explanatory


import math
import os
import numpy as np
from PIL import Image
import random
from math import sqrt

NUMBER_OF_PIXELS = 28 * 28
IMAGE_SIZE = 28


def get_chars(filename):
    """
    Reads the classes of characters
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            chars = [line[0] for line in file]

        return chars

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise


def get_images(filename):
    """
    Reads the images (black pixel is 1, white pixel is 0 in the input)
    Trasnforms (0, 1) values to (-1.0, 1.0)
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    vectors = []

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            for line in file:
                vectors.append([1.0 if float(v) == 1 else -1.0 for v in line.strip().split(',')])

        return vectors

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise


class Perceptron:
    """ Perceptron
        :data: list of objects that represent images
    """

    def __init__(self, images, chars):
        idata = get_images(images)
        cdata = get_chars(chars)
        
        self.weights = np.zeros(NUMBER_OF_PIXELS)

        self.data = [{'vector': v, 'char': c} for (v, c) in zip(idata, cdata)]
        random.seed()
        
    
    

    def train(self, target_char, opposite_char, steps):
        """Trains the perceptron to distinguish target_char from opposite_char"""

        for step in range(steps):
            for e in self.data[:5000]: 
                if e['char'] == target_char:
                    y = 1  
                elif e['char'] == opposite_char:
                    y = -1 
                else:
                    continue

             
                z = np.dot(e['vector'], self.weights)   

                #If you're wrong you essentially move the decision boundary
                #towards the opposite direction

                if y * z <= 0:  
                    self.weights += y * np.array(e['vector'])


    def test(self, target_char, opposite_char):
        """Tests the learned perceptron with the last 1000 x,y pairs.
        (Note that this only counts those ones that belong either to the plus or minus classes.)

        :param target_char: the target character we are trying to distinguish
        :param opposite_char: the opposite character
        :return: the ratio of correctly classified characters
        """
        success = 0
        examples = self.data[5000:]

        examples = [e for e in examples if e['char'] in (target_char, opposite_char)]

        for e in examples:
            z = np.dot(e['vector'], self.weights)
            if (z >= 0 and e['char'] == target_char) or (z < 0 and e['char'] == opposite_char):
                success += 1

        return float(success) / len(examples)

    def save_weights(self, filename):
        """Draws a 28x28 grayscale picture of the weights

        :param filename: Name of the file where weights will be saved
        """
        pixels = [.01 + .98 / (1.0 + float(math.exp(-w))) for w in self.weights]

        Image.fromarray(np.array(pixels).reshape(IMAGE_SIZE, IMAGE_SIZE), mode = "L").save(filename)



class NearestNeighbour:

    def __init__(self, images, chars):
        idata = get_images(images)
        cdata = get_chars(chars)
        self.data = [{'vector': v, 'char': c} for (v, c) in zip(idata, cdata)]

    
    def distance(self, v1, v2):
        return np.sqrt(np.sum((np.array(v2) - np.array(v1))**2))
    

    def train(self, test_vector):
        LARGE_NUMBER = 9 * 10**9
        nearby_distance = LARGE_NUMBER
        label = None

        for e in self.data[:5000]:
            dist = self.distance(test_vector, e['vector'])
            if dist < nearby_distance:
                nearby_distance = dist
                label = e['char']
            
        return label
    
    def test(self, target_char, opposite_char):
        success = 0
        examples = self.data[5000:]
        test_data = [e for e in examples if e['char'] in (target_char, opposite_char)]

        for e in test_data:
            predicted = self.train(e['vector'])
            if predicted == e['char']:
                success += 1

        
        return success/len(test_data)
    

IMGS_FILE = 'mnist-x.data'
CHARS_FILE = 'mnist-y.data'
    
def main():
    perc = Perceptron(IMGS_FILE, CHARS_FILE)
    perc.train('3', '5', 100)
    print(perc.test('3', '5'))
    perc.save_weights('weights.bmp')

    nn_classifier = NearestNeighbour(IMGS_FILE, CHARS_FILE)
    nn = nn_classifier.test('3', '5')  
    print(f"Nearest Neighbor Accuracy: {nn}")

if __name__ == '__main__':
    main()


