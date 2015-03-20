import numpy as np
import matplotlib.pyplot as plt

f = open('processed.cleveland.data')
string_data = f.read().split('\n')
num_patients = (len(string_data)-1)
num_features = 13

data = np.zeros((num_patients, num_features))
values = np.zeros((num_patients,))
means = np.zeros((num_features))
denoms = np.zeros((num_features))

for i in range(num_patients):
	features_and_label = string_data[i].replace('?', '-0.00000000000001').split(',')
	if '-0.00000000000001' in features_and_label:
		print features_and_label 
	values[i] = features_and_label[-1]
	data[i,:] = features_and_label[:-1]
	for j in range(num_features):
		if features_and_label[j] != '-0.00000000000001':
			means[j]+= float(features_and_label[j])
			denoms[j]+=1
means =  means/denoms

# for i in range(num_patients):
# 	features_and_label = string_data[i].replace('?', '-0.00000000000001').split(',')
# 	values[i] = features_and_label[-1]
# 	data[i,:] = features_and_label[:-1]
# 	for j in range(num_features):
# 		if features_and_label[j] != '-0.00000000000001':
# 			data[i,j] = means[j]

beta = np.dot(np.linalg.inv(np.dot(data.transpose(), data)+0.0001*np.identity(13)), np.dot(values, data).transpose())

beta_random = np.random.normal(0,1,size=13)/100
print np.dot(beta_random.transpose(),data[:100,:].transpose())

predictions = np.zeros((100))
#print beta.shape, data.shape
predictions = np.dot(beta.transpose(),data[:100,:].transpose())
#predictions = [int(i) for i in predictions]
predictions_rand = np.dot(beta_random.transpose(),data[:100,:].transpose())
predictions_rand = [int(i) for i in predictions_rand]

#print predictions
rss = 0
rss_rand=0
for i in range(100):
	#print ((float(values[i])-predictions[i])**2)**0.5
	rss += ((float(values[i])-predictions[i])**2)**0.5
	rss_rand += ((float(values[i])-predictions_rand[i])**2)**0.5
print predictions
print values[:100]
print rss/(100-1) #avg absolute deviation from truth
print rss/(99*np.std(values[:100]))
# print rss_rand/99.0

plt.scatter(values[:100], predictions)
plt.show()