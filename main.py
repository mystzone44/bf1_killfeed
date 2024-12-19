from PIL import Image
from modules import capture, Model, kick_player
import numpy as np
import api
import tkinter as tk
from tkinter import ttk
import threading
import globals
from config import read_config, data
import keyboard


def set_widget_readonly(widget):
    text_widget.see(tk.END)
    text_widget.configure(state=tk.DISABLED)

def write_to_widget(msg, widget):
    text_widget.configure(state=tk.NORMAL)
    text_widget.insert(tk.END, msg)
    set_widget_readonly(widget)

def print_and_write(msg, widget):
    print(msg)
    write_to_widget(msg, widget)

def check_killfeed():
    print('Checking killfeed...')
    text_widget.configure(state=tk.NORMAL)
    text_widget.insert(tk.END, "Checking killfeed...\n")

    np_image = capture(data.killfeed_area)

    kick_players = model.predict(np_image)

    for player, weapon_id in kick_players.items():

        with globals.kick_list_lock:
            if player in globals.kick_list:
                print(f'Player {player} already in kick list, skipping')
                continue

        # Kick
        with globals.teams_lock:
            if player not in globals.teams:
                continue
            persona_id = globals.teams[player]
            success, weapon = kick_player(globals.game_id, persona_id, weapon_id)
            if not success:
                print(f'Failed to kick player {player} with weapon {weapon}')
                continue

        print('Kick Player ' + player + ' using weapon ' + weapon)
        text_widget.configure(state=tk.NORMAL)
        text_widget.insert(tk.END, "Kick Player ")
        text_widget.insert(tk.END, player, 'bold')
        text_widget.insert(tk.END, " using weapon ")
        text_widget.insert(tk.END, f"{weapon}\n", 'bold')

    with globals.kick_list_lock:
        globals.kick_list.update(kick_players.keys())

    print('Done')
    text_widget.insert(tk.END, "Done\n")
    set_widget_readonly(text_widget)

def on_close():
    print('Waiting for threads to end')
    text_widget.configure(state=tk.NORMAL)
    write_to_widget("Waiting for threads to end", text_widget)
    globals.threads_stop.set()
    teams_thread.join()
    print('Threads joined, exiting')
    exit()
    
if __name__ == '__main__':

    read_config()

    root = tk.Tk()
    root.title('Killfeed Kicker')
    root.geometry('400x300')
    root.attributes('-alpha', 1)

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12))
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget.configure(yscrollcommand=scrollbar.set)
    text_widget.tag_configure("bold", font=("Arial", 12, "bold"))

    text_widget.configure(state=tk.DISABLED)

    model = Model()

    print('Fetching API details...', end = ' ')

    success, persona_name = api.init()
    if not success:
        raise Exception('Failed to init api')
    
    print('Success')

    print_and_write(f'Connected to API with {persona_name}\n', text_widget)

    print('Fetching server information...', end = ' ')

    success, globals.game_id, full_server_name = api.get_server_id_and_fullname(data.server_name)

    if not success:
        raise Exception('Failed to get server')

    success, globals.teams = api.get_players_by_game_id(globals.game_id)

    if not success:
        raise Exception('Failed to get server teams')

    print('Success')

    print_and_write(f'Found server {full_server_name}\n', text_widget)

    keyboard.add_hotkey(data.pause_hotkey, check_killfeed)

    teams_thread = threading.Thread(target = api.get_players_thread, daemon = True)
    teams_thread.start()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
