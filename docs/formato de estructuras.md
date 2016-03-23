##Formato de Estructuras Compuestas y Complejas

Se denominan Estructuras a los objetos que se componen de más de una imagen, y que tienen propiedades particulares más allá de las que el engine les da por defecto (como por ejemplo, el ser sólidos o producir sombra)

###Estructuras Compuestas
Las Estructuras Compuestas son objetos que se componen de varios otros objetos. Por ejemplo, un objeto-casa puede estar armado por el sprite de la casa propiamente dicha, un sprite separado para la puerta (que puede ser Operable) y un sprite para la ventana, que podría, por ejemplo, emitir luz.


    {
        "tipo":"estructura_compuesta",
        "componentes":{
                "<nombre>":[[<x>,<y>,<z>]],
                ...
        },
        "refs":{
            "<nombre>":<defininción del objeto>,
            ...
        }
    }

###Estructuras Complejas
Las Estructuras Complejas por otro lado, son objetos planteados como tridimiensionales. Esto es, en la definición del objeto (un archivo json) se indican las imagenes que el objeto mostrará cuando la Cámara lo haga ver de frente, de costado, o por detrás, etc.

    {
        "tipo": "estructura_combinada",
        "nombre":"<string>",
        "proyecta_sombra":true|false,
        "componentes":{
            "frente":"props/<filename>.png",
            "lado":"props/<filename>.png",
            "reverso":"props/<filename>.png"
        },
        "propiedades":[]
    }


###Estructuras Complejas Compuestas
Un objeto puede ser una estructura compleja y compuesta a la vez.

    {
        "tipo":"estructura_compleja_compuesta",
        "componentes":{
            "frente":[[<x>,<y>],...],
            "lado":[[<x>,<y>],...],
            "reverso":[[<x>,<y>],...]
        },
        "refs":{
            "frente":"props/<filename>.png",
            "lado":"props/<filename>.png",
            "reverso":"props/<filename>.png"
        }
    }

[Documentación](main.md)