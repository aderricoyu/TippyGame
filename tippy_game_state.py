from game_state import GameState
from tippy_move import TippyMove
from copy import deepcopy


class TippyGameState(GameState):
    '''
    The state of a Tippy Game.

    '''
    # assign class constants
    WIN, LOSE, DRAW = 1.0, -1.0, 0.0

    def __init__(self, p, board=None, interactive=False):
        '''(TippyGameState, str, list of list of str, bool) -> NoneType

        Initialize TippyGameState self with board, an nxn matrix.

        Assume: n >= 3
              p is in {'p1', 'p2'}
        '''
        if interactive:
            n = int(input('Choose an n for size of nxn board:'))
            board = matrix(n)
        GameState.__init__(self, p)
        self.board = board
        if is_tippy_X(self.board) is True or is_tippy_O(self.board) is True:
            self.over = True
        self.instructions = ('You may place your assigned value anywhere'
                            'along the grid, but the goal is to get any'
                            'rotated combination of a tippy, which'
                            'corresponds to green Z and red S tetriminos.'
                            'See link:'
                'http://en.wikipedia.org/wiki/Tetromino#One-sided_tetrominoes')

    def __repr__(self):
        ''' (TippyGameState) -> str

        Return a string representation of TippyGameState self
        that evaluates to an equivalent TippyGameState

        >>> board = matrix(3)
        >>> t = TippyGameState('p1', board)
        >>> t
        TippyGameState('p1', [['_', '_', '_'], ['_', '_', '_'], \
['_', '_', '_']], False)
        '''
        return 'TippyGameState({}, {}, False)'.format(repr(self.next_player),
                                                      repr(self.board))

    def __str__(self):
        ''' (TippyGameState) -> str

        Return a convenient string representation of TippyGameState (self).

        '''
        a = ''
        for row in self.board:
            a = a + str(' '.join(row)) + '\n'
        return ('New board:\n{}and next player: {}'.format(str(a), 
                                                        str(self.next_player)))

    def __eq__(self, other):
        ''' (TippyGameState, object) -> bool

        Return True iff this TippyGameState is the equivalent to other.

        >>> board = matrix(3)
        >>> t1 = TippyGameState('p1', board)
        >>> t2 = TippyGameState('p1', board)
        >>> t1 == t2
        True
        '''
        return (isinstance(other, TippyGameState) and
                self.board == other.board and 
                self.next_player == other.next_player)

    def get_move(self):
        '''(TippyGameState) -> TippyMove

        Prompt user and return a move.
        '''
        return TippyMove(int(input('pick a row between 0 and n-1: ')), 
                         int(input('pick a column between 0 and n-1: ')))

    def apply_move(self, move):
        '''(TippyGameState, TippyMove) -> TippyGameState

        Return the new game state reached by applying move to
        state self, or None if the move is illegal.

        >>> board = matrix(3)
        >>> t1 = TippyGameState('p1', board)
        >>> t2 = t1.apply_move(TippyMove(1, 1))
        >>> print(t2)
        New board:
        _ _ _
        _ X _
        _ _ _
        and next player: p2
        '''
        new_board = deepcopy(self.board)
        if move in self.possible_next_moves():
            if self.next_player == 'p1':
                new_board[move.i][move.j] = 'X'
            elif self.next_player == 'p2':
                new_board[move.i][move.j] = 'O'
            return TippyGameState(self.opponent(), board=new_board)
        else:
            return None

    def rough_outcome(self):
        '''(TippyGameState) -> float

        Return estimate of outcome based only on current state. Value
        is in interval [LOSE, WIN]

        >>>
        '''
        if player == 'p1' and is_rough_tippy_X(self.board):
            return True
        elif player == 'p2' and is_rough_tippy_O(self.board):
            return True
        else:
            return False

    def winner(self, player):
        ''' (TippyGameState, str) -> bool

        Return whether player has won the game.

        Assume: player is either 'p1' or 'p2'
                and there are no more legal moves; the game is over

        >>> board = matrix(4)
        >>> t = TippyGameState('p1', board)
        >>> a = t.apply_move(TippyMove(1, 1))  # p1's move
        >>> b = a.apply_move(TippyMove(3, 1))   # p2's move
        >>> c = b.apply_move(TippyMove(1, 2))    # p1's move
        >>> d = c.apply_move(TippyMove(3, 3))     # p2's move
        >>> e = d.apply_move(TippyMove(2, 2))      # p1's move
        >>> f = e.apply_move(TippyMove(3, 2))       # p2's move
        >>> g = f.apply_move(TippyMove(2, 3))        # p1's move
        >>> g.winner('p1')
        True
        '''
        if player == 'p1' and is_tippy_X(self.board):
            return True
        elif player == 'p2' and is_tippy_O(self.board):
            return True
        else:
            return False


    def possible_next_moves(self):
        ''' (TippyGameState) -> list of TippyMove

        Return a (possibly empty) list of moves that are legal
        from the present state.

        >>> board = matrix(3)
        >>> t1 = TippyGameState('p1', board)
        >>> L1 = t1.possible_next_moves()
        >>> L2 = [TippyMove(0, 0), TippyMove(0, 1), TippyMove(0, 2), \
          TippyMove(1, 0), TippyMove(1, 1), TippyMove(1, 2), TippyMove(2, 0), \
          TippyMove(2, 1), TippyMove(2, 2)]
        >>> (len(L1) == len(L2))
        True
        >>> (all([m in L2 for m in L1]))
        True
        '''
        return [TippyMove(i, j)
                for i in range(len(self.board))
                for j in range(len(self.board))
                if self.board[i][j] == '_']


# Helper Functions:

def matrix(n):
    ''' (int) -> list of list of str

    Return an nxn matrix containing n nested lists and n empty strings within
    the nested list.

    >>> matrix(3)
    [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    '''
    lst = []

    for i in range(n):
        lst.append(['_'] * n)

    return lst


def is_tippy_X(t1):
    ''' (list of list of str) -> bool

    Return True if a tippy has been found from a player who uses 'X' within the
    rows and columns of the matrix. A tippy corresponds to any combination of
    the green Z and red S tetrominos. See link:
    http://en.wikipedia.org/wiki/Tetromino#One-sided_tetrominoes

    Precondition1: t1 must be a matrix of form matrix(n).

    >>> t1 = [['X', 'X', '_'], ['_', 'X', 'X'], ['_', '_', '_']]
    >>> is_tippy_X(t1)
    True
    >>> t1 = [['X', 'X', '_'], ['X', 'X', '_'], ['_', '_', '_']]
    >>> is_tippy_X(t1)
    False
    '''
    for i in range(len(t1)):
        for j in range(len(t1)):
            if (i + 2 < len(t1) and j - 1 >= 0 and t1[i][j] == 'X' and 
                t1[i + 1][j] == 'X' and t1[i + 1][j - 1] == 'X' and 
                t1[i + 2][j - 1] == 'X'):
                return True
            elif (i + 2 < len(t1) and j + 1 < len(t1) and t1[i][j] == 'X' and 
                  t1[i + 1][j] == 'X' and t1[i + 1][j + 1] == 'X' and 
                  t1[i + 2][j + 1] == 'X'):
                return True
            elif (i - 1 >= 0 and j + 2 < len(t1) and t1[i][j] == 'X' and 
                  t1[i][j + 1] == 'X' and t1[i - 1][j + 1] == 'X' and 
                  t1[i - 1][j + 2] == 'X'):
                return True
            elif (i + 1 < len(t1) and j + 2 < len(t1) and t1[i][j] == 'X' and 
                  t1[i][j + 1] == 'X' and t1[i + 1][j + 1] == 'X' and 
                  t1[i + 1][j + 2] == 'X'):
                return True

    return False


def is_tippy_O(t2):
    ''' (list of list of str) -> bool

    Return True if a tippy has been found from a player who uses 'O' within the
    rows and columns of the matrix. A tippy corresponds to any combination of
    the green Z and red S tetrominos. See link:
    http://en.wikipedia.org/wiki/Tetromino#One-sided_tetrominoes

    Precondition1: t2 must be a matrix of form matrix(n).

    >>> t2 = [['O', 'O', '_'], ['_', 'O', 'O'], ['_', '_', '_']]
    >>> is_tippy_O(t2)
    True
    >>> t2 = [['O', 'O', '_'], ['O', '_', 'O'], ['_', '_', '_']]
    >>> is_tippy_O(t2)
    False
    '''
    for i in range(len(t2)):
        for j in range(len(t2)):
            if (i + 2 < len(t2) and j - 1 >= 0 and t2[i][j] == 'O' and
                  t2[i + 1][j] == 'O' and t2[i + 1][j - 1] == 'O' and 
                  t2[i + 2][j - 1] == 'O'):
                return True
            elif (i + 2 < len(t2) and j + 1 < len(t2) and t2[i][j] == 'O' and 
                  t2[i + 1][j] == 'O' and t2[i + 1][j + 1] == 'O' and 
                  t2[i + 2][j + 1] == 'O'):
                return True
            elif (i - 1 >= 0 and j + 2 < len(t2) and t2[i][j] == 'O' and 
                  t2[i][j + 1] == 'O' and t2[i - 1][j + 1] == 'O' and 
                  t2[i - 1][j + 2] == 'O'):
                return True
            elif (i + 1 < len(t2) and j + 2 < len(t2) and t2[i][j] == 'O' and 
                  t2[i][j + 1] == 'O' and t2[i + 1][j + 1] == 'O' and 
                  t2[i + 1][j + 2] == 'O'):
                return True

    return False


def is_rough_tippy_X(t1):
    ''' (list of list of str) -> bool

    Return True if a rough tippy has been found from a player who uses 'X' 
    within the rows and columns of the matrix. A tippy corresponds to any 
    combination of the green Z and red S tetrominos. See link:
    http://en.wikipedia.org/wiki/Tetromino#One-sided_tetrominoes

    Precondition1: t1 must be a matrix of form matrix(n).

    >>> t1 = [['X', 'X', '_'], ['_', 'X', '_'], ['_', '_', '_']]
    >>> is_rough_tippy_X(t1)
    True
    >>> t1 = [['X', 'X', '_'], ['X', 'X', '_'], ['_', '_', '_']]
    >>> is_rough_tippy_X(t1)
    True
    '''
    for i in range(len(t1)):
        for j in range(len(t1)):
            if (i + 2 < len(t1) and j - 1 >= 0 and t1[i][j] == 'X' and 
                t1[i + 1][j] == 'X' and t1[i + 1][j - 1] == 'X' and 
                t1[i + 2][j - 1] == '_'):
                return True
            elif (i + 2 < len(t1) and j + 1 < len(t1) and t1[i][j] == 'X' and 
                  t1[i + 1][j] == 'X' and t1[i + 1][j + 1] == 'X' and 
                  t1[i + 2][j + 1] == '_'):
                return True
            elif (i - 1 >= 0 and j + 2 < len(t1) and t1[i][j] == 'X' and 
                  t1[i][j + 1] == 'X' and t1[i - 1][j + 1] == 'X' and 
                  t1[i - 1][j + 2] == '_'):
                return True
            elif (i + 1 < len(t1) and j + 2 < len(t1) and t1[i][j] == 'X' and 
                  t1[i][j + 1] == 'X' and t1[i + 1][j + 1] == 'X' and 
                  t1[i + 1][j + 2] == '_'):
                return True

    return False


def is_rough_tippy_O(t2):
    ''' (list of list of str) -> bool

    Return True if a rough tippy has been found from a player who uses 'O' 
    within the rows and columns of the matrix. A tippy corresponds to any 
    combination of the green Z and red S tetrominos. See link:
    http://en.wikipedia.org/wiki/Tetromino#One-sided_tetrominoes

    Precondition1: t2 must be a matrix of form matrix(n).

    >>> t2 = [['O', 'O', '_'], ['_', 'O', '_'], ['_', '_', '_']]
    >>> is_rough_tippy_O(t2)
    True
    >>> t2 = [['O', 'O', '_'], ['O', '_', 'O'], ['_', '_', '_']]
    >>> is_rough_tippy_O(t2)
    False
    '''
    for i in range(len(t2)):
        for j in range(len(t2)):
            if (i + 2 < len(t2) and j - 1 >= 0 and t2[i][j] == 'O' and 
                  t2[i + 1][j] == 'O' and t2[i + 1][j - 1] == 'O' and 
                  t2[i + 2][j - 1] == '_'):
                return True
            elif (i + 2 < len(t2) and j + 1 < len(t2) and t2[i][j] == 'O' and 
                  t2[i + 1][j] == 'O' and t2[i + 1][j + 1] == 'O' and 
                  t2[i + 2][j + 1] == '_'):
                return True
            elif (i - 1 >= 0 and j + 2 < len(t2) and t2[i][j] == 'O' and 
                  t2[i][j + 1] == 'O' and t2[i - 1][j + 1] == 'O' and 
                  t2[i - 1][j + 2] == '_'):
                return True
            elif (i + 1 < len(t2) and j + 2 < len(t2) and t2[i][j] == 'O' and 
                  t2[i][j + 1] == 'O' and t2[i + 1][j + 1] == 'O' and 
                  t2[i + 1][j + 2] == '_'):
                return True

    return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()




