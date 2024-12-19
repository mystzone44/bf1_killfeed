import os
import json
from jsonschema import validate
from .schema import schema

def str_to_rgb(str: str) -> tuple[int, int, int]:
    if not str:
        return None
    RGB_CHANNEL_NUM = 3
    split = list(map(int, str.split(',')))
    return tuple(split) if len(split) == RGB_CHANNEL_NUM else None

config_path = 'config.json'

class ConfigData:
    window_title = 'Battlefield™ 1'
    server_name = '![VG]Vanguard'
    discord_log_name = 'mystzone44'
    pause_hotkey = 'p'
    minimum_player_count = 50
    player_name_similarity_probability = 0.8
    ally_colour = (64, 118, 199)
    enemy_colour = (189, 54, 49)
    squad_colour = (74, 155, 44)
    discord_kick_webhook_url = "https://discord.com/api/webhooks/1018551113257074709/VASl0wpyhk1fkfjJNizXTejNcI-95SZ-d3NCSF092eiYeqxcR98sOnG7FP_RT6UrI7wn"
    killfeed_area = (1354, 14, 1846 - 1330, 296 - 14)

data = ConfigData()

def read_config():
    global data
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config_json = json.load(config_file)
        validate(instance=config_json, schema=schema)
        
        if 'window_title' in config_json:
            data.window_title = config_json['window_title']
        if 'server_name' in config_json:
            data.server_name = config_json['server_name']
        if 'discord_log_name' in config_json:
            data.discord_log_name = config_json['discord_log_name']
        if 'pause_hotkey' in config_json:
            data.pause_hotkey = config_json['pause_hotkey']
        if 'minimum_player_count' in config_json:
            data.minimum_player_count = config_json['minimum_player_count']
        if 'discord_kick_webhook_url' in config_json:
            data.discord_kick_webhook_url = config_json['discord_kick_webhook_url']

        if 'colors' in config_json:
            ally_color = str_to_rgb(config_json['colors']['ally_color'])
            if ally_color:
                data.ally_color = ally_color
            enemy_color = str_to_rgb(config_json['colors']['enemy_color'])
            if enemy_color:
                data.enemy_color = enemy_color
            squad_color = str_to_rgb(config_json['colors']['squad_color'])
            if squad_color:
                data.squad_color = squad_color

        if 'killfeed_area' in config_json:
            killfeed_area = config_json['killfeed_area']
            data.killfeed_area = (killfeed_area['x'], killfeed_area['y'], killfeed_area['width'], killfeed_area['height'])