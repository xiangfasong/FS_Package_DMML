import scipy.io
from sklearn import cross_validation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from FS_package.function.similarity_based import fisher_score
from FS_package.utility import construct_W


def main():
    # load matlab data
    mat = scipy.io.loadmat('../data/COIL20.mat')
    X = mat['X']    # data
    y = mat['Y']    # label
    y = y[:, 0]
    X = X.astype(float)
    n_samples, n_features = X.shape

    # split data
    ss = cross_validation.KFold(n_samples, n_folds=10, shuffle=True)

    # evaluation
    num_fea = 100
    neigh = KNeighborsClassifier(n_neighbors=10)
    correct = 0

    for train, test in ss:
        kwargs = {"neighbor_mode": "supervised", "fisher_score": True, 'y': y[train]}
        W = construct_W.construct_W(X[train], **kwargs)
        score = fisher_score.fisher_score(X[train], y[train])
        idx = fisher_score.feature_ranking(score)
        selected_features = X[:, idx[0:num_fea]]
        neigh.fit(selected_features[train], y[train])
        y_predict = neigh.predict(selected_features[test])
        acc = accuracy_score(y[test], y_predict)
        print acc
        correct = correct + acc
    print 'ACC', float(correct)/10


if __name__ == '__main__':
    main()

