from dialog import Dialog
import pygame
from entity import Entity
from settings import *
from support import import_folder
from debug import debug

# from menus import *


class Player(Entity):
    def __init__(
        self,
        pos,
        groups,
        obstacle_sprites,
        dialog_sprites,
        teleport_sprites,
        color_sprites,
        create_attack,
        destroy_weapon,
        create_magic,
        # create_spattack,
    ):
        super().__init__(groups)
        self.image = pygame.image.load(
            "../graphics/player/blue/down_idle/idle_down.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.color = 0
        self.color_sprites = color_sprites
        self.hitbox = self.rect.inflate(
            HITBOX_OFFSET["player"]
        )  # editar conforme a hitbox do personagem

        # graphics setup
        self.import_player_assets()
        self.status = "down"
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # movimento
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self.teleport_sprites = teleport_sprites
        self.dialog_sprites = dialog_sprites
        self.dialog = Dialog()

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
            "speed": 5,
        }
        self.max_stats = {
            "health": 300,
            "energy": 140,
            "attack": 20,
            "magic": 10,
            "speed": 8,
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
        self.exp = 100

        # magica
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Special Attack
        # self.create_spattack = create_spattack
        # self.spattack_index = 0
        # self.spattack = list(spattack_data.keys())[self.spattack_index]

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # import sound
        self.weapon_attack_sound = pygame.mixer.Sound("../audio/sword_sound.wav")
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        if self.color == 0:
            character_path = "../graphics/player/blue/"
        if self.color == 1:
            character_path = "../graphics/player/red/"
        if self.color == 2:
            character_path = "../graphics/player/yellow/"
        if self.color == 3:
            character_path = "../graphics/player/green/"
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

            self.debug_screen = False
            if keys[pygame.K_F3] and self.debug_screen == False:
                self.debug_screen = True
            if self.debug_screen == True:
                debug((self.rect[0], self.rect[1]))

            # input ataque player
            if mbutton == (1, 0, 0):
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

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
            # if self.weapon_index == 3 and self.magic_index == 0:
            #     if keys[pygame.K_x]:
            #         self.attacking = True
            #         self.attack_time = pygame.time.get_ticks()
            #         style = list(spattack_data.keys())[self.spattack_index]
            #         cost = list(spattack_data.values())[self.spattack_index]["cost"]
            #         self.create_spattack(style, cost)

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

    # def get_full_spattack_damage(self):
    #     base_damage = (self.stats["attack"] * 0.20) + (self.stats["magic"] * 0.20)
    #     spattack_damage = spattack_data[self.spattack]["damage"]
    #     return base_damage + spattack_damage

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
        pos = pygame.mouse.get_pos()
        botoes = []
        death_menu = False
        if self.health <= 0:
            death_menu = True
        # while death_menu == True:
        #     pygame.display.flip()

    def dialog_key_down(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.dialog.dialog()

    def logic(self):
        self.display_surface = pygame.display.get_surface()
        Text_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        for sprite in self.dialog_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                text_surf = pygame.font.Font.render(
                    (Text_font),
                    "Press SPACE to talk",
                    False,
                    "#000000",
                )
                x = 795
                y = 235
                text_rect = text_surf.get_rect(bottomright=(x, y))

                self.display_surface.blit(text_surf, text_rect)
                self.dialog_key_down()

        for sprite in self.teleport_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.count > 3:
                    self.hitbox.x = 1988
                    self.hitbox.y = 4558
                    self.count += 1

        if (
            self.rect[0] >= 3385
            and self.rect[0] <= 3655
            and self.rect[1] >= 2444
            and self.rect[1] <= 2619
        ):
            if self.color == 0:
                self.color = 1
        elif (
            self.rect[0] >= 2297
            and self.rect[0] <= 2503
            and self.rect[1] >= 4522
            and self.rect[1] <= 4537
        ):
            if self.color == 1:
                self.color = 2
        # elif (
        #     self.rect[0] >= 3385
        #     and self.rect[0] <= 3655
        #     and self.rect[1] >= 2444
        #     and self.rect[1] <= 2619
        # ):
        #     if self.color == 0:
        #         self.color = 1

        pygame.display.flip()

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"])
        self.energy_recovery()
        self.death()
        self.logic()
        self.import_player_assets()
