############## Dimensionality reduction ##############

def explained_variance_plot(df):

	"""Function calculating and plotting the cumulated explained variance of a Dataframe."""

	#1) Scaling the data
	X_std = StandardScaler().fit_transform(df.values)
	    
	# 2) Calculating Eigenvectors and eigenvalues of Covariance matrix
	mean_vec = np.mean(X_std, axis=0)
	cov_mat = np.cov(X_std.T)
	eig_vals, eig_vecs = np.linalg.eig(cov_mat)

	# 3) Creating a list of (eigenvalue, eigenvector) tuples
	eig_pairs = [(np.abs(eig_vals[i]),eig_vecs[:,i]) for i in range(len(eig_vals))]

	# 4) Sorting the eigenvalue, eigenvector pairs from high to low
	eig_pairs.sort(key = lambda x: x[0], reverse= True)

	# 5) Calculation of Explained Variance from the eigenvalues
	tot = sum(eig_vals)
	var_exp = [(i/tot)*100 for i in sorted(eig_vals, reverse=True)] # Individual explained variance
	cum_var_exp = np.cumsum(var_exp) # Cumulative explained variance

	# 6) Plotting the cumulative explained variance

	plt.figure(figsize=(8,6))
	plt.scatter(range(cum_var_exp.shape[0]), cum_var_exp)
	plt.xlabel('Index', fontsize=12)
	plt.ylabel('Cumulative explained variance', fontsize=12)
	plt.show()

def pca_transform(df_std, n_components):

	"""Function returning the transformed Dataframe reduced to n_components.
	Dataframe argument should be scaled before using this function."""

    pca = PCA(n_components=n_components)
    pca.fit(df_std)
    df_transform = pca.transform(X_std)
    return df_transform


############## NLP-specific ##############

def word_match_share(row, str_1, str_2):

    q1words = {}
    q2words = {}
    for word in str(row[str_1]).lower().split():
        if word not in stop_words:
            q1words[word] = 1
    for word in str(row[str_2]).lower().split():
        if word not in stop_words:
            q2words[word] = 1
    if len(q1words) == 0 or len(q2words) == 0:
        return 0
    shared_words_in_q1 = [w for w in q1words.keys() if w in q2words]
    shared_words_in_q2 = [w for w in q2words.keys() if w in q1words]
    R = (len(shared_words_in_q1) + len(shared_words_in_q2))/(len(q1words) + len(q2words))
    return R

def tf_idf_dict(text_column, min_tf=2):

	vectorizer = TfidfVectorizer(min_df=min_tf)

	X = vectorizer.fit_transform(text_column)
	idf = vectorizer.idf_
	idf_dict = dict(zip(vectorizer.get_feature_names(), idf))

	print('Most common words and weights:')
	print(sorted(idf_dict.items(), key=lambda x: x[1] if x[1] > 0 else 9999)[:10])
	print('\nLeast common words and weights:')
	(sorted(idf_dict.items(), key=lambda x: x[1], reverse=True)[:10])
	return idf_dict