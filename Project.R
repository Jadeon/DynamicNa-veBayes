require('stats')
require('e1071')

# 0. Preparation
Data = as.matrix(read.table('data.txt'))

# 1. K-Means
Clusters = kmeans(Data, 10, 10000)
Clusters = Clusters$cluster

Data = cbind(Data, NA)

for (i in 1:nrow(Data)) {
  if (Clusters[i] == 1) {
    Data[i, ncol(Data)] = 1
  }
  else if (Clusters[i] == 2) {
    Data[i, ncol(Data)] = 2
  }
  else if (Clusters[i] == 3) {
    Data[i, ncol(Data)] = 3
  }
  else if (Clusters[i] == 4){
    Data[i, ncol(Data)] = 4
  }  
  else if (Clusters[i] == 5) {
    Data[i, ncol(Data)] = 5
  }
  else if (Clusters[i] == 6) {
    Data[i, ncol(Data)] = 6
  }
  else if (Clusters[i] == 7) {
    Data[i, ncol(Data)] = 7
  }
  else if (Clusters[i] == 8){
    Data[i, ncol(Data)] = 8
  }  
  else if (Clusters[i] == 9) {
    Data[i, ncol(Data)] = 9
  }
  else if (Clusters[i] == 10) {
    Data[i, ncol(Data)] = 10
  }
}

# 2. Calculate Classifier

Model <- naiveBayes(Data[,-577], as.factor(Data[,577]))
V = Data[2, 1:(ncol(Data)-1)]

print(Data[2, ncol(Data)])
Y = predict(Model, as.data.frame(V))


# 
# print(dim(Titanic))
# m <- naiveBayes(Survived ~ ., data = Titanic)
# S = predict(m, as.data.frame(Titanic)[,1:3])
# print(S)






# trnLabel = as.factor(trnLabel)
# Model = NaiveBayes(trnLabel, trnData)
# V = Data[2, 1:ncol(Data) -1]
# print(Data[2, ncol(Data)])
# Y = predict(Model, V)