from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro
from django.http import JsonResponse
from .forms import LibroForm
from django.views.decorators.http import require_POST
from django.db.models import Q

def buscar_libros(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        libros = Libro.objects.filter(
            Q(nombre__icontains=q) | 
            Q(autor__icontains=q) | 
            Q(categoria__icontains=q)
        )[:5]
        results = []
        for libro in libros:
            libro_json = {
                'id': libro.id,
                'nombre': libro.nombre
            }
            results.append(libro_json)
        return JsonResponse(results, safe=False)
    return JsonResponse({"error": "No se encontraron libros"}, status=400)

def libro_detalles(request, libro_id):
    try:
        libro = Libro.objects.get(pk=libro_id)
        datos = {
            'nombre': libro.nombre,
            'autor': libro.autor,
            'categoria': libro.categoria,
            'fecha_publicacion': libro.fecha_publicacion,
            'descripcion': libro.descripcion,
        }
        return JsonResponse(datos)
    except Libro.DoesNotExist:
        return JsonResponse({'error': 'Libro no encontrado'}, status=404)

def home(request):
    libros = Libro.objects.all().order_by('-id')[:3]  
    return render(request, 'biblioteca/home.html', {'libros': libros})

def admin_page(request):
    libros = Libro.objects.all().order_by('-id')[:3]  # Ordenar por ID descendente y tomar los últimos 3 libros
    return render(request, 'biblioteca/adminpage.html', {'libros': libros})

def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpage')
    return redirect('adminpage')

def actualizar_libro(request):
    if request.method == 'POST':
        libro_id = request.POST.get('id')
        libro = get_object_or_404(Libro, id=libro_id)
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('adminpage')
        else:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)
    return redirect('adminpage')

@require_POST
def eliminar_libro(request):
    libro_id = request.POST.get('id')
    libro = get_object_or_404(Libro, pk=libro_id)
    libro.delete()
    return redirect('adminpage')