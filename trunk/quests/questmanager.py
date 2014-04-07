from globs import MobGroup

class QuestManager:
    quests = {}
    
    def add(script):
        from quests import Quest
        
        if script not in QuestManager.quests:
            quest = Quest(script)
            QuestManager.quests[script] = quest
            for NPC in quest.on_Dialogs:
                MobGroup[NPC].temas_para_hablar[script] = quest.on_Dialogs[NPC]
                MobGroup[NPC].tema_preferido = script
                
    def remove(quest):    
        nombre = quest.nombre
        if nombre in QuestManager.quests:
            del QuestManager.quests[nombre]
            for NPC in quest.off_Dialogs:
                if NPC in MobGroup:
                    npc = MobGroup[NPC]
                    if quest.off_Dialogs[NPC] != "":
                        npc.temas_para_hablar[nombre] = quest.off_Dialogs[NPC]
                    else:
                        npc.tema_preferido = npc.data['tema_preferido']
    
    def update():
        conds = {}
        for quest in QuestManager.quests:
            conds[quest] = QuestManager.quests[quest].update()
            
        for quest in conds:
            if conds[quest]:
                QuestManager.remove(QuestManager.quests[quest])
