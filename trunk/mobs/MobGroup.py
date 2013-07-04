class MobGroup:
    mobs = {}
    
    def addMob(mob):
        nombre = mob.nombre
        MobGroup.mobs[nombre] = mob
    
    def removeMob(mob):
        nombre = mob.nombre
        if nombre in MobGroup.mobs:
            del MobGroup.mobs[nombre]
    
    
