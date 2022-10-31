# Standard libraries:
import time

# 3° libraries:
from rich.console import Console
from rich.table import Table
from rich import box


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
class ChessPlayers():
  '''The class that keeps record of all players relevant data.'''
  def __init__(self, name1="Player 1", color1=WHITES, name2="Player 2"):
    self.history = []
    self.turn = WHITES

    # Player 1:
    self.player_1_name = name1
    self.player_1_color = color1

    # Player 2:
    self.player_2_name = name2
    if self.player_1_color == WHITES:
      player_2_color = BLACKS
    else:
      self.player_2_color = WHITES


class ChessBoard():
  '''The class that keeps track of all the pieces and allows their movements.'''
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
    for pos, _ in enumerate(self.squares[7]):
      self.squares[6][pos] += PIECES_CODE[PAWN] + WHITE

    self.squares[7][0] += PIECES_CODE[ROOK] + WHITE
    self.squares[7][1] += PIECES_CODE[KNIGHT] + WHITE
    self.squares[7][2] += PIECES_CODE[BISHOP] + WHITE
    self.squares[7][3] += PIECES_CODE[KING] + WHITE
    self.squares[7][4] += PIECES_CODE[QUEEN] + WHITE
    self.squares[7][5] += PIECES_CODE[BISHOP] + WHITE
    self.squares[7][6] += PIECES_CODE[KNIGHT] + WHITE
    self.squares[7][7] += PIECES_CODE[ROOK] + WHITE

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
    self.squares[row_destiny][col_destiny] = self.squares[row_destiny][col_destiny][0:2] + piece

    # Removing piece in origin square (removing piece and color strings):
    self.squares[row_origin][col_origin] = self.squares[row_origin][col_origin][0:2]


class TUI():
  '''The Text User Interface class that shows the chessboard on screen via terminal.'''
  def __init__(self):
    self.console = Console(color_system="256")

  def show_pieces(self, board, players):
    '''Method that displays a title followed by a call to another method to display the chessboard pieces.'''
    # Get all current pieces from board:
    full_board = board.squares
    table_title = ""

    # Show board and current chess pieces as a table in terminal.
    # Table title:
    if board.movements > 0:
      table_title = f"{board.movements}) {players.turn.title()}'s move:"
    else:
      table_title = f"New game:"

    # Table:
    table = Table(title=table_title, show_header=True, show_lines=True, box=box.ROUNDED)

    style = "italic not bold grey3"
    # Set 9 columns (8 plus 1 for board letters):
    table.add_column(f"[{style}]a[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]b[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]c[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]d[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]e[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]f[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]g[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]h[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(" ", justify="center", style="italic grey11", no_wrap=True)

    # Set the 8 rows with the current pieces:
    for row_number, row_board in enumerate(full_board, 1):
      row_board = self._format_square_according_to_color_piece(row_board)
      row_board.append(str(ROWS[row_number-1]))
      table.add_row(*row_board)   # Passing as strings (not full list).

    # Show table in terminal:
    print()
    self.console.print(table)

  def _format_square_according_to_color_piece(self, row):
    '''Method that receives an array argument and returns it modified according to its content.'''
    new_row = []

    for square in row:
      # If the square contains a piece and its color, style it as such (and discard the rest):
      if len(square) == 4:
        if square[-1] == WHITE:
          new_row.append(f"[black on white][{square[2]}][/black on white]")
        else:
          new_row.append(f"[white on black][{square[2]}][/white on black]")
      else:
        new_row.append("")

    return new_row


class ChessGame():
  '''The class that uses the others to run the game.'''
  def __init__(self):
    self.board = ChessBoard()
    self.players = ChessPlayers()
    self.tui = TUI()

  def start(self):
    '''Method that starts a chess game, resetting the board, taking initial time and displaying the board with its pieces on terminal/screen.'''
    self.board.reset_chess_pieces()
    self.players.history.append(["Game start", "---", time.ctime()])
    self.tui.show_pieces(self.board, self.players)
    time.sleep(1.5)

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
    self.tui.show_pieces(self.board, self.players)
    self._finish_turn(origin, destiny)

  def _finish_turn(self, origin, destiny):
    '''Method that record last move and time, and assigns new turn for the other player.'''

    # Record last player turn, last piece move and time:
    piece = PIECES_NAMES[origin[2:3].capitalize()]
    origin_square = origin[0:2]
    destiny_square = destiny[0:2]
    self.players.history.append([self.players.turn,
                                 f"{piece}: {origin_square} -> {destiny_square}",
                                 time.ctime()])

    # Change player turn:
    if self.players.turn == WHITES:
      self.players.turn = BLACKS
    else:
      self.players.turn = WHITES

    time.sleep(1.5)


if __name__ == "__main__":
  game = ChessGame()
  game.start()

  game.move_piece("7a", "6a")
  game.move_piece("2b", "4b")
  game.move_piece("7c", "5c")
  game.move_piece("4b", "5c")

  #print(f"\n{game.players.history}\n")
  #print(f"\n# 5c: {game.board.squares[4][2]}\n")
