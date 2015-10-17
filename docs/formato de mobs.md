# Formato de mobs

    {
        "ID": <numero de orden>,
        "nombre": "<nombre del mob>",
        
        "salud": <valor>,
        "fuerza": <valor>,
        "carisma": <valor>,
        
        "velocidad": <valor>,
        
        "imagenes":{
            "idle": "<filename>",
            "atk": "<filename>"| null,
            "death": "<filename>"| null,
            "diag_face": "<filename>"| null
        },
        "alphas":{
            "idle": "<filename>",
            "atk": "<filename>"| null,
            "death": "<filename>"| null
        },
        
        "clase": "<nombre del la clase>",
        "propiedades": ["<propiedad>", ...]
    }


Esta es la estructura de un archivo json que define un mob. Estos archivos se almacenan en la carpeta /mobs de la carpeta de datos del proyecto. Todo dato relevante a un mob se define aqui, excepto cuestiones temporales como sus diálogos, objetivos o AI de movimiento.

- **ID**:  Referencia a la base de datos. Aún no tiene función.
- **nombre**: El nombre del mob en cuestión. Tiene que ser único.
- **salud**, **fuerza**, **carisma**: características del mob. En el [futuro] (wishlist.md) habrá más.
- **velocidad**: cantidad de pixeles por frame a los que se moverá el mob. Para los NPCs es 1.
- **imagenes**: cada "filename" es una ruta de arhivo a la imagen en cuestión. Estas rutas son relativas a la carpeta de datos gráficos (data/grafs), por lo que no es necesario indicar la ruta completa.

  - **idle**: imagen del mob no combativo.
  - **atk**: animacion de ataque. Puede ser `null`.
  - **death**: la imagen del cadaver del mob, si existe. Puede ser `null`.
  - **diag_face**: imagen de diálogo del mob. Puede ser `null`.

- **alphas**: Estas rutas se usarán como máscaras de colisión para el mob.
  - **idle**: posicion por defecto.
  - **atk**: animación de ataque. Puede ser `null`.
  - **death**: cadáver del mob. Puede ser `null`.

- **clase**: el nombre de la clase que se usará para crear el Mob. Ejemplos son "PC", "NPC", etc.
- **propiedades**: Ejemplos son "solido", "pasiva", "hostil" etc.

[Documentación](main.md)
