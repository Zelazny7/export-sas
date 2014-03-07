import pandas as pd

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import six
from sklearn.tree import _tree
import re

# create a dummy tree
df = pd.read_csv("data/relatives.csv", nrows=25000)

# get list of count columns
ct_cols = []
for col in df.columns:
     if re.search('ct|count', col) is not None:
          ct_cols.append(col)

# create decision tree
dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=50)
dt.fit(df.ix[:, ct_cols], df.Fraud)
     
# reverse engineer the dt

# get array positions of all the terminal nodes
idx = np.argwhere(dt.tree_.children_left == -1)[:,0]

# for each node, find the parent and recurse through the branch
# can come from left OR right branch ...



def get_lineage(left, right, child, lineage=None):
     if lineage is None:
          lineage = [child]
     if child in left:
          parent = np.where(left == child)[0].item()
          split = 'l'
     else:
          parent = np.where(right == child)[0].item()
          split = 'r'
     lineage.append((parent, split))
     if parent == 0:
          lineage.reverse()
          return lineage
     else:
          return get_lineage(left, right, parent, lineage)


def get_lineage2(tree, feature_names):
     left      = tree.tree_.children_left
     right     = tree.tree_.children_right
     threshold = tree.tree_.threshold
     features  = [feature_names[i] for i in tree.tree_.feature]
     
     # get ids of child nodes
     idx = np.argwhere(left == -1)[:,0]     

     def recurse(left, right, child, lineage=None):          
          if lineage is None:
               lineage = [child]
          if child in left:
               parent = np.where(left == child)[0].item()
               split = 'l'
          else:
               parent = np.where(right == child)[0].item()
               split = 'r'
          
          lineage.append((parent, split, threshold[parent], features[parent]))
          
          if parent == 0:
               lineage.reverse()
               return lineage
          else:
               return recurse(left, right, parent, lineage)

     for child in idx:
          for node in recurse(left, right, child):
               print node



get_lineage2(dt, ct_cols)