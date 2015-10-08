##Formato de mapas

Dentro de proyecto Mano-Gift, los mapas se componen de tres archivos elementales. En este documento, explicaremos el formato, especificaciones y contenidos de esos tres archivos, a saber:
- Imagen de fondo
- Imagen de colisiones
- Archivo de datos

####Imagen de fondo
La parte visible del mapa, el área recorrida por el héroe y lo que se muestra en pantalla, es una imagen de fondo. Las características de esta imagen son:

- Estará en formato PNG de 24 bits y no contará con alpha layer (no es necesaria la transparecia, pues es el fondo).
- El tamaño minimo de esta imagen debe ser de 512x512 pixeles. No hay un tamaño máximo establecido.

####Imagen de colisiones
La imagen de colisiones es una imagen 'alpha' de la imagen de fondo, que le indicará al engine qué elementos de la imagen de fondo son sólidos e imposibles de atravezar, y qué partes del terreno son transitables. Las características de esta imagen son:

- Ha de tener exactamente las mismas dimensiones que la imagen de fondo.
- El color designado para la detección de colisiones es el _magenta_: RGB 255,0,255
- El color designado para el terreno transitable es el _negro_: RGB 0,0,0
- Normalmente su nombre de archivo se corresponderá con el de la imagen de fondo a la que está asociada, formando pares. Esto no es necesario, sin embargo.

###Archivo de datos
Finalmente, cada mapa cuenta con un archivo de texto plano, llamado de 'datos' que contiene las posiciones iniciales de cada mob y las posiciones (usualmente fijas) de los props. Este es el arhivo que el engine usará para cargar el mapa.

Cada mapa cuenta con dos claves básicas, llamdas capas _background_ y _ground_, que contienen las posiciones de cada mob o prop en pantalla. 
####La capa background
La primera capa (background) tiene la siguiente forma:

    {
        "capa_background":{
            "fondo":"maps/fondos/<filename>.png",
            "colisiones":"maps/colisiones/<filename>.png"
        },

Los filenames no tienen porque ser necesariamente idénticos, y la ruta de cada uno es relativa a la carpeta de gráficos del proyecto.

####La capa ground
La capa _ground_ por otra parte, es algo más compleja. Como la capa background, ground es también un diccionario.

    "capa_ground":{
        "props": {
            <ref>:[[<x>,<y>],[<x>,<y>],...],
            ...
        },
        "mobs": {
            "enemies":{},
            "npcs":{
                <ref>:[[<x>,<y>],[<x>,<y>],...],
                ...
            }
        }
    },

Aquí, "props", "enemies" y "npcs" son diccionarios, donde cada clave es una **referencia** (ver abajo). El valor de cada key/ref es una lista que a su vez contiene pares de integers (una lista de listas). Estos integeres son posiciones medidas en pixeles (x e y, y un futuro, tambien z), y son relativos al mapa, no a la pantalla.

####Entradas y Salidas
Lo siguiente en el archivo de datos son los accesos al mapa. Estos puntos son lugares donde el mapa cambiará en abrupto, en contraste con el movimiento continuo entre chunks en el overworld.

######Entradas
El valor de "entradas" es un diccionario, donde cada key es el nombre de una entrada (un _link_, ver abajo), que a su vez contiene un par de coordenadas (x,y). 
Una entrada en particular demanda una atención especial. La entrada llamada "inicial" es el lugar donde el héroe aparecerá por primera vez. Sólo los mapas con una entrada inicial aparecen en el selector de mapas del debugger.

    "entradas":{
        "inicial":[<x>,y>],
        "<nombre>":[<x>,<y>],
        ...
    },


######Salidas
Las salidas en cambio, tienen más datos. En principio, _salidas_ es un diccionario, donde cada key es el nombre de una salida (un string) que contiene a su vez otro diccionario. Este ultimo dict tiene 3 keys: "rect", "dest" y "link".
- "rect" es una lista con 4 integers, donde los numeros son los valores x,y,w,h del rect.
- "dest" es un string con el nombre del mapa de destino. 
- "link" es un string con el nombre de la entrada (ver arriba) que se vincula con esta salida. 
```
    "salidas":{
        "<nombre de la salida>":{
            "rect":[<x>,<y>,<w>,<h>],
            "dest":"<filename de otro mapa, sin extensión>",
            "link":"<entrada en el otro mapa>",
        },
        ...
    },
```

####Referencias
La clave "refs" es udiccionario, donde cada key es una referencia a los mobs o props utilizados en la capa ground. Los que no figuren aquí usarán un arhivo de datos separado, como el de los mobs. Cada el valor de cada key es una ruta a una imagen. Nótese que los keys deben corresponderse con aquellos presentes en la capa ground.

####Otros datos
Las últimas 4 claves del archivo de datos son "ambiente", que es un string que puede ser "interior" o "exterior"; "amanece", "atardece" y "anochece" son listas con dos integers, donde cada uno representa un par hora,minutos.

        "ambiente":"exterior"|"interior",
        "amanece": [<h>,<m>],
        "atardece": [<h>,<m>],
        "anochece": [<h>,<m>],
    }

[Documentación](main.md)