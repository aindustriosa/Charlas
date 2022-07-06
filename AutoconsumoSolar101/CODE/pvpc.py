

#curl 
#-H "Authorization: Token token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
#-H "Accept: application/json; application/vnd.esios-api-v2+json" 
#-v -L "http://api.esios.ree.es/indicators/10391/?start_date=2021-06-03T03%3A00%3A00Z&end_date=2021-06-03T04%3A00%3A00Z&geo_ids[]=8741"
  

import requests
from datetime import datetime


now = datetime.now()
now_time = now.strftime('%Y-%M-%dT00:00:00Z')
next_time = now.strftime('%Y-%M-%dT23:59:59Z')

serverName = 'https://api.esios.ree.es/indicators/10391/'
serverPath = serverName + "?start_date="+now_time+"&end_date="+next_time+"&geo_ids[]=8741"

token = ''

r = requests.get(
    serverPath,
    headers={
        'Authorization': 'Token token=' + token,
        "Accept":"application/json; application/vnd.esios-api-v2+json"
        }
    )

#print(r. json())#r. status_code -->200

if(r. status_code  == 200):
    v=[]
    for rows in r.json()['indicator']['values']:
        date = datetime.strptime(rows['datetime'],'%Y-%m-%dT%H:00:00.000+02:00')
        hour = date.hour
        value = round(rows['value']/1000,4)
        v.append([value,hour])


    print(max(v))
    print(min(v))
        #0.2957--2021-10-06T00:00:00.000+02:00 --> 2021-10-06 00:00:00

'''

Lo primero que necesitas es obtener un token para la api de esios/red electrica. Es muy fácil. sólo tienes que enviar un mail a   consultasios@ree.es con el texto del asunto asunto  **Solicitud de token personal** . En 10 min responden con el token

Cambiar en Arduino:

const char *ssid     = "XXXXX";

const char *password = "XXXXX";

const String token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";

# API ESIOS RED ELECTICA

https://api.esios.ree.es

https://api.esios.ree.es/indicators //Devuelve los códiigos de funciones
10391 es el código para la tarifa 2.0TD

## Obtener datos diarios de la tarifa
https://api.esios.ree.es/indicators/10391   //2.0 TD

Authorization: Token token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Accept: application/json; application/vnd.esios-api-v2+json

## Obtener datos en un rango de fechas y localización
https://api.esios.ree.es/indicators/10391?start_date=2021-06-03T03%3A00%3A00Z&end_date=2021-06-03T04%3A00%3A00Z&geo_ids[]=8741

Authorization: Token token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Accept: application/json; application/vnd.esios-api-v2+json

{
   "indicator":{
      "name":"Término de facturación de energía activa del PVPC 2.0TD suma componentes",
      "short_name":"2.0TD suma componentes",
      "id":10391,
      "composited":true,
      "step_type":"linear",
      "disaggregated":true,
      "magnitud":[
         {
            "name":"Precio",
            "id":23
         }
      ],
      "tiempo":[
         {
            "name":"Hora",
            "id":4
         }
      ],
      "geos":[
         
      ],
      "values_updated_at":"None",
      "values":[
         {
            "value":295.67,
            "datetime":"2021-10-06T00:00:00.000+02:00",
            "datetime_utc":"2021-10-05T22:00:00Z",
            "tz_time":"2021-10-05T22:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":295.86,
            "datetime":"2021-10-06T01:00:00.000+02:00",
            "datetime_utc":"2021-10-05T23:00:00Z",
            "tz_time":"2021-10-05T23:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":294.11,
            "datetime":"2021-10-06T02:00:00.000+02:00",
            "datetime_utc":"2021-10-06T00:00:00Z",
            "tz_time":"2021-10-06T00:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":289.84,
            "datetime":"2021-10-06T03:00:00.000+02:00",
            "datetime_utc":"2021-10-06T01:00:00Z",
            "tz_time":"2021-10-06T01:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":286.18,
            "datetime":"2021-10-06T04:00:00.000+02:00",
            "datetime_utc":"2021-10-06T02:00:00Z",
            "tz_time":"2021-10-06T02:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":285.79,
            "datetime":"2021-10-06T05:00:00.000+02:00",
            "datetime_utc":"2021-10-06T03:00:00Z",
            "tz_time":"2021-10-06T03:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":293.6,
            "datetime":"2021-10-06T06:00:00.000+02:00",
            "datetime_utc":"2021-10-06T04:00:00Z",
            "tz_time":"2021-10-06T04:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":294.83,
            "datetime":"2021-10-06T07:00:00.000+02:00",
            "datetime_utc":"2021-10-06T05:00:00Z",
            "tz_time":"2021-10-06T05:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":324.75,
            "datetime":"2021-10-06T08:00:00.000+02:00",
            "datetime_utc":"2021-10-06T06:00:00Z",
            "tz_time":"2021-10-06T06:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":309.23,
            "datetime":"2021-10-06T09:00:00.000+02:00",
            "datetime_utc":"2021-10-06T07:00:00Z",
            "tz_time":"2021-10-06T07:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":306.95,
            "datetime":"2021-10-06T10:00:00.000+02:00",
            "datetime_utc":"2021-10-06T08:00:00Z",
            "tz_time":"2021-10-06T08:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":278.41,
            "datetime":"2021-10-06T11:00:00.000+02:00",
            "datetime_utc":"2021-10-06T09:00:00Z",
            "tz_time":"2021-10-06T09:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":272.18,
            "datetime":"2021-10-06T12:00:00.000+02:00",
            "datetime_utc":"2021-10-06T10:00:00Z",
            "tz_time":"2021-10-06T10:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":264.63,
            "datetime":"2021-10-06T13:00:00.000+02:00",
            "datetime_utc":"2021-10-06T11:00:00Z",
            "tz_time":"2021-10-06T11:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":257.92,
            "datetime":"2021-10-06T14:00:00.000+02:00",
            "datetime_utc":"2021-10-06T12:00:00Z",
            "tz_time":"2021-10-06T12:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":258.15,
            "datetime":"2021-10-06T15:00:00.000+02:00",
            "datetime_utc":"2021-10-06T13:00:00Z",
            "tz_time":"2021-10-06T13:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":262.49,
            "datetime":"2021-10-06T16:00:00.000+02:00",
            "datetime_utc":"2021-10-06T14:00:00Z",
            "tz_time":"2021-10-06T14:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":295.77,
            "datetime":"2021-10-06T17:00:00.000+02:00",
            "datetime_utc":"2021-10-06T15:00:00Z",
            "tz_time":"2021-10-06T15:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":321.55,
            "datetime":"2021-10-06T18:00:00.000+02:00",
            "datetime_utc":"2021-10-06T16:00:00Z",
            "tz_time":"2021-10-06T16:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":342.69,
            "datetime":"2021-10-06T19:00:00.000+02:00",
            "datetime_utc":"2021-10-06T17:00:00Z",
            "tz_time":"2021-10-06T17:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":348.86,
            "datetime":"2021-10-06T20:00:00.000+02:00",
            "datetime_utc":"2021-10-06T18:00:00Z",
            "tz_time":"2021-10-06T18:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":332.8,
            "datetime":"2021-10-06T21:00:00.000+02:00",
            "datetime_utc":"2021-10-06T19:00:00Z",
            "tz_time":"2021-10-06T19:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":319.38,
            "datetime":"2021-10-06T22:00:00.000+02:00",
            "datetime_utc":"2021-10-06T20:00:00Z",
            "tz_time":"2021-10-06T20:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         },
         {
            "value":308.65,
            "datetime":"2021-10-06T23:00:00.000+02:00",
            "datetime_utc":"2021-10-06T21:00:00Z",
            "tz_time":"2021-10-06T21:00:00.000Z",
            "geo_id":8741,
            "geo_name":"Península"
         }
      ]
   }
}

'''
