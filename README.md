# uaem.notas.principioslenguajes
Notas de curso Principios de Lenguajes de Programación de la [Universidad
Autónoma del Estado de Morelos][1].

— *Dr. Mario Abarca*

## Inicio rápido
Antes de comenzar se deben de cumplir los siguientes requisitos:
- Tener instalado [Git][2].
- Tener instalado [Docker][3].
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

## Estructura del repositorio
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
  


[1]: https://www.uaem.mx/
[2]: https://git-scm.com/
[3]: https://www.docker.com/
[4]: https://code.visualstudio.com/
[5]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
[6]: https://hatch.pypa.io/