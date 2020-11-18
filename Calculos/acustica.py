def calcularRT60(data, volumen):
    new = {}
    for key, value in data.items():
        if key.endswith('Hz'):
            rt = 0.161 * ( volumen / (data['Área'] * value))
            new.update({key: rt})
    return new