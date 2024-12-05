from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime
from students.models import Estudiante, Pago


def getEstudiantes():
    client = MongoClient(settings.MONGO_CLI)
    db = client['ISIS2304A05202410']

    estudiantes_collection = db['estudiantes']
    estudiantes_db = estudiantes_collection.find({})
    estudiantes = [Estudiante.from_mongo(estudiante) for estudiante in estudiantes_db]

    client.close()
    return estudiantes


def getEstudiante(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client['ISIS2304A05202410']

    estudiantes_collection = db['estudiantes']
    estudiante = estudiantes_collection.find_one({'_id': ObjectId(id)})

    client.close()

    if estudiante is None:
        raise ValueError('Estudiante not found')

    return Estudiante.from_mongo(estudiante)


def verifyEstudianteData(data):
    if 'nombre' not in data:
        raise ValueError('nombre is required')

    estudiante = Estudiante()
    estudiante.nombre = data['nombre']
    estudiante.pagos = data.get('pagos', [])

    return estudiante


def createEstudiante(data):
    # Verify estudiante data
    estudiante = verifyEstudianteData(data)

    # Create estudiante in MongoDB
    client = MongoClient(settings.MONGO_CLI)
    db = client['ISIS2304A05202410']

    estudiantes_collection = db['estudiantes']
    estudiante.id = estudiantes_collection.insert_one({
        'nombre': estudiante.nombre,
        'pagos': estudiante.pagos
    }).inserted_id

    client.close()
    return estudiante


def deleteEstudiante(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client['ISIS2304A05202410']

    estudiantes_collection = db['estudiantes']
    result = estudiantes_collection.delete_one({'_id': ObjectId(id)})

    client.close()
    return result.deleted_count


def verifyPagoData(data):
    if 'valor' not in data or not isinstance(data['valor'], (int, float)):
        raise ValueError('valor is required and must be a number')

    pago = Pago()
    pago.valor = data['valor']
    pago.estudiante_id = data.get('estudiante_id', None)
    if not pago.estudiante_id:
        raise ValueError('estudiante_id is required')

    return pago


def addPago(estudiante_id, data):
    # Verify pago data
    pago = verifyPagoData(data)

    # Add pago to MongoDB
    client = MongoClient(settings.MONGO_CLI)
    db = client['ISIS2304A05202410']

    estudiantes_collection = db['estudiantes']
    estudiante = estudiantes_collection.find_one({'_id': ObjectId(estudiante_id)})

    if estudiante is None:
        raise ValueError('Estudiante not found')

    pago_dict = {
        'valor': pago.valor,
        'datetime': datetime.datetime.now()
    }

    result = estudiantes_collection.update_one(
        {'_id': ObjectId(estudiante_id)},
        {'$push': {'pagos': pago_dict}}
    )

    client.close()
    return result.modified_count


def getAveragePago(estudiante_id):
    client = MongoClient(settings.MONGO_CLI)
    db = client['ISIS2304A05202410']

    estudiantes_collection = db['estudiantes']
    estudiante = estudiantes_collection.find_one({'_id': ObjectId(estudiante_id)})

    if estudiante is None:
        raise ValueError('Estudiante not found')

    pagos = estudiante.get('pagos', [])
    if not pagos:
        return {
            'estudiante': estudiante['nombre'],
            'average': None
        }

    average = sum(pago['valor'] for pago in pagos) / len(pagos)

    client.close()
    return {
        'estudiante': estudiante['nombre'],
        'average': average
    }
