# uaem.notas.principioslenguajes

Notas de curso Principios de Lenguajes de Programación de la [Universidad
Autónoma del Estado de Morelos][1].

— *Dr. Mario Abarca*

## 1. Inicio rápido

Antes de comenzar se deben de cumplir los siguientes requisitos:

- Tener instalado [Git][2].
- Tener instalado el motor de [Docker][3]; en las computadoras con Windows se
  requiere instalar previamente el [Subsistema de Windows para Linux][7] y,
  además, se requiere tener abierto la aplicación [*Docker Desktop*][11] previo
  a abrir el proyecto.
- Tener instalado [Visual Studio Code][4].
- Tener instalado el plugin de [Dev Containers][5] en Visual Studio Code.

Una vez cumplidos los requisitos, se debe de clonar el repositorio y abrirlo en
Visual Studio Code.
Para ello basta abrir Visual Studio Code, acceder a la vista de *control de
versiones* y clonar el repositorio con la siguiente URL:
`https://github.com/knkillname/uaem.notas.principioslenguajes.git`

![Clona el repositorio](https://code.visualstudio.com/assets/docs/sourcecontrol/intro/github-clone.png)

Una vez clonado el repositorio, Visual Studio Code detectará que el proyecto
puede ser abierto en un contenedor de Docker y preguntará si se desea abrir en
un contenedor.
Se debe de aceptar y esperar a que se construya el contenedor.
Una vez construido el contenedor, se puede acceder a las notas desde el
directorio *notas*.

## 2. Estructura del repositorio

El repositorio está estructurado de la siguiente manera:

- `notas`: Contiene las notas del curso.
  Estas se conforman de cuadernos de Jupyter y algunos recursos didácticos en el
  subdirectorio `recursos`.
  Las notas están enumeradas de acuerdo al orden en que se ven en el curso.
- `practicas`: Contiene las prácticas del curso. Estas contienen recursos
  varios como código fuente e instrucciones.
- `src`: Contiene el código fuente de los cuadernos de Jupyter. Aquí es donde
  se almacenan los materiales didácticos para las notas, como simuladores y
  ejemplos. El directorio está estructurado como un paquete de Python.
- `test`: Contiene los archivos de prueba para los materiales didácticos del
  directorio `src`.
- Archivos de configuración y herramientas para el desarrollo:
  - El directorio `.devcontainer` contiene los archivos de configuración para
    el contenedor de Docker que se utiliza en Visual Studio Code.
  - El directorio `.vscode` contiene los archivos de configuración para
    Visual Studio Code.
  - `.gitignore` contiene los patrones de archivos que se ignoran en el
    control de versiones, de manera que el repositorio no se llene de archivos
    innecesarios.
  - `LICENCE` contiene la licencia del repositorio.
  - `Makefile` contiene las instrucciones para construir los materiales
    didácticos del directorio `src` y ejecutar las pruebas del directorio
    `test`.
  - `Pipfile` y `Pipfile.lock` contienen las dependencias de los materiales
    didácticos del directorio `src`, es decir, las bibliotecas de Python que
    se utilizan en los cuadernos de Jupyter.
  - `pyproject.toml` contiene la configuración para construir los materiales
    didácticos del directorio `src` con [Hatch][6].
  - `README.md` es este archivo que te encuentras leyendo.

## 3. Preguntas frecuentes

### ¿Qué es Markdown y cómo lo uso para seguir las prácticas y tareas?

[Markdown][9] es un lenguaje formal para escribir texto enriquecido (con letras
en negritas, cursivas, etc.).
Todo programador debería considerar Markdown porque es muy útil para escribir
documentación de código y tomar notas rápidas (ver [appflowy][20]).
Lo usan sitios como GitHub, Reddit, Stack Overflow, y muchos otros.
Te recomiendo mirar [este tutorial](https://youtu.be/X5mkZXmaKp4) para
aprender a usarlo en 3 minutos.

Algunas variantes de Markdown también soportan ecuaciones en lenguaje $\LaTeX$,
y son particularmente muy usadas en este repositorio.
Revisa el capítulo 3 de [La introducción no-tan-corta a
$\LaTeX\,2_\varepsilon$][10] para aprender más.

### ¿Qué es un cuaderno de Jupyter?

Los cuadernos de [Jupyter][8] son documentos interactivos que permiten combinar
código, texto, imágenes, y otros elementos en un solo lugar.
Puedes pensar en ellos como documentos de Word que te permiten ejecutar código e
interactuar con él.
Los materiales del curso están escritos en cuadernos de Jupyter porque permiten
combinar la teoría con la práctica de una manera muy sencilla.

Jupyter usa un sistema de celdas para organizar el contenido de los cuadernos;
algunas son celdas de código (generalmente Python), otras son celdas de texto
en formato Markdown.

### ¿Qué es un repositorio de GitHub y cómo lo utilizo?

Un repositorio de GitHub es un lugar donde se almacenan archivos de código
fuente y otros recursos de un proyecto.
GitHub funciona con un sistema de control de versiones llamado *Git*.
Este lleva un registro de los cambios que se hacen a los archivos (qué, cuándo,
y quién), de manera que cuando se comete un error se puede regresar a una
versión anterior.

Para utilizarlo, se debe de instalar Git y clonar el repositorio.
En los párrafos anteriores se explica cómo hacerlo mediante Visual Studio Code.
Solo asegúrate de descargar los cambios más recientes de vez en cuando
utilizando el ícono de *sincronizar* 🗘 en la barra de estado de Visual Studio
Code, o bien, escribiendo el comando `git pull` en la terminal.

### No le entiendo a sus símbolos matemáticos. ¿Qué hago?

La notación matemática es estándar en el área de matemáticas y las ciencias de
la computación, si necesitas ayuda con ella te recomiendo la siguiente
referencia:

- Johnsonbaugh, R. (2005). El lenguaje de las matemáticas.
  En *Matemáticas discretas*. Pearson Educación.

### ¿Qué es Docker y por qué necesito instalarlo?

Docker es una herramienta que permite crear contenedores de software.
Los contenedores de software te permiten ejecutar software en un entorno
aislado, de manera que no se afecte el resto del sistema.
En este caso, el contenedor de Docker que se utiliza en este repositorio
contiene todas las herramientas necesarias para ejecutar los cuadernos de
Jupyter así como para realizar las prácticas del curso.
Si eligieras no usar Docker, tendrías que instalar todas las herramientas
necesarias directamente en tu computadora, lo cual puede ser muy complicado.

### ¿Por qué el contenedor está basado en Linux?

El contenedor está basado en Linux porque es el sistema operativo más utilizado
en el área de las ciencias de la computación, tiene un gran soporte para
herramientas de desarrollo, y es de código abierto.

### Me gustaría aprender a usar Linux. ¿Qué recomienda?

Existen varias guías para aprender a usar Linux, algunas completamente
gratuitas, pero en general recomiendo mirar los siguientes recursos:

- Video [🐧 Linux para principiantes](https://youtu.be/tdjGchccSws) explica cómo
  instalar Linux en una computadora y ofrece un paseo rápido por el entorno de
  escritorio.
- Sitio web [Guía de escritorio de Ubuntu](https://help.ubuntu.com/stable/ubuntu-help/).
  Esta es una guía bastante completa acerca del uso básico del escritorio de
  Ubuntu y, aunque no tiene muchas ilustraciones, es fácil de seguir y está
  disponible en español.
- Video [Aprende linux ahora!](https://youtu.be/L906Kti3gzE) explica los
  conceptos básicos de Linux así como el uso de la terminal.
- Lista de reproducción [Curso completo de Linux desde cero para principiantes](https://www.youtube.com/playlist?list=PL2Z95CSZ1N4FKsZQKqCmbylDqssYFJX5A). Este es un curso bastante
  completo acerca del uso de la terminal en Linux así como sus conceptos.

Todo sea dicho, Linux es un ecosistema enorme, así que no te preocupes si no
entiendes todo de una vez o no te gusta tu distribución de Linux; asegúrate de
probar varias distribuciones y de encontrar la que más te guste.
Personalmente he probado [Debian][13], [Ubuntu][14], [Fedora][15],
[Elementary OS][16], [Linux Mint][17], [Pop!_OS][18], y [OpenSUSE][19] entre
otros, pero uso Ubuntu desde hace 15 años porque simplemente funciona y permite
concentrarme en el trabajo.

### ¿Me puede ayudar con mi tarea de esta u otra materia?

No puedo porque ando siempre en [#ModoChamba][12].

### ¿Me puede aprobar el curso si solamente me quiero dedicar a hacer teoría?

Respuesta corta: No. Respuesta larga: Noooooooooooooooooooooooooooooooooooooo.

[1]: https://www.uaem.mx/
[2]: https://git-scm.com/
[3]: https://www.docker.com/
[4]: https://code.visualstudio.com/
[5]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
[6]: https://hatch.pypa.io/
[7]: https://learn.microsoft.com/es-es/windows/wsl/install
[8]: https://jupyter.org/
[9]: https://markdown.es/sintaxis-markdown/
[10]: http://mirrors.ctan.org/info/lshort/spanish/lshort-letter.pdf
[11]: https://docs.docker.com/desktop/use-desktop/
[12]: https://twitter.com/hashtag/ModoChamba
[13]: https://www.debian.org/
[14]: https://ubuntu.com/
[15]: https://getfedora.org/
[16]: https://elementary.io/
[17]: https://linuxmint.com/
[18]: https://pop.system76.com/
[19]: https://www.opensuse.org/
[20]: https://appflowy.io/