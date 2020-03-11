from sklearn.feature_selection import RFE
from sklearn.svm import SVR
import matplotlib.pyplot as plt
#http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html#sklearn.feature_selection.RFE
#根据a coef_ attribute or a feature_importances_ attribute逐渐删除重要性最低的特征子集,直到特征达到指定需要个数为止
select = RFE(SVR(kernel='sigmoid', degree=3, gamma='scale', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1), n_features_to_select=200)
#select = RFE(LogisticRegression(penalty="l1"), n_features_to_select=40)


select.fit(X_train, y_train)
# visualize the selected features:
mask = select.get_support()
plt.matshow(mask.reshape(1, -1), cmap='gray_r')