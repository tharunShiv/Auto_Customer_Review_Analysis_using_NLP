## Thanks to Seby for his help with this code
# Import the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
 
# Import the dataset
dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter='\t', quoting=3)
 
# Cleaning the texts
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
 
def format_review(review):
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    return review
corpus = []
 
for i in range (0, len(dataset.values)):    
    review = format_review(dataset['Review'][i])
    corpus.append(review)        
                        
# Creating the bag of words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=1500)
# .toarray converts our corpus list to a matrix
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, -1].values
 
# Split our training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
 
# Fitting the classifier to our training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)
# Predict our results
y_pred = classifier.predict(X_test)
# Compare our results with the Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
# Evaluate the results
import sklearn.metrics as metrics
print('Accuracy: {}%'.format(metrics.accuracy_score(y_test, y_pred)))
print('Precision Score: {}%'.format(metrics.precision_score(y_test, y_pred, average='macro')))
print('F1 Score: {}%'.format(metrics.f1_score(y_test, y_pred)))
# Predict new review
 
new_review = 'The food was horrible and the crust was not crispy enough'
new_review = format_review(new_review)
 
test_corpus = []
test_corpus.append(new_review)
X_new_test = cv.transform(test_corpus).toarray()
prediction = classifier.predict(X_new_test)

