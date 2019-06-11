#!/usr/bin/env python3

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Data manipulation
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline


def return_randomforest_cls():
    # Set a few plotting defaults
    plt.style.use('fivethirtyeight')
    plt.rcParams['font.size'] = 18
    plt.rcParams['patch.edgecolor'] = 'k'

    train = pd.read_csv('./data/train.csv')
    test = pd.read_csv('./data/test.csv')
    # Add null Target column to test
    test['Target'] = np.nan
    data = train.append(test, ignore_index=True)
    # Heads of household
    heads = data.loc[data['parentesco1'] == 1].copy()

    # Labels for training
    train_labels = data.loc[(data['Target'].notnull()) & (
        data['parentesco1'] == 1), ['Target', 'idhogar']]

    # Value counts of target
    label_counts = train_labels['Target'].value_counts().sort_index()

    # Custom scorer for cross validation
    scorer = make_scorer(f1_score, greater_is_better=True, average='macro')

    # In[105]:

    # Labels for training
    train_labels = np.array(
        list(final[final['Target'].notnull()]['Target'].astype(np.uint8)))

    # Extract the training data
    train_set = final[final['Target'].notnull()].drop(
        columns=['Id', 'idhogar', 'Target'])
    test_set = final[final['Target'].isnull()].drop(
        columns=['Id', 'idhogar', 'Target'])

    # Submission base which is used for making submissions to the competition
    submission_base = test[['Id', 'idhogar']].copy()

    # Because we are going to be comparing different models, we want to scale the features (limit the range of each column to between 0 and 1). For many ensemble models this is not necessary, but when we use models that depend on a distance metric, such as KNearest Neighbors or the Support Vector Machine, feature scaling is an absolute necessity. When comparing different models, it's always safest to scale the features. We also impute the missing values with the median of the feature.
    #
    # For imputing missing values and scaling the features in one step, we can make a pipeline. This will be fit on the training data and used to transform the training and testing data.

    # In[106]:

    features = list(train_set.columns)

    pipeline = Pipeline(
        [('imputer', Imputer(strategy='median')), ('scaler', MinMaxScaler())])

    # Fit and transform training data
    train_set = pipeline.fit_transform(train_set)
    test_set = pipeline.transform(test_set)

    # The data has no missing values and is scaled between zero and one. This means it can be directly used in any Scikit-Learn model.

    # In[107]:

    model = RandomForestClassifier(n_estimators=100, random_state=10,
                                   n_jobs=-1)
    # 10 fold cross validation
    cv_score = cross_val_score(
        model, train_set, train_labels, cv=10, scoring=scorer)

    print(f'10 Fold Cross Validation F1 Score = {round(cv_score.mean(), 4)} with std = {round(cv_score.std(), 4)}')

    # That score is not great, but it will serve as a baseline and leaves us plenty of room to improve!

    # ## Feature Importances
    #
    # With a tree-based model, we can look at the feature importances which show a relative ranking of the usefulness of features in the model. These represent the sum of the reduction in impurity at nodes that used the variable for splitting, but we don't have to pay much attention to the absolute value. Instead we'll focus on relative scores.
    #
    # If we want to view the feature importances, we'll have to train a model on the whole training set. Cross validation does not return the feature importances.

    # In[108]:

    model.fit(train_set, train_labels)

    # Feature importances into a dataframe
    feature_importances = pd.DataFrame(
        {'feature': features, 'importance': model.feature_importances_})
    feature_importances.head()

    # Below is a short function we'll use to plot the feature importances. I use this function a lot and often copy and paste it between scripts. I hope the documentation makes sense!

    # In[109]:

    def plot_feature_importances(df, n=10, threshold=None):
        """Plots n most important features. Also plots the cumulative importance if
        threshold is specified and prints the number of features needed to reach threshold cumulative importance.
        Intended for use with any tree-based feature importances. 

        Args:
            df (dataframe): Dataframe of feature importances. Columns must be "feature" and "importance".

            n (int): Number of most important features to plot. Default is 15.

            threshold (float): Threshold for cumulative importance plot. If not provided, no plot is made. Default is None.

        Returns:
            df (dataframe): Dataframe ordered by feature importances with a normalized column (sums to 1) 
                            and a cumulative importance column

        Note:

            * Normalization in this case means sums to 1. 
            * Cumulative importance is calculated by summing features from most to least important
            * A threshold of 0.9 will show the most important features needed to reach 90% of cumulative importance

        """
        plt.style.use('fivethirtyeight')

        # Sort features with most important at the head
        df = df.sort_values(
            'importance', ascending=False).reset_index(drop=True)

        # Normalize the feature importances to add up to one and calculate cumulative importance
        df['importance_normalized'] = df['importance'] / df['importance'].sum()
        df['cumulative_importance'] = np.cumsum(df['importance_normalized'])

        plt.rcParams['font.size'] = 12

        # Bar plot of n most important features
        df.loc[:n, :].plot.barh(y='importance_normalized',
                                x='feature', color='darkgreen',
                                edgecolor='k', figsize=(12, 8),
                                legend=False, linewidth=2)

        plt.xlabel('Normalized Importance', size=18)
        plt.ylabel('')
        plt.title(f'{n} Most Important Features', size=18)
        plt.gca().invert_yaxis()

        if threshold:
            # Cumulative importance plot
            plt.figure(figsize=(8, 6))
            plt.plot(list(range(len(df))), df['cumulative_importance'], 'b-')
            plt.xlabel('Number of Features', size=16)
            plt.ylabel('Cumulative Importance', size=16)
            plt.title('Cumulative Feature Importance', size=18)

            # Number of features needed for threshold cumulative importance
            # This is the index (will need to add 1 for the actual number)
            importance_index = np.min(
                np.where(df['cumulative_importance'] > threshold))

            # Add vertical line to plot
            plt.vlines(importance_index + 1, ymin=0, ymax=1.05,
                       linestyles='--', colors='red')
            plt.show()

            print('{} features required for {:.0f}% of cumulative importance.'.format(importance_index + 1,
                                                                                      100 * threshold))

        return df

    norm_fi = plot_feature_importances(feature_importances, threshold=0.95)

return_randomforest_cls()