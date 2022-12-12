WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# Hitboxes
HITBOX_OFFSET = {"player": [-8, 0], "object": -40, "grass": -10, "invisible": 0}

# HUD
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "../graphics/font/joystix.ttf"
UI_FONT_SIZE = 18

# Cores Geral
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

# Cores HUD
HEALTH_COLOR = "#B20002"
ENERGY_COLOR = "gold"
UI_BORDER_COLOR_ACTIVE = "gold"

# Cores Menu Upgrade
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

# weapon

weapon_data = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "graphic": "../graphics/weapons/sword/full.png",
    },
    # "lance": {
    #     "cooldown": 400,
    #     "damage": 30,
    #     "graphic": "../graphics/weapons/lance/full.png",
    # },
    # "axe": {
    #     "cooldown": 300,
    #     "damage": 20,
    #     "graphic": "../graphics/weapons/axe/full.png",
    # },
    # "rapier": {
    #     "cooldown": 50,
    #     "damage": 8,
    #     "graphic": "../graphics/weapons/rapier/full.png",
    # },
    # "sai": {
    #     "cooldown": 80,
    #     "damage": 10,
    #     "graphic": "../graphics/weapons/sai/full.png",
    # },
    # "katana": {
    #     "cooldown": 250,
    #     "damage": 17,
    #     "graphic": "../graphics/weapons/katana/full.png",
    # },
    # "leaf_sword": {
    #     "cooldown": 250,
    #     "damage": 17,
    #     "graphic": "../graphics/weapons/leaf_sword/full.png",
    # },
}

# magic

magic_data = {
    # "flame": {
    #     "strength": 5,
    #     "cost": 20,
    #     "graphic": "../graphics/particles/flame/fire.png",
    # },
    "heal": {
        "strength": 20,
        "cost": 10,
        "graphic": "../graphics/particles/heal/heal.png",
    },
}

# special attack

spattack_data = {
    "operation_flame": {
        "damage": 53,
        "cost": 40,
    },
}


# enemy

monster_data = {
    "knight": {
        "health": 100,
        "exp": 110,
        "damage": 10,
        "attack_type": "slash",
        "attack_sound": "../audio/attack/slash.wav",
        "speed": 4,
        "resistance": 3,
        "attack_radius": 100,
        "notice_radius": 200,
    }
}
npc_data = {
    "fishman": {
        "health": 100,
        "exp": 110,
        "damage": 8,
        "attack_type": "thunder",
        "attack_sound": "../audio/attack/fireball.wav",
        "speed": 4,
        "resistance": 3,
        "attack_radius": 1,
        "notice_radius": 1,
    }
}
