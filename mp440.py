import inspect
import sys
import math 

prior = [0 for i in range(0,10)]
conditional = []
numPresent = []
numFeatVals = 2
K = 0.1
'''
Raise a "not defined" exception as a reminder 
'''
def _raise_not_defined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)


'''
Extract 'basic' features, i.e., whether a pixel is background or
forground (part of the digit) 
'''
def extract_basic_features(digit_data, width, height):
    global numFeatVals
    numFeatVals = 2
    features=[]
    # Your code starts here 
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here 
    features = [False for i in range(0, int(width*height))]
    for i in range(0, height):
        for j in range(0, width):
            if digit_data[i][j] != 0:
                features[i*width + j] = True
    return features

'''
Extract advanced features that you will come up with 
'''
def extract_advanced_features(digit_data, width, height):
    features=[]
    features = [0 for i in range(int(width*height))]
    numFeatVals = 3 #Now I will treat numFeatVals as a feature extractor switch rather than its literal meaning
    # Your code starts here 
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    sum = 0     #feature set 1 counter
    sum2 = 0    #feature set 2 counter
    sum3 = 0    #feature set 3 counter

    #Row-wise sum

    for i in range(0, height):
        for j in range(0, width):
            for k in range(j,-1,-1):
                if digit_data[i][k] == 0:
                    sum += 1.0
                else:
                    break
            for k in range(j,width):
                if digit_data[i][k] == 0:
                    sum += 1.0
                else:
                    break
            features[i*width + j] = sum
            sum = 0

    #Column-wise sum

    for i in range(0, height):
        for j in range(0, width):
            for k in range(i,-1,-1):
                if digit_data[k][j] == 0:
                    sum2 += 1.0
                else:
                    break
            for k in range(i,height):
                if digit_data[k][j] == 0:
                    sum2 += 1.0
                else:
                    break
            features[i*width + j] += sum2
            sum2 = 0

    #Neighbor sum





    return features

'''
Extract the final features that you would like to use
'''
def extract_final_features(digit_data, width, height):
    #features=[]
    # Your code starts here 
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    extract_basic_features(digit_data, width, height)

'''
Compupte the parameters including the prior and and all the P(x_i|y). Note
that the features to be used must be computed using the passed in method
feature_extractor, which takes in a single digit data along with the width
and height of the image. For example, the method extract_basic_features
defined above is a function than be passed in as a feature_extractor
implementation.

The percentage parameter controls what percentage of the example data
should be used for training. 
'''
def compute_statistics(data, label, width, height, feature_extractor, percentage=10.0):
    # Your code starts here 
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here 
    global prior, conditional, numPresent, numFeatVals
    #There are 5000 examples
    #print K
    conditional = [[0 for j in range(0,width*height)] for i in range(0,10)]
    numPresent = [[0 for j in range(0,width*height)] for i in range(0,10)]
    totalNum = int(percentage/100.0*5000)
    
    for i in range(0,totalNum):
        l = int(label[i])
        feat = feature_extractor(data[i],width, height)
        prior[l] += 1.0
        for j in range(0,len(feat)):
            numPresent[l][j] += 1.0
            if numFeatVals == 2:
                if feat[j] == True:
                    conditional[l][j] += 1.0
            else:
                if feat[j] > ((width/3)+(height/3)):
                    conditional[l][j] += 1.0


    #smoothing
    for i in range(0,len(conditional)):
        for j in range(0,len(conditional[0])):
#            if conditional[i][j] == 0:
            conditional[i][j] += K
            numPresent[i][j] += numFeatVals*K #for number of possible feature vals
    
    for i in range(0,len(conditional)):
        for j in range(0,len(conditional[0])):
            conditional[i][j] = conditional[i][j]/numPresent[i][j]

    for i in range(len(prior)):
        prior[i] = prior[i]/totalNum


    #print str(prior)
    
    """
    for l in label[0:totalNum]:
        prior[int(l)] += 1.0
        numPresent[int(l)] += 1
    for i in range(0,10):
        prior[i] = math.log(prior[i]/totalNum)
        stats[i] = prior[i]
    
    conditional = [[0 for i in range(0,width*height)] for j in range(0,10)]
    for i in range(0,totalNum):
        featureVec = feature_extractor(data[i], width, height)
        for j in range(0, len(featureVec)):
            if featureVec[j] == True:
                conditional[int(label[i])][j] += 1.0/numPresent[int(label[i])]
    
    for i in range(10):
        print sum(conditional[i])
        print numPresent[i]
    print sum(numPresent)
    
    for i in range(0,len(conditional)):
        tempProb = 0
        for pixel in conditional[i]:
            if pixel == 0:
                tempProb += math.log(k/(k+numPresent[int(label[i])]))
            else:
                tempProb += math.log(pixel)
        stats[i] += tempProb
    """
        

'''
For the given features for a single digit image, compute the class 
'''
def compute_class(features):
    predicted = [math.log(p) for p in prior]


#    predicted = [p for p in prior]
    
    # Your code starts here 
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here 
    
    for f in range(0,len(features)):
        if numFeatVals == 2:
            for lab in range(0,10):
                if features[f] == True:
                    predicted[lab] += math.log(conditional[lab][f])
#                    predicted[lab] *= conditional[lab][f]
                elif features[f] == False:
                    predicted[lab] += math.log(1-conditional[lab][f])
#                    predicted[lab] *= 1-conditional[lab][f]
    
    #print  predicted.index(max(predicted))
    return predicted.index(max(predicted))

'''
Compute joint probaility for all the classes and make predictions for a list
of data
'''
def classify(data, width, height, feature_extractor):

    predicted=[]
    #predicted2 = [math.log(p) for p in prior]
    #val = compute_class(feature_extractor(data))
    
    # Your code starts here 
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here 
    
    for d in data:
        predicted.append(compute_class(feature_extractor(d ,width, height)))

    #print predicted.index(max(predicted))
    return predicted






        
    
