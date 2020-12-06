tymdata = read.csv('Timestamp.csv')
print(tymdata)

tymdata <- na.omit(tymdata)
tymdata <- scale(tymdata)

print(is.data.frame(tymdata))

#kmeans
clusters <- kmeans(x = tymdata,centers = 3,iter.max = 10,nstart = 1)
print(clusters)

tymdata$clusters <- as.factor(clusters$cluster)
head(tymdata)
str(clusters)
print(clusters$centers)

library(ggplot2)
ggplot() +
  geom_point(data = tymdata, mapping = aes(x = TimestampId,y = Timestamp),color = "grey")+
  geom_point(mapping = aes_string(x = clusters$centers[,'TimestampId'], y  = clusters$centers[,'Timestamp']),color = "firebrick",size = 3)+
  ggtitle("Tweets Timestamps using Kmean")
