from django.conf import settings
from requests import request

class BanxicoService:
    
    def getConversionRate(self):
        response = request('GET', 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno', headers={
            'accept': 'application/json',
            'Bmx-Token': settings.BANXICO_TOKEN
        })
        obj = response.json()
        print(obj)
        return float(obj['bmx']['series'][0]['datos'][0]['dato'])

