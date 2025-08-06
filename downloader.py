import os
import shutil
import yt_dlp
import platform
from rich import print
from rich.console import Console

console = Console()

# ----------------------------------------------------------
# 1. Tentukan path otomatis sesuai OS / Specify automatic path according to OS
# ----------------------------------------------------------
def get_download_path():
    os_name = platform.system()
    if os_name == 'Linux' and 'ANDROID_STORAGE' in os.environ:
        # Jalur Android (termux atau aplikasi python android)
        android_path = '/storage/emulated/0/AADownloaderInfinte'
        return android_path
    else:
        # Windows & lainnya
        home = os.path.expanduser('~')
        windows_path = os.path.join(home, 'Downloads', 'Downloaderinfinty')
        return windows_path

DOWNLOAD_FOLDER = get_download_path()

# ----------------------------------------------------------
# 2. Buat folder kalau belum ada / Create a folder if it doesn't exist yet
# ----------------------------------------------------------
def ensure_download_folder():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
        console.print(f"[dim]Folder dibuat: {DOWNLOAD_FOLDER}[/dim]")
    else:
        console.print(f"[dim]Folder sudah ada: {DOWNLOAD_FOLDER}[/dim]")

# ----------------------------------------------------------
# 3. Hapus isi folder (tetap hapus file lama) / Delete folder contents (still delete old files)
# ----------------------------------------------------------
def clear_download_folder():
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            console.print(f"[red]Gagal hapus {file_path}: {e}[/red]")

# ----------------------------------------------------------
# 4. Logo & UI
# ----------------------------------------------------------
def print_logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print("""
[bold cyan]
   ▄█  ███▄▄▄▄      ▄████████  ▄█  ███▄▄▄▄       ███        ▄████████ 
  ███  ███▀▀▀██▄   ███    ███ ███  ███▀▀▀██▄ ▀█████████▄   ███    ███ 
  ███▌ ███   ███   ███    █▀  ███▌ ███   ███    ▀███▀▀██   ███    █▀  
  ███▌ ███   ███  ▄███▄▄▄     ███▌ ███   ███     ███   ▀  ▄███▄▄▄     
  ███▌ ███   ███ ▀▀███▀▀▀     ███▌ ███   ███     ███     ▀▀███▀▀▀     
  ███  ███   ███   ███        ███  ███   ███     ███       ███    █▄  
  ███  ███   ███   ███        ███  ███   ███     ███       ███    ███ 
  █▀    ▀█   █▀    ███        █▀    ▀█   █▀     ▄████▀     ██████████ 
[/bold cyan]
""")
    console.print("[bold green]Simple Downloader CLI | CTRL+C to exit[/bold green]\n")

# ----------------------------------------- -----------------
# 5. Fungsi download / Download function
# ----------------------------------------------------------
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            console.print(f"\n[green]Sukses download ke {DOWNLOAD_FOLDER}[/green]")
    except Exception as e:
        console.print(f"[red]Gagal download: {e}[/red]")

# ----------------------------------------------------------
# 6. Main loop
# ----------------------------------------------------------
def main_loop():
    ensure_download_folder()  # <-- jalan sekali saja saat start
    try:
        while True:
            clear_download_folder()
            print_logo()
            url = console.input("[bold yellow]Masukkan URL video (YouTube / IG / Reddit): [/bold yellow]")
            console.print("\n[blue]Sedang memproses...[/blue]")
            download_video(url)
            input("\n[bold cyan]Tekan ENTER untuk kembali ke menu...[/bold cyan]")
    except KeyboardInterrupt:
        console.print("\n[bold red]Keluar... Sampai jumpa![/bold red]")

if __name__ == "__main__":
    main_loop()
