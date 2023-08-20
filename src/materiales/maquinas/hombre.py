import collections
import enum
from collections.abc import Iterable, Sequence

Memoria = Sequence[int]


class Operador(enum.IntEnum):
    """Instrucciones de la computadora Hombre Pequenno.

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
        self.entrada: collections.deque
        self.salida: collections.deque
        self.reiniciar()

        self.cargar_programa(programa)
        self.contador = int(contador)
        self.acumulador = int(acumulador)
        self.cargar_entrada(entrada)
        self.salida.extend(salida)

    def reiniciar(self) -> None:
        """Reinicia la computadora."""
        self.memoria = [0] * 100
        self.contador = 0
        self.acumulador = 0
        self.entrada = collections.deque()
        self.salida = collections.deque()

    def cargar_programa(self, programa: Memoria) -> None:
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
        if len(programa) > len(self.memoria):
            raise ValueError("El programa no cabe en la memoria")
        self.memoria[: len(programa)] = programa

    def cargar_entrada(self, entrada: Iterable[int]) -> None:
        """Carga una entrada en la computadora.

        Parámetros
        ----------
        entrada : Iterable[int]
            Entrada a cargar en la computadora.
        """
        self.entrada.extend(entrada)

    def transicion(self) -> bool:
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
        try:
            instruccion = self._traer_instruccion()
            operador, operando = self._decodificar_instruccion(instruccion)
            self._ejecutar_instruccion(operador, operando)
        except ComputadoraDetenida:
            return False
        return True

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

    def _ejecutar_instruccion(self, operador: Operador, operando: int):
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
                self.acumulador += self.memoria[operando]
            case Operador.SUB:
                self.acumulador -= self.memoria[operando]
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

    def ejecutar_programa(self, entrada: Iterable[int]) -> list[int]:
        """Ejecuta el programa cargado en la computadora.

        Parámetros
        ----------
        entrada : Iterable[int]
            Entrada para la computadora.

        Retorna
        -------
        list[int]
            Salida de la computadora.
        """
        self.entrada = iter(entrada)
        self.salida = []
        try:
            while True:
                self.transicion()
        except ComputadoraDetenida:
            pass
        return self.salida

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

    def _repr_html_(self):
        def cola(elementos: Iterable[int]) -> str:
            return f"[{', '.join(f'<code>{i:03d}</code>' for i in elementos)}]"

        def td(s: str, highlight: bool = False) -> str:
            if highlight:
                s = f"▶️{s}"
            # Set font to monospace
            return f"<td><code>{s}</code></td>"

        def th(s: str) -> str:
            return f"<th><strong>{s}</strong></th>"

        lineas = []
        lineas.append(f"↓{cola(self.entrada)}")
        lineas.append("<table>")
        lineas.append(
            "<tr>"
            + td(f"{self.acumulador:03d}")
            + "".join(th(f"X{j}") for j in range(10))
            + "</tr>"
        )
        for i in range(10):
            rango = range(i * 10, i * 10 + 10)
            lineas.append(
                "<tr>"
                + th(f"{i}X")
                + "".join(
                    td(f"{self.memoria[i]:03d}", highlight=i == self.contador)
                    for i in rango
                )
                + "</tr>"
            )
        lineas.append("</table>")
        lineas.append(f"↓{cola(self.salida)}")
        return "\n".join(lineas)
