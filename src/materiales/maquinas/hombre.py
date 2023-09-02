"""Computadora del Hombre Pequeño.

Este módulo contiene la implementación de la computadora del Hombre
Pequeño, una computadora de arquitectura de Von Neumann con 100
posiciones de memoria, un acumulador, una entrada y una salida.

Más información:
https://es.wikipedia.org/wiki/Little_man_computer

Clases
------
ComputadoraHombrePequenno
    Computadora del Hombre Pequeño.

Excepciones
-----------
ComputadoraDetenida
    Excepción que se levanta cuando la computadora se detiene.
"""
import collections
import enum
from collections.abc import Iterable, Sequence

Memoria = Sequence[int]


class Operador(enum.IntEnum):
    """Instrucciones de la computadora Hombre Pequeño.

    Las instrucciones se componen de tres dígitos, el primero indica la
    operación a realizar y los dos últimos indican la posición de
    memoria sobre la que se va a operar.

    Atributos
    ---------
    ADD : int
        1xx suma lo que hay en la posicion xx a la acumulador
    SUB : int
        2xx resta lo que hay en la posicion xx a la acumulador
    STA : int
        3xx guarda el valor del acumulador en la posicion xx
    LDA : int
        5xx carga el valor de la posición xx en el acumulador
    BRA : int
        6xx salta a la posicion xx
    BRZ : int
        7xx salta a la posicion xx si el acumulador es cero
    BRP : int
        8xx salta a la posicion xx si el acumulador es positivo
    INP : int
        901 lee un valor de entrada y lo guarda en el acumulador
    OUT : int
        902 imprime el valor del acumulador
    HLT : int
        000 termina la ejecucion del programa
    """

    ADD = 1
    SUB = 2
    STA = 3
    LDA = 5
    BRA = 6
    BRZ = 7
    BRP = 8
    INP = 901
    OUT = 902
    HLT = 0


class Estado(enum.IntEnum):
    """Estados de la computadora Hombre Pequenno.

    Atributos
    ---------
    DETENIDA : int
        La computadora está detenida.
    ACTIVADA : int
        La computadora está activada.
    """

    DETENIDA = enum.auto()
    ACTIVADA = enum.auto()


class ComputadoraDetenida(Exception):
    """Excepción que se levanta cuando la computadora se detiene."""


class ComputadoraHombrePequenno:
    """Computadora del Hombre Pequenno.

    Atributos
    ---------
    memoria : MutableSequence[int]
        Memoria de la computadora.
    contador : int
        Contador de programa.
    acumulador : int
        Acumulador de la computadora.
    entrada : deque[int]
        Entrada de la computadora.
    salida : deque[int]
        Salida de la computadora.
    """

    marcador_pos = "▶"

    def __init__(
        self,
        *,
        programa: Memoria = (),
        contador: int = 0,
        acumulador: int = 0,
        entrada: Iterable[int] = (),
        salida: Iterable[int] = (),
    ):
        self.memoria: list[int]
        self.contador: int
        self.acumulador: int
        self.entrada: collections.deque[int]
        self.salida: collections.deque[int]
        self.estado: Estado
        self.reiniciar()

        self.cargar_programa(programa)
        self.contador = int(contador)
        self.acumulador = int(acumulador)
        self.cargar_entrada(entrada)
        self.salida.extend(salida)

    def reiniciar(self) -> "ComputadoraHombrePequenno":
        """Reinicia la computadora."""
        self.memoria = [0] * 100
        self.contador = 0
        self.acumulador = 0
        self.entrada = collections.deque()
        self.salida = collections.deque()
        self.estado = Estado.ACTIVADA
        return self

    def _verificar_estado(self) -> None:
        """Verifica que el estado de la computadora sea válido."""
        if self.estado == Estado.DETENIDA:
            return
        if not -999 <= self.acumulador <= 999:
            raise ValueError(
                "Se esperaba un acumulador entre -999 y 999, se recibió "
                f"{self.acumulador}"
            )
        if not 0 <= self.contador <= 100:
            raise ValueError(
                f"Se esperaba un contador entre 0 y 100, se recibió {self.contador}"
            )
        for i, instruccion in enumerate(self.memoria):
            if not -999 <= instruccion <= 999:
                raise ValueError(
                    f"Se esperaba una instrucción entre -999 y 999, se recibió "
                    f"{instruccion} en la posición {i}."
                )
        for i, entrada in enumerate(self.entrada):
            if not -999 <= entrada <= 999:
                raise ValueError(
                    "Se esperaba una entrada entre -999 y 999, se recibió "
                    f"{entrada} en la posición {i}."
                )
        for i, salida in enumerate(self.salida):
            if not -999 <= salida <= 999:
                raise ValueError(
                    "Se esperaba una salida entre -999 y 999, se recibió "
                    f"{salida} en la posición {i}."
                )

    def cargar_programa(self, programa: Memoria) -> "ComputadoraHombrePequenno":
        """Carga un programa en la memoria de la computadora.

        Parámetros
        ----------
        programa : Memoria
            Programa a cargar en la memoria.

        Levanta
        -------
        ValueError
            Si el programa no cabe en la memoria.
        """
        n_memoria, n_programa = len(self.memoria), len(programa)
        if n_programa > n_memoria:
            raise ValueError("El programa no cabe en la memoria")
        self.memoria[:n_programa] = programa
        self.memoria[n_programa:] = [0] * (n_memoria - n_programa)
        return self

    def cargar_entrada(self, entrada: Iterable[int]) -> "ComputadoraHombrePequenno":
        """Carga una entrada en la computadora.

        Parámetros
        ----------
        entrada : Iterable[int]
            Entrada a cargar en la computadora.
        """
        self.entrada = collections.deque(entrada)
        return self

    def transicion(self, ignorar_detener: bool = True) -> "ComputadoraHombrePequenno":
        """Realiza un ciclo de instrucción de la computadora.

        Un ciclo de instrucción consiste en:
        1. Obtener la instrucción de la memoria.
        2. Decodificar la instrucción.
        3. Ejecutar la instrucción.

        Levanta
        -------
        ValueError
            Si la instrucción no es válida.
        """
        self._verificar_estado()
        try:
            self._transicion()
        except ComputadoraDetenida:
            if ignorar_detener:
                self.detener()
            else:
                raise
        return self

    def _transicion(self) -> None:
        """Realiza un ciclo de instrucción de la computadora."""
        instruccion = self._traer_instruccion()
        operador, operando = self._decodificar_instruccion(instruccion)
        self._ejecutar_instruccion(operador, operando)

    def detener(self) -> "ComputadoraHombrePequenno":
        """Detiene la computadora."""
        self.estado = Estado.DETENIDA
        print("La computadora se detuvo.")
        return self

    def _traer_instruccion(self) -> int:
        """Obtiene la siguiente instrucción de la memoria.

        Retorna
        -------
        int
            Instrucción obtenida.

        Levanta
        -------
        ComputadoraDetenida
            Si la computadora está detenida.
        """
        try:
            instruccion = self.memoria[self.contador]
        except IndexError as exc:
            raise ComputadoraDetenida(self.salida) from exc
        self.contador += 1
        return instruccion

    def _decodificar_instruccion(self, instuccion: int) -> tuple[Operador, int]:
        """Decodifica una instruccion de la computadora.

        Parámetros
        ----------
        instuccion : int
            Instrucción a decodificar.

        Retorna
        -------
        tuple[Operador, int]
            Operador y operando de la instrucción.

        Levanta
        -------
        ValueError
            Si la instrucción no es válida.
        """
        operador, operando = divmod(instuccion, 100)
        if operador == 9:
            operador, operando = instuccion, 0
        return Operador(operador), operando

    def _ejecutar_instruccion(self, operador: Operador, operando: int) -> None:
        """Ejecuta una instrucción de la computadora.

        Parámetros
        ----------
        operador : Operador
            Operador de la instrucción.
        operando : int
            Operando de la instrucción.

        Levanta
        -------
        ValueError
            Si el operador no es válido.
        """
        match operador:
            case Operador.ADD:
                self._asignar_acumulador(self.acumulador + self.memoria[operando])
            case Operador.SUB:
                self._asignar_acumulador(self.acumulador - self.memoria[operando])
            case Operador.STA:
                self.memoria[operando] = self.acumulador
            case Operador.LDA:
                self.acumulador = self.memoria[operando]
            case Operador.BRA:
                self.contador = operando
            case Operador.BRZ:
                if self.acumulador == 0:
                    self.contador = operando
            case Operador.BRP:
                if self.acumulador > 0:
                    self.contador = operando
            case Operador.INP:
                self.acumulador = self.entrada.popleft()
            case Operador.OUT:
                self.salida.append(self.acumulador)
            case Operador.HLT:
                self.contador = len(self.memoria)
                self.detener()
                raise ComputadoraDetenida()

    def _asignar_acumulador(self, valor: int) -> None:
        if -999 <= valor <= 999:
            self.acumulador = valor
        else:
            raise OverflowError()

    def ejecutar(self) -> None:
        """Ejecuta el programa cargado en la computadora."""
        self._verificar_estado()
        try:
            while True:
                self._transicion()
        except ComputadoraDetenida:
            pass

    def __repr__(self) -> str:
        # Recortar el programa ignorando la cola de ceros del final
        programa = self.memoria
        i_final = 0
        for i, instruccion in enumerate(programa):
            if instruccion != 0:
                i_final = i
        programa = programa[: i_final + 1]
        return (
            f"{self.__class__.__name__}("
            f"programa={programa}, "
            f"contador={self.contador}, "
            f"acumulador={self.acumulador}, "
            f"entrada={self.entrada}, "
            f"salida={self.salida})"
        )

    def __str__(self) -> str:
        def ind(i: int) -> str:
            if i == self.contador:
                return "→"
            return " "

        lineas = []
        lineas.append(
            f"{self.acumulador:03d} │ " + " ".join(f" X{j}" for j in range(10))
        )
        lineas.append("────┼─" + "─" * 39)
        mem = self.memoria
        for i in range(10):
            rango = range(i * 10, i * 10 + 10)
            lineas.append(f" {i}X │" + "".join(f"{ind(i)}{mem[i]:03d}" for i in rango))
        return "\n".join(lineas)

    def _repr_html_(self) -> str:
        def cola(elementos: Iterable[int]) -> str:
            """Crea una cola de elementos HTML."""
            return f"[{', '.join(f'<code>{i:03d}</code>' for i in elementos)}]"

        def td_(contenido: str, hombrecito: bool = False) -> str:
            """Crea una celda de una tabla HTML."""
            if hombrecito:
                contenido = f"{self.marcador_pos}{contenido}"
            # Set font to monospace
            return f"<td><code>{contenido}</code></td>"

        def th_(contenido: str) -> str:
            """Crea una celda de encabezado de una tabla HTML."""
            return f"<th><strong>{contenido}</strong></th>"

        lineas = []
        lineas.append(f"↓{cola(self.entrada)}")
        lineas.append("<table>")
        lineas.append(
            "<tr>"
            + td_(f"{self.acumulador:03d}")
            + "".join(th_(f"X{j}") for j in range(10))
            + "</tr>"
        )
        for i in range(10):
            rango = range(i * 10, i * 10 + 10)
            lineas.append(
                "<tr>"
                + th_(f"{i}X")
                + "".join(
                    td_(f"{self.memoria[i]:03d}", hombrecito=i == self.contador)
                    for i in rango
                )
                + "</tr>"
            )
        lineas.append("</table>")
        lineas.append(f"↓{cola(self.salida)}")
        return "\n".join(lineas)
