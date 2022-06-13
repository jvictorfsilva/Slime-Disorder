import pygame
from entity import Entity
from settings import *
from support import import_folder


class Player(Entity):
    def __init__(
        self,
        pos,
        groups,
        obstacle_sprites,
        create_attack,
        destroy_weapon,
        create_magic,
        create_spattack,
    ):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(
            HITBOX_OFFSET["player"]
        )  # editar conforme a hitbox do personagem

        # graphics setup
        self.import_player_assets()
        self.status = "down"

        # movimento
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # Weapon
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # status
        self.stats = {
            "health": 100,
            "energy": 60,
            "attack": 10,
            "magic": 4,
            "speed": 4,
        }
        self.max_stats = {
            "health": 300,
            "energy": 140,
            "attack": 20,
            "magic": 10,
            "speed": 7,
        }
        self.upgrade_cost = {
            "health": 100,
            "energy": 100,
            "attack": 100,
            "magic": 100,
            "speed": 300,
        }

        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        self.exp = 500

        # magica
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Special Attack
        self.create_spattack = create_spattack
        self.spattack_index = 0
        self.spattack = list(spattack_data.keys())[self.spattack_index]

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # import sound
        # self.weapon_attack_sound = pygame.mixer.Sound("../audio/sword_sound.wav")
        # self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        character_path = "../graphics/player/"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
            "right_attack": [],
            "left_attack": [],
            "up_attack": [],
            "down_attack": [],
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
        if not self.attacking:
            keys = pygame.key.get_pressed()
            mbutton = pygame.mouse.get_pressed()

            # Input movimentação player
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            # input ataque player
            if mbutton == (1, 0, 0):
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                # self.weapon_attack_sound.play()

            # Troca das weapons

            if keys[pygame.K_q] and self.can_switch_weapon:

                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # input poder/magica
            if keys[pygame.K_f]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = (
                    list(magic_data.values())[self.magic_index]["strength"]
                    + self.stats["magic"]
                )
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)

            # troca poder/magica

            if keys[pygame.K_e] and self.can_switch_magic:

                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

            # special attack
            if self.weapon_index == 3 and self.magic_index == 0:
                if keys[pygame.K_x]:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = list(spattack_data.keys())[self.spattack_index]
                    cost = list(spattack_data.values())[self.spattack_index]["cost"]
                    self.create_spattack(style, cost)

    def get_status(self):

        # Parado
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

            if self.attacking:
                self.direction.x = 0
                self.direction.y = 0
                if not "attack" in self.status:
                    if "idle" in self.status:
                        self.status = self.status.replace("_idle", "_attack")
                    else:
                        self.status = self.status + "_attack"
            else:
                if "attack" in self.status:
                    self.status = self.status.replace("_attack", "")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if (
                current_time - self.attack_time
                >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]
            ):
                self.attacking = False
                self.destroy_weapon()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats["magic"]
        spell_damage = magic_data[self.magic]["strength"]
        return base_damage + spell_damage

    def get_full_spattack_damage(self):
        base_damage = (self.stats["attack"] * 0.20) + (self.stats["magic"] * 0.20)
        spattack_damage = spattack_data[self.spattack]["damage"]
        return base_damage + spattack_damage

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:

            # Calculo regeneração de mana
            self.energy += 0.01 * (self.stats["magic"] * 0.25)
        else:
            self.energy = self.stats["energy"]

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def death(self):
        if self.health <= 0:
            pygame.quit()

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"])
        self.energy_recovery()
        self.death()
