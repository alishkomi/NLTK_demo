"""
Author: Alisher Komilov
email: axk153430@utdallas.edu
Date: Sunday January 31, 2021

Homework assignment 2 for CS4395 Karen Mazidi
"""
import sys  # for reading and exiting from file and program
import re  # for removing unnecessary characters in text (tokenizing text)
import nltk  # word_tokenize, WordNetLemmatizer, stopwords, and pos_tag functions
from random import randint  # used to pick a random word from lemmatized nouns


# define Dictionary to store nouns and their count in text
class Dictionary(dict):

    def __init__(self):
        super().__init__()
        self = dict()

    # key is noun value is number of times the noun appears in text
    def add(self, key, value):
        self[key] = value


# define tokenize to remove grammar characters and use NLTK word_tokenize method to tokenize text
def tokenize(document):
    document = re.sub(r'[.?!,:;()_\-\n\d]', ' ', document.lower())
    tokens = nltk.word_tokenize(document)
    return tokens


# Step 2: calculates lexical diversity of text by dividing number of unique words by total number of words
def lex_diversity(document):
    diversity = round((100 * len(set(tokenize(document))) / len(tokenize(document))), 2)
    return diversity


# Step 3.a: returns only alpha tokens longer than 5 letters that are not in NLTK stopword list
def alpha(document):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in tokenize(document) if w not in stopwords and len(w) > 5]
    return content


# Step 3.b: lemmatizes tokens and returns a set of unique words
def unique(document):
    wnl = nltk.WordNetLemmatizer()
    content_lem = [wnl.lemmatize(t) for t in alpha(document)]
    content_lem_uniq = set(content_lem)
    return content_lem_uniq


# Step 3.c.1: performs position tagging words with their appropriate part of speech
def pos_tag(document):
    tagged_cont = nltk.pos_tag(unique(document))
    return tagged_cont


# Step 3.c.2: returns first 20 tagged items(words) from text
def print_20(document):
    tagged_20 = pos_tag(document)[:20]
    return tagged_20


# Step 3.d: returns a list of nouns that are unique and lemmatized
def nouns(document):
    noun_list = [w for w in pos_tag(document) if w[1].startswith("NN")]
    return noun_list


# Step 4: define dictionary function to store 50 common nouns in text
def dictionary(document):
    temp_dict = Dictionary()
    temp_token = tokenize(document)
    noun_list = nouns(document)

    # for every noun in noun_list
    for x in noun_list:
        # add the number of times the word appears in the original text(words with 6 letters or more)
        count = 1 + temp_token.count(x[0][:5])
        # add words to dictionary with number of times they appear in text. Keys are words and count is value
        temp_dict.add(x[0], count)

    # Sorting dictionary to have most common words to be at the beginning of dictionary
    sorted_dict = dict(sorted(temp_dict.items(), key=lambda item: item[1], reverse=True))
    # Save only 50 of the words from step before
    first_fifty = list(sorted_dict.items())[:50]

    return first_fifty


# Step 5 self calling function that takes text and score value as parameters
def game(document, score):
    # initiating noun words bank
    glossary = dictionary(document)
    # picking one random word from dictionary
    word = glossary[randint(1, 50)][0]
    # displaying number of characters using '_' character
    display = '_' * len(word)
    # temporary list used to store user guessed letters
    used_letters = []

    # while user still has points
    while score >= 0:
        # print the word characters user have successfully guessed
        print(display)
        # ask user for input
        temp = input("Guess a letter:")

        # if user input is '!' exit from program
        if temp == "!":
            exit()

        # else if user input is not a letter ask for a letter
        elif not temp.isalpha():
            print("Guess only a letter.")

        # else if user input is more than one character ask for only one letter
        elif len(temp) > 1:
            print("Guess only one letter.")

        # else if user input is already guessed print a message
        elif temp in used_letters:
            print("You have already guessed this letter.")

        # else if user input does not match any letters in current word
        elif temp.lower() not in word:
            # lower score
            score -= 1

            # and if no more lives left quit program
            if score < 0:
                exit("\nGame over:( No more lives left.")

            # else print a message and store guessed character
            else:
                print("Sorry, guess again. Score is", score)
            used_letters.append(temp.lower())

        # finally if user input matches a letter in current word
        else:
            # give a point
            score += 1
            # store guessed letter in used list
            used_letters.append(temp.lower())
            # print a message
            print("Right! Score is", score)
            # update the function that prints the status of the word
            updated_display = ''

            for w, l in zip(word, display):
                if temp.lower() == w:
                    # reveal the correct guessed letter
                    updated_display += temp.lower()
                else:
                    # keep the unknown letters hidden
                    updated_display += l

            # print the word with correctly guessed letters
            display = updated_display

            # if there are no letters left to guess
            if '_' not in display:
                # reveal the word
                print(display)
                print("You solved it!\n")
                print("Current score:", score)
                print("\nGuess another word")
                # repeat the game from beginning
                game(document, score)


# define main function that executes all functions with appropriate descriptions
def main():
    # check to see if user successfully passed the text filename as argument in terminal
    if len(sys.argv) < 2:
        exit("Program requires filename passed as argument in terminal")

    else:
        # read the text
        with open(str(sys.argv[1]), 'r') as file:
            text = file.read()

        print("\nThe lexical diversity of the tokenized text is:", lex_diversity(text), "percent.")
        print("The first 20 tagged unique lemmas are:\n\n", print_20(text), "\n")
        print("The number of unique words(of length 6 or more letters) in the text is:", len(alpha(text)))
        print("The number of nouns within those unique words is:", len(nouns(text)), "\n")
        print("The 50 most common words and their counts are:\n\n", dictionary(text), "\n")
        print("\n\nLet's play a word guessing game!\n")

        # Score is defined outside of the game function so that if user decides to continue to play,
        # the score is not reset to 5 and it is current one.
        score = 5
        game(text, score)


# end of program
main()
