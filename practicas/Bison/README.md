# Explorando una gramática de ejemplo con Bison

## 1. Objetivo

Comprender la aplicación de las Gramáticas Libres de Contexto y la notación BNF
en el mundo real a través de un ejemplo práctico utilizando [Bison][1].
Esta comprensión no solo proporciona una base sólida en teoría de lenguajes
formales, sino que también les facilitará la introducción a campos avanzados de
la Inteligencia Artificial, como el procesamiento de lenguaje natural y el
desarrollo de compiladores para desafíos complejos en el procesamiento de datos
no estructurados y la construcción de sistemas de software avanzados.

## 2. Descripción

En esta práctica exploraremos una [gramática de ejemplo][2] utilizando Bison.

### Bison: un generador de analizadores sintácticos

Bison es una herramienta que nos permite generar un analizador sintáctico a
partir de una gramática libre de contexto.

Bison recibe como entrada un archivo de texto que contiene la gramática en
notación BNF así como el código en lenguaje C/C++/Java que implementa la
semántica de la gramática; a continuación, Bison genera un archivo en lenguaje
C/C++/Java que contiene el analizador sintáctico para dicha gramática.

El ejemplo en concreto es una calculadora de[notación polaca inversa][3].

### La notación polaca inversa

La notación polaca inversa es una forma sencilla de representar expresiones
matemáticas que no requiere de paréntesis ni de precedencia de operadores; en
esta notación los operadores se escriben después de los operandos, por ejemplo,
escribimos $a\,b\,+$ en lugar de $a+b$, $a\,b\,\cdot\,c\,+$ en lugar de $a\cdot
b+c$.

Una forma de pensar en la notación polaca inversa es mediante dos reglas de
lectura:

1. Cuando leemos un operando como $a$, $\pi$ o $1.618$, lo agregamos a la cima
   de una pila de operandos.
2. Cuando leemos un operador como $+$, $\cdot$ o $\div$, sacamos dos operandos
   de la cima de la pila, los operamos (sumamos, multiplicamos, etc.) y
   agregamos el resultado a la cima de la pila.
   Algunos operadores, como $\sqrt{\phantom{x}}$ y $\neg$, solo requieren un
   operando, mientras que $\sum$ y $\prod$ requieren un número variable de
   operandos.

En algún universo paralelo donde la notación polaca inversa es la forma estándar
de escribir álgebra, la [fórmula chicharronera][4] para resolver polinomios de
segundo grado la escriben así:
$$b\,\neg\,b\,2\,\uparrow\,4\,a\,\cdot\,c\,\cdot\,-\,\sqrt{\phantom{x}}\,\pm\,2
\,a\,\cdot\,\div\,x\,=$$
Aquí hemos usado $\neg$ para representar el operador de cambio de signo,
$\uparrow$ para representar el operador de potencia, y $\sqrt{\phantom{x}}$ para
representar el operador de raíz cuadrada.

## 3. Instrucciones

Abre una terminal en Visual Studio Code y cambia el directorio de trabajo a
`practicas/Bison`; para ello, ejecuta el siguiente comando:

```bash
cd practicas/Bison
```

Copia el ejemplo desde la documentación de Bison:

```bash
cp -r /usr/share/doc/bison/examples/c/rpcalc .
```

Deberías ver un nuevo directorio llamado `rpcalc` en el explorador de archivos
de Visual Studio Code, justo dentro del directorio `practicas/Bison`.
Abre el documento `rpcalc.y`, explora su contenido y resuelve las siguientes
preguntas:

- ¿Dónde se define la gramática?
- ¿Qué parecido tiene esta notación a la BNF estándar?
- ¿Dónde se define la semántica de la gramática?
- ¿Qué hace la función `main`?
- ¿Cómo funciona el analizador léxico `yylex`?

A continuación, compila el programa usando el siguiente comando:

```bash
bison rpcalc.y
```

Deberías de ver un nuevo archivo llamado `rpcalc.tab.c` que contiene el código
en lenguaje C que implementa el analizador sintáctico y la semántica de la
gramática.
La función `main` se encuentra al final de este archivo; busca las funciones
`yylex` y `yyparse` en este archivo.

Finalmente, compila el programa usando el siguiente comando:

```bash
gcc -o rpcalc rpcalc.tab.c -lm
```

Ahora deberías tener un nuevo archivo llamado `rpcalc` en el directorio actual.
Este es un programa ejecutable en lenguaje máquina que implementa la calculadora
de notación polaca inversa.
Ejecútalo desde la terminal usando el siguiente comando:

```bash
./rpcalc
```

Prueba escribiendo algo simple como `1 2 + 3 *` y presiona la tecla ↲.
Para salir presiona la combinación de teclas **Ctrl+Z**.

[1]: https://www.gnu.org/software/bison/
[2]: https://www.gnu.org/software/bison/manual/html_node/RPN-Calc.html
[3]: https://es.wikipedia.org/wiki/Notaci%C3%B3n_polaca_inversa
[4]: https://es.wikipedia.org/w/index.php?title=Ecuaci%C3%B3n_de_segundo_grado&oldid=152292972#Soluciones_de_la_ecuaci%C3%B3n_de_segundo_grado