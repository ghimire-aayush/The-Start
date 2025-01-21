## We are effectively using 4 different files here, so there is no need to split between train
## and test functions. We use Naive Bayes classifier to identify the previously unseen spam and ham messages

import os
from math import log

SMALL_NUMBER = 0.00001


def get_occurrences(filename):
    results = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            for line in file:
                count, word = line.strip().split(' ')
                results[word] = int(count)

        return results

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s" % str(e))
        raise


def get_words(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            words = [word for line in file for word in line.split()]

        return words

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise


class SpamHam:
    """ Naive Bayes spam filter
        :attr spam: dictionary of occurrences for spam messages {word: count}
        :attr ham: dictionary of occurrences for ham messages {word: count}
    """

    def __init__(self, spam_file, ham_file):
        self.spam = get_occurrences(spam_file)
        self.ham = get_occurrences(ham_file)

        #Total values for later probability calculation
        self.total_spam = sum(self.spam.values())
        self.total_ham = sum(self.ham.values())

    def evaluate_from_file(self, filename):
        words = get_words(filename)
        return self.evaluate(words)

    def evaluate_from_input(self):
        words = input().split()
        return self.evaluate(words)
    
    #Gives probability for spam and ham respectively
    
    def spam_prob(self, word):
        if word in self.spam:
            return self.spam[word] / self.total_spam
        else:
            return SMALL_NUMBER

    
    def ham_prob(self, word):
        if word in self.ham:
            return self.ham[word] / self.total_ham
        else:
            return SMALL_NUMBER

    def evaluate(self, words):
        """
        :param words: Array of str
        :return: probability that the message is spam (float)
        """
        initial_pspam = self.total_spam / (self.total_ham + self.total_spam)
        initial_pham = self.total_ham / (self.total_ham + self.total_spam)

        #Should use logarithm if the dataset is larger to avoid spilling

        R = initial_pspam / initial_pham

        for w in words:
            R = R * (self.spam_prob(w) / self.ham_prob(w))
        
        spam_prob = R /(1+R)
        return spam_prob





if __name__ =="__main__":
    train = SpamHam('spamcount.txt','hamcount.txt')
    result1 = train.evaluate_from_file("spamesim.txt")
    result2 = train.evaluate_from_file('hamesim.txt')

    
    for result in [result1, result2]:
        print("SPAM" if result > 0.5 else "HAM")