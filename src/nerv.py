import os
import json

colors = {
    "normal": "\033[0m",    # Beyaz
    "angry": "\033[91m",     # Kırmızı
    "blushing": "\033[95m",  # Mor
    "thinking": "\033[96m",  # Mavi
    "smile": "\033[92m",     # Yeşil
}

def print_colored(text, status):
    color = colors.get(status, "\033[0m")
    print(f"{color}{text}\033[0m")

