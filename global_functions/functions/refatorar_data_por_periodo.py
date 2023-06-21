from datetime import timedelta


def refatorar_data_por_periodo(data_base, tipo_filtro):
    data = ''
    if tipo_filtro == 'diario':
        data = f"{data_base.day if data_base.day > 9 else ('0' + str(data_base.day))}/{data_base.month if data_base.month > 9 else ('0' + str(data_base.month))}/{str(data_base.year)[-2::]}"
    elif tipo_filtro == 'mensal':
        data = f"{data_base.month if data_base.month > 9 else ('0' + str(data_base.month))}/{str(data_base.year)[-2::]}"
    elif tipo_filtro == 'anual':
        data = f"{data_base.year}"
    elif tipo_filtro == 'semanal':
        start_date = data_base - timedelta(days=data_base.weekday())
        end_date = start_date + timedelta(days=6)
        data = f"Semana de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
    elif tipo_filtro == 'horario':
        data = f"{data_base.strftime('%d/%m/%Y')} de {data_base.strftime('%H:%M')} às {data_base.replace(hour=(data_base.hour + 1) % 24).strftime('%H:%M')}"

    return data
