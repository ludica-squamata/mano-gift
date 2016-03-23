##Propiedades

Los mobs y los props disponen de un atributo opcional denominado _propiedades_, que en la definición del mob o prop es una lista de strings. En la definición del mob, las propiedades aparecen de la siguiente forma:

    "propiedades":["<item>","<item>",...],

A continuación, algunos de los strings con significados que tenemos hasta ahora.

###Propiedades de mobs
Los mobs pueden ser _hostiles_, _pasivos_ o _solidos_, por el momento
* **Hostil**: un mob hostil buscará atacar a los mobs pasivos. Típicamente esta propiedad se le asigna a los monstruos.
* **Pasivo**: al contrario que un mob hostil, uno pasivo no busca combate directamente, y [evitará](wishlist.md) a los mobs que le causen daño.
* **Solido**: finalmente, la propiedad sólido indica si el mob en cuestión debe someterse a la detección de colisiones con otros mobs sólidos o no. Un fantasma por ejemplo, no sería sólido.

Típicamente un mob no puede ser pasivo y hostil a la vez. Aunque en el [futuro](wishlist.md) podrá alternar entre una actitud y la otra.

###Propiedades de los props
Los props comparten una propiedad con los mobs (sólido), además de añadir algunas otras, específicas de este tipo de entidad.
* **Stackable**: un ítem stackable es uno que se puede apilar (stackable es una expresión en inglés, que significa "que puede apilarse"). Un mob que recolecte varios ítems del mismo tipo con esta propiedad aparecerán con un único ícono y un número (representando la cantidad) en el inventario del mob.
* Otras propiedades serán añadidadas en el [futuro](wishlist.md).
