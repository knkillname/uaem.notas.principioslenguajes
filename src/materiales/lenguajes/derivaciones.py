from IPython.display import Markdown, display

from .estructuras import Cadena, DerivacionDict
from .gramaticas import GramaticaLibreContexto


class Derivacion:
    def __init__(self, gramatica: GramaticaLibreContexto, cadena: Cadena) -> None:
        self._gramatica = gramatica
        self._cadena = cadena
        self._historial: list[DerivacionDict] = []

    def disponibles(self) -> list[DerivacionDict]:
        return self._gramatica.reglas_aplicables(self._cadena)

    def aplicar(self, regla: DerivacionDict) -> None:
        """Aplica una regla de producción a la cadena."""
        regla = dict(regla)  # Copia de la regla
        regla["cadena"] = self._cadena
        cadena = self._gramatica.aplicar(**regla)
        if cadena != self._cadena:
            self._historial.append(regla)
            self._cadena = cadena

    def interactiva(self) -> None:
        """Realiza una derivación interactiva."""
        # pylint: disable=protected-access
        producciones = self._gramatica.producciones

        def mostrar_disponibles(disponibles: list[DerivacionDict]) -> None:
            if not disponibles:
                display(Markdown("No hay más reglas disponibles."))
                return
            lineas = ["Reglas disponibles:\n"]
            for i, regla in enumerate(disponibles):
                produccion = producciones[regla["n_produccion"]]
                resultado = self._gramatica.aplicar(**regla)
                lineas.append(
                    f"{i + 1}. Aplicar {produccion._repr_markdown_()} para "
                    f"obtener {resultado._repr_markdown_()}"
                )
            lineas.append(f"{len(disponibles) + 1}. Salir")
            display(Markdown("\n".join(lineas)))

        while True:
            disponibles = self.disponibles()
            mostrar_disponibles(disponibles)
            if not disponibles:
                break
            opcion = int(input("Opción: "))
            if opcion > len(disponibles):
                break
            self.aplicar(disponibles[opcion - 1])
            display(Markdown(self._cadena._repr_markdown_()))

    def __str__(self) -> str:
        historial = [str(paso["cadena"]) for paso in self._historial]
        historial.append(str(self._cadena))
        return " ⇒ ".join(historial)

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        historial = [paso["cadena"]._repr_markdown_() for paso in self._historial]
        historial.append(self._cadena._repr_markdown_())

        if not historial:
            return r"$\emptyset$"
        if len(historial) == 1:
            return historial[0]

        lineas = [
            r"$$\begin{align*}",
            rf"{historial[0]} &\Rightarrow {historial[1]} \\",
        ]
        lineas.extend(rf"&\Rightarrow {cadena} \\" for cadena in historial[2:])
        lineas.append(r"\end{align*}$$")

        return "\n".join(lineas)
