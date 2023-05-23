import requests
import json
import os
os.system("cls")
#https://api.papermc.io/v2/projects/paper/versions/1.17.1/builds/411/downloads/paper-1.17.1-411.jar
#https://api.papermc.io/v2/projects/paper/versions/1.19.1/builds
version=input("Ingresa una version\n(ejemplo 1.8.8)\nIngrese:")
a=requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds")
if a.status_code==200:
    a=a.json()
    base=(a.get("builds")[-1])
    build=base.get("build")
    jarname=(base.get("downloads").get("application").get("name"))
    #https://api.papermc.io/v2/projects/paper/versions/1.19.1/builds/111/downloads/paper-1.19.1-111.jar
    print(fr"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/{jarname}")
else:
    print("La version de paper que seleccionate no exite,prueba con otra")
