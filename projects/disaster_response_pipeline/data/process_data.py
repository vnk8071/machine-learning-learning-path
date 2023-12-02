import sys
import pandas as pd


def load_data(messages_filepath, categories_filepath):
    """Load data from csv files and merge them into a single dataframe.

    Args:
        messages_filepath (str): Path to messages csv file.
        categories_filepath (str): Path to categories csv file.

    Returns:
        df (pandas.DataFrame): Dataframe containing messages and categories.
    """
    df_messages = pd.read_csv(messages_filepath)
    df_categories = pd.read_csv(categories_filepath)
    df = pd.merge(df_messages, df_categories, on='id')
    return df


def clean_data(df):
    """Clean dataframe by splitting categories into separate columns and

    Args:
        df (pandas.DataFrame): Dataframe containing messages and categories.

    Returns:
        df (pandas.DataFrame): Cleaned dataframe.
    """
    # Drop duplicates
    df = df.drop_duplicates()

    # Split categories into separate columns
    categories = df['categories'].str.split(';', expand=True)
    category_colnames = [category.split('-')[0]
                         for category in categories.iloc[0]]
    categories.columns = category_colnames

    # Convert category values to binary
    for column in categories:
        categories[column] = categories[column].str[-1]
        categories[column] = categories[column].astype(int)
        categories.drop(categories[categories[column] > 1].index, inplace=True)

    # Replace categories column in df with new category columns
    df = df.drop('categories', axis=1)
    df = pd.concat([df, categories], axis=1)

    # Check values
    for column in categories:
        print(df[column].value_counts())
    return df


def save_data(df, database_filename):
    """Save dataframe to a sqlite database.

    Args:
        df (pandas.DataFrame): Dataframe containing messages and categories.
        database_filename (str): Filename of database.
    """
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('messages', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '
              'datasets as the first and second argument respectively, as '
              'well as the filepath of the database to save the cleaned data '
              'to as the third argument. \n\nExample: python process_data.py '
              'disaster_messages.csv disaster_categories.csv '
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
