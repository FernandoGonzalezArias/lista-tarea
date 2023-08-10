from django.shortcuts import render
from django.http import HttpResponseRedirect
from administrar.models import Tarea
from .forms import TareaForm
from django.contrib.auth import logout
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required 


@login_required(login_url = "/iniciar-sesion")
@permission_required('administrar.view_tarea',  login_url= "/permisos-denegados")
def v_index(request):
  if request.method == 'POST':
    if not request.user.has_perm("administrar.add_tarea"):
      return HttpResponseRedirect("/permisos-denegados")
    _titulo = request.POST["titulo"]
    datos = request.POST.copy()
    form = TareaForm(datos)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect("/")
    else:
      return HttpResponseRedirect("/")
  else:
    consulta = Tarea.objects.filter(titulo__icontains = request.GET.get("titulo", ""))
    if request.GET.get("estado", "") != "":
        consulta = consulta.filter(estado = request.GET.get("estado", ""))
    context = {
      'lista': consulta
    }
    return render(request, 'index.html', context)
  
  
@login_required(login_url = "/iniciar-sesion")
@permission_required('administrar.delete_tarea',  login_url= "/permisos-denegados")
def v_eliminar(request, tarea_id):
  Tarea.objects.filter(id = tarea_id).delete()
  return HttpResponseRedirect("/")


@login_required(login_url = "/iniciar-sesion")
@permission_required('administrar.change_tarea',  login_url= "/permisos-denegados")
def v_completado(request, tarea_id):
  task = Tarea.objects.get(id = tarea_id)
  task.estado = 1
  task.save()
  return HttpResponseRedirect("/")

def v_login(request):
  if request.method == "POST":
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(username = form.cleaned_data["username"],
      password = form.cleaned_data["password"])
      if user is not None:
        login(request, user)
        return HttpResponseRedirect("/")
      else:
        return HttpResponseRedirect("/")
    else:
      return HttpResponseRedirect("/")
  else:
     context = {
       "form": LoginForm(request.POST)
     }
     return render(request, "login.html", context)
  
def v_logout(request):
   if request.user.is_authenticated:
     logout(request)
     
   return HttpResponseRedirect("/")
 
def v_permisos(request):
  return render(request, "permisos-denegados.html" )