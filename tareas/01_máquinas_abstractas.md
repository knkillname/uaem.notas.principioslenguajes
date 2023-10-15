# Tarea 1: Máquinas abstractas
<!-- Este es un comentario Markdown; estos comentarios no son visibles en el
documento final. He colocado comentarios como este para indicar el texto que
debes reemplazar. -->

- Unidad de aprendizaje: Principios de Lenguajes de Programación
- Facilitador: [Mario Abarca](mailto:mario.abarca@uaem.edu.mx)
- Sujeto de aprendizaje: [<!-- Tu nombre aquí -->](mailto:<!-- Tu correo institucional aquí -->)

----
**Ejercicio 1.**(12 pts.) Proporciona tres ejemplos de máquinas abstractas en
diferentes contextos.

*Respuesta:*

1. <!-- Tu primer ejemplo aquí. -->
2. <!-- Tu segundo ejemplo aquí. -->
3. <!-- Tu tercer ejemplo aquí. -->

**Ejercicio 2.**(4 pts.) Describe en términos generales cómo funciona un
intérprete de un lenguaje de programación.

*Respuesta:* <!-- Tu respuesta aquí. -->

**Ejercicio 3.**(4 pts.) Describe cuáles son las diferencias entre un intérprete
y un compilador. ¿Qué ventajas y desventajas tiene cada uno?

*Respuesta:* <!-- Tu respuesta aquí. -->

**Ejercicio 4.**(4 pts.) Supongamos que tenemos una máquina $M$ que interpreta a
algún lenguaje de programación $A$, pero deseamos correr un programa que escrito en
algún otro lenguaje $B$. ¿Qué podemos hacer para que $M$ pueda correr programas
escritos en $B$?

*Respuesta:* <!-- Tu respuesta aquí. -->

**Ejercicio 5.**(4 pts.) ¿Qué ventajas y desventajas tiene el usar una máquina
intermedia para implementar un lenguaje de programación?

*Respuesta:* <!-- Tu respuesta aquí. -->

**Ejercicio 6.**(4 pts.) Existen lenguajes $A$ (p.ej. Java) que se compilan a un
lenguaje intermedio $B$ (p.ej. [Java Bytecode][1]) y usan un intérprete que lo
ejecuta en una máquina huésped $M$.
La intuición indica que si ya existe un compilador de $A$ a $B$ y un intérprete
de $B$ en $M$, entonces podríamos modificar el compilador de $A$ para que
genere código para $M$ directamente.
¿Qué ventajas y desventajas tiene esta modificación? ¿Por qué no siempre es
posible hacer esta modificación?

*Respuesta:* <!-- Tu respuesta aquí. -->

**Ejercicio 7.**(4 pts.) Sea $f(x_1, x_2, \ldots, x_n)$ una función de $n$
argumentos.
Definimos la [*aplicación parcial*][2] $\mathtt{parcial}(f, x_1^*)$ como la
función $g$ de $n-1$ argumentos que se obtiene al dejar fijo el primer argumento
de $f$ en $x_1^*$, es decir,
$$g(x_2, \ldots, x_n) = f(x_1^*, x_2, \ldots, x_n)$$

Por ejemplo, si $f(x, y) = 3\,x + y$, entonces $\mathtt{parcial}(f, 2)$
es la función $g(y) = f(2, y) = y + 6$.

Según nuestra definición, un intérprete es una función $I(p, d)$ que toma un
programa $p\in A$ y los datos de entrada $d\in D$, y devuelve el resultado de
ejecutar $p(d)$.
Dado un programa concreto $p^*$, ¿qué se obtiene al hacer
$\mathtt{parcial}(I, p^*)$?
Justifica tu respuesta.

*Respuesta:* <!-- Tu respuesta aquí. -->

**Puntos extra.**(4 pts.) Acaba el juego [Human Resource Machine][3] y manda una
fotografía de ti junto con el mensaje de felicitación que aparece al final del
juego como evidencia de que lo completaste.

<!-- Referencias a continuación: -->
[1]: https://en.wikipedia.org/wiki/Java_bytecode
[2]: https://en.wikipedia.org/wiki/Partial_application
[3]: http://tomorrowcorporation.com/humanresourcemachine
