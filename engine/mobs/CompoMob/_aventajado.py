from . import Caracterizado
from os import getcwd, path
from csv import DictReader


class Aventajado(Caracterizado):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.perk_data = self.perks_file_loader('perks.csv')
        self.perks = []
        # for id in self.perk_data:
        #     cumple = self.check_reqs(id)
        #     if cumple:
        #         print(self.nombre, self.perk_data[id]['name'])
        # print()

    @staticmethod
    def perks_file_loader(csv_file):
        data = {}
        with open(path.join(getcwd(), 'data/game', csv_file), encoding='utf-8') as cvsfile:
            reader = DictReader(cvsfile, delimiter=';')
            for row in reader:
                data[int(row['id'])] = {k: row[k] for k in row if k != 'id'}
        return data

    def check_reqs(self, id):
        valid = True
        if id not in self.perk_data:
            raise ValueError('Perk ID is invalid')
        else:
            perk = self.perk_data[id]
            if "|" in perk['hab_req']:
                try:
                    reqs = [int(x) for x in perk['hab_req'].split('|')]
                    valid = valid and any([x in self.perks for x in reqs])
                except ValueError: # perk 24
                    hab_reqs = perk['hab_req'].split('|')
                    for req in hab_reqs:
                        if "&" in req:
                            reqs = [int(x) for x in req.split('&')]
                            valid = valid and all([x in self.perks for x in reqs])
                        else:
                            reqs = [int(x) for x in req]
                            valid = valid and any([x in self.perks for x in reqs])

            elif "&" in perk['hab_req']:
                reqs = [int(x) for x in perk['hab_req'].split('&')]
                valid = valid and all([x in self.perks for x in reqs])

            elif perk['hab_req'].isnumeric():
                valid = valid and int(perk['hab_req']) in self.perks

            if ">=" in perk['char_req']:
                char, req = perk['char_req'].split('>=')
                valid = valid and self[char] >= int(req)
            elif "<=" in perk['char_req']:
                char, req = perk['char_req'].split("<=")
                valid = valid and self[char] <= int(req)
            elif ">" in perk['char_req']:
                char, req = perk['char_req'].split('>')
                valid = valid and self[char] > int(req)
            elif "<" in perk['char_req']:
                char, req = perk['char_req'].split('<')
                valid = valid and self[char] < int(req)
            elif "==" in perk['char_req']:
                char, req = perk['char_req'].split('==')
                valid = valid and self[char] == int(req)
            elif "<>" in perk['char_req']:
                char, req = perk['char_req'].split('<>')
                valid = valid and self[char] != int(req)

            if perk['affinity_requirements'] != 'null':
                colors = 'Rojo,Azul,Verde,Amarillo,Cian,Magenta'.split(',')
                char, req = perk['affinity_requirements'].split('>=')
                if char != "Multi" and char != 'Any':
                    valid = valid and self[char] >= int(req)
                elif char == 'Any':
                    valid = valid and any([self[char]>=int(req) for char in colors])
                elif char == 'Multi': # el requito de multi es doble.
                    # Por un lado varias afinidades tienen que ser mayores que el requisito,
                    # y también cuenta la cantidad de afinidades que superen el requito.
                    # aunque puede ser overkill.
                    affinities = [self[color] for color in colors]
                    valid = valid and len([aff >= req for aff in affinities]) >= req

            # resource_requirements are not checked, yet
        return valid