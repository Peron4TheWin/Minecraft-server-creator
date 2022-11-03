from ensurepip import version
import subprocess
from requests import *
import os
import requests
from bs4 import BeautifulSoup
import re
import os
from termcolor import colored
import zipfile
from dataclasses import dataclass
import time
def clear():
    subprocess.call('cls',shell=True)
clear()
def cmd(command):
    return subprocess.check_output(command,shell=True).decode('utf-8').replace('','').replace("\r","").replace("\n","")
def cmdnormal(command):
    subprocess.run(command,shell=True)
def changepath(path):
    os.chdir(path)
def download(url, file_name):
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)
def extract(file_name):
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()
def fileexists(file_name):
    return os.path.isfile(file_name)
def direxists(dir_name):
    return os.path.isdir(dir_name)
def split_sentence(sentence, character):
    return re.split(character, sentence)

@dataclass
class paper:
    version:str
    serverlink:str
    paperlink:str
    papername:str
    java:str


@dataclass
class minecraft:
    version:str
    serverlink:str
    java:str

def launchnopaper(mc = minecraft("","","")):
    currpath = os.getcwd()
    listtmp = split_sentence(currpath,r'\\')
    templong = len(listtmp)-1
    if not listtmp[templong] == mc.version and not direxists(mc.version):
        cmdnormal(f"mkdir {mc.version}")
        changepath(mc.version)
    if not fileexists("server.jar"):
        download(mc.serverlink, "server.jar")
    if not fileexists("server.properties"):
        launchnp(mc,1)
        firstlaunch(mc,ver="normal")
    launchnp(mc)


def firstlaunch(mc = paper("", "", "", "", ""), ver = "paper"):
    global replacer
    cmdnormal(f'cscript {replacer} "server.properties" "online-mode=true" "online-mode=false')
    cmdnormal(f'cscript {replacer} "server.properties" "difficulty=easy" "difficulty=hard')
    cmdnormal(f'cscript {replacer} "server.properties" "allow-flight=false" "allow-flight=true')
    cmdnormal(f'cscript {replacer} "server.properties" "spawn-protection=16" "spawn-protection=0')
    os.system("rd /s /q plugins")
    if ver == "paper":
        launch(mc) 
    else:
        cmdnormal(f'cscript {replacer} "eula.txt" "eula=false" "eula=true')
        launchnp(mc)
    

def launchnp(mc = minecraft("", "", ""), first = 0):
    os.system(f"{mc.java} -Xms5G -Xmx5G -jar server.jar nogui")
    if first ==0:
        boolean=input("quieres reiniciar el servidor? (y/n)")
        if boolean == "y":
            launch(mc)
        else:
            for i in reversed(range(6,1)):
                clear()
                print("gracias por usar")
                print(f"{colored(f'saliendo en {i} segundos', 'red')}")
                time.sleep(1)
            exit()


def launch(mc = paper("", "", "", "", ""), first = 0):
    flags = fr"-Xms5G -Xmx5G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -Dcom.mojang.eula.agree=true -DPaper.IgnoreJavaVersion=True -jar {mc.papername} nogui"
    os.system(f"{mc.java} {flags}")
    if first ==0:
        boolean=input("quieres reiniciar el servidor? (y/n)")
        if boolean == "y":
            launch(mc)
        else:
            for i in reversed(range(6,1)):
                clear()
                print("gracias por usar")
                print(f"{colored(f'saliendo en {i} segundos', 'red')}")
                time.sleep(1)
            exit()

def versioner(mc = paper("", "", "", "", "")):
    currpath = os.getcwd()
    listtmp = split_sentence(currpath,r'\\')
    templong = len(listtmp)-1
    if not listtmp[templong] == mc.version and not direxists(mc.version):
        cmdnormal(f"mkdir {mc.version}")
        changepath(mc.version)
    if not fileexists("server.jar"):
        download(mc.serverlink, "server.jar")
        download(mc.paperlink, mc.papername)
    
    if not fileexists("server.properties"):
        cmdnormal(f"mkdir plugins")
        download("https://cdn.discordapp.com/attachments/864214612257800192/944807735587917844/plugins.zip", "plugins.zip")
        cmdnormal("move plugins.zip plugins")
        cmdnormal(fr"cd plugins && powershell Expand-Archive plugins.zip -DestinationPath {currpath}\plugins")
        launch(mc,1)
        firstlaunch(mc)
    launch(mc)

print("recuerda que todo en la carpeta del script sirve para algo")
print("no borres nada, todo es utilizado")
print("Seguime en tw @Peron4TheWin")
input("presiona enter para continuar")
clear()
ip = get('https://api.ipify.org').text

print(f"recuerda que la ip para que se unan sus amigos sera {colored(f'{ip}:25565','green')}")
print("si no sabes como abrir el puerto 25565, busca en google")
disk = cmd("echo %HOMEDRIVE%")
tmpvarpath = cmd (r"echo %userprofile%\documents\server")

if not direxists(tmpvarpath):
    cmdnormal(r"mkdir %userprofile%\documents\server")
serverroot = cmd(r"echo %userprofile%\documents\server")
changepath(fr"{serverroot}")

# TODO ESTO PARA ENTRAR EN LA CARPETA DEL SV AJAJJAJJAJAAJ

java8dir = "jre1.8.0_202"
java17dir = "jdk-17.0.2"

if not direxists(java8dir) and not direxists(java17dir):
    print("descargando java 17")
    download("https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_windows-x64_bin.zip","java17.zip")
    download("https://cdn.discordapp.com/attachments/901637950520033291/944710863296815184/test.vbs","test.vbs")
    print("descargando java 8")
    download("https://www.dropbox.com/s/0b2qv8ilyvshlu7/jre1.8.0_202.zip?dl=1","java8.zip")
    clear()
    extract("java17.zip")
    extract("java8.zip")
    cmdnormal("del /q /f java17.zip")
    cmdnormal("del /q /f java8.zip")
java8exe = fr"{serverroot}\{java8dir}\bin\java.exe"
java17exe = fr"{serverroot}\{java17dir}\bin\java.exe"
replacer = fr"{serverroot}\test.vbs"

versionn=""
#make al list with all available versions

def get_serverjar(version:str):
    url = f'https://mcversions.net/download/{version}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        try:
            var = split_sentence(link.get('href'),"/")[6]
            if var in ['server.jar']:
                return(link.get('href'))
        except:
            pass
papervers=["1.8.8","1.12.2","1.14.4","1.16.5","1.17.1","1.18.1","1.19.2"]
uno = paper(
    "1.8.8",
    "https://launcher.mojang.com/v1/objects/5fafba3f58c40dc51b5c3ca72a98f62dfdae1db7/server.jar",
    "https://papermc.io/api/v2/projects/paper/versions/1.8.8/builds/445/downloads/paper-1.8.8-445.jar",
    "paper-1.8.8-445.jar",
    java8exe
)
dos = paper(
    "1.12.2",
    "https://launcher.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar",
    "https://papermc.io/api/v2/projects/paper/versions/1.12.2/builds/1620/downloads/paper-1.12.2-1620.jar",
    "paper-1.12.2-1620.jar",
    java8exe
)
tres = paper(
    "1.14.4",
    "https://launcher.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar",
    "https://papermc.io/api/v2/projects/paper/versions/1.14.4/builds/245/downloads/paper-1.14.4-245.jar",
    "paper-1.14.4-245.jar",
    java8exe
)
cuatro = paper(
    "1.16.5",
    "https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar",
    "https://papermc.io/api/v2/projects/paper/versions/1.16.5/builds/794/downloads/paper-1.16.5-794.jar",
    "paper-1.16.5-794.jar",
    java8exe
)
cinco = paper(
    "1.17.1",
    "https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar",
    "https://papermc.io/api/v2/projects/paper/versions/1.17.1/builds/408/downloads/paper-1.17.1-408.jar",
    "paper-1.17.1-408.jar",
    java17exe
)
seis = paper(
    "1.18.1",
    "https://launcher.mojang.com/v1/objects/125e5adf40c659fd3bce3e66e67a16bb49ecc1b9/server.jar",
    "https://papermc.io/api/v2/projects/paper/versions/1.18.1/builds/203/downloads/paper-1.18.1-203.jar",
    "paper-1.18.1-203.jar",
    java17exe
)
siete = paper(
    "1.19.2",
    "https://piston-data.mojang.com/v1/objects/f69c284232d7c7580bd89a5a4931c3581eae1378/server.jar",
    "https://api.papermc.io/v2/projects/paper/versions/1.19.2/builds/243/downloads/paper-1.19.2-243.jar",
    "paper-1.19.2-243.jar",
    java17exe
)
input("presione enter para continuar")
clear()

#print all inside papervers like a single string using library
print("versiones disponibles (paper):")
print(*papervers," ")


print(f"""Quiere usar las versiones predeterminadas
(vienen con paperMC y configuradas con las mejores flags para el rendimiento)
o una custom (admite cualquier version, las predeterminadas solo aceptan )

{colored('predeterminada = 1','blue')}

{colored('custom = 2','magenta')}""")

if input("1 o 2? ") == "1":
    versionn=""
    while versionn not in papervers:
        print("ingrese la version a lanzar")
        print("1.8.8")
        print("1.12.2")
        print("1.14.4")
        print("1.16.5")
        print("1.17.1")
        print("1.18.1")
        print("1.19.2")
        versionn = input("version: ")
else:
    while True:
        versionn = input("ingrese la version a lanzar: ")
            #1165> java17
        if get_serverjar(versionn) == None:
            print("la version no existe")
            print("igrese otra")
        else:
            if int(versionn.replace(".","")) > 1165:
                javaexe = java17exe
            else:
                javaexe = java8exe
            custom = minecraft(versionn,get_serverjar(versionn),javaexe)
            launchnopaper(custom)
            





if versionn == "1.8.8":
    versioner(uno)
elif versionn == "1.12.2":
    versioner(dos)
elif versionn == "1.14.4":
    versioner(tres)
elif versionn == "1.16.5":
    versioner(cuatro)
elif versionn == "1.17.1":
    versioner(cinco)
elif versionn == "1.18.1":
    versioner(seis)
elif versionn == "1.19.2":
    versioner(siete)

