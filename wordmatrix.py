"""
This will be the class for storing the words.
"""

import itertools

class WordMatrix():
    """The class that has the words in it like in a matrix.
    """
    _matrix_string = None
    _wordlist = None

    @property
    def wordlist(self):
        """Returns the current list of words.
        
        Arguments:
        - `self`:
        """
        return self._wordlist
    
    def __init__(self, matrix_string = None):
        """Stores a word matrix.
        
        Arguments:
        - `matrix_string`:
        """
        self._matrix_string = matrix_string
        self._wordlist = []
        if isinstance(matrix_string, str) or isinstance(matrix_string, unicode):
            self.find_words()

    def find_words(self):
        """Finds all the words in the matrix (does not validate them),
        and stores them in the word list.
        
        Arguments:
        - `self`:
        """
        horiz_list = self._matrix_string.split('\n')
        vert_list = map(None, *horiz_list)

        get_words = lambda line: [s for s in \
                                      line.decode('utf8').strip().split() \
                                      if s != '' and len(s) > 1]
        for word in horiz_list:
            self._wordlist.extend(get_words(word))

        for word in vert_list:
            word = map(lambda x: x if x != None else ' ', word)
            self._wordlist.extend(get_words(u''.join(word)))

if __name__ == '__main__':
    simple = WordMatrix(u"word")
    vertical = WordMatrix(\
u"""w
o
r
d""")
    _complex = WordMatrix(\
u"""   u      
   n      
train     
   t      
   at     
 veritable
   dead   
     odd  """)
    _uneven = WordMatrix(\
u"""   u
   n
train
   t
   at
 veritable
   dead
     odd""")


    def print_list(str_list):
        for word in str_list:
            print word

    print "Simple case:"
    print_list(simple.wordlist)
    print "Vertical case:"
    print_list(vertical.wordlist)
    print "Complex case:"
    print_list(_complex.wordlist)
    print "Complex 2 case (uneven):"
    print_list(_uneven.wordlist)
