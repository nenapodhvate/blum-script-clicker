from pyautogui import screenshot
import pygetwindow as gw
import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
from colorama import Fore, init

init(autoreset=True)
mouse = Controller()

def print_intro():
    print(Fore.RED + "кусакаби - t.me/zxcqusakabi")

def print_message(message):
    if "Play" in message:
        print(Fore.MAGENTA + message)
    else:
        print(message)

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

def activate_window(window):
    try:
        if window.isMinimized:
            window.restore()
        window.activate()
        return True
    except Exception as e:
        print(Fore.RED + f"[Error] | Could not activate window: {e}")
        return False

def click_play_button(window, is_first_time):
    try:
        if is_first_time:
            play_button_coords = (window.left + int(window.width * 0.75), window.top + int(window.height * 0.6))
        else:
            play_button_coords = (window.left + int(window.width * 0.5), window.top + int(window.height * 0.85) - 10)

        if activate_window(window):
            click(play_button_coords[0], play_button_coords[1])
            print_message('[🌙] | Play button clicked.')
            time.sleep(1)
    except Exception as e:
        print(Fore.RED + f"[Error] | Could not click 'Play' button: {e}")

def find_and_click_bacteria(window):
    scrn = screenshot(region=(window.left, window.top, window.width, window.height))
    width, height = scrn.size
    bacteria_found = False

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))
            if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                is_bomb = False
                for bx in range(-5, 6):
                    for by in range(-5, 6):
                        if 0 <= x + bx < width and 0 <= y + by < height:
                            br, bg, bb = scrn.getpixel((x + bx, y + by))
                            if br in range(100, 160) and bg in range(100, 160) and bb in range(100, 160):
                                is_bomb = True
                                break
                    if is_bomb:
                        break

                if not is_bomb:
                    screen_x = window.left + x
                    screen_y = window.top + y
                    click(screen_x + 4, screen_y)
                    time.sleep(0.001)
                    bacteria_found = True
    return bacteria_found

def handle_pause(paused):
    if keyboard.is_pressed('q'):
        paused = not paused
        if paused:
            print('[🌙] | Paused')
        else:
            print('[🌙] | Resuming')
        time.sleep(1)
    return paused

def start_game():
    window_name = input('\n[⚡️] | Crypto Clickers Hub | Press 1 ')
    if window_name == '1':
        window_name = "TelegramDesktop"

    try:
        num_games = int(input('\n[☘️] | Enter the number of games you want to play: '))
    except ValueError:
        print(Fore.RED + "[Error] | Invalid input for number of games!")
        return

    check = gw.getWindowsWithTitle(window_name)
    if not check:
        print(Fore.RED + f"[❌] | Window - {window_name} not found!")
        return

    print(f"[☘️] | Window found - {window_name}\n[☘️] | Press 'q' to pause.")
    telegram_window = check[0]
    paused = False
    games_played = 0
    is_first_time = True

    while games_played < num_games:
        click_play_button(telegram_window, is_first_time)
        is_first_time = False

        game_start_time = time.time()
        while time.time() - game_start_time < 31:
            paused = handle_pause(paused)
            while paused:
                paused = handle_pause(paused)

            if not paused:
                bacteria_found = find_and_click_bacteria(telegram_window)
                if not bacteria_found:
                    time.sleep(0.1)

        games_played += 1
        print(f"[🌕] | Game finished. Games played: {games_played}")

        if games_played < num_games:
            time.sleep(2)

    print(f'[☘️] | {num_games} games completed, script paused.')

if __name__ == "__main__":
    print_intro()
    while True:
        start_game()

