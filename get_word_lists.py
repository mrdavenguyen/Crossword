import random

def main():
    wordlists = create_wordlists()

def create_wordlists():
    wordlists = {i: [] for i in range(3, 16)}
    with open("words_alpha.txt") as file:
        for word in file:
            word = word.strip()
            if 3 <= len(word) <= 15:
                wordlists[len(word)].append(word)
    for length in wordlists:
        random.shuffle(wordlists[length])
    return wordlists

if __name__ == "__main__":
    main()