import requests

#fonction de requete via url
def request_API(url):

    try:
        reponse_url=requests.get(url)

        if reponse_url.status_code==200:
            return(reponse_url.json())
        else:
            print(reponse_url.status_code)
            return{}
        
    except Exception as e:
        return ({"Error":f"Error {e} during the process"})
    
