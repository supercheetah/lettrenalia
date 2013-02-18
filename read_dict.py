"""
This will have the dictionary reading and letters counting class.
"""

class DictAndLetters(object):
    """
    This reads in the dictionary file from a file.
    """
    _wordlist = []
    _letter_points = None

    @property
    def wordlist(self):
        """Returns the word list.
        """
        return self._wordlist

    @property
    def letter_points(self):
        """Returns the letters and points dictionary.
        """
        return self._letter_points

    
    def __init__(self, dict_file, transform=None):
        """
        
        Arguments:
        - `dict_file`: An iterable object containing the words to
        read.
        - `transform`: Function to perform on each word read from
        dict_file.
        """
        
        for line in dict_file:
            line = line.decode('utf-8').strip()
            if transform:
                line = transform(line)
                
            self._wordlist.append(line)

        lettercount = {}

        for word in self._wordlist:
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

        self._letter_points = dict(zip(letters_sorted, reversed(counts_sorted)))

    def __contains__(self, word):
        """Returns whether the word is in the word list.
        
        Arguments:
        - `word`: The word to compare.
        """
        return word in self._wordlist

    def get_points(self, word):
        """Return the number of points for a word.
        
        Arguments:
        - `word`: The word we want points from.
        """
        _sum = 0
        for letter in word:
            _sum += self._letter_points[letter]

        return _sum



if __name__ == '__main__':
    with open('dict') as dict_file:
        dal_dict = DictAndLetters(dict_file, lambda (line): line.upper())

    for word in dal_dict.wordlist:
        print word

    for k, v in sorted(dal_dict.letter_points.iteritems(), key = lambda (k, v): (v, k)):
        print u"{0}: {1}".format(k, v)

    wordtest = raw_input("Word to find: ").strip().encode('utf-8').upper()

    print u"{0} is a word: {1}".format(wordtest, wordtest in dal_dict)
    print u"points awarded: {0}".format(dal_dict.get_points(wordtest))
