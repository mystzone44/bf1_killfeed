schema = { 
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'window_title': {
            'type': 'string'
        },
        'server_name': {
            'type': 'string'
        },
        'discord_log_name': {
            'type': 'string'
        },
        'kick_hotkey': {
            'type': 'string'
        },
        'player_name_similarity_probability': {
            'type': 'number',
            'minimum': 0,
            'maximum': 1
        },
        'minimum_player_count': {
            'type': 'number',
            'minimum': 0,
            'maximum': 64
        },
        'colors': {
            'type': 'object',
            'properties': {
                'ally_color': {
                    'type': 'string',
                    "pattern": r"^(\d+),(\d+),(\d+)$"
                },
                'enemy_color': {
                    'type': 'string',
                    "pattern": r"^(\d+),(\d+),(\d+)$"
                },
                'squad_color': {
                    'type': 'string',
                    "pattern": r"^(\d+),(\d+),(\d+)$"
                }
            },
            'additionalProperties': False
        },
        'discord_monitoring_webhook_url': {
            'type': 'string',
            'format': 'uri'
        },
        'killfeed_area': {
            'type': ['object', 'null'],
            'properties': {
                'x': {
                    'type': 'number',
                    'minimum': 0
                },
                'y': {
                    'type': 'number',
                    'minimum': 0
                },
                'width': {
                    'type': 'number',
                    'minimum': 0
                },
                'height': {
                    'type': 'number',
                    'minimum': 0
                }
            },
            'required': ['x', 'y', 'width', 'height'],
            'additionalProperties': False
        }
    }
}