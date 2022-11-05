# Standard libraries:
import os
import time

# 3° libraries:
from rich.console import Console
from rich.table import Table
from rich import box
import numpy


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

PIECES_COLORS = {WHITE: WHITES, BLACK: BLACKS}
PIECES_CODE = {KING: 'K', QUEEN: 'Q', ROOK: 'R', BISHOP: 'B', KNIGHT: 'N', PAWN: 'P'}
PIECES_NAMES = {'K': KING, 'Q': QUEEN, 'R': ROOK, 'B': BISHOP, 'N': KNIGHT, 'P': PAWN}
TOTAL_ROWS = 8
TOTAL_COLS = 8
ROWS = ('1', '2', '3', '4', '5', '6', '7', '8')
COLS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
COL_NUMBER_IN_ARRAY = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
SECOND_ROW = 1
SEVENTH_ROW = 6


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
    self.squares = None
    self.aux = Aux()

  def check_move(self, source, destination, squares):
    '''Method that checks if the move of a piece is legal. It receives 3 arguments, one with the source,the other with its destination and the last with the board object.
    Returns a boolean according to the case.'''
    can_move = None
    self.squares = squares

    # Get rows and cols numbers from source and destination:
    row_source, col_source, row_destination, col_destination = self.aux.get_rows_and_cols_from(source, destination)

    # Get source and destination pieces:
    square_source = self.squares[row_source, col_source]

    # Get piece and color from source square:
    piece_source = PIECES_NAMES[square_source[0]]
    color_source = square_source[1]

    # Creating dict for passing to methods below:
    move_data_dict = {
      "row_source": row_source,
      "col_source": col_source,
      "row_destination": row_destination,
      "col_destination": col_destination,
      "piece_source": piece_source,
      "color_source": color_source
    }

    # Call the appropiate method:
    if piece_source == KING:
      can_move = self._king_move(move_data_dict)
    elif piece_source == QUEEN:
      can_move = self._queen_move(move_data_dict)
    elif piece_source == ROOK:
      can_move = self._rook_move(move_data_dict)
    elif piece_source == BISHOP:
      can_move = self._bishop_move(move_data_dict)
    elif piece_source == KNIGHT:
      can_move = self._knight_move(move_data_dict)
    elif piece_source == PAWN:
      can_move = self._pawn_move(move_data_dict)
    else:
      raise ValueError("Invalid piece_name inside check_move method in ChessRules class.")

    return can_move

  def check_attack(self, source, destination, squares):
    '''Method that checks if the attack of a piece is legal. It receives 3 arguments, the 1st with the source, the 2nd with its destination and the 3rd with the board object.
    Returns a boolean according to the case.'''
    # print(f"### source:{source} | destination:{destination} ###")
    can_attack = True
    self.squares = squares

    # Get rows and cols numbers from source and destination:
    row_source, col_source, row_destination, col_destination = self.aux.get_rows_and_cols_from(source, destination)

    # Get source and destination pieces:
    square_source = self.squares[row_source, col_source]
    square_destination = self.squares[row_destination, col_destination]

    # Get piece and color from source and destination squares:
    piece_source = PIECES_NAMES[square_source[0]]
    color_source = square_source[1]
    piece_destination = PIECES_NAMES[square_destination[0]]
    color_destination = square_destination[1]

    # Creating dict for passing to methods below:
    attack_data_dict = {
      "row_source": row_source,
      "col_source": col_source,
      "row_destination": row_destination,
      "col_destination": col_destination,
      "piece_source": piece_source,
      "color_source": color_source,
      "piece_destination": piece_destination,
      "color_destination": color_destination
    }

    # Call the appropiate method:
    if piece_source == KING:
      can_attack = self._king_attack(attack_data_dict)
    elif piece_source == QUEEN:
      can_attack = self._queen_attack(attack_data_dict)
    elif piece_source == ROOK:
      can_attack = self._rook_attack(attack_data_dict)
    elif piece_source == BISHOP:
      can_attack = self._bishop_attack(attack_data_dict)
    elif piece_source == KNIGHT:
      can_attack = self._knight_attack(attack_data_dict)
    elif piece_source == PAWN:
      can_attack = self._pawn_attack(attack_data_dict)
    else:
      raise ValueError("Invalid piece_name_source inside check_attack in ChessRules class.")

    return can_attack

  def check_any_pieces_between(self, row_source, col_source, row_destination, col_destination):
    '''Method that checks if there is any pieces in a line (row, column, diagonal). It receives 4 int arguments and returns a boolean according to the case.'''
    piece_found = None
    array_move = None
    squares = self.squares # Local copy required to avoid any array mutation.

    # ROW movement:
    if row_source == row_destination:
      # Get only the cols in which the piece moves in the row:
      array_move = squares[row_source, col_source:col_destination]

    # COLUMN movement:
    elif col_source == col_destination:
      # Get only the rows in which the piece moves in the col:
      array_move = squares[row_source:row_destination, col_source]

    # DIAGONAL movement:
    else:
      # Check if "normal" numpy diagonal direction kind:
      if row_destination > row_source and col_destination > col_source or \
         row_destination < row_source and col_destination < col_source:
        pass

      # If "inverted" numpy diagonal direction kind:
      else:
        # Invert and compensate row and cols values:
        squares = numpy.rot90(squares)
        old_col_source = col_source
        old_col_destination = col_destination
        col_source = row_source
        col_destination = row_destination
        row_source = (TOTAL_ROWS-1) - old_col_source
        row_destination = (TOTAL_COLS-1) - old_col_destination

      print(f"\n{squares}\n")
      
      # Get diagonal offset from squares source:
      offset = col_source - row_source

      # Create array based on source-destination relative locations:
      col_offset = 0
      if col_destination > col_source:

        # Create column offset:
        if row_destination > row_source:
            if offset > 0:
                col_offset = offset
        else:
            if offset < 0:
                col_offset = offset
        # print(f"offset: {offset} | col_offset: {col_offset}")
        # Get only the rows in which the piece moves in the diagonal (including source and dest.):
        array_move = squares.diagonal(offset)[col_source-col_offset:col_destination+1]

      else:
        # Create column offset:
        if row_destination > row_source:
            if offset > 0:
                col_offset = offset
        else:
            if offset < 0:
                col_offset = offset

        # Get only the rows in which the piece moves in the diagonal (including source and dest.):
        array_move = squares.diagonal(offset)[col_destination-col_offset:col_source+1]

    array_move = array_move.tolist()
    # print(array_move)
    results = [x for x in array_move if x != '']
    # print(f"{results}\n")
    if len(results) > 1: # More than 2 because source piece is included in results.
      piece_found = True
    else:
      piece_found = False

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

  def _knight_attack(self, attack_data_dict):
    '''Method that check if current attack is valid for the knight. It receives 1 dict argument and returns a boolean according to the case.'''
    valid_attack = True

    return valid_attack

  def _pawn_move(self, move_data_dict):
    '''Method that check if the current move is valid for the pawn. It receives 1 dict argument and returns a boolean according to the case.'''
    #print(f"### move_data_dict:{move_data_dict}")
    valid_move = None

    # Since pawns can only move in the same column,
    # check first if source and destination columns are the same:
    if move_data_dict["col_source"] == move_data_dict["col_destination"]:

      # Black pawns:
      if move_data_dict["color_source"] == BLACK:

        # If they are in 2nd row, they can move 1 or 2 squares row-ascending:
        if move_data_dict["row_source"] == SECOND_ROW:

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
      else:

        # If they are in 7th row, they can move 1 or 2 squares row-descending:
        if move_data_dict["row_source"] == SEVENTH_ROW:

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
    if attack_data_dict["color_source"] == BLACK:
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
    # Filling 8x8 squares with empty strings:
    self.squares = numpy.array([[""] * TOTAL_COLS] * TOTAL_ROWS, dtype='<U2')
    self.moves = 0
    self.rules = ChessRules()
    self.aux = Aux()

  def reset_chess_pieces(self):
    '''Method that sets up the chess pieces with the initial chess positions to start a game.'''
    # Blacks:
    self.squares[0, 0] = PIECES_CODE[ROOK] + BLACK
    self.squares[0, 1] = PIECES_CODE[KNIGHT] + BLACK
    self.squares[0, 2] = PIECES_CODE[BISHOP] + BLACK
    self.squares[0, 3] = PIECES_CODE[QUEEN] + BLACK
    self.squares[0, 4] = PIECES_CODE[KING] + BLACK
    self.squares[0, 5] = PIECES_CODE[BISHOP] + BLACK
    self.squares[0, 6] = PIECES_CODE[KNIGHT] + BLACK
    self.squares[0, 7] = PIECES_CODE[ROOK] + BLACK
    self.squares[0, 7] = PIECES_CODE[ROOK] + BLACK
    self.squares[1] = PIECES_CODE[PAWN] + BLACK     # 2nd row with black pawns.

    # Whites:
    self.squares[6] = PIECES_CODE[PAWN] + WHITE     # 6th row with white pawns.
    self.squares[7, 0] = PIECES_CODE[ROOK] + WHITE
    self.squares[7, 1] = PIECES_CODE[KNIGHT] + WHITE
    self.squares[7, 2] = PIECES_CODE[BISHOP] + WHITE
    self.squares[7, 3] = PIECES_CODE[QUEEN] + WHITE
    self.squares[7, 4] = PIECES_CODE[KING] + WHITE
    self.squares[7, 5] = PIECES_CODE[BISHOP] + WHITE
    self.squares[7, 6] = PIECES_CODE[KNIGHT] + WHITE
    self.squares[7, 7] = PIECES_CODE[ROOK] + WHITE

  def move_piece(self, source, destination):
    '''Method that moves a piece from its source square to its destination square, according to the values passed as arguments.
    The method checks if the arguments are correct and then calls other methods to check if the move is valid and, if it is, call another method to change it.'''
    status = None
    message = None

    # Checking received arguments:
    if source[0] not in ROWS and source[1] not in COLS:
      status = False
      message = "An invalid starting position was received as an argument."

    elif destination[0] not in ROWS and destination[1] not in COLS:
      status = False
      message = "An invalid end position was received as an argument."

    else:
      # If the move or attack is legal, do it:
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

    # 1) Get rows and cols numbers from source and destination:
    row_source, col_source, row_destination, col_destination = self.aux.get_rows_and_cols_from(source, destination)

    # 2) Get source and destination pieces:
    square_source = self.squares[row_source, col_source]
    square_destination = self.squares[row_destination, col_destination]

    # 3) Get piece and color from source square:
    piece_source = PIECES_NAMES[square_source[0]]
    color_source = PIECES_COLORS[square_source[1]]

    # 4a) If there is piece in source square...
    if len(square_source) > 0:

      # 5a) Checking if source piece can make a legal move to destination square:
      if len(square_destination) == 0:
        if self.rules.check_move(source, destination, self.squares):
          status = True
          message = f"Moving {color_source} {piece_source} from {source} to {destination}."
        else:
          status = False
          message = "This move is not legal for this piece."

      # 5b) Checking if source piece can make a legal attack to destination piece:
      else:
        # 6) Get piece and color from destination square:
        piece_destination = PIECES_NAMES[square_destination[0]]
        color_destination = PIECES_COLORS[square_destination[1]]

        if self.rules.check_attack(source, destination, self.squares):
          status = True
          message = f"Attacking with {color_source} {piece_source} from {source} " \
                      f"to {color_destination} final_square{piece_destination} in {destination}."
        else:
          status = False
          message = "This attack is not legal for this piece."

    # 4b) If there is no piece at source...
    else:
      status = False
      message = f"No piece was found in the square {square_source}."

    return status, message

  def _change_piece_position(self, source, destination):
    '''Method that moves a chess piece from its current position. It receives 2 arguments, one with the source of a chess piece and the other with its destination.
    This method only modifies the values of an array of arrays of the class.'''
    # Get rows and cols numbers from source and destination:
    row_source, col_source, row_destination, col_destination = self.aux.get_rows_and_cols_from(source, destination)

    # Get piece from source square:
    piece = self.squares[row_source, col_source]

    # Putting the source piece in destination square:
    self.squares[row_destination, col_destination] = piece

    # Remove piece in source square:
    self.squares[row_source, col_source] = ""


class Aux():
  '''A class with auxiliary methods.'''
  def get_rows_and_cols_from(self, source, destination):
    '''Method that gets and returns rows and cols strings from a source and destination string arguments.'''
    row_source = int(source[0])-1
    col_source = COL_NUMBER_IN_ARRAY[source[1]]
    row_destination = int(destination[0])-1
    col_destination = COL_NUMBER_IN_ARRAY[destination[1]]

    return row_source, col_source, row_destination, col_destination

  def clear_terminal_console(self):
    '''Method that clears any text from the terminal console.'''
    command = "clear"
    if os.name in ("nt", "dos"):  # If OS is running Windows, uses 'cls' command.
        command = "cls"
    os.system(command)


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
    # Table title:
    table_title = ""
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
    for row_number, row_board in enumerate(board.squares, 1):
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
      if len(square) > 0:
        piece = square[0]
        color = square[1]
        if color == WHITE:
          new_row.append(f"[black on white][{piece}][/black on white]")
        else:
          new_row.append(f"[white on black][{piece}][/white on black]")
      else:
        new_row.append("")

    return new_row


class ChessGame():
  '''The class that uses all the others classes to run the game.'''
  def __init__(self):
    self.board = ChessBoard()
    self.players = ChessPlayers()
    self.ui = TUI()
    self.aux = Aux()

  def start(self):
    '''A method that starts a chess game by resetting the pieces on the board to their initial positions, taking the initial time and finally displaying the board on the terminal.'''
    self.board.reset_chess_pieces()
    self.players.history.append(["Start", "--------------", time.ctime()])
    self.ui.show_pieces(self.board, self.players)
    time.sleep(1.5)

  def move(self, source, destination):
    '''Method that moves a chess part from its source to its destination, both received by argument.
    This method calls another method from ChessBoard class to complete the task.'''
    # Checking source and destination values:
    if len(source) == 0 or len(source) > 2:
      raise ValueError("Invalid source value.")

    if len(destination) == 0 or len(destination) > 2:
      raise ValueError("Invalid destination value.")

    # Move piece to destination:
    status, message = self.board.move_piece(source, destination)

    # If the piece was moved successfully, show move on terminal and end turn:
    if status:
      self.aux.clear_terminal_console()
      self.ui.show_pieces(self.board, self.players)
      self._save_last_move(source, destination)
      self._finish_turn(source, destination)

    # Otherwise, show error:
    else:
      raise ValueError(message)

  def _finish_turn(self, source, destination):
    '''Simple method that assigns new turn for the other player in internal string.'''
    # Change player turn and wait a few seconds:
    if self.players.turn == WHITES:
      self.players.turn = BLACKS
    else:
      self.players.turn = WHITES
    time.sleep(1.5)

  def _save_last_move(self, source, destination):
    '''Method that saves last move in history array. Receives 2 strings arguments.'''
    # Get rows and cols numbers from source and destination:
    _, _, row_destination, col_destination = self.aux.get_rows_and_cols_from(source, destination)

    # Get current source piece:
    square = self.board.squares[row_destination, col_destination]
    piece = PIECES_NAMES[square[0]]

    # Save move on history array:
    self.players.history.append([self.players.turn,
                                 f"{piece}: {source} -> {destination}",
                                 time.ctime()])

  def _show_history(self):
    '''Internal method only used for showin self.players.history array content.'''
    print()
    print("-"*55)
    print("# History:")
    print("-"*55)
    for row in self.players.history:
      print(row)
    print("-"*55)
    print()


# Main:
if __name__ == "__main__":
  game = ChessGame()
  game.start()

  game.move("7b", "6b")
  game.move("2b", "3b")

  game.move("7c", "5c")
  game.move("2c", "4c")

  game.move("7d", "5d")
  game.move("2d", "4d")

  game.move("5d", "4c")
  game.move("4d", "5c")

  game.move("4c", "3b")
  game.move("5c", "6b")

  game.move("3b", "2a")
  game.move("6b", "7a")

  game.move("2a", "1b")
  game.move("7a", "8b")

  # print(f"{game._show_history()}")
  # print(f"\n# 1a: {game.board.squares[0, 0]}\n")
