# Function to find all close matches of
# input string in given list of possible strings
from difflib import get_close_matches

def closeMatches(patterns, word):
    print(get_close_matches(word, patterns,n=10, cutoff=0.5))


# Driver program
if __name__ == "__main__":
    word = 'au'
    patterns = ['anna','annu','anuraj','anurag','imran','irfan','iran','iman','iraq','indonesia']
    closeMatches(patterns, word)