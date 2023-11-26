# Tarea 2: Lenguajes Formales
<!-- Este es un comentario Markdown; estos comentarios no son visibles en el
documento final. He colocado comentarios como este para indicar el texto que
debes reemplazar. -->

- Unidad de aprendizaje: Principios de Lenguajes de Programación
- Facilitador: [Mario Abarca](mailto:mario.abarca@uaem.edu.mx)
- Sujeto de aprendizaje: [<!-- Tu nombre aquí -->](mailto:<!-- Tu correo institucional aquí -->)

----
**Ejercicio 1.**(8 pts.) Explica en un enunciado qué significa que una
gramática sea ambigua y luego muestra que efectivamente la siguiente gramática
es ambigua:
$$\begin{align*}
E &\to T | T \texttt{+} E | T \texttt{-} E \\
T &\to A | E \texttt{*} T \\
A &\to I | \texttt{-(}A\texttt{)} | \texttt{(}E\texttt{)} \\
I &\to \texttt{a} | \texttt{b} | I\texttt{a} | I\texttt{b} \\
\end{align*}$$

*Respuesta:* <!-- Tu respuesta aquí. Debe ser más o menos así: "Una gramática es
ambigua cuando tal y tal. Esta gramática es ambigua porque, como podemos ver en
este ejemplo, bla bla bla." -->

**Ejercicio 2.**(12 pts.) Proporciona una gramática no ambigua para la sentencia
`if-then-else` de un lenguaje de programación, de manera que el siguiente
segmento de código sea válido, y justifica tu respuesta:

```basic
if foo then if bar then baz else qux
```

*Respuesta:*
<!-- Tu respuesta aquí, debe ser más o menos así:
La gramática que propongo es esta:
$$\begin{align*}
... &\to ... \\
... &\to ... \\
...
\end{align*}$$
Mi gramática evita la ambigüedad porque tal y tal. Por ejemplo, la sentencia
`if foo then if bar then baz else baz` tiene una única interpretación en mi
gramática como se muestra a continuación: ...
-->

**Ejercicio 3.**(8 pts.) Crea una gramática para el lenguaje de los paréntesis
bien balanceados, es decir, el lenguaje que contiene a las cadenas de paréntesis
`(` y `)` tales que cada paréntesis abierto tiene un paréntesis cerrado
correspondiente y viceversa. Tu gramática debe de poder generar cadenas como
`((()))`, `()()()`, `(()(()))`, etc., pero no cadenas como `)()`, `())`, etc.
Justifica tu respuesta. 4 puntos extra si puedes hacer tu gramática con solo dos
reglas y una variable.

*Respuesta:* <!-- Tu respuesta aquí. -->

**Ejercicio 4.**(8 pts.) Una gramática es *regular* si todas sus reglas producen
un símbolo terminal seguido de una variable con la única excepción de que la
variable inicial también puede producir la cadena vacía.
Es decir que si $G$ es una gramática regular, entonces todas sus reglas solo
pueden tener tres formas posibles $A \to aB$, $A \to a$ o $S \to \varepsilon$,
donde $A$ y $B$ son variables, $a$ es un símbolo terminal y $S$ es la variable
inicial.
Ahora bien, considera el siguiente lenguaje
$$L = \{ \texttt{a}^n \texttt{b}^n \mid n \geq 0 \}$$
este es el lenguaje de todas las cadenas de `a` seguidas de la misma cantidad de
`b`, incluyendo la cadena vacía.
Tu misión es explicar por qué $L$ no es regular, es decir, por qué cualquier
gramática que genere $L$ debe tener al menos una regla que no sea como de las
tres formas mencionadas anteriormente.

*Respuesta:* <!-- No creo que se pueda. Porque si intetmos hacer una
grámitca (así y asá) ... encontramos entonces que tiene el problema ... -->
