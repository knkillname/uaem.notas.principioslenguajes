from collections.abc import Collection, Mapping, Sequence


class GramaticaLibreDeContexto:
    def __init__(
        self,
        no_terminales: str,
        terminales: str,
        producciones: Sequence[tuple[str, str]],
        inicial: str,
    ):
        self.no_terminales: Collection[str] = frozenset(no_terminales)
        self.terminales: Collection[str] = frozenset(terminales)
        self.producciones: Sequence[tuple[str, str]] = list(dict(producciones).items())
        self.inicial: str = inicial

    def usar_regla(self, n_produccion: int, cadena: str) -> str:
        """
        Reemplazar un no terminal en una cadena mediante una producción.

        Parámetros
        ----------
        n_produccion : int
            Índice de la producción a aplicar.
        cadena : str
            Cadena en la que se reemplazará el no terminal.

        Regresa
        -------
        str
            Cadena con el no terminal reemplazado por la producción.
        """
        no_terminal, produccion = self.producciones[n_produccion]
        return cadena.replace(no_terminal, produccion, 1)

    def es_terminal(self, simbolo: str) -> bool:
        """
        Verificar si un símbolo es terminal.

        Parámetros
        ----------
        simbolo : str
            Símbolo a verificar.

        Regresa
        -------
        bool
            `True` si el símbolo es terminal, `False` en otro caso.
        """
        return simbolo in self.terminales

    def es_no_terminal(self, simbolo: str) -> bool:
        """
        Verificar si un símbolo es no terminal.

        Parámetros
        ----------
        simbolo : str
            Símbolo a verificar.

        Regresa
        -------
        bool
            `True` si el símbolo es no terminal, `False` en otro caso.
        """
        return simbolo in self.no_terminales

    def contiene_no_terminales(self, cadena: str) -> bool:
        """
        Verificar si una cadena contiene no terminales.

        Parámetros
        ----------
        cadena : str
            Cadena a verificar.

        Regresa
        -------
        bool
            `True` si la cadena contiene no terminales, `False` en
            caso contrario.
        """
        return any(no_terminal in cadena for no_terminal in self.no_terminales)

    # Métodos mágicos
    def __str__(self) -> str:
        """Convierte la gramática a una cadena de caracteres."""
        nt_ = f"{{{', '.join(self.no_terminales)}}}"
        ter = f"{{{', '.join(self.terminales)}}}"
        aux_p = (
            f"{no_terminal} → {produccion}"
            for no_terminal, produccion in self.producciones.items()
        )
        pro = f"{{{', '.join(aux_p)}}}"
        return f"(N={nt_}, T={ter}, P={pro}, S={self.inicial})"

    def __repr__(self) -> str:
        """Representa la gramática como una cadena de caracteres."""
        clase = type(self).__name__
        return (
            f"{clase}({list(self.no_terminales)}, {list(self.terminales)}, "
            f"{dict(self.producciones)}, {self.inicial})"
        )

    def _repr_markdown_(self) -> str:
        """Representa la gramática como en Markdown."""
        renglones = ["$G = (N, T, P, S)$, donde:"]
        nt_ = ", ".join(self.no_terminales)
        renglones.append(f"* $N = {{{nt_}}}$")
        ter = ", ".join(self.terminales)
        renglones.append(f"* $T = {{{ter}}}$")

        renglones.append("* $P$ es un conjunto con los siguientes elementos:")
        renglones.append("$$\\begin{align}")
        for terminal, produccion in self.producciones.items():
            renglones.append(f"  {terminal} &\\to {produccion} \\\\")
        renglones.append("\\end{align}$$")

        renglones.append(f"* $S = {self.inicial}$")
