import pygame
from spattack import Spattack
from magic import MagicPlayer
from particles import AnimationPlayer
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from support import *
from random import choice, randint
from weapon import Weapon
from upgrade import Upgrade
from npc import Npc

# from debug import debug
from ui import UI


class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.game_paused_upgrade = False
        self.game_paused_menu = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.teleport_sprites = pygame.sprite.Group()
        self.color_sprites = pygame.sprite.Group()
        self.dialog_sprites = pygame.sprite.Group()
        self.constructions_sprites = pygame.sprite.Group()
        self.constructions_details_sprites = pygame.sprite.Group()

        self.create_map()

        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        self.current_spattack = None

    def create_map(self):
        layout = {
            "boundary": import_csv_layout("../map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("../map/map_Grass.csv"),
            "object": import_csv_layout("../map/map_Objects.csv"),
            "entities": import_csv_layout("../map/map_Entities.csv"),
            "teleport": import_csv_layout("../map/map_Teleport.csv"),
            "dialog": import_csv_layout("../map/map_Dialog.csv"),
            "constructions": import_csv_layout("../map/map_Constructions.csv"),
            "constructionDetails": import_csv_layout(
                "../map/map_ConstructionsDetails.csv"
            ),
            "color": import_csv_layout("../map/map_Color.csv"),
        }
        graphics = {
            "grass": import_folder("../graphics/Grass"),
            "object": import_folder("../graphics/objects"),
            "constructions": import_folder("../graphics/constructions"),
            "constructionsDetails": import_folder("../graphics/constructions_details"),
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile(
                                (x, y),
                                [
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites,
                                ],
                                "grass",
                                random_grass_image,
                            )
                        if style == "object":
                            idx = int(col) - 1
                            surf = graphics["object"][idx]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                surf,
                            )
                        if style == "constructions":
                            idx = int(col) - 1
                            surf = graphics["constructions"][idx]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                surf,
                            )
                        if style == "constructionDetails":
                            idx = int(col) - 1
                            surf = graphics["constructionsDetails"][idx]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                surf,
                            )
                        if style == "entities":
                            if col == "394":
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.dialog_sprites,
                                    self.teleport_sprites,
                                    self.color_sprites,
                                    self.create_attack,
                                    self.destroy_weapon,
                                    self.create_magic,
                                    # self.create_spattack,
                                )

                            else:
                                if col == "300":
                                    npc_name = "fishman"
                                    Npc(
                                        npc_name,
                                        (x, y),
                                        [self.visible_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particle,
                                        self.add_exp,
                                    )
                                elif col == "234":
                                    monster_name = "knight"

                                    Enemy(
                                        monster_name,
                                        (x, y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particle,
                                        self.add_exp,
                                    )
                        if style == "colors":
                            if col == "1":
                                Tile((x, y), [self.color_sprites], "invisible")
                            if col == "2":
                                Tile((x, y), [self.color_sprites], "invisible")
                            if col == "3":
                                Tile((x, y), [self.color_sprites], "invisible")
                        if style == "teleport":
                            Tile((x, y), [self.teleport_sprites], "invisible")
                        if style == "dialog":
                            Tile((x, y), [self.dialog_sprites], "invisible")

    def create_attack(self):
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites]
        )

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        # if style == "flame":
        #     self.magic_player.flame(
        #         self.player, cost, [self.visible_sprites, self.attack_sprites]
        #     )

    # def create_spattack(self, style, cost):
    #     if style == "operation_flame":
    #         if self.player.energy >= cost:
    #             self.player.energy -= cost
    #             self.current_spattack = Spattack(
    #                 self.player, [self.visible_sprites, self.attack_sprites]
    #             )

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        if self.current_spattack:
            self.current_spattack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    pos - offset,
                                    [self.visible_sprites],
                                )
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type
                            )

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(
                attack_type, self.player.rect.center, [self.visible_sprites]
            )

    def trigger_death_particle(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):

        self.player.exp += amount

    def toggle_upgrade_menu(self):
        self.game_paused_upgrade = not self.game_paused_upgrade

    def toggle_pause_menu(self):
        self.game_paused_menu = not self.game_paused_menu

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused_upgrade:
            self.upgrade.display()
        elif self.game_paused_menu:
            self.pause_menu.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load("../graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
