# Librerías:
import time

# Constantes:
BLANCAS = "blancas"
NEGRAS = "negras"
BLANCO = "w"
NEGRO = "b"

REY = "Rey"
REINA = "Reina"
TORRE = "Torre"
ALFIL = "Alfil"
CABALLO = "Caballo"
PEON = "Peón"

COLORES_PIEZAS = (BLANCO, NEGRO)
TIPOS_PIEZAS = (REY, REINA, TORRE, ALFIL, CABALLO, PEON)
COD_PIEZAS = {REY: 'K', REINA: 'Q', TORRE: 'R', ALFIL: 'B', CABALLO: 'N', PEON: 'P'}
NOMBRE_PIEZAS = {'K': REY, 'Q': REINA, 'R': TORRE, 'B': ALFIL, 'N': CABALLO, 'P': PEON}
FILAS = (1, 2, 3, 4, 5, 6, 7, 8)
COLUMNAS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
NRO_COL = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

# Clases:
class Jugador():
  def __init__(self, nombre, color):
    self.nombre = nombre
    self.color = color

class Tablero():
  def __init__(self):
    self.casillas = [[f"{fil+1}{col}" for col in COLUMNAS]
                                      for fil in range(8)]
    self.movimientos = 0

  def resetear_piezas(self):
    '''Método que setea las piezas de ajedrez con las posiciones iniciales por defecto para
    iniciar una partida.'''

    # Negras:
    self.casillas[0][0] += COD_PIEZAS[TORRE] + NEGRO
    self.casillas[0][1] += COD_PIEZAS[CABALLO] + NEGRO
    self.casillas[0][2] += COD_PIEZAS[ALFIL] + NEGRO
    self.casillas[0][3] += COD_PIEZAS[REY] + NEGRO
    self.casillas[0][4] += COD_PIEZAS[REINA] + NEGRO
    self.casillas[0][5] += COD_PIEZAS[ALFIL] + NEGRO
    self.casillas[0][6] += COD_PIEZAS[CABALLO] + NEGRO
    self.casillas[0][7] += COD_PIEZAS[TORRE] + NEGRO

    for pos, _ in enumerate(self.casillas[1]):
      self.casillas[1][pos] += COD_PIEZAS[PEON] + NEGRO

    # Blancas:
    self.casillas[6][0] += COD_PIEZAS[TORRE] + BLANCO
    self.casillas[6][1] += COD_PIEZAS[CABALLO] + BLANCO
    self.casillas[6][2] += COD_PIEZAS[ALFIL] + BLANCO
    self.casillas[6][3] += COD_PIEZAS[REY] + BLANCO
    self.casillas[6][4] += COD_PIEZAS[REINA] + BLANCO
    self.casillas[6][5] += COD_PIEZAS[ALFIL] + BLANCO
    self.casillas[6][6] += COD_PIEZAS[CABALLO] + BLANCO
    self.casillas[6][7] += COD_PIEZAS[TORRE] + BLANCO

    for pos, _ in enumerate(self.casillas[7]):
      self.casillas[7][pos] += COD_PIEZAS[PEON] + BLANCO

  def mover_pieza(self, origen, destino):
    '''Método que mueve una pieza desde su origen a su destino según valores pasados por argumento.
    El método chequea si los argumentos son correctos y llama luego a otros métodos para chequear si
    el movimiento es válido y, si lo es, cambiarlo.'''
    status = None
    mensaje = None

    # Chequeando argumentos recibidos:
    if origen[0] not in FILAS and origen[1] not in COLUMNAS:
      raise ValueError("Se recibió una posición inicial inválida como argumento en método Tablero.mover().")

    if destino[0] not in FILAS and destino[1] not in COLUMNAS:
      raise ValueError("Se recibió una posición final inválida como argumento en método Tablero.mover().")

    # Si el movimiento es legal, cambiar. Caso contrario no se hace nada.
    # En ambos casos se finaliza retornando bool de status y mensaje:
    status, mensaje = self._chequear_movimiento(origen, destino)
    if status:
      self._cambiar_pieza_de_posicion(origen, destino)
      self.movimientos += 1

    return status, mensaje

  def _chequear_movimiento(self, origen, destino):
    '''Método que chequea si el movimiento deseo de una pieza es legal. Recibe 2 argumentos, uno
    con el origen de una pieza de ajedrez y el otro su destino. Llama a otros métodos para
    chequear si el movimiento o ataque es legal. Retorna tupla de datos según el caso.'''
    status = None
    mensaje = None
    casilla_origen = ""
    casilla_destino = ""

    # Convirtiendo a valores númericos las posiciones de origen y destino para buscar en array:
    fila_origen = int(origen[0])-1
    col_origen = NRO_COL[origen[1]]
    fila_destino = int(destino[0])-1
    col_destino = NRO_COL[destino[1]]

    # 1a) Chequeando si existen casilla en origen:
    casilla_origen = self._existe_casillero(fila_origen, col_origen)
    if not casilla_origen:
      status = False
      mensaje = "La casilla de origen es inválida o no existe."

    if casilla_origen:
      # 1b) Chequeando si existe una casilla en destino:
      casilla_destino = self._existe_casillero(fila_destino, col_destino)
      if not casilla_destino:
        status = False
        mensaje = "La casilla de destino es inválida o no existe)."

    if casilla_origen and casilla_destino:
      # 2a) Chequeando si hay pieza en casilla origen:
      if len(casilla_origen) > 2:
        pieza_origen = casilla_origen[2] # El 3° caracter del string representa la pieza.

        # 3a) Chequeando si dicha pieza puede realizar un movimiento legal:
        if len(casilla_destino) == 2:
          if self._es_movimiento_legal(casilla_origen, casilla_destino):
            status = True
            mensaje = f"Moviendo {NOMBRE_PIEZAS[pieza_origen]} desde {casilla_origen[:2]} " \
                    + f"hacia {casilla_destino}."
          else:
            status = False
            mensaje = "Este movimiento no es legal para esta pieza."

        # 2b) Chequeando si se puede comer una pieza enemiga en destino:
        elif len(casilla_destino) > 2:
          pieza_destino = casilla_destino[2] # El 3° caracter del string representa la pieza.

          # 3b) Chequeando si dicha pieza puede realizar un ataque legal:
          if self._es_ataque_legal(casilla_origen, casilla_destino):
            status = True
            mensaje = f"Atacando con {NOMBRE_PIEZAS[pieza_origen]} en {casilla_origen[:2]} " \
                      f"a {NOMBRE_PIEZAS[pieza_destino]} en {casilla_destino[:2]}."
          else:
            status = False
            mensaje = "Este ataque no es legal para esta pieza."

        else:
          status = False
          mensaje = "Error desconocido."

      # 2b) Si no hay pieza de origen, fijar status y mensaje correspondiente:
      elif len(casilla_origen) == 2:
        status = False
        mensaje = f"No se encontró ninguna pieza en la casilla {casilla_origen}."

    return status, mensaje

  def _existe_casillero(self, fila, columna):
    '''Método que cheque si existe un casillero en una fila y columna recibidas por argumento.
    Retorna booleano según el caso.'''
    casilla = ""

    try:
      casilla = self.casillas[fila][columna]
    except TypeError as error:
      # print(f"\n### ERROR: {error} ###")
      pass
    finally:
      # print(f"\n### casilla: {casilla} | fila: {fila} | columna: {columna} ###")
      return casilla

  def _es_movimiento_legal(self, origen, destino):
    '''Método que chequea si el movimiento de una pieza es legal. Recibe 2 argumentos, uno
    con el origen de una pieza de ajedrez y el otro su destino. Retorna booleano según el caso.'''
    status = None
    pieza_origen = origen[2]  # El 3° caracter del string representa la pieza.
    pos_origen = origen[0:2]
    pos_destino = destino[0:2]

    return True

  def _es_ataque_legal(self, origen, destino):
    '''Método que chequea si el ataque de una pieza es legal. Recibe 2 argumentos, uno con
    el origen de una pieza de ajedrez y el otro su destino. Retorna booleano según el caso.'''
    status = None
    pieza_origen = origen[2]  # El 3° caracter del string representa la pieza.
    pieza_destino = destino[2]  # El 3° caracter del string representa la pieza.
    pos_origen = origen[0:2]
    pos_destino = destino[0:2]

    return True

  def _cambiar_pieza_de_posicion(self, origen, destino):
    '''Método que mueve una pieza de ajedrez de posición. Recibe 2 argumentos, uno con el
    origen de una pieza de ajedrez y el otro su destino. Este método solo modifica valores
    de un array de arrays interno.'''
    pieza = origen[2:]  # 3° y 4° caracteres representan pieza y color.

    fila_origen = int(origen[0]) - 1    # Restar 1 porque se empieza desde cero en array.
    col_origen = NRO_COL[origen[1]]
    fila_destino = int(destino[0]) - 1  # Restar 1 porque se empieza desde cero en array.
    col_destino = NRO_COL[destino[1]]
    print(f"\n### pieza:{pieza} | fila_origen:{fila_origen} | col_origen:{col_origen} | fila_destino:{fila_destino} | col_destino:{col_destino} ###\n")

    # Poniendo pieza en casilla de destino:
    self.casillas[fila_destino][col_destino] += pieza

    # Quitando pieza en casilla de origen (borrando pieza y color):
    self.casillas[fila_origen][col_origen] = self.casillas[fila_origen][col_origen][0:2]

  def mostrar_piezas(self):
    '''Método que imprime por pantalla las piezas actuales en sus respectivos casilleros.'''
    print()
    for filas in self.casillas:
      print(filas)
    print()


class Juego():
  def __init__(self):
    self.tablero = Tablero()
    self.tiempo = []
    self.turno = BLANCAS

  def iniciar(self):
    '''Método que inicia partida de ajedrez, reseteando tablero, tomando tiempo y mostrando
    el tablero en pantalla.'''
    self.tablero.resetear_piezas()
    self.tiempo.append(time.time())
    self.mostrar()

  def _terminar_turno(self):
    '''Método que muestra título de finalizar turno, asigna nuevo turno para el otro jugador y
    registra en array el tiempo de la última partida.'''
    self._titulo(f"Turno de las {self.turno} finalizado.")

    if self.turno == BLANCAS:
      self.turno = NEGRAS
    else:
      self.turno = BLANCAS

    self.tiempo.append(time.time())
    time.sleep(2)

  def _titulo(self, texto):
    '''Simple método para mostrar un texto recibido por argumento a terminal/pantalla.'''
    print(f"{texto}")

  def mostrar(self):
    '''Método que muestra un título seguido de una llamada a otro método para mostrar las
    piezas del tablero de ajedrez.'''
    # Titulos:
    if self.tablero.movimientos > 0:
      self._titulo(f"\n{self.tablero.movimientos}) {self.turno.title()} moviendo:")
    else:
      self._titulo(f"\n{self.tablero.movimientos}) Iniciando partida.")

    # Mostrar piezas del tablero:
    self.tablero.mostrar_piezas()

  def mover(self, origen, destino):
    '''Método que mueve una pieza desde un origen a un destino, ambos recibidos por argumento.'''
    # Chequeando que solo esten fila y col. en el origen recibido:
    if len(origen) > 2:
      origen = origen[:2]
    # Tomando la pieza existente en casillas y agregarlo a origen:
    fila_origen = int(origen[0]) - 1   # Restar 1 porque se empieza desde cero en array.
    col_origen = NRO_COL[origen[1]]
    origen = self.tablero.casillas[fila_origen][col_origen]

    # Mover, mostrar y terminar turno:
    self.tablero.mover_pieza(origen, destino)
    self.mostrar()
    self._terminar_turno()


if __name__ == "__main__":
  juego = Juego()
  juego.iniciar()

  juego.mover("7a", "6a")
  #juego.mover("7b", "5b")
  #juego.mover("7c", "6c")
