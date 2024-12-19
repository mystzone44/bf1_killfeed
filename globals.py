import threading

game_id = None

threads_stop = threading.Event()

teams_lock = threading.Lock()
teams = None
kick_list_lock = threading.Lock()
kick_list = set()