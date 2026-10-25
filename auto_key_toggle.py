import time
import sys
import threading
import pyautogui
import keyboard

# Desativa a trava de segurança do PyAutoGUI
pyautogui.FAILSAFE = False

# Configurações fixas
tecla = "r"
atalho = "f8"
intervalo = 0.5

# Variáveis de controle
executando = False
ativo = False

def loop_press():
    """Roda em segundo plano enviando a tecla quando estiver ativo."""
    global ativo, executando
    contador = 1
    while executando:
        if ativo:
            pyautogui.press(tecla)
            print(f"[{time.strftime('%H:%M:%S')}] Tecla '{tecla}' pressionada ({contador}x)")
            contador += 1
            time.sleep(intervalo)
        else:
            time.sleep(0.1)

def alternar_estado():
    """Liga ou Pausa o envio das teclas ao pressionar o atalho."""
    global ativo
    ativo = not ativo
    status = "LIGADO [ON]" if ativo else "PAUSADO [OFF]"
    print(f"\n>>> Autoclicker {status} <<<\n")

print("=== AUTO KEY PRESSER (COM ATALHO) ===")
print(f"Tecla a repetir: {tecla.upper()}")
print(f"Intervalo: {intervalo}s")
print("-------------------------------------------------")
print(f"Pressione '{atalho.upper()}' a qualquer momento para LIGAR ou PAUSAR.")
print("Para encerrar o programa, pressione 'Ctrl + C' no terminal.")
print("-------------------------------------------------\n")

# Associa a tecla de atalho à função de ligar/desligar
keyboard.add_hotkey(atalho, alternar_estado)

# Inicia a thread secundária
executando = True
thread = threading.Thread(target=loop_press, daemon=True)
thread.start()

try:
    keyboard.wait()
except KeyboardInterrupt:
    executando = False
    print("\nPrograma encerrado pelo usuário.")
    sys.exit()