import csv
from datetime import date
from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from data_scraper.models import WeatherData, DataSource, StationSuggestion

# Create your views here.
def index(request):
    return render(request, 'index.html')


def fontes(request):
    context = {
        'fontes': DataSource.objects.all(),
        'sugestoes_pendentes': StationSuggestion.objects.filter(status='pending')
    }
    return render(request, 'fontes.html', context)


@csrf_exempt
def export_weather_data(request):
    if request.method == 'POST':
        # Recupere as datas do formulário POST
        start_date_str = request.POST.get('startdate')
        end_date_str = request.POST.get('enddate')
        fonte = request.POST.get('fonte')

        # Converta as strings de data para objetos datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        print(fonte)
        # Consulte o banco de dados para recuperar os dados dentro do intervalo de tempo especificado
        weather_data = WeatherData.objects.filter(date__range=(start_date, end_date), fonte__id=fonte)

        # Crie a resposta CSV
        # Get the current date
        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        
        # Obter o nome da fonte
        fonte_obj = DataSource.objects.get(id=fonte)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{fonte_obj.name}_{current_date}_weather_data.csv"'

        # Escreva os dados no arquivo CSV
        writer = csv.writer(response)
        writer.writerow(['Date', 'Temperature', 'Wind_Gust_Direction', 'Wind_Gust', 'Dewpoint', 'Precip_Rate', 'Pressure', 'Humidity', 'Precip_Accum', 'UV', 'Fonte'])
        for data in weather_data:
            writer.writerow([
                data.date.strftime('%Y-%m-%d %H:%M:%S'),
                data.temperature,
                data.wind_gust_direction,
                data.wind_gust,
                data.dewpoint,
                data.precip_rate,
                data.pressure,
                data.humidity,
                data.precip_accum,
                data.uv,
                data.fonte.name
            ])

        return response

    return render(request, 'filter.html', context={'fontes': DataSource.objects.all()})


@csrf_exempt
def view_weather_data(request):
    context={'fontes': DataSource.objects.all()}
    if request.method == 'POST':
        start_date_str = request.POST.get('startdate')
        end_date_str = request.POST.get('enddate')
        fonte = request.POST.get('fonte')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        weather_data = WeatherData.objects.filter(date__range=(start_date, end_date), fonte__id=fonte)
        context['startdate'] = start_date_str
        context['enddate'] = end_date_str
        context['datas'] = weather_data
        return render(request, 'ver_dados.html', context)

    return render(request, 'filter_online.html', context)


def json_fontes(request):
    fontes = DataSource.objects.all()
    return JsonResponse(json.loads(serialize('json', fontes)), safe=False)

def json_dados(request,  fonte_id, dt_start, dt_end):
        dados = WeatherData.objects.filter(date__range=(dt_start, dt_end), fonte__id=fonte_id)
        valores = []
        for dado in dados:
            valores.append({
                'temperature': dado.temperature,
                'wind_gust_direction': dado.wind_gust_direction,
                'wind_gust': dado.wind_gust,
                'dewpoint': dado.dewpoint,
                'precip_rate': dado.precip_rate,
                'pressure': dado.pressure,
                'humidity': dado.humidity,
                'precip_accum': dado.precip_accum,
                'uv': dado.uv,
                'date': dado.date,
                'fonte': dado.fonte.name
            })
        return JsonResponse(valores, safe=False)


@csrf_exempt
def suggest_station(request):
    """View para usuários sugerirem novas estações"""
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        message = request.POST.get('message', '')
        
        if name and url:
            suggestion = StationSuggestion.objects.create(
                name=name,
                url=url,
                message=message
            )
            messages.success(request, 'Sugestão enviada com sucesso! Obrigado pela contribuição.')
            return redirect('suggest_station')
        else:
            messages.error(request, 'Nome e URL são obrigatórios.')
    
    return render(request, 'suggest_station.html')


def manage_suggestions(request):
    """View para administradores gerenciarem as sugestões"""
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    suggestions = StationSuggestion.objects.all()
    context= {
                'suggestions': suggestions,
                'total_pending': suggestions.filter(status='pending').count(),
                'total_approved': suggestions.filter(status='approved').count(),
                'total_rejected': suggestions.filter(status='rejected').count(),
              }
    return render(request, 'manage_suggestions.html', context)


@csrf_exempt
def approve_suggestion(request, suggestion_id):
    """View para aprovar uma sugestão e criar um DataSource"""
    if request.method == 'POST':
        suggestion = get_object_or_404(StationSuggestion, id=suggestion_id)
        
        if suggestion.status == 'pending':
            # Criar o DataSource
            data_source = DataSource.objects.create(
                name=suggestion.name,
                url=suggestion.url
            )
            
            # Atualizar status da sugestão
            suggestion.status = 'approved'
            suggestion.save()
            
            messages.success(request, f'Sugestão aprovada! DataSource "{suggestion.name}" criado com sucesso.')
        else:
            messages.warning(request, 'Esta sugestão já foi processada.')
    
    return redirect('manage_suggestions')


@csrf_exempt
def reject_suggestion(request, suggestion_id):
    """View para rejeitar uma sugestão"""
    if request.method == 'POST':
        suggestion = get_object_or_404(StationSuggestion, id=suggestion_id)
        
        if suggestion.status == 'pending':
            suggestion.status = 'rejected'
            suggestion.save()
            messages.success(request, f'Sugestão "{suggestion.name}" rejeitada.')
        else:
            messages.warning(request, 'Esta sugestão já foi processada.')
    
    return redirect('manage_suggestions')


def saiba_mais(request):
    """View para a página Saiba Mais"""
    return render(request, 'saiba_mais.html')