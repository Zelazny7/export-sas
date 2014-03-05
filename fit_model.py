import pandas as pd
import re
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import auc


# import file
df = pd.read_csv("../data/relatives.csv")

# get list of count columns
ct_cols = []
for col in df.columns:
     if re.search('ct|count', col) is not None:
          ct_cols.append(col)

# fit gb model
gb = GradientBoostingClassifier(n_estimators=50, max_depth=5)

scores = cross_val_score(gb, df[ct_cols], df.Fraud, scoring='roc_auc')

print scores



# gb.fit(df.ix[:, ct_cols], df.Fraud)
# 
# # get top 5 features
# features = np.argsort(gb.feature_importances_)[-5:].tolist()
# features += [(11,4)]
#      
# fig, axs = plot_partial_dependence(gb, df.ix[:,ct_cols], features, feature_names=ct_cols)