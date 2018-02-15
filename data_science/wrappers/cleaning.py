############## Empty values handling ##############

def missing_values_table(df): 

    l = len(df)
    mis_val = df.isnull().sum().reset_index(name='count_nan')
    mis_val['pcent_total'] = mis_val.count_nan.apply(lambda x: x/l)
    mis_val = mis_val[mis_val.count_nan > 0].sort_values('pcent_total', ascending=False)
    return mis_val

def nan_viz(df, features):

    msno.matrix(df=df[features], figsize=(20,14), color=(0.5,0,0))

def nan_to_median(df, cols):
    for c in cols:
        med = df[c].median()
        df[c] = df[c].fillna(med)
    return df

############## NLP-specific ##############

def filter_stopwords(row):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(row)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = ' '.join(filtered_sentence)
    return filtered_sentence
