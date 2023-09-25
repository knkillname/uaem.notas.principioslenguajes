"""Módulo de gramáticas libres de contexto."""
import collections
import itertools
from collections.abc import Collection, Iterator, Mapping, Sequence
from functools import cached_property
from typing import Self

from .. import notacion
from . import bnf
from .estructuras import (
    Cadena,
    DerivacionDict,
    GramaticaLibreContextoMap,
    MultiProduccion,
    Produccion,
    Terminal,
    Variable,
)

_latex = notacion.obtener_latex


class GramaticaLibreContexto(Mapping[Variable, Sequence[Cadena]]):
    """Representa una gramática libre de contexto."""

    def __init__(self, gramatica: GramaticaLibreContextoMap) -> None:
        """Inicializa la gramática."""
        self._datos: GramaticaLibreContextoMap = gramatica

        # Construir el índice de las producciones.
        indice: dict[Variable, int] = {}
        cuenta = 0
        for izq, der in gramatica.items():
            indice[izq] = cuenta
            cuenta += len(der)

        self._indice = indice

    @classmethod
    def desde_bnf(cls, texto: str) -> Self:
        """
        Construye una gramática a partir de una cadena de texto.

        Parámetros
        ----------
        texto : str
            La cadena de texto en notación BNF.

        Devuelve
        --------
        GramaticaLibreContexto
            La gramática construida.
        """
        return cls(bnf.ParserBNFLibreContexto().diseccionar(texto))

    @cached_property
    def variables(self) -> Collection[Variable]:
        """Devuelve las variables de la gramática."""
        resultado = set(self._datos.keys())
        for cadenas in self._datos.values():
            for cadena in cadenas:
                for simbolo in cadena:
                    if isinstance(simbolo, Variable):
                        resultado.add(simbolo)
        return notacion.Conjunto(resultado)

    @cached_property
    def terminales(self) -> Collection[Terminal]:
        """Devuelve los terminales de la gramática."""
        resultado = set()
        for cadenas in self._datos.values():
            for cadena in cadenas:
                for simbolo in cadena:
                    if isinstance(simbolo, Terminal):
                        resultado.add(simbolo)
        return notacion.Conjunto(resultado)

    @cached_property
    def producciones(self) -> Sequence[Produccion]:
        """Devuelve las reglas de producción de la gramática."""
        resultado = []
        for izq, der in self._datos.items():
            for cadena in der:
                resultado.append(Produccion(izq, Cadena(cadena)))
        return notacion.ListaNumerada(resultado)

    @cached_property
    def variable_inicial(self) -> Variable:
        """Devuelve la variable inicial de la gramática."""
        return next(iter(self._datos.keys()))

    def reglas_aplicables(self, cadena: Cadena) -> Iterator[DerivacionDict]:
        """Devuelve las reglas de producción aplicables a una cadena.

        Parámetros
        ----------
        cadena : Cadena
            La cadena a la que se le aplicarán las reglas de producción.

        Devuelve
        --------
        Sequence[DerivacionDict]
            Las reglas de producción aplicables a la cadena.
        """
        # Encontrar las variables que aparecen en la cadena y contar
        # cuántas veces aparece cada una.
        no_terminales = collections.Counter(
            simbolo for simbolo in cadena if isinstance(simbolo, Variable)
        )

        # Encontrar las reglas de producción aplicables a la cadena.
        for n_produccion, (izq, _) in enumerate(self.producciones):
            if not no_terminales[izq]:  # ¿No aparece la variable en la cadena?
                continue  # Ignoramos la producción.
            # Se puede aplicar la producción.
            yield DerivacionDict(n_produccion=n_produccion)  # A la primera aparición.
            for n_salto in range(1, no_terminales[izq]):
                # A las siguientes apariciones.
                yield DerivacionDict(n_produccion=n_produccion, n_salto=n_salto)

    def hacer_derivacion(self) -> "Derivacion":
        """Inicia una derivación de la gramática."""
        return Derivacion(self)

    def __repr__(self) -> str:
        """Devuelve una representación de la gramática."""
        return f"{self.__class__.__name__}({self._datos!r})"

    def __str__(self) -> str:
        """Devuelve una representación de la gramática."""
        renglones = (MultiProduccion(izq, der) for izq, der in self._datos.items())
        return "\n".join(str(prod) for prod in renglones)

    def _repr_markdown_(self) -> str:
        """Devuelve una representación de la gramática."""
        # pylint: disable=protected-access
        renglones = (MultiProduccion(izq, der) for izq, der in self._datos.items())
        return "\n".join(f"- {prod._repr_markdown_()}" for prod in renglones)

    def _repr_latex_(self) -> str:
        """Devuelve una representación LaTeX de la gramática."""
        # pylint: disable=protected-access
        renglones = [r"$\begin{align*}"]
        for izq, der in self._datos.items():
            renglones.append(rf"{_latex(izq)} & \to {_latex(der)} \\")
        renglones.append(r"\end{align*}$")
        return "${}$".format("\n".join(renglones))

    def __getitem__(self, key: Variable) -> Sequence[Cadena]:
        """Devuelve las producciones de una variable."""
        return self._datos[key]

    def __iter__(self) -> Iterator[Variable]:
        """Devuelve un iterador sobre las variables de la gramática."""
        yield from (self._datos)

    def __len__(self) -> int:
        """Devuelve el número de variables de la gramática."""
        return len(self._datos)


class Derivacion:
    """Representa una derivación de una cadena.

    Atributos
    ---------
    cadena : Cadena
        La cadena actual.
    historial : Sequence[DerivacionDict]
        El historial de la derivación.

    Métodos
    -------
    aplicar(n_produccion, n_salto=0)
        Aplica una regla de producción a la cadena.
    """

    def __init__(self, gramatica: GramaticaLibreContexto) -> None:
        self._gramatica = gramatica
        self._cadena = Cadena([gramatica.variable_inicial])
        self._historial: list[DerivacionDict] = []

    @property
    def cadena(self) -> Cadena:
        """Devuelve la cadena actual."""
        return Cadena(self._cadena)

    @property
    def historial(self) -> Sequence[DerivacionDict]:
        """Devuelve el historial de la derivación."""
        return tuple(self._historial)

    def aplicar(self, n_produccion: int, n_salto: int = 0) -> Self:
        """Aplica una regla de producción a la cadena.

        Parámetros
        ----------
        n_produccion : int
            El índice de la producción a aplicar, comenzando en 1.
        n_salto : int, opcional
            Cuando la variable aparece más de una vez en la cadena, este
            parámetro indica cuál aparición se debe reemplazar. Por
            defecto, se reemplaza la aparición 0 (la más a la
            izquierda).
        """
        derivacion = DerivacionDict(
            cadena=self._cadena, n_produccion=n_produccion - 1, n_salto=n_salto
        )
        self._historial.append(derivacion)
        produccion = self._gramatica.producciones[n_produccion - 1]
        self._cadena = produccion.aplicar(self._cadena, n_salto)
        return self

    def _repr_latex_(self) -> str:
        """Devuelve una representación LaTeX de la derivación."""
        # pylint: disable=protected-access
        if not self._historial:
            return f"${_latex(self._cadena)}$"
        if len(self._historial) == 1:
            return (
                f"${_latex(self._historial[0]['cadena'])} "
                r"\Rightarrow "
                f"{_latex(self._cadena)}$"
            )
        lineas = [r"\begin{align*}"]
        historial = itertools.chain(
            (derivacion["cadena"] for derivacion in self._historial), (self._cadena,)
        )
        inicial = next(historial)
        cadena = next(historial)
        lineas.append(rf"{_latex(inicial)} & \Rightarrow {_latex(cadena)} \\")
        for cadena in historial:
            lineas.append(rf"& \Rightarrow {_latex(cadena)} \\")
        lineas.append(r"\end{align*}")
        return "$${}$$".format("\n".join(lineas))
