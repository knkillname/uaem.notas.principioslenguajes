# Compilar y ejecutar un programa en ensamblador

## Objetivo
Explora el proceso de compilación y ejecución de un programa en ensamblador y
familiarízate con este lenguaje.

## Descripción
Abre el archivo `hola.asm` y analiza su contenido.
Este programa imprime el mensaje `Hola, mundo!` en la pantalla.
Notarás que el programa se divide en tres secciones: `.data`, `.text` y
`_start`; cada una de estas secciones tiene un propósito específico:
- La sección `.data` se utiliza para declarar variables y constantes.
- La sección `.text` se utiliza para declarar funciones, es decir, bloques de
  código que pueden ser llamados desde otras partes del programa.
- La sección `_start` es la función principal del programa, es decir, es la
  función que se ejecuta primero cuando el programa es ejecutado.

El programa contiene comentarios que explican cada una de las instrucciones
utilizadas.

Para compilar el programa disponemos de dos herramientas: `nasm` y `ld`, ambas
integradas en nuestra imagen de Docker.
- `nasm` es el ensamblador, es decir, es la herramienta que traduce el código
  en ensamblador a lenguaje máquina.
  Nosotros usaremos el formato ELF de 64 bits, que es el formato utilizado por
  los sistemas operativos Linux.
- `ld` es el enlazador, es decir, es la herramienta que se encarga de unir
  nuestro programa con las librerías que utiliza.

## Instrucciones
Abre una terminal en Visual Studio Code y cambia el directorio de trabajo a
`practicas/ensamblador/hola`; para ello, ejecuta el siguiente comando:
```bash
cd practicas/ensamblador/hola
```

Una vez en el directorio de trabajo, ejecuta el siguiente comando para compilar
el programa:
```bash
nasm -f elf64 hola.asm
```
Esto generará un archivo llamado `hola.o` que contiene el código máquina del
programa.
Quizá te interese ver el contenido del archivo `hola.o`; este contenedor de
desarrollo incluye una extensión de Visual Studio Code llamada *Hex Editor* que
te permite ver el contenido de un archivo binario en formato hexadecimal, para
ello solo dale doble clic al archivo `hola.o` y selecciona la opción *Hex
Editor*.
¿Puedes encontrar el mensaje `Hola, mundo!` en el archivo?
La otra variable que se declara en el programa es la longitud del mensaje, que
es 13, ¿puedes encontrarla en el archivo?

A continuación vamos a enlazar el programa con las librerías que utiliza usando
el siguiente comando:
```bash
ld hola.o -o hola
```
Esto generará un archivo llamado `hola` que es el programa ejecutable.
Este archivo debería ser más grande que el archivo `hola.o` porque incluye las
librerías que utiliza el programa.

Antes de poder ejecutar el programa, debemos darle permisos de ejecución usando
el siguiente comando:
```bash
chmod +x hola
```
Finalmente, ejecuta el programa usando el siguiente comando:
```bash
./hola
```
Deberías ver el mensaje `Hola, mundo!` en la pantalla.
