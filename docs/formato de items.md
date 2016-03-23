##Formato de Items

###Escenografía
Se denomina escenografía a los objetos que están presentes en el mapa, como las casas o los árboles. Un objeto escenografía puede ser de los siguientes tipos.

- _Agarrable_: se pueden tomar del mapa y pasan a ser **Ítems** en el Inventario.
- _Movible_: es posible hacer que se muevan, empujándolos.
- _Destruible_: WIP
- _Operable_: tienen diversos estados que pueden cambiarse al accionarlos.

###Item
Los objetos agarrables se convierten en Item cuando son tomados del mapa y pasan a formar parte del invetario de un mob. Pueden ser de los siguientes tipos.
 - Equipable: por ejemplo, una parte de armadura.
 - Consumible: por ejmplo, una fruta.

La estructura general para las escenografías es:

    {
        "tipo":"<string>",
        "subtipo":"<string>" (si tiene),
        "peso":int, "volumen":int,
        "image": "props/<filename>.png",
        "proyecta_sombra":true|false
        "propiedades":[]
    }

#####Consumible
Una escenografía _Agarrable_ puede ser también consumible:

    "subtipo":"consumible",
    "efecto":{
        "des":"<string, descripción>",
        "stat":"<string>",
        "mod":int}

O bien Equipable:

    "subtipo":"equipable",
    "efecto":{
        "des":"<string, descripción>",
        "equipo":"<slot>"}



####Operable
Un tipo particular de Escenografía es aquella que puede ser operada por un mob, pero que no puede pasar a formar parte del inventario de éste. Por ejemplo, una puerta.

    "operable":[
        {"ID":0,
         "image":"props/<filename>.png",
         "solido":true,
         "next":1
        },
        {"ID":1,
         "image":"props/<filename>.png",
         "solido":false,
         "next":0
        }]

####Eventos
Finalmente, un objeto de la escenografía puede tener eventos asociados.

    "script":"<string. Nombre del script.py>",
    "eventos":{
        "<nombre del evento>":"<nombre de la función>"

