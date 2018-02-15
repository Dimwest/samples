def kmeans_silhouette_score_analysis(df, clustering_features, min_n_clusters=5, max_n_clusters=20, num_rows=10000):

    """Calculates and displays silhouette scores for kmeans clustering for the range of k provided."""

    range_n_clusters = list(range(min_n_clusters, max_n_clusters))
    clustering_set = df[clustering_features][:num_rows]

    silhouette_scores = []

    for n_clusters in range_n_clusters:

        scl = StandardScaler()

        X = scl.fit_transform(clustering_set)

        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)

        silhouette_avg = silhouette_score(X, cluster_labels)

        silhouette_scores.append(silhouette_avg)

        print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)


    #Showing on plot
    plt.figure(figsize=(8,6))
    plt.scatter(range_n_clusters, silhouette_scores)
    plt.xlabel('n_clusters', fontsize=12)
    plt.ylabel('silhouette_score', fontsize=12)
    plt.show()