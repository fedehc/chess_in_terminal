# Librerías:
import time

# Constantes:
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

# Clases:
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

    # Negras:
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

    # Blancas:
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

    # Chequeando argumentos recibidos:
    if origin[0] not in ROWS and origin[1] not in COLUMNS:
      raise ValueError("Se recibió una posición inicial inválida como argumento en método ChessBoard.mover().")

    if destiny[0] not in ROWS and destiny[1] not in COLUMNS:
      raise ValueError("Se recibió una posición final inválida como argumento en método ChessBoard.mover().")

    # Si el movimiento es legal, cambiar. Caso contrario no se hace nada.
    # En ambos casos se finaliza retornando bool de status y message:
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
    casilla_origin = ""
    casilla_destiny = ""

    # Convirtiendo a valores númericos las posiciones de origin y destiny para buscar en array:
    row_origin = int(origin[0])-1
    col_origin = COL_NUMBER_IN_ARRAY[origin[1]]
    row_destiny = int(destiny[0])-1
    col_destiny = COL_NUMBER_IN_ARRAY[destiny[1]]

    # 1a) Chequeando si existen casilla en origin:
    casilla_origin = self._check_if_seat_exist(row_origin, col_origin)
    if not casilla_origin:
      status = False
      message = "La casilla de origin es inválida o no existe."

    if casilla_origin:
      # 1b) Chequeando si existe una casilla en destiny:
      casilla_destiny = self._check_if_seat_exist(row_destiny, col_destiny)
      if not casilla_destiny:
        status = False
        message = "La casilla de destiny es inválida o no existe)."

    if casilla_origin and casilla_destiny:
      # 2a) Chequeando si hay pieza en casilla origin:
      if len(casilla_origin) > 2:
        pieza_origin = casilla_origin[2] # El 3° caracter del string representa la pieza.

        # 3a) Chequeando si dicha pieza puede realizar un movimiento legal:
        if len(casilla_destiny) == 2:
          if self._check_if_move_is_legal(casilla_origin, casilla_destiny):
            status = True
            message = f"Moviendo {PIECES_NAMES[pieza_origin]} desde {casilla_origin[:2]} " \
                    + f"hacia {casilla_destiny}."
          else:
            status = False
            message = "Este movimiento no es legal para esta pieza."

        # 2b) Chequeando si se puede comer una pieza enemiga en destiny:
        elif len(casilla_destiny) > 2:
          pieza_destiny = casilla_destiny[2] # El 3° caracter del string representa la pieza.

          # 3b) Chequeando si dicha pieza puede realizar un ataque legal:
          if self._check_if_attack_is_legal(casilla_origin, casilla_destiny):
            status = True
            message = f"Atacando con {PIECES_NAMES[pieza_origin]} en {casilla_origin[:2]} " \
                      f"a {PIECES_NAMES[pieza_destiny]} en {casilla_destiny[:2]}."
          else:
            status = False
            message = "Este ataque no es legal para esta pieza."

        else:
          status = False
          message = "Error desconocido."

      # 2b) Si no hay pieza de origin, fijar status y message correspondiente:
      elif len(casilla_origin) == 2:
        status = False
        message = f"No se encontró ninguna pieza en la casilla {casilla_origin}."

    return status, message

  def _check_if_seat_exist(self, row, column):
    '''Method that checks if there is a square in a row and column received by arguments. Returns boolean according to the case.'''
    casilla = ""

    try:
      casilla = self.squares[row][column]
    except TypeError as error:
      # print(f"\n### ERROR: {error} ###")
      pass
    finally:
      # print(f"\n### casilla: {casilla} | row: {row} | column: {column} ###")
      return casilla

  def _check_if_move_is_legal(self, origin, destiny):
    '''Method that checks if the movement of a piece is legal. It receives 2 arguments, one with the origin of a chess piece and the other with its destiny. Returns boolean according to the case.'''
    status = None
    pieza_origin = origin[2]  # El 3° caracter del string representa la pieza.
    pos_origin = origin[0:2]
    pos_destiny = destiny[0:2]

    return True

  def _check_if_attack_is_legal(self, origin, destiny):
    '''Method that checks if the attack of a piece is legal. It receives 2 arguments, one with the origin of a chess piece and the other with its destiny. Returns boolean according to the case.'''
    status = None
    pieza_origin = origin[2]  # El 3° caracter del string representa la pieza.
    pieza_destiny = destiny[2]  # El 3° caracter del string representa la pieza.
    pos_origin = origin[0:2]
    pos_destiny = destiny[0:2]

    return True

  def _change_piece_position(self, origin, destiny):
    '''Method that moves a chess piece from its current position. It receives 2 arguments, one with the origin of a chess piece and the other with its destiny.
    This method only modifies values of an internal array of arrays.'''
    pieza = origin[2:]  # 3° y 4° caracteres representan pieza y color.

    row_origin = int(origin[0]) - 1    # Restar 1 porque se empieza desde cero en array.
    col_origin = COL_NUMBER_IN_ARRAY[origin[1]]
    row_destiny = int(destiny[0]) - 1  # Restar 1 porque se empieza desde cero en array.
    col_destiny = COL_NUMBER_IN_ARRAY[destiny[1]]
    # print(f"\n### pieza:{pieza} | row_origin:{row_origin} | col_origin:{col_origin} | row_destiny:{row_destiny} | col_destiny:{col_destiny} ###\n")

    # Poniendo pieza en casilla de destiny:
    self.squares[row_destiny][col_destiny] += pieza

    # Quitando pieza en casilla de origin (borrando pieza y color):
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
    # Titulos:
    if self.board.movements > 0:
      self._show_title(f"\n{self.board.movements}) {self.player_turn.title()}'s moving:")
    else:
      self._show_title(f"\n{self.board.movements}) Starting new game.")

    # Mostrar piezas del tablero:
    self.board.show_pieces()

  def move_piece(self, origin, destiny):
    '''Method that moves a part from its origin to its destination, both received by argument.'''
    # Chequeando que solo esten row y col. en el origin recibido:
    if len(origin) > 2:
      origin = origin[:2]
    # Tomando la pieza existente en casillas y agregarlo a origin:
    row_origin = int(origin[0]) - 1   # Restar 1 porque se empieza desde cero en array.
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
