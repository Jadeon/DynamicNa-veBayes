import numpy, random, Queue, time
from sklearn.naive_bayes import MultinomialNB as MNB
# from sklearn.cluster import KMeans, MeanShift
# from sklearn import mixture
# from sklearn.naive_bayes import GaussianNB as NB, MultinomialNB as MNB
# from sklearn.svm import SVC

# def prepare(path):
#     return numpy.loadtxt(path)
# 
# def kmeans(data):
#     return KMeans(init='k-means++', n_clusters=10, n_init=10, max_iter=1000).fit_predict(data)
# 
# def naiveBayes_init():
#     return NB()
# 
# def naiveBayes_train(model, data, label):
#     return model.fit(data, label)
# 
# def naiveBayes_classify(model, data):
#     return model.predict(data)

def main():
    
    # 1. Data Preparation
    data = numpy.loadtxt('mod_data.txt')
    labels = numpy.loadtxt('mod_labels.txt')

    test_data = numpy.loadtxt('mod_test_data.txt')
    test_labels = numpy.loadtxt('mod_test_label.txt')
    test = numpy.column_stack((test_data, test_labels))
    # print(test[0,0:-1])
    
    # 2. Create Sorted Data Vector by Label
    sorted_data = [[], [], [], [], [], [], [], [] ,[] ,[]]
    idx = 0
    for row in data:
        sorted_data[int(labels[idx]) - 1].append(row)
        idx += 1
    sorted_data = numpy.asarray(sorted_data)

    # 3. Calculate Cluster Scores
    cluster_scores = [[], [], [], [], [], [], [], [] ,[] ,[]]
    for idx in range(0, 10):
        cluster_scores[idx] = numpy.mean(sorted_data[idx], axis=0)
    cluster_scores = numpy.around(cluster_scores, decimals=5)
    
    # 3. Initial Training
    nb_classifier = MNB().fit(data, labels)
    
    # 4. Initial Enqueue of All New Agents
    new_queue = Queue.Queue(0)
    recycle_queue = Queue.Queue(0)
    for v in test:
        new_queue.put(v)
    
    # 5. Event Loop
    itr = 1
    correct = 0
    # total = 0
    # while True:
    for i in range(0,5000):
        # print "[Iteration %d]" % itr
        agent = None
        # 5-1 New Agent Queue
        if not new_queue.empty():
            agent = new_queue.get()
            # print("New Agent Dequeued")
        # 5-2 Recycled Agent Queue
        else:
            if not recycle_queue.empty():
                agent = recycle_queue.get()
                # print("Recycled Agent Dequeued")
            # 5-3 Random Event
            # else:
            #     n = random.random()
            #     if (n < 0.01):
            #         print("Random Event!")
            #         time.sleep(2)
            #         continue
        # time.sleep(1)

        # 5-4 Classification            
        if agent is not None:
            result = nb_classifier.predict(agent[0:-1])
        
        if int(result) == int(agent[-1]):
            correct += 1
        
        idx = int(result) - 1    
        # print "Label: %d" % int(result)
        
        
        # 5-5 Integrity Check
        integrities = numpy.isclose(cluster_scores[idx], agent[0:-1], atol=50)
        accepted = True if numpy.bincount(integrities)[0] < 50 else False
        # print "Accepted: %r" % accepted
        # 5-6 Re-train Classifier
        if accepted:
            # 5-6-1 Add Accepted Agent into Table
            sorted_data[idx].append(agent[0:-1])
            
            # 5-6-2 Recalculate Cluster Scores
            cluster_scores[idx] = numpy.mean(sorted_data[idx], axis=0)
            cluster_scores[idx] = numpy.around(cluster_scores[idx], decimals=5)
            
            # 5-6-3 Reject any agents in that cluster (reevaluate the compatibility with the new cluster score)
            # Rejects go to recycle_queue
            
            # 5-6-4 Update Naive Bayes Classifier (Partial Fit)
            nb_classifier = nb_classifier.partial_fit(cluster_scores, numpy.arange(1, 11))
            
        # 5-7 Enqueue in Recycled Queue
        else:
            recycle_queue.put(agent)
        
        # print "New Agent Queue: %d\nRecycle Queue: %d\n" % (new_queue.qsize(), recycle_queue.qsize())
        itr += 1
    
    print "Correct: %d" % (correct)

if __name__ == '__main__':
    main()





    # 2. Clustering
    # label = kmeans(data)
    # # print(label)
    # label1 = mixture.GMM(n_components=10).fit(data).predict(data)
    # label2 = MeanShift().fit_predict(data)
    # print(label1)
    # a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 
    # for i in label:
    #     num = int(i) - 1
    #     a[num] = a[num] + 1
    # print(a)
    
    # b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 
    # for i in label1:
    #     num = int(i) - 1
    #     b[num] = b[num] + 1
    # print(b)
    # 
    # 
    # c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 
    # for i in label2:
    #     num = int(i) - 1
    #     c[num] = c[num] + 1
    # print(c)
    # 
    # correct = 0
    # incorrect = 0
    # for i in labels:
    #     if labels[i] == label[i]:
    #         correct = correct + 1
    #     else:
    #         incorrect = incorrect + 1
    #     # print(str(labels[i]) + " / " + str(label[i])
    # 
    # a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 
    # for i in labels:
    #     num = int(i) - 1
    #     a[num] = a[num] + 1
    # print(a)
    # # print(label)
    # model = naiveBayes_init()
    # model = naiveBayes_train(model, data, label)
    # A = naiveBayes_classify(model, data)
    # # A = naiveBayes(data, label)
    # c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 
    # for i in A:
    #     num = int(i) - 1
    #     c[num] = c[num] + 1
    # print(c)
    # print(A)
    
    # correct = 0
    # incorrect = 0
    # i = 0
    # while (i < 1409):
    #     if label[i] == A[i]:
    #         correct = correct + 1
    #     else:
    #         incorrect = incorrect + 1
    #     i = i + 1
    #     # print(str(labels[i]) + " / " + str(label[i])
    # print(correct)
    # print(correct + incorrect)
