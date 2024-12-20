import api

weapon_classes = {
    0: 'heavy bomber',
    1: 'smg08',
    2: 'artillery truck',
    3: 'rifle grenade',
    4: 'mortar'
}

def kick_player(game_id, persona_id, weapon_class_id):
    if weapon_class_id != 4:
        weapon = weapon_classes[weapon_class_id]
        reason = f"No {weapon}, Read Rules!"
        success, _ = api.kick_player(game_id, persona_id, reason)
        return success, weapon

    return False, ""
    