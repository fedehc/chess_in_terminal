# Libraries:
import time

# Constants:
WHITES = "white"
BLACKS = "black"
WHITE = "w"
BLACK = "b"

KING = "King"
QUEEN = "Queen"
ROOK = "Rook"
BISHOP = "Bishop"
KNIGHT = "Knight"
PAWN = "Pawn"

PIECES_COLORS = (WHITE, BLACK)
PIECES_TYPES = (KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN)
PIECES_CODE = {KING: 'K', QUEEN: 'Q', ROOK: 'R', BISHOP: 'B', KNIGHT: 'N', PAWN: 'P'}
PIECES_NAMES = {'K': KING, 'Q': QUEEN, 'R': ROOK, 'B': BISHOP, 'N': KNIGHT, 'P': PAWN}
ROWS = (1, 2, 3, 4, 5, 6, 7, 8)
COLUMNS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
COL_NUMBER_IN_ARRAY = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

# Classes:
class ChessPlayer():
  def __init__(self, name, color):
    self.name = name
    self.color = color


class ChessBoard():
  def __init__(self):
    self.squares = [[f"{fil+1}{col}" for col in COLUMNS]
                                      for fil in range(8)]
    self.movements = 0

  def reset_chess_pieces(self):
    '''Method that sets up the chess pieces with the initial chess positions to start a game.'''

    # Blacks:
    self.squares[0][0] += PIECES_CODE[ROOK] + BLACK
    self.squares[0][1] += PIECES_CODE[KNIGHT] + BLACK
    self.squares[0][2] += PIECES_CODE[BISHOP] + BLACK
    self.squares[0][3] += PIECES_CODE[KING] + BLACK
    self.squares[0][4] += PIECES_CODE[QUEEN] + BLACK
    self.squares[0][5] += PIECES_CODE[BISHOP] + BLACK
    self.squares[0][6] += PIECES_CODE[KNIGHT] + BLACK
    self.squares[0][7] += PIECES_CODE[ROOK] + BLACK

    for pos, _ in enumerate(self.squares[1]):
      self.squares[1][pos] += PIECES_CODE[PAWN] + BLACK

    # Whites:
    self.squares[6][0] += PIECES_CODE[ROOK] + WHITE
    self.squares[6][1] += PIECES_CODE[KNIGHT] + WHITE
    self.squares[6][2] += PIECES_CODE[BISHOP] + WHITE
    self.squares[6][3] += PIECES_CODE[KING] + WHITE
    self.squares[6][4] += PIECES_CODE[QUEEN] + WHITE
    self.squares[6][5] += PIECES_CODE[BISHOP] + WHITE
    self.squares[6][6] += PIECES_CODE[KNIGHT] + WHITE
    self.squares[6][7] += PIECES_CODE[ROOK] + WHITE

    for pos, _ in enumerate(self.squares[7]):
      self.squares[7][pos] += PIECES_CODE[PAWN] + WHITE

  def move_piece(self, origin, destiny):
    '''Method that moves a piece from its origin square to its destination square, according to the values passed as arguments.
    The method checks if the arguments are correct and then calls other methods to check if the move is valid and, if it is, call another method to change it'''
    status = None
    message = None

    # Checking received arguments:
    if origin[0] not in ROWS and origin[1] not in COLUMNS:
      raise ValueError("An invalid starting position was received as an argument in ChessBoard.move_piece() method.")

    if destiny[0] not in ROWS and destiny[1] not in COLUMNS:
      raise ValueError("An invalid end position was received as an argument in ChessBoard.move_piece() method.")

    # If the movement is legal, change it. Otherwise do nothing.
    # In both cases it ends by returning status boolean and a message.:
    status, message = self._check_move(origin, destiny)
    if status:
      self._change_piece_position(origin, destiny)
      self.movements += 1

    return status, message

  def show_pieces(self):
    '''Method that prints on screen the current chess pieces in their current positions.'''
    print()
    for rows in self.squares:
      print(rows)
    print()

  def _check_move(self, origin, destiny):
    '''Method that checks if the desired movement of a chess piece is legal. It receives 2 arguments, one with the origin of a piece and the other with its destiny.
    Calls other methods to check if the move or attack is legal. Returns tuple of data according to the case.'''
    status = None
    message = None
    origin_square = ""
    destiny_square = ""

    # Converting the origin and destiny positions to numerical values to be able to search in array:
    row_origin = int(origin[0])-1
    col_origin = COL_NUMBER_IN_ARRAY[origin[1]]
    row_destiny = int(destiny[0])-1
    col_destiny = COL_NUMBER_IN_ARRAY[destiny[1]]

    # 1a) Checking if there are any square in origin:
    origin_square = self._check_if_square_exist(row_origin, col_origin)
    if not origin_square:
      status = False
      message = "The origin square is invalid or doesn't exist."

    if origin_square:
      # 1b) Checking if there are any square in destiny:
      destiny_square = self._check_if_square_exist(row_destiny, col_destiny)
      if not destiny_square:
        status = False
        message = "The destiny square is invalid or doesn't exist."

    if origin_square and destiny_square:
      # 2a) Checking if there is piece in origin square:
      if len(origin_square) > 2:
        piece_origin = origin_square[2] # The 3rd character of the string represents the name of the piece.

        # 3a) Checking whether the piece can make a legal move:
        if len(destiny_square) == 2:
          if self._check_if_move_is_legal(origin_square, destiny_square):
            status = True
            message = f"Moving {PIECES_NAMES[piece_origin]} from {origin_square[:2]} " \
                    + f"to {destiny_square}."
          else:
            status = False
            message = "This movement is not legal for this piece."

        # 2b) Checking if it is possible to attack an enemy piece in destiny:
        elif len(destiny_square) > 2:
          piece_destiny = destiny_square[2] # The 3rd character of the string represents the name of the piece.

          # 3b) Checking if the piece can perform a legal attack:
          if self._check_if_attack_is_legal(origin_square, destiny_square):
            status = True
            message = f"Atacando con {PIECES_NAMES[piece_origin]} en {origin_square[:2]} " \
                      f"a {PIECES_NAMES[piece_destiny]} en {destiny_square[:2]}."
          else:
            status = False
            message = "This attack is not legal for this piece."

        else:
          status = False
          message = "Unknown error."

      # 2b) If there is no piece at origin, set the corresponding status and message:
      elif len(origin_square) == 2:
        status = False
        message = f"No piece was found in the square {origin_square}."

    return status, message

  def _check_if_square_exist(self, row, column):
    '''Method that checks if there is a square in a row and column received by arguments. Returns boolean according to the case.'''
    square = ""

    try:
      square = self.squares[row][column]
    except TypeError as error:
      # print(f"\n### ERROR: {error} ###")
      pass
    finally:
      # print(f"\n### square: {square} | row: {row} | column: {column} ###")
      return square

  def _check_if_move_is_legal(self, origin, destiny):
    '''Method that checks if the movement of a piece is legal. It receives 2 arguments, one with the origin of a chess piece and the other with its destiny. Returns boolean according to the case.'''
    status = None
    piece_origin = origin[2]  # The 3rd character of the string represents the name of the piece.
    pos_origin = origin[0:2]
    pos_destiny = destiny[0:2]

    return True

  def _check_if_attack_is_legal(self, origin, destiny):
    '''Method that checks if the attack of a piece is legal. It receives 2 arguments, one with the origin of a chess piece and the other with its destiny. Returns boolean according to the case.'''
    status = None
    piece_origin = origin[2]    # The 3rd character of the string represents the name of the piece.
    piece_destiny = destiny[2]  # Idem above.
    pos_destiny = destiny[0:2]

    return True

  def _change_piece_position(self, origin, destiny):
    '''Method that moves a chess piece from its current position. It receives 2 arguments, one with the origin of a chess piece and the other with its destiny.
    This method only modifies values of an internal array of arrays.'''
    piece = origin[2:]  # 3rd and 4th characters represent piece and color.

    row_origin = int(origin[0]) - 1    # Subtract 1 because array starts from zero.
    col_origin = COL_NUMBER_IN_ARRAY[origin[1]]
    row_destiny = int(destiny[0]) - 1  # Subtract 1 because array starts from zero.
    col_destiny = COL_NUMBER_IN_ARRAY[destiny[1]]
    # print(f"\n### piece:{piece} | row_origin:{row_origin} | col_origin:{col_origin} | row_destiny:{row_destiny} | col_destiny:{col_destiny} ###\n")

    # Putting the piece in the destination square:
    self.squares[row_destiny][col_destiny] += piece

    # Removing piece in origin square (removing piece and color strings):
    self.squares[row_origin][col_origin] = self.squares[row_origin][col_origin][0:2]


class ChessGame():
  def __init__(self):
    self.board = ChessBoard()
    self.turn_times = []
    self.player_turn = WHITES

  def start(self):
    '''Method that starts a chess game, resetting the board, taking initial time and displaying the board with its pieces on terminal/screen.'''
    self.board.reset_chess_pieces()
    self.turn_times.append(time.time())
    self.show_pieces()

  def show_pieces(self):
    '''Method that displays a title followed by a call to another method to display the chessboard pieces.'''
    # Titles:
    if self.board.movements > 0:
      self._show_title(f"\n{self.board.movements}) {self.player_turn.title()}'s moving:")
    else:
      self._show_title(f"\n{self.board.movements}) Starting new game.")

    # Showing pieces on board:
    self.board.show_pieces()

  def move_piece(self, origin, destiny):
    '''Method that moves a part from its origin to its destination, both received by argument.'''
    # Checking that only row and column are in the received origin:
    if len(origin) > 2:
      origin = origin[:2]
    # Getting the existing piece in square and add it to origin:
    row_origin = int(origin[0]) - 1   # Subtract 1 because array starts from zero.
    col_origin = COL_NUMBER_IN_ARRAY[origin[1]]
    origin = self.board.squares[row_origin][col_origin]

    # Mover, mostrar y terminar turno:
    self.board.move_piece(origin, destiny)
    self.show_pieces()
    self._finish_turn()

  def _finish_turn(self):
    '''Method that displays end turn title, assigns new turn for the other player and records the last game time in array.'''
    self._show_title(f"{self.player_turn.title()}'s end of turn.")

    if self.player_turn == WHITES:
      self.player_turn = BLACKS
    else:
      self.player_turn = WHITES

    self.turn_times.append(time.time())
    time.sleep(2)

  def _show_title(self, text):
    '''Simple method to display a text received by argument to screen/terminal.'''
    print(f"{text}")


if __name__ == "__main__":
  chess_game = ChessGame()
  chess_game.start()

  chess_game.move_piece("7a", "6a")
  #chess_game.move_piece("7b", "5b")
  #chess_game.move_piece("7c", "6c")
