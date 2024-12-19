import api
import globals
import time

def get_players_thread() -> None:
    elapsed_time = 0
    while not globals.threads_stop.is_set():
        time.sleep(1)
        elapsed_time += 1

        if elapsed_time >= 15:
            success, teams = api.get_players_by_game_id(globals.game_id)
            if success:
                with globals.teams_lock:
                    globals.teams = teams
                print('Updated teams')
            elapsed_time = 0
