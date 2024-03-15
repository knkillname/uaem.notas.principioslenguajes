# Guía de examen para Principios de Lenguajes de Programación

- *Dr. Mario Abarca* `<mario.abarca@uaem.edu.mx>`

## 1. Máquinas abstractas

**Ejercicio 1.1**. (2 pts.)
¿Qué es una máquina abstracta? Define con tus palabras y proporciona tres
ejemplos de máquinas abstractas.

**Ejercicio 1.2**. (2 pts.)
Explica el ciclo *traer-decodificar-ejecutar* de una máquina abstracta.

**Ejercicio 1.3**. (2 pts.)
¿Qué es un lenguaje máquina? ¿Qué relación tiene con una máquina abstracta?

**Ejercicio 1.4**. (2 pts.)
A continuación se muestra el resultado de desensamblar un programa en lenguaje
Python.
Describe qué hace el programa y señala en qué instrucción se almacena el
resultado.

```text
  1           0 RESUME                   0

  2           2 LOAD_FAST                0 (base)
              4 LOAD_FAST                1 (altura)
              6 BINARY_OP                5 (*)
             10 LOAD_CONST               1 (2)
             12 BINARY_OP               11 (/)
             16 STORE_FAST               2 (area)

  3          18 LOAD_FAST                2 (area)
             20 RETURN_VALUE
```

**Ejercicio 1.5**. (4 pts.)
Define qué es un compilador y un intérprete para un lenguaje de programación.
¿Qué semejanzas y diferencias tienen?

**Ejercicio 1.6**. (6 pts.)
¿A qué se le conoce como *lenguaje intermedio* y *máquina virtual*?
¿Por qué es útil en la implementación de lenguajes de programación?

**Ejercicio 1.7**. (4 pts.)
Describe la implementación de estos lenguajes de programación (compilado,
interpretado, mixto, etc.). No olvides justificar tu respuesta.

- C++
- Java
- JavaScript
- Python

## Lenguajes formales

**Ejercicio 2.1**. (4 pts.)
Define los conceptos de *alfabeto*, *cadena* y *lenguaje*.
¿Cuál es la relación entre estos conceptos?

**Ejercicio 2.2**. (1 pts.)
Ordena las siguientes cadenas en orden shortléxico:

- `harina`
- `leche`
- `zanahoria`
- `huevo`

**Ejercicio 2.3**. (2 pts.)
¿El siguiente conjunto es un lenguaje formal? Justifica tu respuesta:

$$L = \{\texttt{monja}, \texttt{jamon}\}$$

**Ejercicio 2.4**. (4 pts.)
Define qué es una gramática libre de contexto.
¿Por qué es importante en el diseño de lenguajes de programación?

**Ejercicio 2.5** (4 pts.)
Considera el siguiente ejemplo de gramática donde la coma “`,`” es parte del
alfabeto.
$$\begin{align*}
E &\to I\texttt{(}A\texttt{)} \\
A &\to I \mid I\texttt{,}A \mid E \\
I &\to \texttt{foo} \mid \texttt{bar} \mid \texttt{baz} \mid \texttt{qux} \\
\end{align*}$$

Identifica las variables, los símbolos terminales y las reglas de producción.

**Ejercicio 2.6** (6 pts.)
Usa la gramática anterior para producir las siguientes cadenas:
- `foo(bar, baz, qux)`
- `foo(bar(baz))`
- `foo(bar(baz), bar(qux))`

**Ejercicio 2.7** (4 pts.)
Dibuja el árbol de derivación para la cadena `foo(bar(baz), bar(qux))` usando
la gramática anterior.

## 3. Paradigmas imperativos

**Ejercicio 3.1** (4 pts.)
¿En qué consiste el paradigma imperativo de lenguajes de programación?
Proporciona un ejemplo.

**Ejercicio 3.2** (4 pts.)
¿Qué es un identificador en un lenguaje de programación y qué es un objeto
denotable?

**Ejercicio 3.3** (2 pts.)
¿Qué es una estructura de control? Proporciona un ejemplo.

**Ejercicio 3.4** (2 pts.)
¿Qué es la programación estructurada?
¿En qué se diferencia de la programación no estructurada?

**Ejercicio 3.5** (2 pts.)
Proporciona un ejemplo de un lenguaje de programación no estructurado y otro
que sí es estructurado.

**Ejercicio 3.6** (4 pts.)
¿Cuáles son los tipos de datos más comunes en los lenguajes de programación?

**Ejercicio 3.7** (2 pts.)
¿Qué significa que un lenguaje de programación sea *fuertemente tipado* o
*débilmente tipado*?

**Ejercicio 3.8** (2 pts.)
¿Qué significa que un lenguaje de programación sea *dinámicamente tipado* o
*estáticamente tipado*?

**Ejercicio 3.9** (4 pts.)
¿Qué es la programaicón orientada a objetos?
Proporciona un ejemplo de lenguaje no orientado a objetos y otro orientado a objetos.

**Ejercicio 3.10** (4 pts.)
¿Qué diferencia hay entre una clase y un objeto?

## 4. Paradigmas declarativos

**Ejercicio 4.1** (4 pts.)
¿Cuál es la diferencia entre un paradigma imperativo y un paradigma declarativo?

**Ejercicio 4.2** (2 pts.)
¿Qué es un lenguaje de programación funcional?

**Ejercicio 4.3** (2 pts.)
¿Qué es una función lambda y para qué se utiliza?

**Ejercicio 4.4** (2 pts.)
¿Qué ventajas tiene el uso de funciones puras en un lenguaje de programación?

## 5. Puntos extra

Para cada uno de los siguientes lenguajes, determina si es un lenguaje de
programación imperativo o declarativo, de tipo estático o dinámico, y si es
fuertemente o débilmente tipado.
Finalmente, determina para qué tipo de aplicaciones es más adecuado.

**Ejercicio 5.1** (2 pts.)
Lenguaje de programación C++.

**Ejercicio 5.2** (2 pts.)
Lenguaje de programación LISP.

**Ejercicio 5.3** (2 pts.)
Lenguaje de programación Java.

**Ejercicio 5.4** (2 pts.)
Lenguaje de programación Python.

**Ejercicio 5.5** (2 pts.)
Lenguaje de programación Haskell.

**Ejercicio 5.6** (2 pts.)
Lenguaje de programación JavaScript.
