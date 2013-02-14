"""
This will be the class for storing the words.
"""

class Coords(object):
    """
    """
    x = None
    y = None
    
    def __init__(self, x, y):
        """
        
        Arguments:
        - `x`:
        - `y`:
        """
        if not isinstance(x, int):
            raise TypeException("x is not an integer.")
        if not isinstance(y, int):
            raise TypeException("y is not an integer.")
        self.x = x
        self.y = y

    def __repr__(self):
        """
        
        Arguments:
        - `self`:
        """
        return "Coords({0}, {1})".format(self.x, self.y)

    def __str__(self):
        """
        
        Arguments:
        - `self`:
        """
        return "x = {0} ; y = {1}".format(self.x, self.y)



class SubMatrix(object):
    """
    """
    _top_left = None
    _bottom_right = None

    def __repr__(self):
        """
        
        Arguments:
        - `self`:
        """
        return "SubMatrix(tl:{0}, br:{1})".format(repr(self._top_left), repr(self._bottom_right))

    def __str__(self):
        """
        
        Arguments:
        - `self`:
        """
        return "top left: {0}\n\tbottom right: {1}".format(str(self._top_left), str(self._bottom_right))

    @property
    def top_left(self):
        """
        
        Arguments:
        - `self`:
        """
        return self._top_left

    @property
    def bottom_right(self):
        """
        
        Arguments:
        - `self`:
        """
        return self._bottom_right

    @property
    def tl(self):
        """
        
        Arguments:
        - `self`:
        """
        return self._top_left

    @property
    def br(self):
        """
        
        Arguments:
        - `self`:
        """
        return self._bottom_right
    
    def __init__(self, top_left, bottom_right):
        """
        
        Arguments:
        - `top_left`:
        - `bottom_right`:
        """
        if not isinstance(top_left, Coords):
            raise TypeException("Must be of a Coords type")
        if not isinstance(bottom_right, Coords):
            raise TypeException("Must be of a Coords type")
        self._top_left = top_left
        self._bottom_right = bottom_right
        


class WordMatrix(object):
    """The class that has the words in it like in a matrix.
    """
    _matrix_string = None
    _transposed = None
    _wordlist = None
    _submatrices = None

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
        else:
            self._transposed = self._matrix_string #this will mostly
                                                   #be used for
                                                   #testing

    def find_words(self):
        """Finds all the words in the matrix (does not validate them),
        and stores them in the word list.
        
        Arguments:
        - `self`:
        """
        horiz_list = self._matrix_string.split('\n')
        self._transposed = map(None, *horiz_list)
        vert_list = self._transposed

        get_words = lambda line: [s for s in \
                                      line.decode('utf8').strip().split() \
                                      if s != '' and len(s) > 1]
        for word in horiz_list:
            self._wordlist.extend(get_words(word))

        for word in vert_list:
            word = map(lambda x: x if x != None else ' ', word)
            self._wordlist.extend(get_words(u''.join(word)))

    def find_contiguous_blocks(self):
        """Return list of coordinates in the matrix for contiguous
        blocks of letters. Must be at least of size 2x2.

        num_of_ones(a,b,c,d) = helper_matrix[c][d] + helper_matrix[a-1][b-1] - helper_matrix[a-1][d] - helper_matrix[c][b-1]
        
        Arguments:
        - `self`:
        """
        coords_list = []

        empty = (' ', '', '0', 0, None) #zero is for testing
        def next_is_occupied(_x, _y):
            if len(self._transposed[_y]) <= _x:
                return False

            return not self._transposed[_y][_x + 1] in empty

        def below_is_occupied(_x, _y):
            if len(self._transposed) <= _y:
                return False

            return not self._transposed[_y + 1][_x] in empty


        def find_bottom_right(_x, _y):
            if next_is_occupied(_x, _y):
                return find_bottom_right(_x + 1, _y)
            elif below_is_occupied(_x, _y):
                return find_bottom_right(_x, _y + 1)

            return Coords(_x, _y)

        def is_contiguous(subm):
            """
            
            Arguments:
            - `subm`:
            """
            for _y in range(subm.tl.y + 1, subm.br.y):
                for _x in range(subm.tl.x, subm.br.x - 1):
                    if self._transposed[_y][_x] in empty:
                        return False

            return True


        x = 0
        y = 0
        for row in self._transposed:
            for col in row:
                if (not col in empty) and next_is_occupied(x, y) and \
                        below_is_occupied(x, y):
                    bottom_rt = find_bottom_right(x, y)
                    if (bottom_rt.x - x > 0) and (bottom_rt.y - y > 0):
                        subm = SubMatrix(Coords(x, y), bottom_rt)
                        if is_contiguous(subm):
                            coords_list.append(subm)
                x += 1
            x = 0
            y += 1

        self._submatrices = coords_list


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

    matrix_test = WordMatrix( [[0, 0, 0, 0, 0],
                               [0, 0, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0]] )


    def print_list(str_list):
        for word in str_list:
            print "\t" + word

    print "Simple case:"
    print_list(simple.wordlist)
    print "Vertical case:"
    print_list(vertical.wordlist)
    print "Complex case:"
    print_list(_complex.wordlist)
    print "Complex 2 case (uneven):"
    print_list(_uneven.wordlist)

    matrix_test.find_contiguous_blocks()
    print "Submatrices in matrix test:"
    for matrix in matrix_test._submatrices:
        print "\t" + repr(matrix)
