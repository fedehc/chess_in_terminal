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

ROW = "Row"
COLUMN = "Column"
DIAGONAL = "Diagonal"


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
      self.player_2_color = BLACKS
    else:
      self.player_2_color = WHITES


class ChessRules():
  '''The class that contains the rules with all the legal moves of the pieces within the board..'''
  def __init__(self):
    pass

  def check_move(self, source, destination):
    '''Method that checks if the move of a piece is legal. It receives 2 arguments, one with the source of a chess piece and the other with its destination. Returns a boolean according to the case.'''
    # print(f"### source:{source} | destination:{destination} ###")
    can_move = None
    # Get piece name from pierce source:
    piece_name = PIECES_NAMES[source[2]]

    # Creating dict for passing to methods below:
    move_data_dict = {
      "row_source": int(source[0]),
      "col_source": COL_NUMBER_IN_ARRAY[source[1]]+1, # Add 1 because columms starts from 0.
      "piece_source": source[2],
      "piece_color": source[3],
      "row_destination": int(destination[0]),
      "col_destination": COL_NUMBER_IN_ARRAY[destination[1]]+1  # Add 1 because columms starts from 0.
    }

    # Call the appropiate method:
    if piece_name == KING:
      can_move = self._king_move(move_data_dict)
    elif piece_name == QUEEN:
      can_move = self._queen_move(move_data_dict)
    elif piece_name == ROOK:
      can_move = self._rook_move(move_data_dict)
    elif piece_name == BISHOP:
      can_move = self._bishop_move(move_data_dict)
    elif piece_name == KNIGHT:
      can_move = self._knight_move(move_data_dict)
    elif piece_name == PAWN:
      can_move = self._pawn_move(move_data_dict)
    else:
      raise ValueError("Invalid piece_name inside check_move method in ChessRules class.")

    return can_move

  def check_attack(self, source, destination):
    '''Method that checks if the attack of a piece is legal. It receives 2 arguments, one with the source of a chess piece and the other with its destination. Returns a boolean according to the case.'''
    # print(f"### source:{source} | destination:{destination} ###")
    can_attack = True
    # Get piece name from pierce source:
    piece_name_source = PIECES_NAMES[source[2]]

    # Creating dict for passing to methods below:
    attack_data_dict = {
      "row_source": int(source[0]),
      "col_source": COL_NUMBER_IN_ARRAY[source[1]]+1, # Add 1 because columms starts from 0.
      "piece_source": source[2],
      "source_color": source[3],
      "row_destination": int(destination[0]),
      "col_destination": COL_NUMBER_IN_ARRAY[destination[1]]+1  # Add 1 because columms starts from 0.
    }

    # Call the appropiate method:
    if piece_name_source == KING:
      can_attack = self._king_attack(attack_data_dict)
    elif piece_name_source == QUEEN:
      can_attack = self._queen_attack(attack_data_dict)
    elif piece_name_source == ROOK:
      can_attack = self._rook_attack(attack_data_dict)
    elif piece_name_source == BISHOP:
      can_attack = self._bishop_attack(attack_data_dict)
    elif piece_name_source == KNIGHT:
      can_attack = self._knight_attack(attack_data_dict)
    elif piece_name_source == PAWN:
      can_attack = self._pawn_attack(attack_data_dict)
    else:
      raise ValueError("Invalid piece_name_source inside check_attack in ChessRules class.")

    return can_attack

  def check_any_pieces_between(self, source, destinantion):
    '''Method that checks if there is any pieces in a line (row, column, diagonal). It receives origin and destination string arguments and returns a boolean according to the case.'''
    piece_found = None

    return piece_found

  def _king_move(self, move_data_dict):
    '''Method that check if the current move is valid for the king. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_move = True

    return valid_move

  def _king_attack(self, attack_data_dict):
    '''Method that check if current attack is valid for the king. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_attack = True

    return valid_attack

  def _queen_move(self, move_data_dict):
    '''Method that check if the current move is valid for the queen. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_move = True

    return valid_move

  def _queen_attack(self, attack_data_dict):
    '''Method that check if current attack is valid for the queen. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_attack = True

    return valid_attack

  def _rook_move(self, move_data_dict):
    '''Method that check if the current move is valid for the rook. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_move = True

    return valid_move

  def _rook_attack(self, attack_data_dict):
    '''Method that check if current attack is valid for the rook. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_attack = True

    return valid_attack

  def _bishop_move(self, move_data_dict):
    '''Method that check if the current move is valid for the bishop. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_move = True

    return valid_move

  def _bishop_attack(self, attack_data_dict):
    '''Method that check if current attack is valid for the bishop. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_attack = True

    return valid_attack

  def _knight_move(self, move_data_dict):
    '''Method that check if the current move is valid for the knight. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_move = True

    return valid_move

  def _knight_attack(attack_data_dict):
    '''Method that check if current attack is valid for the knight. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_attack = True

    return valid_attack

  def _pawn_move(self, move_data_dict):
    '''Method that check if the current move is valid for the pawn. It receives 1 dict argument and returns a boolean according to the case.'''
    # print(f"### move_data_dict:{move_data_dict}")
    valid_move = None

    # Since pawns can only move in the same column,
    # check first if source and destination columns are the same:
    if move_data_dict["col_source"] == move_data_dict["col_destination"]:

      # Black pawns:
      if move_data_dict["piece_color"] == BLACK:
        # If they are in 2nd row, they can move 1 or 2 squares row-ascending:
        if move_data_dict["row_source"] == 2:
          # The rows between source and destination are no more than 2 squares:
          if move_data_dict["row_destination"] - move_data_dict["row_source"] <= 2:
            valid_move = True
          else:
            valid_move = False
        # If not in 2nd row, they can only move 1 square row-ascending:
        else:
          if move_data_dict["row_destination"] - move_data_dict["row_source"] == 1:
            valid_move = True
          else:
            valid_move = False

      # White pawns:
      elif move_data_dict["piece_color"] == WHITE:
        # If they are in 7th row, they can move 1 or 2 squares row-descending:
        if move_data_dict["row_source"] == 7:
          # The rows between source and destination are no more than 2 squares:
          if move_data_dict["row_source"] - move_data_dict["row_destination"] <= 2:
            valid_move = True
          else:
            valid_move = False
        # If not in 7th row, they can only move 1 square row-descending:
        else:
          if move_data_dict["row_source"] - move_data_dict["row_destination"] == 1:
            valid_move = True
          else:
            valid_move = False
      else:
        raise ValueError("Invalid piece_color value inside dict in _pawn_move method in ChessRules class.")

    # If pawns source and destination columns are not the same...
    else:
      valid_move = False

    # print(f"### valid_move:{valid_move} ###")
    return valid_move

  def _pawn_attack(self, attack_data_dict):
    '''Method that check if current attack is valid for the pawn. It receives 1 dict argument and returns a boolean according to the case.'''
    # print(f"### attack_data_dict:{attack_data_dict}")
    valid_attack = None

    # Black pawns can attack only 1 square forward diagonally row-ascending:
    if attack_data_dict["source_color"] == BLACK:
      if attack_data_dict["row_destination"] - attack_data_dict["row_source"] == 1 and \
         abs(attack_data_dict["col_destination"] - attack_data_dict["col_source"]) == 1:
        valid_attack = True
      else:
        valid_attack = False
    # White pawns can attack only 1 square forward diagonally row-descending:
    else:
      if attack_data_dict["row_source"] - attack_data_dict["row_destination"] == 1 and \
         abs(attack_data_dict["col_destination"] - attack_data_dict["col_source"]) == 1:
        valid_attack = True
      else:
        valid_attack = False

    # print(f"### valid_attack:{valid_attack} ###")
    return valid_attack


class ChessBoard():
  '''The class that keeps track of all the pieces on a chessboard and enables their moves.'''
  def __init__(self):
    self.squares = None
    self.moves = 0
    self.rules = ChessRules()

  def reset_chess_pieces(self):
    '''Method that sets up the chess pieces with the initial chess positions to start a game.'''
    # Creating squares array, with only row and column content in each square:
    self.squares = [[f"{fil+1}{col}" for col in COLUMNS]
                                     for fil in range(8)]

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

  def move_piece(self, source, destination):
    '''Method that moves a piece from its source square to its destination square, according to the values passed as arguments.
    The method checks if the arguments are correct and then calls other methods to check if the move is valid and, if it is, call another method to change it.'''
    status = None
    message = None

    # Checking received arguments:
    if source[0] not in ROWS and source[1] not in COLUMNS:
      raise ValueError("An invalid starting position was received as an argument in ChessBoard.move_piece() method.")

    if destination[0] not in ROWS and destination[1] not in COLUMNS:
      raise ValueError("An invalid end position was received as an argument in ChessBoard.move_piece() method.")

    # If the move is legal, change it. Otherwise do nothing.
    # In both cases it ends by returning status boolean and a message.:
    status, message = self._check_move(source, destination)
    if status:
      self._change_piece_position(source, destination)
      self.moves += 1

    return status, message

  def _check_move(self, source, destination):
    '''Method that checks if the desired move of a piece is legal. It receives 2 arguments, one with the source of a piece and the other with its destination.
    Calls other methods to check if the move or attack is legal. Returns tuple of data according to the case.'''
    status = None
    message = None
    source_square = ""
    destination_square = ""

    # Converting the source and destination positions to numerical values to be able to search in array:
    row_source = int(source[0])-1
    col_source = COL_NUMBER_IN_ARRAY[source[1]]
    row_destination = int(destination[0])-1
    col_destination = COL_NUMBER_IN_ARRAY[destination[1]]

    # 1a) Checking if exists squares in souce and destination:
    source_square = self._check_if_square_exist(row_source, col_source)
    destination_square = self._check_if_square_exist(row_destination, col_destination)
    if source_square and destination_square:

      # 2a) Checking if there is piece in source square:
      if len(source_square) > 2:
        piece_source = source_square[2] # The 3rd character of the string represents the name of the piece.

        # 3a) Checking whether the piece can make a legal move:
        if len(destination_square) == 2:
          if self.rules.check_move(source_square, destination_square):
            status = True
            message = f"Moving {PIECES_NAMES[piece_source]} from {source_square[:2]} " \
                    + f"to {destination_square}."
          else:
            status = False
            message = "This move is not legal for this piece."

        # 2b) Checking if it is possible to attack an enemy piece in destination:
        elif len(destination_square) > 2:
          if self.rules.check_attack(source_square, destination_square):
            initial_square = source_square[0:2]
            final_square = destination_square[0:2]
            attacked_piece = destination_square[2]

            # 3b) Checking if the piece can perform a legal attack:
            if self.rules.check_attack(source_square, destination_square):
              status = True
              message = f"Attacking with {PIECES_NAMES[piece_source]} from {initial_square} " \
                        f"to {PIECES_NAMES[attacked_piece]} in {final_square}."
          else:
            status = False
            message = "This attack is not legal for this piece."

        # 2b) If there is no piece at source, set the corresponding status and message:
        elif len(source_square) == 2:
          status = False
          message = f"No piece was found in the square {source_square}."
      else:
        status = False
        message = "The destination square is invalid or doesn't exist."
    else:
      status = False
      message = "The source or destination_square square are invalid or doesn't exist."

    #print(f"### message: {message} ###")
    return status, message

  def _check_if_square_exist(self, row, column):
    '''Method that checks if exists a square on the board according to row and column received by arguments. Returns a string type according to the case.'''
    square = ""
    # Get square value, if exists:
    try:
      square = self.squares[row][column]
    # If doesn't exist square, do nothing:
    except TypeError as error:
      pass
    # In any case, return square value:
    finally:
      # print(f"\n### square: {square} | row: {row} | column: {column} ###")
      return square

  def _change_piece_position(self, source, destination):
    '''Method that moves a chess piece from its current position. It receives 2 arguments, one with the source of a chess piece and the other with its destination.
    This method only modifies the values of an array of arrays of the class.'''
    piece = source[2:]  # 3rd and 4th characters represent piece and color.

    row_source = int(source[0]) - 1    # Subtract 1 because array starts from zero.
    col_source = COL_NUMBER_IN_ARRAY[source[1]]
    row_destination = int(destination[0]) - 1  # Subtract 1 because array starts from zero.
    col_destination = COL_NUMBER_IN_ARRAY[destination[1]]
    # print(f"\n### piece:{piece} | row_source:{row_source} | col_source:{col_source} | row_destination:{row_destination} | col_destination:{col_destination} ###\n")

    # Putting the piece in the destination square:
    self.squares[row_destination][col_destination] = self.squares[row_destination][col_destination][0:2] + piece

    # Removing piece in source square (removing piece and color strings):
    self.squares[row_source][col_source] = self.squares[row_source][col_source][0:2]


class UI():
  '''A class uses as (informal) interface for any other UI type classes.'''
  def show_pieces(self):
    '''This method shows player name/turn and all current pieces from a board.'''
    pass


class TUI(UI):
  '''The Text User Interface class that shows the chessboard on screen via terminal console.'''
  def __init__(self):
    self.console = Console(color_system="256")

  def show_pieces(self, board, players):
    '''Method that creates a table (using Rich library) according to the position of the pieces on the board (from internal array of the class).
    And then the content of this table is printed on the terminal.'''
    full_board = board.squares    # Get all current pieces from board.
    table_title = ""

    # Table title:
    if board.moves > 0:
      table_title = f"{board.moves}) {players.turn.title()}'s move:"
    else:
      table_title = f"New game:"

    # Table:
    table = Table(title=table_title, show_header=True, show_lines=True, box=box.ROUNDED)

    style = "italic not bold grey11"
    # Set 9 columns (8 plus 1 for board letters):
    table.add_column(f"[{style}]a[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]b[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]c[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]d[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]e[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]f[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]g[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(f"[{style}]h[/{style}]", justify="center", style="black", no_wrap=True)
    table.add_column(" ", justify="center", style=style, no_wrap=True)

    # Set the 8 rows with the current pieces:
    for row_number, row_board in enumerate(full_board, 1):
      # Each square that has a piece is colored and then is saved in array:
      row_board = self._format_square_according_to_color_piece(row_board)
  
      # Adding a last column of board numbers to each row in array:
      row_board.append(str(ROWS[row_number-1]))

      # Adding each row to table:
      table.add_row(*row_board)   # Passing as strings (not full list).

    # Show table in terminal:
    print()
    self.console.print(table)

  def _format_square_according_to_color_piece(self, row):
    '''Method that receives an array as argument and returns it modified based on its content.'''
    new_row = []

    for square in row:
      # If the square contains a piece and its color, style it as such and discard the rest:
      if len(square) == 4:
        if square[-1] == WHITE:
          new_row.append(f"[black on white][{square[2]}][/black on white]")
        else:
          new_row.append(f"[white on black][{square[2]}][/white on black]")
      else:
        new_row.append("")

    return new_row


class ChessGame():
  '''The class that uses all the others classes to run the game.'''
  def __init__(self):
    self.board = ChessBoard()
    self.players = ChessPlayers()
    self.ui = TUI()

  def start(self):
    '''A method that starts a chess game by resetting the pieces on the board to their initial positions, taking the initial time and finally displaying the board on the terminal.'''
    self.board.reset_chess_pieces()
    self.players.history.append(["Game start", "---", time.ctime()])
    self.ui.show_pieces(self.board, self.players)
    time.sleep(1.5)

  def move_piece(self, source, destination):
    '''Method that moves a chess part from its source to its destination, both received by argument.
    This method calls another method from ChessBoard class to complete the task.'''
    # 1) Get piece from source.
    # Checking that there is only a row and a column in source:
    if len(source) > 2:
      source = source[:2]
    # Get current piece in square and add it to source:
    row_source = int(source[0]) - 1   # Subtract 1 because array starts from zero.
    col_source = COL_NUMBER_IN_ARRAY[source[1]]
    source = self.board.squares[row_source][col_source]

    # 2) Move piece to destination and end turn:
    self.board.move_piece(source, destination)
    self.ui.show_pieces(self.board, self.players)
    self._finish_turn(source, destination)

  def _finish_turn(self, source, destination):
    '''Method that record last move and time, and assigns new turn for the other player.'''

    # Record last player turn, last piece move and time:
    piece = PIECES_NAMES[source[2]]
    source_square = source[0:2]
    destination_square = destination[0:2]
    self.players.history.append([self.players.turn,
                                 f"{piece}: {source_square} -> {destination_square}",
                                 time.ctime()])

    # Change player turn:
    if self.players.turn == WHITES:
      self.players.turn = BLACKS
    else:
      self.players.turn = WHITES

    time.sleep(1.5)


# Main:
if __name__ == "__main__":
  game = ChessGame()
  game.start()

  game.move_piece("7b", "6b")
  game.move_piece("2b", "3b")

  game.move_piece("7c", "5c")
  game.move_piece("2c", "4c")

  game.move_piece("7d", "5d")
  game.move_piece("2d", "4d")

  game.move_piece("5d", "4c")
  game.move_piece("4d", "5c")

  game.move_piece("4c", "3b")
  game.move_piece("5c", "6b")

  game.move_piece("3b", "2a")
  game.move_piece("6b", "7a")

  game.move_piece("2a", "1b")
  game.move_piece("7a", "8b")

  #print(f"\n{game.players.history}\n")
  #print(f"\n# 5c: {game.board.squares[4][2]}\n")
