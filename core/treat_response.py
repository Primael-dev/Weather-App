from core.getApi import request_API
from dotenv import load_dotenv
from core.getLocation import locate

load_dotenv()

#recup via getenv
LAT,LONG=locate()


URL_WEATHER = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LONG}&daily=temperature_2m_max,temperature_2m_min,weathercode"
    f"&timezone=auto"
)

#traitement de la reponse de weather
def treat_response_weather():
    try:
        weather=request_API(URL_WEATHER)
        return(weather)
    except Exception as e:
        return({f"Sorry error ":str(e)})
    
