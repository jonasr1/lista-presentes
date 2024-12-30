from typing import List
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse

from noivos.styles import IMPORTANCIA_STYLES
from noivos.models import Convidados, Presentes


def home(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        presentes = Presentes.objects.all()
        nao_reservado = Presentes.objects.filter(reservado=False).count()
        reservado = Presentes.objects.filter(reservado=True).count()
        data = [nao_reservado, reservado]
        return render(request, template_name='home.html', context={
                    'presentes': add_styles_to_presentes(presentes), 'data': data})
    elif request.method == 'POST':
        try:
            importancia = int(request.POST.get('importancia'))
        except (ValueError, TypeError):
            return redirect('home')
        if importancia not in range(1,6):
            return redirect('home')
        
        nome_presente= request.POST.get('nome_presente')
        foto = request.FILES.get('foto')
        preco = request.POST.get('preco')
        
        presentes = Presentes(
            nome_presente= nome_presente,
            foto = foto,
            preco = preco,
            importancia = importancia
        )
        presentes.save()
        return redirect('home')
    return HttpResponse(status=405)  # Retorna um erro 405 caso o método não seja GET ou POST           

def lista_convidados(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        convidados = Convidados.objects.all()
        return render(request=request, template_name='lista_convidados.html', context={'convidados': convidados})
    elif request.method == 'POST':
        nome_convidado=request.POST.get('nome_convidado')
        whatsapp=request.POST.get('whatsapp')
        maximo_acompanhantes=int(request.POST.get('maximo_acompanhantes'))
        convidados = Convidados(
            nome_convidado=nome_convidado,
            whatsapp=whatsapp,
            maximo_acompanhantes=maximo_acompanhantes
        )
        convidados.save() # type: ignore
        return redirect('lista_convidados')


def add_styles_to_presentes(presentes: List[Presentes]) -> List[Presentes]:
    for presente in presentes:
        if presente.importancia <= 2:
            presente.style = IMPORTANCIA_STYLES['pouco_importante']
        elif presente.importancia >= 4:
            presente.style = IMPORTANCIA_STYLES['muito_importante']
        elif 2 < presente.importancia < 4:
            presente.style = IMPORTANCIA_STYLES['importante']
        else:
            presente.style = IMPORTANCIA_STYLES['moderada']
    return presentes
