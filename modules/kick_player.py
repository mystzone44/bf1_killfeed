import api

weapon_classes = {
    0: 'heavy bomber',
    1: 'smg08',
    2: 'artillery truck',
    3: 'rifle grenade',
    4: 'mortar'
}


def kick_player(game_id, persona_id, weapon_class_id):
    weapon = weapon_classes[id]
    reason = f"No {weapon}, Read Rules!"
    #success, _ = api.kick_player(game_id, persona_id, reason)
    success = False

    return success, weapon
    