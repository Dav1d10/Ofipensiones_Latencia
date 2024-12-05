from django.urls import path
from .views import estudiantes, estudianteDetail, pagos, averagePago

urlpatterns = [
    # Ruta para obtener todos los estudiantes y crear uno nuevo
    path('estudiantes/', estudiantes, name='estudiantes'),

    # Ruta para obtener detalles y eliminar un estudiante por ID
    path('estudiantes/<str:estudiante_id>/', estudianteDetail, name='estudianteDetail'),

    # Ruta para obtener y agregar pagos de un estudiante
    path('estudiantes/<str:estudiante_id>/pagos/', pagos, name='pagos'),

    # Ruta para calcular el promedio de pagos de un estudiante
    path('estudiantes/<str:estudiante_id>/average/', averagePago, name='averagePago'),
]

