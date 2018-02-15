def classifier_selection(train, features, target, test_size=.25, rf_param_grid=None, grid_search_cvs=5):

    """Tests main classifiers and displays their accuracy as well as the ROC curve and the AUC.
    The function does not support NaN values, which must be handled before using it, whether by
    drop, replacement of creation of a NaN feature.
    Largely inspired by code from Field Cady's Data Science Handbook.

    Next cool feature could be to add the error type we want to measure as parameter."""

    CLASS_MAP = {
        'LogisticRegression' : ('-', LogisticRegression()),
        'Naive Bayes' : ('--', GaussianNB()),
        'Decision Tree': ('.-', DecisionTreeClassifier(max_depth=5)),
        'Random Forest': (':', RandomForestClassifier())
    }

    if rf_param_grid is None:

        param_grid = {
                     'n_estimators': [40, 70, 100],
                     'max_depth': [2, 5, 7, 9],
                     'max_features': [2, 5, 7, 9]
                 }

    else:

        param_grid = rf_param_grid

    scl = StandardScaler()

    feat = pd.get_dummies(feat)

    X, Y = feat, target

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = test_size)

    X_train = scl.fit_transform(X_train)
    X_test = scl.transform(X_test)

    for name, (line_fmt, model) in CLASS_MAP.items():

        if name == 'Random Forest':
            model = GridSearchCV(model, param_grid, cv=grid_search_cvs)

        model.fit(X_train, Y_train)
        preds = model.predict_proba(X_test)
        pred = pd.Series(preds[:,1])
        fpr, tpr, thresholds = roc_curve(Y_test, pred)
        auc_score = auc(fpr, tpr)
        classic_score = model.score(X_train, Y_train)
        display_score = name + ": " + str(classic_score)
        print(display_score)
        label = '%s: auc=%f' % (name, auc_score)
        plt.plot(fpr, tpr, line_fmt, linewidth=5, label=label)

    plt.legend(loc="lower right")
    plt.title("Classifiers comparison")
    plt.plot([0,1], [0,1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.show()