# Formato de mobs

    {
        "ID":<>,
        "nombre":string,
        
        "salud":integer,
        "fuerza":integer,
        "carisma":integer,
        
        "velocidad":integer,
        
        "imagenes":{
            "idle":"<filename>",
            "atk":"<filename>",
            "death":"<filename>",
            "diag_face":"<filename>"
        },
        "alphas":{
            "idle":<filename>,
            "atk":<filename>,
            "death":<filename>
        },
        
        "clase":string,
        "propiedades":lista de strings
    }


Esta es la estructura de un archivo json que define un mob. Estos archivos se almacenan en la carpeta /mobs de la carpeta de datos del proyecto. Todo dato relevante a un mob se define aqui, excepto cuestiones temporales como sus diálogos, objetivos o AI de movimiento.

- **ID**: un integer que referencia a la base de datos. Aun no tiene función.
- **nombre**: un string con el nombre del mob en cuestión.
- **salud**, **fuerza**, **carisma**: características del mob. Todos estos son integers. En el [futuro] (wishlist.md) habrá más caracteristicas.
- **velocidad**: un integer que mide la cantidad de pixeles por frame a los que se moverá el mob. Por defecto es 1 para los NPCs
- **imagenes**: este es un diccionario con cuatro claves. Cada clave contiene un string, que debe ser la ruta de arhivo a la imagen en cuestión. Recordar que las rutas son relativas a la carpeta de datos gráficos (data/grafs), por lo que no es necesario indicar la ruta completa.

  - **idle**: la ruta a la imagen del mob cuando éste está parado sin hacer nada.
  - **atk**: la ruta a la imagen del mob para su animacion de ataque. Puede ser `null`.
  - **death**: la imagen del cadaver del mob, si existe. Puede ser `null`.
  - **diag_face**: la ruta a la imagen de diálogo del mob. Puede ser `null`.

- **alphas**: otro diccionario contiendo rutas a imagenes. Estas rutas se usarán como máscaras de colisión para el mob.
  - **idle**: la ruta a la imagen de colision para la posicion por defecto.
  - **atk**: la ruta a la imagen de colisión para la animación de ataque. Puede ser `null`.
  - **death**: la ruta a la imagen de colisión para el cadáver del mob. Puede ser `null`.

- **clase**: un string indicando el nombre de la clase que se usará para crear el Mob. Ejemplos son "PC", "NPC", etc.
- **propiedades**: una lista con strings. Cada string es una propiedad del mob. Ejemplos son "solido", "pasiva", etc.

[Documentación](main.md)
