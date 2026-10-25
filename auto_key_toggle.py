import time
import sys
import threading
from http.cookiejar import offset_from_tz_string

import pyautogui
import keyboard
from numpy import fft

# Desativa a trava de segurança do PyAutoGUI
pyautogui.FAILSAFE = False

# Configurações fixas - Tecla 1 (F)
tecla = "f"
atalho = "f8"
intervalo = 0.5

# Configurações fixas - Tecla 2 (Tab / Agro)
teclaAgro = "tab"
atalhoAgro = "f7"
intervaloAgro = 1.5

# Variáveis de controle
executando = False
ativo = False
ativoAgro = False

# Objeto para sincronizar os prints no terminal e evitar que se misturem
print_lock = threading.Lock()


def loop_press():
    """Roda em segundo plano enviando a primeira tecla quando ativo."""
    global ativo, executando
    contador = 1
    while executando:
        if ativo:
            pyautogui.press(tecla)
            with print_lock:
                print(f"[{time.strftime('%H:%M:%S')}] Tecla '{tecla}' pressionada ({contador}x)")
            contador += 1
            time.sleep(intervalo)
        else:
            time.sleep(0.1)


def loop_press_agro():
    """Roda em segundo plano enviando a tecla Tab quando ativo."""
    global ativoAgro, executando
    contador = 1
    while executando:
        if ativoAgro:
            pyautogui.press(teclaAgro)
            with print_lock:
                print(f"[{time.strftime('%H:%M:%S')}] Tecla '{teclaAgro}' pressionada ({contador}x)")
            contador += 1
            time.sleep(intervaloAgro)
        else:
            time.sleep(0.1)

def alternar_estado():
    """Liga ou Pausa o envio da primeira tecla."""
    global ativo
    ativo = not ativo
    status = "LIGADO [ON]" if ativo else "PAUSADO [OFF]"
    with print_lock:
        print(f"\n>>> Tecla '{tecla.upper()}' ({atalho.upper()}) {status} <<<\n")


def alternar_estado_agro():
    """Liga ou Pausa o envio da tecla Tab."""
    global ativoAgro
    ativoAgro = not ativoAgro
    status = "LIGADO [ON]" if ativoAgro else "PAUSADO [OFF]"
    with print_lock:
        print(f"\n>>> Tecla '{teclaAgro.upper()}' ({atalhoAgro.upper()}) {status} <<<\n")


print("=== AUTO KEY PRESSER (DUPLO ATALHO) ===")
print(f"1) Tecla: {tecla.upper()} | Atalho: {atalho.upper()} | Intervalo: {intervalo}s")
print(f"2) Tecla: {teclaAgro.upper()} | Atalho: {atalhoAgro.upper()} | Intervalo: {intervaloAgro}s")
print("-------------------------------------------------")
print("Para encerrar o programa, pressione 'Ctrl + C' no terminal.")
print("-------------------------------------------------\n")

# Associa as teclas de atalho às respectivas funções
keyboard.add_hotkey(atalho, alternar_estado)
keyboard.add_hotkey(atalhoAgro, alternar_estado_agro)

# Inicia as threads secundárias
executando = True
thread1 = threading.Thread(target=loop_press, daemon=True)
thread1.start()

thread2 = threading.Thread(target=loop_press_agro, daemon=True)
thread2.start()

try:
    keyboard.wait()
except KeyboardInterrupt:
    executando = False
    print("\nPrograma encerrado pelo usuário.")
    sys.exit()