class Pago:
    def __init__(self, id="", valor="", estudiante_id=""):
        self.id = id
        self.valor = valor
        self.estudiante_id = estudiante_id

    def __str__(self):
        return f"Pago(id={self.id}, valor={self.valor}, estudiante_id={self.estudiante_id})"

    @staticmethod
    def from_mongo(dto):
        pago = Pago()
        pago.id = str(dto.get('_id', ''))
        pago.valor = str(dto.get('valor', ''))
        pago.estudiante_id = str(dto.get('estudiante_id', ''))
        return pago


class Estudiante:
    def __init__(self, id="", nombre="", pagos=None):
        self.id = id
        self.nombre = nombre
        self.pagos = pagos if pagos is not None else []

    def __str__(self):
        return f"Estudiante(id={self.id}, nombre={self.nombre}, pagos={self.pagos})"

    @staticmethod
    def from_mongo(dto):
        estudiante = Estudiante()
        estudiante.id = str(dto.get('_id', ''))
        estudiante.nombre = str(dto.get('nombre', ''))
        estudiante.pagos = dto.get('pagos', [])
        return estudiante

    
    
    
    
