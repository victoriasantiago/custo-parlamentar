from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Deputados, GastoMensal, Categorias
import time


def retorna_gastos(request, ano='', mes=''):
    try:
        slug_deputado = request.POST.get('slug_deputado')
        ano = request.POST.get('ano')
    except Exception as e:
        print(e)
        return HttpResponse('Não foi possível salvar informações.', status=401)

    deputado_id = Deputados.objects.get(slug=slug_deputado).id_deputado
    dados = GastoMensal.objects.filter(ano=str(ano), id_deputado=deputado_id)
    gastos = {}
    gastos[ano] = {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}, '8': {}, '9': {}, '10': {}, '11': {}, '12': {}}
    categorias = ['10', '11', '12', '13', '14', '15']

    for(k, v) in gastos[ano].items():
        for cat in categorias:
            gastos[ano][k][cat] = {}

    for gasto in dados:
        gastos[ano][str(gasto.mes)][str(gasto.id_categoria.id_categoria)] = str(gasto.valor)

    return gastos

def DadosDeputadoView(request):
    gastos = retorna_gastos(request)
    # try:
    #     slug_deputado = request.POST.get('slug_deputado')
    #     ano = request.POST.get('ano')
    # except Exception as e:
    #     print(e)
    #     return HttpResponse('Não foi possível salvar informações.', status=401)
    #
    # deputado_id = Deputados.objects.get(slug=slug_deputado).id_deputado
    # dados = GastoMensal.objects.filter(ano=str(ano), id_deputado=deputado_id)
    # gastos = {}
    # gastos[ano] = {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}, '8': {}, '9': {}, '10': {}, '11': {}, '12': {}}
    # categorias = ['10', '11', '12', '13', '14', '15']
    #
    # for(k, v) in gastos[ano].items():
    #     for cat in categorias:
    #         gastos[ano][k][cat] = {}
    #
    # for gasto in dados:
    #     gastos[ano][str(gasto.mes)][str(gasto.id_categoria.id_categoria)] = str(gasto.valor)

    return JsonResponse(gastos)

def IndexView(request, slug='', ano='', mes=''):
    todos_deputados = Deputados.objects.all().exclude(mandato_atual=False)
    context = {'deputados': todos_deputados}

    if ano == '' or mes == '':
        mes = time.strftime("%m")
        ano = time.strftime("%Y")
    try:
        if Deputados.objects.get(slug=slug) and slug != 'favicon.ico':
            deputado_atual = Deputados.objects.get(slug=slug)
            id_do_deputado = Deputados.objects.get(slug=slug).id_deputado
            context['deputado_atual'] = deputado_atual
    except Exception as e:
        deputado_atual = 'Alba'

    def retorna_valores_items(gastos_mes):
        gastos = {}
        for item in gastos_mes:
            i = item.id_categoria.id_categoria
            gastos[i] = {}
            gastos[i]['id_deputado'] = item.id_deputado
            gastos[i]['mes'] = item.mes
            gastos[i]['id_categoria'] = item.id_categoria.id_categoria
            gastos[i]['valor'] = str(item.valor)
            gastos[i]['ano'] = item.ano
        return gastos

    try:
        month = int(mes)
        year = int(ano)
    except Exception as e:
        print(e)

    if deputado_atual != 'Alba' and ((type(month) == int and (month > 0 and month < 13)) and (type(year) == int and (year > 2007 and year < 2018))):
        gastos_mes = GastoMensal.objects.filter(ano=str(ano), mes=str(mes), id_deputado=id_do_deputado)
        context['gastos'] = retorna_valores_items(gastos_mes)


    # elif deputado_atual == 'Alba':
    #     gastos_mes = GastoMensal.objects.filter(ano=ano_atual, mes=mes_atual, id_deputado=id_do_deputado)
    #     gastos = retorna_valores_items(gastos_mes)
    #     print(gastos)

    # categorias_gastos = Categorias.objects.all()
    # context['categorias'] = categorias_gastos
    #print(context)

    return render(request, 'index.html', context)
