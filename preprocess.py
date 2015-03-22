import json
import os
import random
import scipy.io
import codecs
import numpy as np
from collections import defaultdict
import sys
#Usage: python data_preprocess.py <feature directory> <json dataset file> <outputfile>
feat_dir = sys.argv[1]
datasetfile = sys.argv[2]
outputfile = sys.argv[3]
dataset = json.load(open(datasetfile, 'r'))
filenames = [item['filename'] for item in dataset['images']]
features_mtx = []
for imgfilename in filenames:
  wds = imgfilename.split(os.sep)
  feature_path = os.path.join(feat_dir,wds[len(wds)-1].split(".")[0])
  fin = open(feature_path)
  for line in fin:
    feats = line.strip().split(" ")
    feature = [float(item) for item in feats]
    features_mtx.append(feature)
  fin.close()
features = np.array(features_mtx).transpose() # 4096 * N
features_dic = {}
features_dic['feats'] = features
features_struct = scipy.io.savemat(outputfile, features_dic, appendmat=True)
