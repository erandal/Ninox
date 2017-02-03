"""
 Get data from HDFS, build a model and save it to mongoDb.

https://www.mapr.com/blog/apache-spark-machine-learning-tutorial

"""

from __future__ import print_function
from pyspark import SparkContext

# Libraries for predictive analytics
#from pyspark.mllib.tree import RandomForest, RandomForestModel
#from pyspark.mllib.regression import LabeledPoint

from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD, LinearRegressionModel

import numpy as np
import functools

# Load and parse the data
def parsePoint(line):
    values = [float(x) for x in line.split(',')]
    return LabeledPoint(values[1], values[2:])

sc = SparkContext(appName="BatchBuildModel")

# Load data
data_file = sc.textFile("hdfs://172.254.0.2:9000/user/root/initial.csv")

parsedData = data_file.map(parsePoint)

model = LinearRegressionWithSGD.train(parsedData,100000,0.01)

model.save(sc, "hdfs://172.254.0.2:9000/user/root/models/first.model")
#model = RandomForest.trainRegressor(parsedData, categoricalFeaturesInfo={}, numTrees=3, featureSubsetStrategy="auto", impurity='variance', maxDepth=4, maxBins=32)
sc.stop()