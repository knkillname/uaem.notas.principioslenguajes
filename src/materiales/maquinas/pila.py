"""Máquina de Pila.

Este módulo implementa una máquina abstracta basada en una pila
de datos con múltiples operadores para manipularla.
"""

from typing import Any, Self


class MaquinaDePila:  # pylint: disable=too-many-public-methods
    """Clase que implementa una máquina de pila.

    Una máquina de pila es un tipo de máquina abstracta en la que las
    operaciones se realizan en una pila de datos.
    Los operadores desapilan uno o más elementos de la pila, realizan
    la operación correspondiente y apilan el resultado.

    Atributos
    ---------
    pila : list[Any]
        Pila de datos.

    Métodos
    -------
    apilar(elemento: Any) -> None
        Apila un elemento en la pila.
    desapilar() -> Any
        Desapila un elemento de la pila.
    esta_vacia() -> bool
        Indica si la pila está vacía.
    ver_cima() -> Any
        Retorna el elemento en la cima de la pila.
    suma() -> None
        Desapila b y a, y apila a + b.
    resta() -> None
        Desapila b y a, y apila a - b.
    invertir_signo() -> None
        Desapila a y apila -a.
    multiplicacion() -> None
        Desapila b y a, y apila a * b.
    division() -> None
        Desapila b y a, y apila a / b.
    division_entera() -> None
        Desapila b y a, y apila a // b.
    modulo() -> None
        Desapila b y a, y apila a % b.
    potencia() -> None
        Desapila b y a, y apila a ** b.
    menor_que() -> None
        Desapila b y a, y apila a < b.
    menor_o_igual_que() -> None
        Desapila b y a, y apila a <= b.
    igual_que() -> None
        Desapila b y a, y apila a == b.
    diferente_que() -> None
        Desapila b y a, y apila a != b.
    mayor_o_igual_que() -> None
        Desapila b y a, y apila a >= b.
    mayor_que() -> None
        Desapila b y a, y apila a > b.
    y_logico() -> None
        Desapila b y a, y apila a and b.
    o_logico() -> None
        Desapila b y a, y apila a or b.
    negacion() -> None
        Desapila a y apila not a.
    y_bit_a_bit() -> None
        Desapila b y a, y apila a & b.
    o_bit_a_bit() -> None
        Desapila b y a, y apila a | b.
    xor() -> None
        Desapila b y a, y apila a ^ b.
    negacion_bit_a_bit() -> None
        Desapila a y apila ~a.
    corrimiento_izquierda() -> None
        Desapila b y a, y apila a << b.
    corrimiento_derecha() -> None
        Desapila b y a, y apila a >> b.
    """

    def __init__(self) -> None:
        self.pila: list[Any] = []

    def _repr_markdown_(self) -> str:
        """Retorna una representación en Markdown de la pila."""
        lineas = ["| Nivel | Elemento |", "|---|---|"]
        for i, elemento in zip(range(len(self.pila) - 1, -1, -1), reversed(self.pila)):
            lineas.append(f"| {i} | `{elemento!r}` |")
        return "\n".join(lineas)

    def apilar(self, elemento: Any) -> Self:
        """Apila un elemento en la pila.

        Parámetros
        ----------
        elemento : Any
            Elemento a apilar.
        """
        self.pila.append(elemento)
        return self

    def desapilar(self) -> Any:
        """Desapila un elemento de la pila.

        Retorna
        -------
        Any
            Elemento desapilado.
        """
        return self.pila.pop()

    def esta_vacia(self) -> bool:
        """Indica si la pila está vacía.

        Retorna
        -------
        bool
            True si la pila está vacía, False en caso contrario.
        """
        return len(self.pila) == 0

    def ver_cima(self) -> Any:
        """Retorna el elemento en la cima de la pila.

        Retorna
        -------
        Any
            Elemento en la cima de la pila.
        """
        return self.pila[-1]

    def vaciar(self) -> Self:
        """Vacía la pila."""
        self.pila.clear()
        return self

    # Operadores aritméticos +, -, -, *, /, //, %, **
    def suma(self) -> Self:
        """Desapila b y a, y apila a + b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a + b)
        return self

    def resta(self) -> Self:
        """Desapila b y a, y apila a - b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a - b)
        return self

    def invertir_signo(self) -> Self:
        """Desapila a y apila -a."""
        a = self.desapilar()
        self.apilar(-a)
        return self

    def multiplicacion(self) -> Self:
        """Desapila b y a, y apila a * b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a * b)
        return self

    def division(self) -> Self:
        """Desapila b y a, y apila a / b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a / b)
        return self

    def division_entera(self) -> Self:
        """Desapila b y a, y apila a // b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a // b)
        return self

    def modulo(self) -> Self:
        """Desapila b y a, y apila a % b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a % b)
        return self

    def potencia(self) -> Self:
        """Desapila b y a, y apila a ** b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a**b)
        return self

    # Operadores de comparación <, <=, ==, !=, >=, >
    def menor_que(self) -> Self:
        """Desapila b y a, y apila a < b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a < b)
        return self

    def menor_o_igual_que(self) -> Self:
        """Desapila b y a, y apila a <= b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a <= b)
        return self

    def igual_que(self) -> Self:
        """Desapila b y a, y apila a == b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a == b)
        return self

    def diferente_que(self) -> Self:
        """Desapila b y a, y apila a != b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a != b)
        return self

    def mayor_o_igual_que(self) -> Self:
        """Desapila b y a, y apila a >= b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a >= b)
        return self

    def mayor_que(self) -> Self:
        """Desapila b y a, y apila a > b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a > b)
        return self

    # Operadores lógicos and, or, not
    def y_logico(self) -> Self:
        """Desapila b y a, y apila a and b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a and b)
        return self

    def o_logico(self) -> Self:
        """Desapila b y a, y apila a or b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a or b)
        return self

    def negacion(self) -> Self:
        """Desapila a y apila not a."""
        a = self.desapilar()
        self.apilar(not a)
        return self

    # Operadores de bits &, |, ^, ~, <<, >>
    def y_bit_a_bit(self) -> Self:
        """Desapila b y a, y apila a & b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a & b)
        return self

    def o_bit_a_bit(self) -> Self:
        """Desapila b y a, y apila a | b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a | b)
        return self

    def xor(self) -> Self:
        """Desapila b y a, y apila a ^ b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a ^ b)
        return self

    def negacion_bit_a_bit(self) -> Self:
        """Desapila a y apila ~a."""
        a = self.desapilar()
        self.apilar(~a)
        return self

    def corrimiento_izquierda(self) -> Self:
        """Desapila b y a, y apila a << b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a << b)
        return self

    def corrimiento_derecha(self) -> Self:
        """Desapila b y a, y apila a >> b."""
        b, a = self.desapilar(), self.desapilar()
        self.apilar(a >> b)
        return self
