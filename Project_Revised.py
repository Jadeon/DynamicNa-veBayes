import numpy, random, Queue, time
from sklearn.naive_bayes import MultinomialNB as MNB

def main():
    
    # 1. Data Preparation
    data = numpy.loadtxt('mod_data.txt')
    labels = numpy.loadtxt('mod_labels.txt')

    test_data = numpy.loadtxt('mod_test_data.txt')
    test_labels = numpy.loadtxt('mod_test_label.txt')
    test = numpy.column_stack((test_data, test_labels))

    
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
    cluster_scores = numpy.around(cluster_scores)
    
    # 4. Initial Training
    nb_classifier = MNB().fit(data, labels)
    
    # 5. Initial Enqueue of All New Agents
    new_queue = Queue.Queue(0)
    recycle_queue = Queue.Queue(0)
    for v in test:
        new_queue.put(v)
    
    # 6. Event Loop
    itr = 1
    correct = 0
    for i in range(0,500):
        print "[Iteration %d]" % itr
        agent = None
        # 6-1 New Agent Queue
        if not new_queue.empty():
            agent = new_queue.get()
            print("New Agent Dequeued")
        # 6-2 Recycled Agent Queue
        else:
            if not recycle_queue.empty():
                agent = recycle_queue.get()
                print("Recycled Agent Dequeued")
            # 6-3 Random Event
            else:
                n = random.random()
                if (n < 0.01):
                    print("Random Event!")
                    time.sleep(2)
                    continue

        # 6-4 Classification            
        if agent is not None:
            result = nb_classifier.predict(agent[0:-1])
        
        if int(result) == int(agent[-1]):
            correct += 1
        
        idx = int(result) - 1    
        print "Label: %d" % int(result)
        
        
        # 6-5 Integrity Check (Tolerance to 10, Reject Threshold 10 ~ 1.7%)
        integrities = numpy.isclose(cluster_scores[idx], agent[0:-1], atol=50)
        accepted = True if numpy.bincount(integrities)[0] < 50 else False
        print "Accepted: %r" % accepted

        # 6-6 Re-train Classifier
        if accepted:
            # 6-6-1 Add Accepted Agent into Table
            sorted_data[idx].append(agent[0:-1])
            
            # 6-6-2 Recalculate Cluster Scores
            cluster_scores[idx] = numpy.mean(sorted_data[idx], axis=0)
            cluster_scores[idx] = numpy.around(cluster_scores[idx], decimals=5)
            
            # 6-6-3 Recheck Integrity of Individual Agent
            index = 0
            for row in sorted_data[idx]:
                row_integrities = numpy.isclose(cluster_scores[idx], row, atol=5)
                accepted = True if numpy.bincount(integrities)[0] < 5 else False
                if not accepted:
                    recycle_queue.put(accepted)
                    numpy.delete(sorted_data[idx], row)
                    print "Agent %d in Cluster %d Rejected. Placed in recycle_queue" % (index, idx)
                index += 1
                    
            
            # 6-6-4 Update Naive Bayes Classifier (Partial Fit)
            nb_classifier = nb_classifier.partial_fit(cluster_scores, numpy.arange(1, 11))

            
        # 6-7 Enqueue in Recycled Queue
        else:
            recycle_queue.put(agent)
        
        print "New Agent Queue: %d\nRecycle Queue: %d\n" % (new_queue.qsize(), recycle_queue.qsize())
        itr += 1
    
    print "Correct: %d" % (correct)

if __name__ == '__main__':
    main()


