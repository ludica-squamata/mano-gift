from .resources import abrir_json, guardar_json
from os import path, listdir, getcwd
from hashlib import md5

ruta1 = path.join(getcwd,'/data/items')
ruta2 = path.join(getcwd,'/data/props')
ruta3 = path.join(getcwd,'/data/mobs')

for ruta in ruta1, ruta2, ruta3:
    for filepath in listdir(ruta):
        path_ruta = ruta + '/' + filepath
        if path.isfile(path_ruta):
            data = abrir_json(path_ruta,'utf-8')
            nombre = data['nombre'] if 'nombre' in data else filepath[:-5]
            data['prefix'] = md5(nombre.encode()).hexdigest()[:4].upper()
            guardar_json(path_ruta,data,'utf-8')