def obtenerLimites(paredes):
    menores, mayores = min_max(paredes)
    limite = 0
    for i in range(3):
        distancia = mayores[i] - menores[i]
        if distancia > limite:
            limite = distancia
    restos = [((mayores[i] - menores[i]) - limite) / 2 for i in range(3)]
    limites = []
    for i in range(3):
        lim_i = [menores[i] + restos[i],
                 mayores[i] - restos[i]]
        limites.append(lim_i)
    return tuple(limites)
def min_max(paredes):
    x, y, z = [], [], []
    for pared in paredes:
        for vertice in pared:
            x.append(vertice[0])
            y.append(vertice[1])
            z.append(vertice[2])
    mayores = [max(x), max(y), max(z)]
    menores = [min(x), min(y), min(z)]
    return menores, mayores
