"""Módulo de gramáticas libres de contexto."""
from collections.abc import Collection, Sequence
from typing import Self

from .. import notacion
from . import bnf
from .estructuras import (
    Cadena,
    DerivacionDict,
    GramaticaLibreContextoMap,
    MultiProduccion,
    NoTerminal,
    Produccion,
    Terminal,
)


class GramaticaLibreContexto:
    """Representa una gramática libre de contexto."""

    def __init__(self, gramatica: GramaticaLibreContextoMap) -> None:
        """Inicializa la gramática."""
        self._datos: GramaticaLibreContextoMap = gramatica

    @classmethod
    def desde_cadena(cls, texto: str) -> Self:
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

    @property
    def no_terminales(self) -> Collection[NoTerminal]:
        """Devuelve los no terminales de la gramática."""
        resultado = set(self._datos.keys())
        for cadenas in self._datos.values():
            for cadena in cadenas:
                for simbolo in cadena:
                    if isinstance(simbolo, NoTerminal):
                        resultado.add(simbolo)
        return notacion.Conjunto(resultado)

    @property
    def terminales(self) -> Collection[Terminal]:
        """Devuelve los terminales de la gramática."""
        resultado = set()
        for cadenas in self._datos.values():
            for cadena in cadenas:
                for simbolo in cadena:
                    if isinstance(simbolo, Terminal):
                        resultado.add(simbolo)
        return notacion.Conjunto(resultado)

    @property
    def producciones(self) -> Sequence[Produccion]:
        """Devuelve las reglas de producción de la gramática."""
        resultado = []
        for izq, der in self._datos.items():
            for cadena in der:
                resultado.append(Produccion(izq, tuple(cadena)))
        return notacion.Sucesion(resultado)

    @property
    def simbolo_inicial(self) -> NoTerminal:
        """Devuelve el símbolo inicial de la gramática."""
        return next(iter(self._datos.keys()))

    def aplicar(self, n_produccion: int, cadena: Cadena, n_salto: int = 0) -> Cadena:
        """Aplica una producción de la gramática a una cadena.

        Parámetros
        ----------
        n_produccion : int
            El número de la producción a aplicar.
        cadena : Cadena
            La cadena a la que se le aplicará la producción.
        n_salto : int, opcional
            El número de veces que se omitirá la aplicación de la
            producción de izquierda a derecha.
            Por defecto es 0, lo que significa que se aplicará la
            producción al símbolo no terminal más a la izquierda.

        Devuelve
        --------
        Cadena
            La cadena resultante de aplicar la producción.
        """
        izq, der = self.producciones[n_produccion]

        # Obtenemos los índices de los símbolos no terminales a los que
        # se les puede aplicar la producción.
        indices = [i for (i, simbolo) in enumerate(cadena) if simbolo == izq]

        # Aplicamos la producción al (n_salto)-ésimo símbolo no terminal
        # que coincida con el símbolo izquierdo de la producción.
        if n_salto < len(indices):
            indice = indices[n_salto]
            return cadena[:indice] + der + cadena[indice + 1 :]
        return cadena

    def reglas_aplicables(self, cadena: Cadena) -> Sequence[DerivacionDict]:
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
        resultado = []
        for n_produccion, (izq, _) in enumerate(self.producciones):
            indices = [i for (i, simbolo) in enumerate(cadena) if simbolo == izq]
            resultado.append({"n_produccion": n_produccion})
            for n_salto in range(1, len(indices)):
                resultado.append({"n_produccion": n_produccion, "n_salto": n_salto})
        return resultado

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
