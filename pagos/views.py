import students.logic as students_logic
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse


@api_view(["GET", "POST"])
def estudiantes(request):
    if request.method == "GET":
        estudiantes = students_logic.getEstudiantes()
        return JsonResponse([estudiante.__dict__ for estudiante in estudiantes], safe=False)

    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            estudiante = students_logic.createEstudiante(data)
            response = {
                "objectId": str(estudiante.id),
                "message": f"Estudiante {estudiante.nombre} creado en la base de datos"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)


@api_view(["GET", "DELETE"])
def estudianteDetail(request, estudiante_id):
    if request.method == "GET":
        try:
            estudiante = students_logic.getEstudiante(estudiante_id)
            return JsonResponse(estudiante.__dict__, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)

    if request.method == "DELETE":
        result = students_logic.deleteEstudiante(estudiante_id)
        response = {
            "objectId": str(result),
            "message": "Estudiante eliminado de la base de datos"
        }
        return JsonResponse(response, safe=False)


@api_view(["GET", "POST"])
def pagos(request, estudiante_id):
    if request.method == "GET":
        try:
            estudiante = students_logic.getEstudiante(estudiante_id)
            pagos = estudiante.pagos
            return JsonResponse(pagos, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)

    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            result = students_logic.addPago(estudiante_id, data)
            response = {
                "result": str(result),
                "message": f"Pago agregado para el estudiante con ID {estudiante_id}"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)


@api_view(["GET"])
def averagePago(request, estudiante_id):
    try:
        average_data = students_logic.getAveragePago(estudiante_id)
        response = {
            "estudiante": average_data["estudiante"],
            "average": average_data["average"]
        }
        return JsonResponse(response, safe=False)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)

