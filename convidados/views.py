from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from noivos.models import Convidados, Presentes

def convidados(request: HttpRequest) -> HttpResponse:
    token = request.GET.get('token')
    if not token:
        return HttpResponse('Token não fornecido', status=400)
    convidado = get_object_or_404(Convidados, token=token)
    presentes = Presentes.objects.filter(reservado=False).order_by('-importancia')
    return render(request=request, template_name='convidados.html', 
                context={'convidado': convidado, 'presentes': presentes})

def responder_presenca(request: HttpRequest) -> HttpResponse:
    resposta = request.GET.get('resposta')
    print(resposta)
    token = request.GET.get('token')
    if not token or not resposta:
        # messages.error(request, 'Parâmetros inválidos')
        # return HttpResponse('Parâmetros inválidos', status=400)
        return redirect(reverse('convidados')+f'?token={token}')
    if resposta not in ['C','R']:
        return redirect(reverse('convidados')+f'?token={token}')
    try:
        convidado = get_object_or_404(Convidados, token=token)
        convidado.status = resposta
        convidado.save()
        return redirect(reverse('convidados')+f'?token={token}')
    except Exception as e:
        return HttpResponse('Erro ao processar resposta', status=500)
    
def reservar_presente(request: HttpRequest, id: int) -> HttpResponse:
    token = request.GET.get('token')
    if not token:
        # messages.error(request, 'Token não fornecido')
        return HttpResponse('Token não fornecido', status=400)
    try:
        convidado = get_object_or_404(Convidados, token=token)
        presente = get_object_or_404(Presentes, id=id)
        # Verifica se o presente já está reservado
        if presente.reservado:
            # messages.warning(request, 'Este presente já foi reservado')
            return redirect(reverse('convidados') + f'?token={token}')
        presente.reservado=True
        presente.reservado_por=convidado
        presente.save()
    except Exception as e:
        # messages.error(request, 'Erro ao reservar presente')
        return HttpResponse('Erro ao processar reserva', status=500)
    return redirect(reverse('convidados') + f'?token={token}')