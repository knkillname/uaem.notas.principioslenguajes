# Tarea 3: Paradigmas imperativos
<!-- Este es un comentario Markdown; estos comentarios no son visibles en el
documento final. He colocado comentarios como este para indicar el texto que
debes reemplazar. 

POR FAVOR BORRA TODOS LOS COMENTARIOS INCLUYENDO SUS DELIMITADORES "<!––" Y
"––>" ANTES DE ENTREGAR TU TAREA. Y POR FAVOR USA LA FUNCIÓN DE PREVISUALIZACIÓN
DE VISUAL STUDIO CODE PARA VERIFICAR EL FORMATO. -->

- Unidad de aprendizaje: Principios de Lenguajes de Programación
- Facilitador: [Mario Abarca](mailto:mario.abarca@uaem.edu.mx)
- Sujeto de aprendizaje: [<!-- Tu nombre aquí -->](mailto:<!-- Tu correo institucional aquí -->)

----

**Ejercicio 1.**(4 pts.) Lee [este artículo de Wikipedia][paradigmas] sobre los
distintos paradigmas de programación y describe cuál es el paradigma de
programación te parece más interesante y por qué.

*Respuesta:*
<!-- Tu respuesta aquí. -->

**Ejercicio 2.**(8 pts.) Describe las ventajas de utilizar estructuras de
control, como bucles y condicionales, en contraste con el uso de la instrucción
`goto`.
¿Cómo contribuyen estas estructuras a la legibilidad, mantenibilidad y
estructura general del código en comparación con el `goto`?
Proporciona ejemplos concretos para ilustrar tus argumentos.

*Respuesta:*
<!-- Tu respuesta aquí. -->

**Ejercicio 3.**(8 pts.) ¿Qué similitudes y diferencias hay entre el concepto de
*algoritmo* y una función en un lenguaje de programación?
Justifica tu respuesta.

*Respuesta:*
<!-- Tu respuesta aquí. -->

**Ejercicio 4.**(8 pts.) El paso por referencia es un concepto que permite
modificar el valor de una variable en una función y que esa modificación se
refleje fuera de esa función.
Puedes leer más sobre el paso por referencia en
[este artículo de Wikipedia][paso-ref].

Este es un ejemplo de una función que recibe un argumento por referencia en C++:

```c++
#include <iostream>
using namespace std;

void cuadrado(int& n) { n *= n; }

int main() {
  int arg;
  cout << "arg = ";
  cin >> arg;
  cuadrado(arg);
  cout << "arg = " << arg << endl;
  return 0;
}
```

Python no tiene paso por referencia, pero podemos simularlo usando la palabra
reservada `global`.
Averigua cómo funciona y escribe un programa que simule el ejemplo anterior en
Python.

*Respuesta:*
<!--
Tu respuesta aquí debe ser más o menos así:

```python
# Tu código aquí
```
-->

**Ejercicio 5.**(4 pts.) Relacionado al ejercicio anterior, ¿por qué crees que
Python decidió no incluir el paso por referencia en su lenguaje?
¿Qué ventajas y desventajas crees que tiene el paso por referencia?

*Respuesta:*
<!-- Tu respuesta aquí. -->

**Ejercicio 6.**(4 pts.) ¿Qué es lo que aporta la programación orientada a
objetos que no aportan los lenguajes imperativos tradicionales?
¿Por qué crees que la programación orientada a objetos se ha vuelto tan popular?

*Respuesta:*
<!-- Tu respuesta aquí. -->

**Ejercicio 7.**(8 pts. extras) Mira este [video de filosofía][filosofia]; y
escribe un micro ensayo donde respondas a las siguientes preguntas según tu
criterio:

- ¿Existen las variables y objetos denotables en un programa de computadora?
- ¿Qué es lo que existe en un programa de computadora?
- ¿Los programas de computadora son reales?

Justifica tus respuestas.
Nota: el video pertenece a un curso de filosofía de PBS y está en inglés, pero
tiene subtítulos en español disponibles.

*Respuesta:*
<!-- Tu respuesta aquí. -->

<!-- Referencias -->
<!-- OBSERVACIÓN: Nota que los URL de Wikipedia delatan que está escrito en
lenguaje PHP; las páginas no terminan en ".html" sino en ".php".
-->
[paradigmas]: https://es.wikipedia.org/w/index.php?title=Paradigma_de_programaci%C3%B3n&oldid=154946258
[paso-ref]: https://es.wikipedia.org/w/index.php?title=Argumento_(inform%C3%A1tica)&oldid=147312673
[filosofia]: https://youtu.be/Y7v2kESrqDQ?si=9N9UqROcfM0oAMaG
