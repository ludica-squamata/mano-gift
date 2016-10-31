##Formato de eventos
El Ázoe Engine soporta un sistema interno de eventos que comunican distintas partes de motor de forma asincrónica y en cascada. Lo eventos se disparan importanto la clase EventDispatcher del siguinete modo
    
    from engine.globs.eventDispatcher import EventDispatcher

Luego, cuando el evento sea ejecutado, se realiza un trigger()
    
    EventDispatcher.trigger("<nombre del evento>", "<clase de origen>", {<datos del evento>})

Para que otros módulos y clases respondan al evento, es neceario que primero se registren, mediante el método register().
    
    EventDispatcher.register(<método o función>, "<evento1>" , "<evento2>", ...)

Cuando ya no sea necenario responder a un evento, la clase puede llamar al método deregister(). Los parámetros de este método son los mismos que se usan en register().

    EventDispatcher.deregister(<método o función>, "<evento1>" , "<evento2>", ...)

Nótese que los métodos permiten de/registrar cada oyente a un numero artbitrario de eventos.

Los eventos que actualmente están en el engine son:

- **NuevoJuego**: se dispara cuando se inicia un juego.
- **CambiarMapa**: cuando héroe cambia de mapas, este evento le avisa al engine que cambie el mapa.
- **hora: cada vez que el reloj llegue a una hora, se dispara este evento. Está vinculado al movimiento solar.
- **MovimientoSolar**: cambia las sombras de los sprites.
- **DialogEvent**: cuando un fragmento de diálogo lance un evento, será de este tipo.
- **MobHerido**: se dispara cuando un mob resulta herido. Actualiza el HUD si el mob es el héroe.
- **MobMuerto**: se dispara cuando un mob muere. Esto cierra el juego si el mob es el héroe.
- **DelItem**: cuando el héroe agarra un item del mapa, éste evento se lanza para hacerlo desaparecer del mapa.
- **button_activated**: este evento está vinculado a las EventFlags.
- **Pause**: se activa cuando el juego entra en pausa. detiene el correr del tiempo.
- **key**: cada vez que el jugador toca una tecla, se dispara este evento. Cada evento tendrá un efecto diferente dependiendo del modo de juego en el que se encuentre el motor, la tecla pulsada, y el modo en el que se haya pulsado (tap, hold o release).
- **OpenMenu**: cuando Pausa u otro menú llaman a nuevos menúes se dispara este evento para abrirlos.
- **ToggleSetKey**: cuando el usuario elija una tecla para modificar el input, se dispara este evento para capturar el keydown de una tecla no registrada.
- **Save**, **SaveData** y **SaveDataFile**: estos tres eventos se disparan en cascada. El primero avisa a todas las clases oyentes que se va a guardar el estado del juego. Cada clase, a su vez, lanza SaveData con los datos que se quieren guardar (posicion del personaje, hora, etc). Finalmente, SaveFileData le indica al engine que tiene que guardar la data en el archivo de salvado.

[Documentación](main.md)