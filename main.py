import pandas as pd

WORD_LENGTH = 6


def create_all_words(df):
    # Only keep words of 5 characters long
    df = df[df['Woord'].str.len() == WORD_LENGTH]

    # Convert Woord column to uppercase and drop all duplicates
    df['Woord'] = df['Woord'].str.upper()
    df = df.drop_duplicates(subset='Woord')

    # Drop all columns except for Woord
    df = df[['Woord']]
    df = df.sort_values(by='Woord')

    # Save the cleaned DataFrame back to the CSV file
    df.to_csv(f'words_pruned_{WORD_LENGTH}.csv', index=False, sep=';', header=False)


def create_candidate_words(df):
    # Only keep words of 5 characters long
    df = df[df['Lemma'].str.len() == WORD_LENGTH]

    # Drop all words where the Woorddata column starts with NOU-P
    allowed_types = ['NOU-C', 'VRB']
    candidate_words = []
    for word_type in allowed_types:
        words = df[df['lemmadata'].str.startswith(word_type)]
        words = words[~words['lemmadata'].str.contains('wf=abbr')]
        words = words[~words['lemmadata'].str.contains('number=pl')]
        candidate_words.append(words)

    df = pd.concat(candidate_words)

    # Convert Lemma column to uppercase and drop all duplicates
    df['Lemma'] = df['Lemma'].str.upper()
    df = df.drop_duplicates(subset='Lemma')

    # Drop all columns except for Lemma
    df = df[['Lemma']]
    df = df.rename(columns={'Lemma': 'Woord'})
    df = df.sort_values(by='Woord')

    # Save the cleaned DataFrame back to the CSV file
    df.to_csv(f'candidate_words_pruned_{WORD_LENGTH}.csv', index=False, sep=';', header=False)


def main():
    # Read the CSV file
    df = pd.read_csv('words.csv', sep=';')

    # Drop all nan values
    df = df.dropna()

    # Only keep the rows with alphanumeric characters. The words are in columns Lemma and Woord
    df = df[df['Lemma'].str.isalpha() & df['Woord'].str.isalpha()]

    # Convert all special characters to regular letters (e.g. é -> e)
    df['Lemma'] = df['Lemma'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df['Woord'] = df['Woord'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    create_all_words(df)
    create_candidate_words(df)


if __name__ == '__main__':
    main()
