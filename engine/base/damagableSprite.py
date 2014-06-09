
class damageableSprite(_giftSprite):
    
    def recibir_danio(self):
        self.salud -= 1
       
        if self.salud <= 0:
            if self.death_img != None:
                self.image = self.death_img
            else: # esto queda hasta que haga sprites 'muertos' de los npcs
                ED.RENDERER.delObj(self)
                self.stage.delProperty(self)
            self.dead = True
            MobGroup.remove(self)

