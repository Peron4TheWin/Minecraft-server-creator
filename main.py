import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import zipfile
import subprocess
import threading
import tkinter as tk

def GetJARlink(version:str):
    url = 'https://mcversions.net/download/'+version
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            if href.endswith("server.jar"):
                return(href)

def GetPaperLink(version:str):
    a=requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds")
    if a.status_code==200:
        os.system("cls")
        a=a.json()
        base=(a.get("builds")[-1])
        build=base.get("build")
        jarname=(base.get("downloads").get("application").get("name"))
        return(fr"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/{jarname}")

def folder_exists(folder_path):
    return os.path.exists(folder_path)

def download(url,filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    block_size = 1024  # Adjust the block size as per your preference
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    filename = filename

    with open(filename, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    return filename

def extract_zip(ZipName):
    with zipfile.ZipFile(ZipName, 'r') as zip_ref:
        zip_ref.extractall()

def HavePaper(version:str):
    a=requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds")
    if a.status_code==200:
        return True
    else:
        return False
    
def direxist(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        os.chdir(directory_path)
        return False
    else:
        os.chdir(directory_path)
        return True
    
def get_java_version(minecraft_version):
    ver = int(minecraft_version.replace(".", ""))
    if ver >1165:
        return "17"
    else:
        return "8"
    
def AceptEula():
    file_path = "eula.txt"
    replacement_line = "eula=true"

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip() == "eula=false":
            lines[i] = replacement_line + "\n"

    with open(file_path, 'w') as file:
        file.writelines(lines)

def ConfigPropierties():
    file_path = "server.properties"
    replacements = {
        "online-mode=true": "online-mode=false",
        "difficulty=easy": "difficulty=hard",
        "allow-flight=false": "allow-flight=true",
        "spawn-protection=16": "spawn-protection=0"
    }

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        for original_line, new_line in replacements.items():
            if line.strip().startswith(original_line):
                lines[i] = new_line + "\n"
                break

    with open(file_path, 'w') as file:
        file.writelines(lines)



#Entrar a la carpeta C:\server (la crea si no existe)
disco = os.path.abspath(os.sep)
os.chdir(disco)
direxist("server")
rootfolder=os.getcwd()
javadic = {
    "8" : rootfolder+r"\j8\bin\java.exe",
    "17" : rootfolder+r"\j17\bin\java.exe"
}

#chequea si existe java, si no lo baja y lo extrae dejando dos carpetas (j8 y j17)
if not folder_exists("j8") or not folder_exists("j17"):
    download("https://cdn.discordapp.com/attachments/901637950520033291/1110983698066722997/java.zip","java.zip")
    extract_zip("java.zip")
    os.remove("java.zip")



while True:
    version=input("Ingrese una version a usar, por ejemplo 1.12.2\n:")
    try:
        #si la version no existe reintenta
        if requests.get('https://mcversions.net/download/'+version).status_code !=200:
            raise Exception("version no compatible")
        java=(javadic.get(get_java_version(version))) #obtiene el java (8 o 17)
        jarlink=GetJARlink(version) #consigue el link del server.jar
        direxist(version) #Si la carpeta no existe la crea luego hace CD, si no entra directamente
        os.system("cls")
        if not os.path.isfile("server.jar"):
            download(jarlink,"server.jar") #descarga server.jar si no existe
        if HavePaper(version): #si la version que elejiste tiene PaperMC, lo usa
            paperlink=GetPaperLink(version)
            if not os.path.isfile("paper.jar"):
                download(paperlink,"paper.jar")
            launchflags="-Xms5G -Xmx5G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -DPaper.IgnoreJavaVersion=True -jar paper.jar nogui"
        else:
            launchflags="-Xms5G -Xmx5G -jar server.jar nogui"
        command= fr"{java} {launchflags}"
        break
    except Exception as e:
        os.system("cls")
        print("La version que ingresaste no es correcta, reintenta")

def close_window(root):
    root.destroy()

def create_gui():
    root = tk.Tk()
    root.title("Configuration")
    
    message = "Please wait, configuring everything for you..."
    label = tk.Label(root, text=message)
    label.pack(padx=20, pady=20)
    
    root.after(60000, close_window,root)  # Close the window after 60 seconds
    
    root.mainloop()


if not os.path.isfile("eula.txt"):
    def start_server():
        server_command = command
        subprocess.call(server_command, shell=True)

    def stop_server():
        subprocess.call("taskkill /IM java.exe /f", shell=True)
    os.system(command)
    AceptEula()
    os.system("cls")
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    create_gui()
    stop_server()
    server_thread.join()
    ConfigPropierties()
os.system("cls")
while True:
    subprocess.call(command,shell=True)
    subprocess.call("cls",shell=True)
    if input("Deseas reiniciar el server? y/n")=="n":
        break