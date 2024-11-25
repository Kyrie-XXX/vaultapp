from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adminpage/', views.admin_page, name='adminpage'),
    path('agregar_libro/', views.agregar_libro, name='agregar_libro'),
    path('actualizar_libro/', views.actualizar_libro, name='actualizar_libro'),
    path('libro-detalles/<int:libro_id>/', views.libro_detalles, name='libro-detalles'),
    path('eliminar_libro/', views.eliminar_libro, name='eliminar_libro'),
    path('buscar-libros/', views.buscar_libros, name='buscar_libros'),
]
