import pygame
import os
import colorama
from colorama import Fore, Style, init
from time import sleep

RED = Fore.LIGHTRED_EX + Style.BRIGHT
GREEN = Fore.LIGHTGREEN_EX + Style.BRIGHT
BLUE = Fore.LIGHTCYAN_EX + Style.BRIGHT
MAGENTA = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
WHITE = Fore.LIGHTWHITE_EX + Style.BRIGHT
RESET = Style.RESET_ALL

def initialize_player():
    pygame.init()
    pygame.mixer.init()

def load_file(filepath):
    if not os.path.isfile(filepath):
        print(f"\n{WHITE}[{RED}ERR_FILE_NOT_FOUND{WHITE}] File does not exist.{RESET}")
        return False, 0

    try:
        pygame.mixer.music.load(filepath)
        # Get file info using pygame
        audio = pygame.mixer.Sound(filepath)
        duration = audio.get_length()
        file_size = os.path.getsize(filepath)
        return duration, file_size
    except pygame.error as e:
        print(f"\n{WHITE}[{RED}err{WHITE}] Error loading file:{RED} {e}{RESET}")
        return False, 0

def play():
    pygame.mixer.music.play()
    global playing
    playing = True

def pause():
    pygame.mixer.music.pause()
    global playing
    playing = False

def unpause():
    pygame.mixer.music.unpause()
    global playing
    playing = True

def stop():
    pygame.mixer.music.stop()
    global playing
    playing = False

def set_volume(percentage):
    # Convert percentage (0-100) to volume level (0.0-1.0)
    volume_level = percentage / 100.0
    pygame.mixer.music.set_volume(volume_level)
    print(f"\n{WHITE}>> Volume set to: {GREEN}{percentage}%{RESET}\n")

def command_loop():
    global playing, duration
    while True:
        command = input(f"{WHITE}[{BLUE}>{WHITE}] Enter command:{GREEN} ").strip().split()
        RESET
        
        if len(command) == 0:
            continue
        
        action = command[0].lower()
        
        if action == "load" and len(command) > 1:
            filepath = " ".join(command[1:])
            duration, file_size = load_file(filepath)
            if duration:
                print(f'\n{WHITE}======================================{RESET}')
                print(f"{WHITE}>> Loaded file:{GREEN} {filepath}{RESET}")
                print(f"{WHITE}>> Duration:{GREEN} {int(duration)} seconds{RESET}")
                print(f"{WHITE}>> File size:{GREEN} {format_file_size(file_size)}{RESET}")
                print(f'{WHITE}======================================{RESET}\n')
            else:
                print(f"\n{WHITE}>>{GREEN} Failed to load file{RESET}\n")
        elif action == "play":
            if duration:
                play()
                print(f"\n{WHITE}>>{GREEN} Playing...{RESET}\n")
            else:
                print(f"\n{WHITE}>>{RED} No file loaded{RESET}\n")
        elif action == "pause":
            pause()
            print(f"\n{WHITE}>> {GREEN}Paused{RESET}\n")
        elif action == "unpause":
            unpause()
            print(f"\n{WHITE}>>{GREEN} Unpaused\n")
        elif action == "stop":
            stop()
            print(f"\n{WHITE}>>{GREEN} Stopped\n")
        elif action == "volume" and len(command) > 1:
            try:
                new_volume = int(command[1])
                if 0 <= new_volume <= 100:
                    set_volume(new_volume)
                else:
                    print(f"\n{WHITE}>> {BLUE}Volume level must be between 0 and 100\n")
            except ValueError:
                print(f"\n{WHITE}>>{RED} Invalid volume level\n")
        elif action == "quit":
            stop()
            print(f"\n{WHITE}>>{BLUE} Exiting player\n")
            sleep(2)
            break
        else:
            print(f"\n{WHITE}>>{RED} Unknown command\n")

def format_file_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

def main():
    initialize_player()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'''{WHITE}
===========================================================================
{BLUE}                              pyPlayer v1.0.1                          {WHITE}
==========================================================================={RESET}\n''')
    
    print(f"{WHITE}// Commands: {MAGENTA}load <filepath>{WHITE}, {MAGENTA}play{WHITE}, {MAGENTA}pause{WHITE}, {MAGENTA}unpause{WHITE}, {MAGENTA}stop{WHITE}, {MAGENTA}volume <0-100>{WHITE}, {MAGENTA}quit {WHITE}//{RESET}")
    print(f"{WHITE}// Info: {GREEN}Only can load audio files for now, additional formats may be included in future updates...{WHITE} //{RESET}\n")

    global playing, duration
    playing = False
    duration = 0

    command_loop()

if __name__ == "__main__":
    main()
