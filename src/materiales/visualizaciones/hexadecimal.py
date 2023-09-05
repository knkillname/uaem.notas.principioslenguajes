"""Visualizador de bytes en formato hexadecimal.""

Este módulo contiene la clase `VisorHexadecimal`, que permite
visualizar bytes en formato hexadecimal.
"""
import string


def _generar_traductor(car_no_imprimible: str) -> dict[int, str]:
    """Genera un traductor de bytes a caracteres imprimibles.

    Si un byte no es imprimible, se reemplaza por el caracter
    `car_no_imprimible`.

    Parámetros
    ----------
    car_no_imprimible : str
        Caracter que se utiliza para reemplazar los bytes no
        imprimibles.

    Retorna
    -------
    dict[int, str]
        Traductor de bytes a caracteres imprimibles.
    """
    traductor = dict.fromkeys(range(256), car_no_imprimible)
    for car in string.printable:
        traductor[ord(car)] = car
    return traductor


class VisorHexadecimal:
    """Visualizador de bytes en formato hexadecimal.

    Atributos
    ---------
    n_renglon : int
        Cantidad de bytes que se muestran por renglón.
    car_no_imprimible : str
        Caracter que se utiliza para reemplazar los bytes no
        imprimibles.

    Métodos
    -------
    mostrar_bytes(contenido: bytes) -> None
        Muestra el contenido en formato hexadecimal.
    """

    def __init__(
        self,
        n_renglon: int = 10,
        car_no_imprimible: str = "·",
    ) -> None:
        """Inicializa el visualizador.

        Parámetros
        ----------
        n_renglon : int, opcional
            Cantidad de bytes que se muestran por renglón.
            Por defecto, 10.
        car_no_imprimible : str, opcional
            Caracter que se utiliza para reemplazar los bytes no
            imprimibles. Por defecto, "·".
        """
        self._n_renglon: int
        self._car_no_imprimible: str
        self._traductor: dict[int, str]

        self.n_renglon = n_renglon
        self.car_no_imprimible = car_no_imprimible

    @property
    def n_renglon(self) -> int:
        """Cantidad de bytes que se muestran por renglón."""
        return self._n_renglon

    @n_renglon.setter
    def n_renglon(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError(f"Se esperaba un valor positivo, no {valor}.")
        self._n_renglon = int(valor)

    @property
    def car_no_imprimible(self) -> str:
        """Caracter que se usa para reemplazar los bytes no imprimibles."""
        return self._car_no_imprimible

    @car_no_imprimible.setter
    def car_no_imprimible(self, valor: str) -> None:
        if len(valor) != 1:
            raise ValueError(f"Se esperaba un caracter, no {valor}.")
        self._car_no_imprimible = str(valor)
        self._regenerar_traductor()

    def mostrar_bytes(self, contenido: bytes) -> None:
        """Muestra el contenido en formato hexadecimal.

        Parámetros
        ----------
        contenido : bytes
            Contenido a mostrar.
        """
        print(self.representar_bytes(contenido))

    def representar_bytes(self, contenido: bytes) -> str:
        """Representa el contenido en formato hexadecimal.

        Parámetros
        ----------
        contenido : bytes
            Contenido a representar.

        Retorna
        -------
        str
            Representación del contenido en formato hexadecimal.
        """
        renglones: list[str] = []
        for k in range(0, len(contenido), self.n_renglon):
            renglon_bytes = contenido[k : k + self.n_renglon]
            renglon_hex = self._formatear_hex(renglon_bytes)
            renglon_str = self._formatear_str(renglon_bytes)
            renglones.append(f"{renglon_hex}│{renglon_str}")
        return "\n".join(renglones)

    def _regenerar_traductor(self) -> None:
        self._traductor = _generar_traductor(self.car_no_imprimible)

    def _formatear_hex(self, renglon: bytes) -> str:
        resultado = " ".join(f"{byte:02X}" for byte in renglon)
        if len(renglon) < self.n_renglon:
            resultado += "   " * (self.n_renglon - len(renglon))
        return resultado

    def _formatear_str(self, renglon: bytes) -> str:
        return " ".join(map(self._traductor.get, renglon))
