from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from convidados.models import Acompanhante
from noivos.models import Convidados, Presentes


def adicionar_acompanhantes(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        convidado = get_object_or_404(Convidados, token=request.GET.get('token'))
        return redirect(reverse('convidados') + f'?token={request.POST.get("token")}')
    parametros = {'token': 'POST', 'nome': 'POST'}
    valores = {}
    token = request.POST.get('token')
    for parametro, _ in parametros.items():
        if not (valor := request.POST.get(parametro)):
            messages.add_message(request, messages.WARNING, message=f'{parametro.capitalize()} do acompanhante não fornecido')
            return redirect(reverse('convidados') + f'?token={request.POST.get("token")}')
        valores[parametro] = valor
    convidado = get_object_or_404(Convidados, token=valores['token'])
    if convidado.acompanhantes_confirmados >= convidado.maximo_acompanhantes:
        messages.warning(request, 'Número máximo de acompanhantes atingido')
        return redirect(reverse('convidados') + f'?token={valores["token"]}')
    nome=str(valores['nome']).strip()
    if not nome.isalpha():
        messages.warning(request, 'O nome do acompanhante deve conter apenas letras')
        return redirect(reverse('convidados') + f'?token={valores["token"]}')
    nome = nome.capitalize()
    Acompanhante.objects.create(nome=nome, convidado=convidado)
    convidado.acompanhantes_confirmados +=1
    convidado.save()
    messages.success(request, f'Acompanhante {nome} adicionado com sucesso!')
    return redirect(reverse('convidados') + f'?token={token}')


def detatalhe_convidado(request: HttpRequest) -> HttpResponse:
    token = request.GET.get('token')
    if not token:
        return HttpResponse('Token não fornecido', status=400)
    convidado = get_object_or_404(Convidados, token=token)
    presentes = Presentes.objects.filter(reservado=False).order_by('-importancia')
    acompanhates = Acompanhante.objects.filter(convidado=convidado)
    return render(request=request, template_name='convidados.html', 
                context={'convidado': convidado, 'presentes': presentes, 'acompanhantes': acompanhates})


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
    except Exception:
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
    except Convidados.DoesNotExist:
        return HttpResponse('Convidado não encontrado', status=404)
    except Presentes.DoesNotExist:
        return HttpResponse('Presente não encontrado', status=404)
    except Exception:
        # messages.error(request, 'Erro ao reservar presente')
        return HttpResponse('Erro ao processar reserva', status=500)
    return redirect(reverse('convidados') + f'?token={token}')
