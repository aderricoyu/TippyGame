from move import Move


class TippyMove(Move):
    ''' A move in the game of Tippy.

    position -- the position your letter will be on the board.
    '''

    def __init__(self, i, j):
        ''' (TippyMove, int, int) -> NoneType

        Initialize a TippyMove for inserting a value 'X' or 'O'.

        Assume: i -- row starting at 0 to n-1
                j -- column starting at 0 to n-1
        '''
        self.i = i
        self.j = j
       
    def __repr__(self):
        ''' (TippyMove) -> str

        Return a string representation of this TippyMove.
        >>> m1 = TippyMove(1, 1)
        >>> m1
        TippyMove(1, 1)
        '''
        return 'TippyMove({}, {})'.format(str(self.i), str(self.j)) 
                                              
    def __str__(self):
        ''' (TippyMove) -> str

        Return a string representation of this TippyMove
        that is suitable for users to read.

        >>> m1 = TippyMove(0, 0)
        >>> print(m1)
        Insert letter at row 0, column 0
        '''

        return 'Insert letter at row {}, column {}'.format(str(self.i), 
                                                           str(self.j))

    def __eq__(self, other):
        ''' (TippyMove, TippyMove) -> bool

        Return True iff this TippyMove is the same as other.

        >>> m1 = TippyMove(1, 1)
        >>> m2 = TippyMove(1, 2)
        >>> print(m1 == m2)
        False
        '''
        return (isinstance(other, TippyMove) and self.i == other.i and 
                self.j == other.j)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
