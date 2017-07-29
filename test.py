import numpy, random, Queue, time
from sklearn.cluster import KMeans, MeanShift
from sklearn import mixture
from sklearn.naive_bayes import MultinomialNB as MNB

data = numpy.loadtxt('mod_data.txt')
labels = numpy.loadtxt('mod_labels.txt')
label1 = KMeans(init='k-means++', n_clusters=10, n_init=10, max_iter=1000).fit_predict(data)
label2 = mixture.GMM(n_components=10).fit(data).predict(data)

# label = kmeans(data)
# print(label)
# label1 = mixture.GMM(n_components=10).fit(data).predict(data)
# label2 = MeanShift().fit_predict(data)
# print(label1)
a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in label1:
    num = int(i) - 1
    a[num] = a[num] + 1
print(a)
    
b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in label2:
    num = int(i) - 1
    b[num] = b[num] + 1
print(b)
    
correct = 0
incorrect = 0
i = 0
while (i < len(labels)):
    if labels[i] == label1[i]:
        correct = correct + 1
    else:
        incorrect = incorrect + 1
    i = i + 1
print(correct)
print(correct + incorrect)

correct = 0
incorrect = 0
i = 0
while (i < len(labels)):
    if labels[i] == label2[i]:
        correct = correct + 1
    else:
        incorrect = incorrect + 1
    i = i + 1
print(correct)
print(correct + incorrect)
