from sklearn import preprocessing


class Preprocessor:
    def __init__(self, pass_col=None):
        '''
        preprocess: fillna and label encoder
        '''
        self.le_dict = {}
        self.na_rule = {}
        self.pass_col = pass_col

    def fit_transform(self, df):  # for training
        df = self.na_fill(df, is_train=True)  # fill na
        df = self.label_encoder(df, is_train=True)  # categorical col encoder

        return df

    def transform(self, df):  # for prediction
        df = self.na_fill(df, is_train=False)
        df = self.label_encoder(df, is_train=False)

        return df

    def na_fill(self, df, is_train):
        if is_train:
            for col in df.columns:
                if col == self.pass_col:
                    continue
                
                if df[col].dtypes == 'object':  # category fill by mode
                    self.na_rule.update({col: df[col].mode()[0]})

                elif df[col].dtypes != 'object':  # numeric fill by median
                    self.na_rule.update({col: df[col].median()})

        # fill na with na_rule
        df_c = df.copy()
        na_cnt = df.isnull().sum()
        fill_col = list(na_cnt[na_cnt > 0].index)
        
        for col in fill_col:
            if col ==self.pass_col:
                continue
            
            df_c[col].fillna(self.na_rule[col], inplace=True, downcast=False)

        return df_c

    def label_encoder(self, df, is_train):
        categorical_features = list(df.select_dtypes(include=['category', 'object']))
        tmp_df = df.copy()

        if is_train:
            for c in categorical_features:
                if c == self.pass_col:
                    continue

                self.le_dict[c] = preprocessing.LabelEncoder()
                tmp_df[c] = self.le_dict[c].fit_transform(tmp_df[c].astype(str))
                '''
                Here, treat na as a category. if there is some na rule in domain knowledge, than na_fill will be process before
                if don't want to remain na in column, can consider below page:
                ref: https://stackoverflow.com/questions/36808434/label-encoder-encoding-missing-values
                '''
        else:
            for c in categorical_features:
                if c not in list(self.le_dict.keys()):  # if new column, then skip it
                    continue
                
                le = self.le_dict[c]
                mapping = dict(zip(le.classes_, le.transform(le.classes_)))  # get mapping dict from label encoder
                tmp_df[c] = tmp_df[c].apply(lambda x: mapping.get(x, -1))
                # if there are new category, then it will not map to any key and give it -1
                # ref: https://stackoverflow.com/questions/21057621/sklearn-labelencoder-with-never-seen-before-values

        return tmp_df
