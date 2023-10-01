"""Módulo de gramáticas libres de contexto."""
import collections
import dataclasses
import html
import itertools
from collections import Counter
from collections.abc import Collection, Iterator, Mapping, Sequence
from functools import cached_property
from typing import NamedTuple, Self

import pygraphviz  # type: ignore

import materiales.lenguajes.latex  # type: ignore

from .. import notacion
from . import bnf
from .estructuras import (
    Cadena,
    DerivacionDict,
    GramaticaLibreContextoMap,
    MultiRegla,
    Regla,
    Simbolo,
    Terminal,
    Variable,
)

_latex = materiales.lenguajes.latex.obtener_latex


class GramaticaLibreContexto(Mapping[Variable, Sequence[Cadena]]):
    """Representa una gramática libre de contexto."""

    def __init__(self, gramatica: GramaticaLibreContextoMap) -> None:
        """Inicializa la gramática."""
        self._validar_gramatica(gramatica)
        self._datos: GramaticaLibreContextoMap = gramatica

    def _validar_gramatica(self, gramatica):
        if not isinstance(gramatica, Mapping):
            if isinstance(gramatica, str):
                clase = self.__class__.__name__
                raise TypeError(
                    "La gramática debe ser un diccionario. Si quieres "
                    "construir una gramática a partir de una cadena de "
                    f"texto, usa el método '{clase}.desde_bnf'."
                )
            raise TypeError("La gramática debe ser un diccionario.")
        for izq, der in gramatica.items():
            if not isinstance(izq, Variable):
                raise TypeError(
                    f"La variable izquierda '{izq}' no es una variable válida."
                )
            if not isinstance(der, Sequence):
                raise TypeError(
                    f"La variable derecha '{der}' no es una sucesión válida."
                )
            for cadena in der:
                if not isinstance(cadena, Sequence):
                    raise TypeError(f"La cadena '{cadena}' no es una sucesión válida.")
                for simbolo in cadena:
                    if not isinstance(simbolo, Simbolo):
                        raise TypeError(
                            f"El símbolo '{simbolo}' no es un símbolo válido."
                        )

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
        resultado: set[Terminal] = set()
        for cadenas in self._datos.values():
            for cadena in cadenas:
                for simbolo in cadena:
                    if isinstance(simbolo, Terminal):
                        resultado.add(simbolo)
        return notacion.Conjunto(resultado)

    @cached_property
    def reglas(self) -> Sequence[Regla]:
        """Devuelve las reglas de producción de la gramática."""
        resultado = []
        for izq, der in self._datos.items():
            for cadena in der:
                resultado.append(Regla(izq, Cadena(cadena)))
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
        no_terminales = Counter(
            simbolo for simbolo in cadena if isinstance(simbolo, Variable)
        )

        # Encontrar las reglas de producción aplicables a la cadena.
        for n_regla, (izq, _) in enumerate(self.reglas):
            if not no_terminales[izq]:  # ¿No aparece la variable en la cadena?
                continue  # Ignoramos la producción.
            # Se puede aplicar la producción.
            yield DerivacionDict(n_regla=n_regla)  # A la primera aparición.
            for n_salto in range(1, no_terminales[izq]):
                # A las siguientes apariciones.
                yield DerivacionDict(n_regla=n_regla, n_salto=n_salto)

    def producir_lenguaje(self) -> Iterator[str]:
        """Enumera todas las cadenas del lenguaje de la gramática."""
        cadenas: collections.deque[list[Simbolo]]
        cadenas = collections.deque([[self.variable_inicial]])
        while cadenas:
            palabra = cadenas.popleft()
            cadena = (i for i, sim in enumerate(palabra) if isinstance(sim, Variable))
            try:
                # Encontrar el índice de la variable más a la izquierda.
                i = next(cadena)
            except StopIteration:
                # No hay más variables en la palabra.
                yield "".join(sim.valor for sim in palabra)
                continue
            # Realizar todas las sustituciones posibles para esa variable.
            variable = palabra[i]
            assert isinstance(variable, Variable)
            for sustitucion in self[variable]:
                nueva = [*palabra[:i], *sustitucion, *palabra[i + 1 :]]
                cadenas.append(nueva)  # Agregar la nueva palabra al final de la cola.

    def hacer_derivacion(self) -> "Derivacion":
        """Inicia una derivación de la gramática."""
        return Derivacion(self)

    def __repr__(self) -> str:
        """Devuelve una representación de la gramática."""
        return f"{self.__class__.__name__}({self._datos!r})"

    def __str__(self) -> str:
        """Devuelve una representación de la gramática."""
        renglones = (MultiRegla(izq, der) for izq, der in self._datos.items())
        return "\n".join(str(prod) for prod in renglones)

    def _repr_markdown_(self) -> str:
        """Devuelve una representación de la gramática."""
        # pylint: disable=protected-access
        renglones = (MultiRegla(izq, der) for izq, der in self._datos.items())
        return "\n".join(f"- {prod._repr_markdown_()}" for prod in renglones)

    def _repr_latex_(self) -> str:
        """Devuelve una representación LaTeX de la gramática."""
        # pylint: disable=protected-access
        renglones = [r"$\begin{align*}"]
        for izq, der in self._datos.items():
            renglones.append(rf"{_latex(izq)} & \to {_latex(der)} \\")
        renglones.append(r"\end{align*}$")
        return r"${}$".format("\n".join(renglones))

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
    aplicar(n_regla, n_salto=0)
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

    def aplicar_regla(self, n_regla: int, n_salto: int = 0) -> Self:
        """Aplica una regla de producción a la cadena.

        Parámetros
        ----------
        n_regla : int
            El índice de la producción a aplicar, comenzando en 1.
        n_salto : int, opcional
            Cuando la variable aparece más de una vez en la cadena, este
            parámetro indica cuál aparición se debe reemplazar. Por
            defecto, se reemplaza la aparición 0 (la más a la
            izquierda).
        """
        derivacion = DerivacionDict(
            cadena=self._cadena, n_regla=n_regla - 1, n_salto=n_salto
        )
        self._historial.append(derivacion)
        regla = self._gramatica.reglas[n_regla - 1]
        self._cadena = regla.aplicar(self._cadena, n_salto)
        return self

    def arbol(self) -> "ArbolDeDerivacion":
        """Devuelve el árbol de derivación."""
        return ArbolDeDerivacion(self, self._gramatica)

    def _repr_latex_(self) -> str:
        """Devuelve una representación LaTeX de la derivación."""
        # pylint: disable=protected-access
        comentario_fmt = r"\text{{(por regla {})}}"
        if not self._historial:
            return f"${_latex(self._cadena)}$"
        if len(self._historial) == 1:
            n_regla = self._historial[0]["n_regla"] + 1
            return (
                f"${_latex(self._historial[0]['cadena'])} "
                r"\Rightarrow "
                rf"{_latex(self._cadena)} \qquad {comentario_fmt.format(n_regla)}$"
            )
        lineas = [r"\begin{align*}"]  # Lista de líneas de LaTeX.
        cadenas: Iterator[Cadena]
        cadenas = (derivacion["cadena"] for derivacion in self._historial)
        cadenas = itertools.chain(cadenas, (self._cadena,))  # Agregar la cadena final.
        reglas = (derivacion["n_regla"] + 1 for derivacion in self._historial)
        cad_inicial = next(cadenas)
        cadena, n_regla = next(cadenas), next(reglas)
        comentario = comentario_fmt.format(n_regla)
        lineas.append(
            rf"{_latex(cad_inicial)} & \Rightarrow {_latex(cadena)} & {comentario} \\"
        )
        for cadena, n_regla in zip(cadenas, reglas):
            comentario = comentario_fmt.format(n_regla)
            lineas.append(rf"& \Rightarrow {_latex(cadena)} & {comentario}\\")
        lineas.append(r"\end{align*}")
        return "$${}$$".format("\n".join(lineas))


class Nodo(NamedTuple):
    """Representa un nodo del árbol de derivación.

    Atributos
    ---------
    nombre : str
        Identificador único del nodo.
    simbolo : Simbolo
        Símbolo asociado con el nodo.
    """

    nombre: str
    simbolo: Simbolo


_ATTRS_DEFECTO = {
    "grafo": {"fontname": "serif", "nodesep": "0.5"},
    "nodos": {"oridering": "out", "shape": "plain"},
    "aristas": {"color": "cornflowerblue", "arrowhead": "none"},
    "variables": {"fontcolor": "firebrick"},
    "terminales": {"fontname": "monospace"},
    "epsilon": {"fontcolor": "slategray"},
}


@dataclasses.dataclass
class AtributosArbol:
    """Representa los atributos de un árbol de derivación.

    Atributos
    ---------
    grafo : dict[str, str]
        Atributos del grafo.
    nodos : dict[str, str]
        Atributos de los nodos.
    aristas : dict[str, str]
        Atributos de las aristas.
    variables : dict[str, str]
        Atributos de los nodos asociados con variables.
    terminales : dict[str, str]
        Atributos de los nodos asociados con terminales.
    epsilon : dict[str, str]
        Atributos de los nodos asociados con la cadena vacía.
    """

    grafo: dict[str, str] = dataclasses.field(
        default_factory=_ATTRS_DEFECTO["grafo"].copy
    )
    nodos: dict[str, str] = dataclasses.field(
        default_factory=_ATTRS_DEFECTO["nodos"].copy
    )
    aristas: dict[str, str] = dataclasses.field(
        default_factory=_ATTRS_DEFECTO["aristas"].copy
    )
    variables: dict[str, str] = dataclasses.field(
        default_factory=_ATTRS_DEFECTO["variables"].copy
    )
    terminales: dict[str, str] = dataclasses.field(
        default_factory=_ATTRS_DEFECTO["terminales"].copy
    )
    epsilon: dict[str, str] = dataclasses.field(
        default_factory=_ATTRS_DEFECTO["epsilon"].copy
    )


class ArbolDeDerivacion:
    """Representa un árbol de derivación.

    Atributos
    ---------
    attrs_nodos : dict[str, str]
        Atributos de los nodos.
    attrs_variables : dict[str, str]
        Atributos de los nodos asociados con variables.
    attrs_terminales : dict[str, str]
        Atributos de los nodos asociados con terminales.
    fmt_variable : str
        Formato de los nodos asociados con variables.
    fmt_terminal : str
        Formato de los nodos asociados con terminales.

    Métodos
    -------
    a_graphviz()
        Devuelve el árbol de derivación en formato Graphviz.
    """

    def __init__(
        self,
        derivacion: Derivacion,
        gramatica: GramaticaLibreContexto,
        *,  # Parámetros opcionales y nombrados a partir de aquí.
        atributos: AtributosArbol | None = None,
    ) -> None:
        self._derivacion = derivacion
        self._gramatica = gramatica
        self._arbol: pygraphviz.AGraph
        self._cuenta_etiquetas: Counter[str] = Counter()
        self._atributos = atributos if atributos is not None else AtributosArbol()

        self.reconstruir_arbol()

    def a_graphviz(self) -> str:
        """Devuelve el árbol de derivación en formato Graphviz."""
        return str(self._arbol)

    def a_svg(self) -> str:
        """Devuelve una representación SVG del árbol de derivación."""
        resultado = self._arbol.draw(format="svg", prog="dot")
        if resultado is None:
            raise RuntimeError("Error al generar el SVG.")
        assert isinstance(resultado, bytes)
        return resultado.decode("utf-8")

    @property
    def atributos(self) -> AtributosArbol:
        """Devuelve los atributos del árbol de derivación."""
        return self._atributos

    def _repr_svg_(self) -> str:
        """Devuelve una representación SVG del árbol de derivación."""
        return self.a_svg()

    def etiquetar_variable(self, simbolo: Variable) -> str:
        """Devuelve la etiqueta asociada con una variable.

        Parámetros
        ----------
        simbolo : Variable
            La variable a etiquetar.

        Devuelve
        --------
        str
            La etiqueta asociada con la variable.
        """
        return f"<<i>{html.escape(simbolo.valor)}</i>>"

    def etiquetar_terminal(self, simbolo: Terminal) -> str:
        """Devuelve la etiqueta asociada con un terminal.

        Parámetros
        ----------
        simbolo : Terminal
            El símbolo terminal a etiquetar.

        Devuelve
        --------
        str
            La etiqueta asociada con el terminal.
        """
        if not simbolo.valor:  # ¿Es la cadena vacía?
            return "<<i>ε</i>>"
        # Reemplazar espacios en blanco por espacios visibles:
        return simbolo.valor.replace(" ", "␣").replace("\t", "␉").replace("\n", "␤")

    def nombrar(self, simbolo: Simbolo) -> str:
        """Devuelve un id único para un nodo asociado con un símbolo.

        Parámetros
        ----------
        simbolo : Simbolo
            El símbolo asociado con el nodo.

        Devuelve
        --------
        str
            Un id único para el nodo.
        """
        etiqueta = "var_" if isinstance(simbolo, Variable) else "trm_"
        etiqueta += simbolo.valor or "ε"
        self._cuenta_etiquetas[etiqueta] += 1
        return f"{etiqueta}{self._cuenta_etiquetas[etiqueta]}"

    def crear_nodo(self, simbolo: Simbolo) -> Nodo:
        """Crea un nodo asociado con un símbolo."""
        assert self._arbol is not None
        nombre = self.nombrar(simbolo)
        if isinstance(simbolo, Variable):
            etiqueta = self.etiquetar_variable(simbolo)
            attrs = self.atributos.variables
        else:
            assert isinstance(simbolo, Terminal)  # Si no es variable, es terminal.
            etiqueta = self.etiquetar_terminal(simbolo)
            attrs = self.atributos.terminales
            if not simbolo.valor:
                attrs = self.atributos.epsilon

        self._arbol.add_node(nombre, label=etiqueta, **attrs)
        return Nodo(nombre=nombre, simbolo=simbolo)

    def encontrar_nodo(self, simbolo: Simbolo, nodos: list[Nodo], n_salto: int) -> int:
        """Encuentra el nodo asociado con un símbolo."""
        indices = (i for i, nodo in enumerate(nodos) if nodo.simbolo == simbolo)
        return next(itertools.islice(indices, n_salto, None), -1)

    def reconstruir_arbol(self) -> Self:
        """Construye el árbol de derivación."""
        producciones = self._gramatica.reglas

        # Crear el árbol de derivación.
        arbol = self._arbol = pygraphviz.AGraph(directed=True, strict=True)
        arbol.graph_attr.update(self.atributos.grafo)
        arbol.node_attr.update(self.atributos.nodos)
        arbol.edge_attr.update(self.atributos.aristas)

        # Crear la raíz, que a su vez es la primera hoja.
        raiz = self.crear_nodo(self._gramatica.variable_inicial)
        hojas: list[Nodo] = [raiz]  # Hojas que contienen variables.

        # Iterar sobre historial de reemplazos.
        for derivacion in self._derivacion.historial:
            # Obtener la producción que se aplicó.
            izq, der = producciones[derivacion["n_regla"]]

            # Encontrar índice del nodo a expandir.
            i = self.encontrar_nodo(izq, hojas, derivacion["n_salto"])
            if i == -1:
                continue  # No hay nada que hacer.
            nodo = hojas[i]

            # Crear nodos hijos y conectarlos.
            hijos = [self.crear_nodo(simbolo) for simbolo in der]
            if not hijos:  # ¿La producción es vacía?
                hijos = [self.crear_nodo(Terminal(""))]
            for hijo in hijos:
                self._arbol.add_edge(nodo.nombre, hijo.nombre)

            # Reemplazar nodo por hijos en las hojas
            hojas[i : i + 1] = (v for v in hijos if isinstance(v.simbolo, Variable))
        return self
