
#Implementing K-nearest neighbour algorithm and testing its accuracy from the famous iris dataset


# For a test dataset, the algorithm should find the average of the k nearest data points. 
# For a classification problem, it classifies the new data point as the majority of the k nearest points

import numpy as np
from collections import Counter

class KNN():
    def __init__(self, k):
        self.k = k
        self.x_trainvalue = None
        self.y_trainvalue = None

    def train(self, x_value, y_value):
        self.x_trainvalue = np.array(x_value)
        self.y_trainvalue = np.array(y_value)


    def euclidean(self, x1, x2):
        return np.sqrt(np.sum((x1-x2)**2))
    
    def closest_point(self, x_test):
        distances = [self.euclidean(i, x_test) for i in self.x_trainvalue]

        #Sorts it out and gives the indices simultenously
        k_indices = np.argsort(distances)[:self.k]
        k_labels = self.y_trainvalue[k_indices]

        return Counter(k_labels).most_common(1)[0][0]
    
    def predict(self, x_test):
        return np.array([self.closest_point(test) for test in x_test])
    


from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


iris = load_iris()
X, y = iris.data, iris.target


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
dataset = KNN(k=50)
dataset.train(X_train, y_train)

y_predict = dataset.predict(X_test)
print(accuracy_score(y_test, y_predict))
