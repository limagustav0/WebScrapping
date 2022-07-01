def getkey(lista,key):
    for c in range(0,len(lista)):
        if lista[c]['nome'] == key:
            return lista[c]