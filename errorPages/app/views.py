from django.shortcuts import render
from django.http import HttpResponse
from .utils import google_search
from .models import ErrorLog
from django.http import JsonResponse


def index(request):
  return HttpResponse("<h1>Hola Mundo</h1>")

def user(req):
  return render(req, 'user.html', status=200)

def show_error_404(req):
  return render(req, '404.html', status=404)

def show_error_500(req):
  return render(req, '500.html', status=500)

def generar_error(req):
  return 7/0

def onepage(req):
  return render(req, 'onepage.html', status=200)

def busqueda(req):
  query = req.GET.get("q", "")
  results = []
  if query: 
    data = google_search(query)
    results= data.get("items", [])
  return render(req, "search.html", {"results": results, "query": query})

def error_logs(req):
  return render(req, 'error_logs.html')

def get_error_logs(req):
  errors = ErrorLog.objects.values('id', 'codigo', 'mensaje', 'fecha')
  return JsonResponse({'data': list(errors)})