"""
This will be the class for storing the words.
"""

#this is meant to be reassigned to a function that either prints to
#the screen or to a logger, or otherwise meant to look like a
#function, but does nothing when it's not needed
matrix_logger = None

class Coords(object):
    """
    """
    x = None
    y = None
    highlight_char = None
    
    def __init__(self, x, y, highlight_char = None):
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
        self.highlight_char = highlight_char

    def __repr__(self):
        """
        
        Arguments:
        - `self`:
        """
        return u"{0}({1}, {2}, '{3}')".format(self.__class__.__name__, self.x, self.y, repr(self.highlight_char))

    def __str__(self):
        """
        
        Arguments:
        - `self`:
        """
        return u"x = {0} ; y = {1} ; highlight = '{2}'".format(self.x, self.y, self.highlight_char)

    def __eq__(self, other):
        """
        
        Arguments:
        - `self`:
        - `other`:
        """
        return self.x == other.x and self.y == other.y



class SubMatrix(object):
    """
    """
    _top_left = None
    _bottom_right = None

    def __eq__(self, other):
        """
        
        Arguments:
        - `self`:
        - `other`:
        """
        return self._top_left == other._top_left and self._bottom_right == other._bottom_right


    def __contains__(self, other):
        """
        
        Arguments:
        - `self`:
        - `other`:
        """
        if matrix_logger:
            matrix_logger(u"Checking if {0} is inside {1}".format(repr(other), repr(self)))

        if self == other:
            return True
        
        if other._top_left.x < self._top_left.x:
            return False

        if other._top_left.y < self._top_left.x:
            return False

        if other._bottom_right.x > self._bottom_right.x:
            return False

        if other._bottom_right.y > self._bottom_right.y:
            return False

        if matrix_logger:
            matrix_logger(u"\tTrue")
        return True


    def __repr__(self):
        """
        
        Arguments:
        - `self`:
        """
        return u"{0}(tl:{1}, br:{2})".format(self.__class__.__name__, repr(self._top_left), repr(self._bottom_right))

    def __str__(self):
        """
        
        Arguments:
        - `self`:
        """
        return u"top left: {0}\n\tbottom right: {1}".format(str(self._top_left), str(self._bottom_right))

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
        self._wordlist = []
        if isinstance(matrix_string, str) or isinstance(matrix_string, unicode):
            self._matrix_string = self.split_string(matrix_string)
            self.find_words()
        else:
            self._matrix_string = matrix_string

    def split_string(self, matrix_string):
        """Returns an evenly spaced matrix list of strings.
        
        Arguments:
        - `self`:
        - `matrix_string`:
        """
        uneven_matrix = matrix_string.decode('utf-8').split(u'\n')
        line_lengths = map(len, uneven_matrix)
        max_length = max(line_lengths)
        spacers = [(max_length - num_spaces) * ' ' for num_spaces in line_lengths]
        even_matrix = [line + spaces for line, spaces in zip(uneven_matrix, spacers)]
        return even_matrix


    def find_words(self):
        """Finds all the words in the matrix (does not validate them),
        and stores them in the word list.
        
        Arguments:
        - `self`:
        """
        horiz_list = self._matrix_string
        vert_list = map(None, *horiz_list)

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
        
        Arguments:
        - `self`:
        """
        submatrices = []

        empty = (' ', '', 0, None) #zero is for testing
        def print_matrix(*coords):
            if not matrix_logger:
                return

            print_string = u"\n"
            
            for _y in xrange(0, len(self._matrix_string)):
                for _x in xrange(0, len(self._matrix_string[_y])):
                    try:
                        highlight_coord = coords[coords.index(Coords(_x, _y))]
                    except ValueError:
                        highlight_coord = None
                    if highlight_coord:
                        print_string += u"\t{0}{1}".format(self._matrix_string[_y][_x], highlight_coord.highlight_char)
                    else:
                        print_string += u"\t{0}".format(self._matrix_string[_y][_x])

                print_string += u"\n"

            matrix_logger(print_string)

        def next_is_occupied(_x, _y):
            rt_arrow = u"\u21e8"
            if len(self._matrix_string[_y]) <= _x + 1:
                print_matrix(Coords(_x, _y, rt_arrow))
                return False

            print_matrix(Coords(_x, _y, rt_arrow), Coords(_x + 1, _y, "*"))
            return not self._matrix_string[_y][_x + 1] in empty

        def below_is_occupied(_x, _y):
            dn_arrow = u"\u21e9"
            if len(self._matrix_string) <= _y + 1:
                print_matrix(Coords(_x, _y, dn_arrow))
                return False

            print_matrix(Coords(_x, _y, dn_arrow), Coords(_x, _y + 1, "*"))
            return not self._matrix_string[_y + 1][_x] in empty


        def find_bottom_right(_x, _y, xstop = 100, ystop = 100, level = 0):
            if matrix_logger:
                matrix_logger("Trying to find submatrix, level {0}, xstop {1}, ystop {2}:".format(level, xstop, ystop))
                print_matrix(Coords(_x, _y, "@"))
            if _x <= xstop and next_is_occupied(_x, _y):
                return find_bottom_right(_x + 1, _y, xstop = xstop,
                                         ystop = ystop, level = level + 1)
            else:
                xstop = xstop if xstop <= _x else _x - 1
                
            if _y <= ystop and below_is_occupied(_x, _y):
                return find_bottom_right(_x, _y + 1, xstop = xstop,
                                         ystop = ystop, level = level + 1)

            if matrix_logger:
                matrix_logger("Found bottom right, x={0}, y={1}, level {2}:".format(_x, _y, level))
                print_matrix(Coords(_x, _y, "$"))
            return Coords(_x, _y)

        def is_contiguous(subm):
            if matrix_logger:
                matrix_logger("Checking for contiguousness:")

            top_left = subm.tl
            bottom_rt = subm.br
            top_left.highlight_char = u"\u21e8"
            bottom_rt.highlight_char = u"\u21e7"
            coords = [top_left, bottom_rt]
            _yrange = xrange(top_left.y + 1, bottom_rt.y + 1) if (bottom_rt.y - top_left.y > 1) else [bottom_rt.y]
            _xrange = xrange(top_left.x, bottom_rt.x) if (bottom_rt.x - top_left.x > 1) else [top_left.x]
            for _y in _yrange:
                for _x in _xrange:
                    if self._matrix_string[_y][_x] in empty:
                        if matrix_logger:
                            matrix_logger("\tNot contiguous")
                            coords.append(Coords(_x, _y, "!"))
                            print_matrix(*coords)
                        return False
                    coords.append(Coords(_x, _y, "+"))
                    
            if matrix_logger:
                print_matrix(*coords)
                matrix_logger("\tIs  contiguous")
            return True

        def add_submatrix(current_coords, bottom_right):
            subm = SubMatrix(current_coords, bottom_right)
            is_sub_submatrix = False
            for _subm in submatrices:
                if subm in _subm:
                    is_sub_submatrix = True
                    break
            if (not is_sub_submatrix) and is_contiguous(subm):
                submatrices.append(subm)

        x = 0
        y = 0
        for row in self._matrix_string:
            for col in row:
                if matrix_logger:
                    matrix_logger("Current position:")
                    print_matrix(Coords(x, y, "^"))
                if (not col in empty) and next_is_occupied(x, y) and \
                        below_is_occupied(x, y):
                    bottom_rt = find_bottom_right(x, y)
                    current_coords = Coords(x, y)
                    if (bottom_rt.x - x > 0) and (bottom_rt.y - y > 0):
                        add_submatrix(current_coords, bottom_rt)
                    stop_x = x
                    for _x in reversed(xrange(x, bottom_rt.x - 1)):
                        for _y in reversed(xrange(y, bottom_rt.y + 1)):
                            br_iter = find_bottom_right(_x, y, xstop = _x, ystop = _y)
                            if br_iter.y - y > 0 and br_iter.x - x > 0:
                                add_submatrix(current_coords, br_iter)                                
                x += 1
            x = 0
            y += 1

        self._submatrices = submatrices

#all unit testing is being done here
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    def log_fn(mesg):
        """
        
        Arguments:
        - `mesg`:
        """
        logging.debug(mesg)

    matrix_logger = log_fn

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

    matrix_test_single = WordMatrix( [[0, 0, 0, 0, 0],
                                      [0, 1, 1, 1, 0],
                                      [0, 1, 1, 1, 0],
                                      [0, 1, 1, 1, 0],
                                      [0, 0, 0, 0, 0]] )

    matrix_test_2 = WordMatrix( [[0, 0, 0, 0, 0],
                                 [0, 1, 1, 1, 1],
                                 [0, 1, 1, 1, 1],
                                 [0, 1, 1, 1, 1],
                                 [0, 1, 1, 1, 0]] )

    matrix_test_fail = WordMatrix( [[0, 0, 0, 0, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 1, 0, 1, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 0, 0, 0, 0]] )

    matrix_stair_case = WordMatrix( [[0, 0, 0, 0, 0],
                                     [0, 1, 1, 1, 1],
                                     [0, 1, 1, 1, 0],
                                     [0, 1, 1, 0, 0],
                                     [0, 1, 0, 0, 0],
                                     [0, 0, 0, 0, 0]] )

    matrix_col_test = WordMatrix( [[1, 1, 0, 0, 0],
                                   [1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 1]] )


    def print_list(str_list):
        for word in str_list:
            print u"\t" + word

    def find_and_print_matrices(wm):
        """
        
        Arguments:
        - `wm`:
        """
        wm.find_contiguous_blocks()
        for matrix in wm._submatrices:
            print u"\t" + repr(matrix)

    print "Simple case (no matrices):"
    print_list(simple.wordlist)
    find_and_print_matrices(simple)
    print "Vertical case (no matrices):"
    print_list(vertical.wordlist)
    find_and_print_matrices(vertical)
    print "Complex case (3 matrices):"
    print_list(_complex.wordlist)
    find_and_print_matrices(_complex)
    print "Complex 2 case (uneven) (3 matrices):"
    print_list(_uneven.wordlist)
    find_and_print_matrices(_uneven)

    print "Two submatrices in matrix test:"
    find_and_print_matrices(matrix_test)

    print "Single submatrix test:"
    find_and_print_matrices(matrix_test_single)

    print "Two submatrix test with the same top left:"
    find_and_print_matrices(matrix_test_2)

    print "There should be no submatrices here:"
    find_and_print_matrices(matrix_test_fail)

    print "Stair case test, two submatrices with the same top left:"
    find_and_print_matrices(matrix_stair_case)

    print "Column test, there should be three submatrces:"
    find_and_print_matrices(matrix_col_test)
