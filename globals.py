import threading

game_id = None

threads_stop = threading.Event()

teams = None
kick_list = set()