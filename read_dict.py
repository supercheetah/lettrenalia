"""
This will have the dictionary reading and letters counting class.
"""

class DictAndLetters():
    """
    This reads in the dictionary file from a file.
    """
    wordlist = []
    letter_points = None
    
    def __init__(self, dict_file, transform=None):
        """
        
        Arguments: - `dict_file`: An iterable object containing the
        words to read.
        - `transform`: Function to perform on each word read from
        dict_file.
        """
        
        for line in _d:
            if transform:
                line = transform(line)
            self.wordlist.append(line.strip().decode('utf-8'))

        lettercount = {}

        for word in self.wordlist:
            for letter in word:
                if letter in lettercount:
                    lettercount[letter] += 1
                else:
                    lettercount[letter] = 1

        letters_sorted = []
        counts_sorted = []

        for key, val in sorted(lettercount.iteritems(), key = lambda (k, v): (v, k)):
            letters_sorted.append(key)
            counts_sorted.append(val)

        self.letter_points = dict(zip(letters_sorted, reversed(counts_sorted)))

    def __contains__(self, word):
        """Returns whether the word is in the word list.
        
        Arguments:
        - `self`:
        - `word`:
        """
        pass
