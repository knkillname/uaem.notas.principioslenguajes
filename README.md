# uaem.notas.principioslenguajes
Notas de curso Principios de Lenguajes de Programación de la Universidad
Autónoma del Estado de Morelos.

— *Dr. Mario Abarca*

## Inicio rápido
Antes de comenzar se deben de cumplir los siguientes requisitos:
- Tener instalado [Git][1].
- Tener instalado [Docker][2].
- Tener instalado [Visual Studio Code][3].
- Tener instalado el plugin de [Dev Containers][4] en Visual Studio Code.

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

[1]: https://git-scm.com/
[2]: https://www.docker.com/
[3]: https://code.visualstudio.com/
[4]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers