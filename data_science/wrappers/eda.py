def cumsum_pcent_plot(df, target_column):

    """Function adding to a Dataframe the cumulated sum of the target column as share of the target column total, sorted descencing.
    Useful for EDA."""

    df = df.sort_values(target_column, ascending=False)
    new_col_name = target_column + ' cumsum %'
    df['revenue_cumsum'] = df.total_revenue.cumsum()/df.total_revenue.sum()

    ax = sns.distplot(df[target_column]dropna(), bins=50, kde=False)
    plt.xlabel(target_column, 'cumsum %')
    plt.ylabel('# records')
    plt.show()

    return df