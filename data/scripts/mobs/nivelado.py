def nivel(mob):
    proto_nivel = 0
    for char in mob.get_chars():
        proto_nivel += char
    mob['Nivel'] = 1 + (proto_nivel - 50) // 6
    mob['Ataque'] += mob['Nivel']
    mob['Evasión'] += mob['Nivel']
