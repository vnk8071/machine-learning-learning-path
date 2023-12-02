from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import sys

import pandas as pd
import nltk
nltk.download(['punkt', 'wordnet'])


def load_data(database_filepath):
    """Load data from sqlite database.

    Args:
        database_filepath (str): Path to sqlite database.

    Returns:
        X (pandas.Series): Series containing messages.
        Y (pandas.DataFrame): Dataframe containing categories.
        category_names (list): List of category names.
    """
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql_table('messages', engine)
    df = df[:100]
    X = df['message']
    Y = df.drop(['id', 'message', 'original', 'genre'], axis=1)
    category_names = Y.columns.tolist()
    return X, Y, category_names


def tokenize(text):
    """Tokenize text

    Args:
        text (str): Text to tokenize.

    Returns:
        tokens (list): List of tokens.
    """
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token).lower().strip() for token in tokens]
    return tokens


def build_model():
    """Build model

    Returns:
        model (sklearn.pipeline.Pipeline): Pipeline containing classifier.
    """
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier())),
    ])
    print(pipeline.get_params())
    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    """Evaluate model

    Args:
        model (sklearn.pipeline.Pipeline): Pipeline containing classifier.
        X_test (pandas.Series): Series containing messages.
        Y_test (pandas.DataFrame): Dataframe containing categories.
        category_names (list): List of category names.
    """

    Y_pred = model.predict(X_test)
    Y_pred = pd.DataFrame(Y_pred, columns=category_names)
    for column in category_names:
        print('Category: {}'.format(column))
        print(classification_report(Y_test[column], Y_pred[column]))
        print(
            'Accuracy: {}'.format(
                accuracy_score(
                    Y_test[column],
                    Y_pred[column])))
        print(
            'F1 score: {}'.format(
                f1_score(
                    Y_test[column],
                    Y_pred[column],
                    average='weighted')))
        print(
            'Precision: {}'.format(
                precision_score(
                    Y_test[column],
                    Y_pred[column],
                    average='weighted')))
        print(
            'Recall: {}'.format(
                recall_score(
                    Y_test[column],
                    Y_pred[column],
                    average='weighted')))


def save_model(model, model_filepath):
    """Save model to pickle file

    Args:
        model (sklearn.pipeline.Pipeline): Pipeline containing classifier.
        model_filepath (str): Path to pickle file.
    """

    import pickle
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        # model.fit(X_train, Y_train)
        parameters = {
            'clf__estimator__n_estimators': [10, 20],
            'clf__estimator__min_samples_split': [2, 4],
        }
        gs = GridSearchCV(model, parameters)
        gs.fit(X_train, Y_train)
        print('Best parameter...')
        print(gs.best_params_)

        print('Evaluating model...')
        evaluate_model(gs, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '
              'as the first argument and the filepath of the pickle file to '
              'save the model to as the second argument. \n\nExample: python '
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
