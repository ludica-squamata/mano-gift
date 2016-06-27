##Formato de Estructuras 3D

Se denominan Estructuras 3D a los objetos que se componen de más de un objeto, y que pueden ser vistos desde distintas cámaras (efecto 3D). Por ejemplo, una Estructura3D "casa" puede estar armada por el sprite de la casa propiamente dicha, un sprite separado para la puerta (que puede ser **Operable**) y un sprite para la ventana, que podría, por ejemplo, emitir luz. Las Estructuras 3D tienen caras para los componentes: "frente" son los objetos que se verán cuando la camara mire a la estructura de frente (la perspectiva por defecto). Los objetos del "lado" se veran cuando la estructura sea vista de lado; y finalmente "reverso" refiere a los objetos que se verán cuando la camara vea la parte trasera de la estructura. Estos componentes no tienen porqué ser los mismos en cada lado. Una Casa puede tener una puerta al frente, pero no necesariamente atrás o por el costado.

Cada componente listado debe estar dentro de las "referencias". Aquí se indican, mediante strings, rutas a achivos de imagen png (para componentes que son solo eso, una imagen sin interacción); rutas a la definición de un objeto (que puede ser una estructura 3D como ésta o algún tipo de Prop, por ejemplo un **Operable**) o una _definición embebida_ de un objeto (que sería lo mismo que encontraríamos en el archivo json de la definición de un objeto).

Finalmente, la propiedad "cara" puede estar o no presente. Su presencia indica que la estructura es final (es decir, es la que vemos). De no estar, el renderer no sabe con qué cara mostrar al objeto, por lo que este tipo de estructuras "sin cara" no pueden ser vistas directamente. Un ejemplo de estructura3D sin cara son los palotes.

    {
      "tipo":"estructura3D",
      "nombre":"<nombre>",
      "componentes":{
        "frente":{
          "<componente>":[[<x>,<y>,<z>]],
          ...
        },
        "lado":{
            "<componente>":[[<x>,<y>,<z>]],
            ...
        },
        "reverso":{
            "<componente>":[[<x>,<y>,<z>]],
            ...
        }
      },
      "referencias":{
        "<componente1>":"<ruta a un archivo png>",
        "<componente2>":"<ruta a la defición de un objeto>",
        "<componente3>":"<definición embebida de un objeto>",
        }
      },
      "proyecta_sombra":true|false,
  
      "cara":"frente"|"lado"|"reverso"
    }

[Documentación](main.md)