from random import randint, choice
from sys import exit

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_idle = pygame.image.load('graphics/Player/player_idle.png').convert_alpha()
        self.player_walk = [
            player_idle,
            pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha(),
            player_idle,
            pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        ]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 304))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 304:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 304:
            self.rect.bottom = 304

    def animation_stage(self):
        if self.rect.bottom < 304:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_stage()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.__annotations__ = type
        size = 1.0

        if type == 'fly':
            self.frames = [
                pygame.transform.rotozoom(pygame.image.load('graphics/Fly/Fly1.png').convert_alpha(), 0, size),
                pygame.transform.rotozoom(pygame.image.load('graphics/Fly/Fly2.png').convert_alpha(), 0, size)
            ]
            y_pos = 210
        else:
            self.frames = [
                pygame.transform.rotozoom(pygame.image.load('graphics/snail/snail1.png').convert_alpha(), 0, size),
                pygame.transform.rotozoom(pygame.image.load('graphics/snail/snail2.png').convert_alpha(), 0, size)
            ]
            y_pos = 305

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos)).inflate(-20, 0)

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 4 + (difficulty_modifier / 18)
        self.destroy()

    def destroy(self):
        if self.rect.x < -180:
            self.kill()


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = test_font.render(f'Score:  {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

    return current_time


def difficulty():
    return int((pygame.time.get_ticks() - start_time) / 1000)


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# start_screen | active | dying
game_stage = 'start_screen'

start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
# player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

player_dead = pygame.image.load('graphics/Player/player_dead.png').convert_alpha()
player_dead = pygame.transform.rotozoom(player_dead, 0, 2)
player_dead_rect = player_stand.get_rect(center=(400, 260))

game_name = test_font.render('Snail Jumper', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 70))

game_message = test_font.render('Press SPACE to START', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 340))

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Obstacles
# Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_fame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_fame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_fame_1, fly_fame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []
obstacle_collision = []

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomright=(100, 300))
player_gravity = 0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

snail_anim_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_anim_timer, 500)

fly_anim_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_anim_timer, 100)

counter = 0
difficulty_modifier = 0

death_frames_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_stage == 'active':
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20

            if difficulty_modifier != display_score():
                difficulty_modifier = difficulty()
                counter += 1

            if counter == 10 and difficulty_modifier < 100:
                pygame.time.set_timer(obstacle_timer, 1600 - (difficulty_modifier * 10))
                counter = 0

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

            if event.type == snail_anim_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_anim_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_stage = 'active'
                start_time = pygame.time.get_ticks()

    if game_stage == 'active':
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        # game_active = collision_sprite()
        obstacle_collision = pygame.sprite.spritecollide(player.sprite, obstacle_group, False,
                                                         collided=pygame.sprite.collide_rect_ratio(.54))

        if obstacle_collision:
            game_stage = 'dying'

    elif game_stage == 'dying':
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()
        obstacle_group.draw(screen)

        death_frames_counter += 1
        player.sprite.rect.y -= 8
        player.sprite.rect.x *= 1.08
        dying_player = pygame.transform.rotozoom(player.sprite.image, death_frames_counter * 2, 1.0 - (death_frames_counter / 60))
        screen.blit(dying_player, player.sprite.rect)

        if death_frames_counter > 50:
            death_frames_counter = 0
            obstacle_group.empty()
            player.sprite.rect.midbottom = (80, 300)
            player_gravity = 0
            game_stage = 'start_screen'

    else:
        screen.fill((94, 129, 162))

        if obstacle_collision:
            screen.blit(player_dead, player_dead_rect)

            if obstacle_collision[0].__annotations__ == 'fly':
                killer = Obstacle('fly').frames[0]
            else:
                killer = Obstacle('snail').frames[0]

            killer = pygame.transform.rotozoom(killer, 0, 1.4)
            killer_rect = killer.get_rect(center=(400, 150))
            screen.blit(killer, killer_rect)
        else:
            screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score:  {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 320))
        restart_message = test_font.render('Press SPACE to RESTART', False, (111, 196, 169))
        restart_message_rect = restart_message.get_rect(center=(400, 360))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(restart_message, restart_message_rect)

    # 60 fps
    pygame.display.update()
    clock.tick(60)

# Comments
# def obstacle_movement(obstacle_list):
#     if obstacle_list:  # Se lista vazia, avalia pra false
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5
#
#             if obstacle_rect.bottom == 300:
#                 screen.blit(snail_surf, obstacle_rect)
#             else:
#                 screen.blit(fly_surf, obstacle_rect)
#
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
#
#         return obstacle_list
#     else:
#         return []
#
#
# def collisions(player, obstacles):
#     if obstacles:
#         for obstacle_rect in obstacles:
#             if player.colliderect(obstacle_rect):
#                 return False
#     return True
#
# pygame.draw.rect(screen, '#C0E8EC', score_rect.inflate(20, 10).move(0, -4), 0, 10)
# screen.blit(score_surf, score_rect)
#
# snail_rect.x -= 4
# if snail_rect.right <= 0: snail_rect.left = 800
# screen.blit(snail_surf, snail_rect)
#
# Player
# player_gravity += 1
# player_rect.y += player_gravity
# if player_rect.bottom >= 300:
#     player_rect.bottom = 300
# player_animation()
# screen.blit(player_surf, player_rect)
#
# rectangu = player.sprite.rect
# pygame.draw.rect(screen, (111, 196, 169), rectangu)
#
# Obstacle movement
# obstacle_rect_list = obstacle_movement(obstacle_rect_list)
#
# game_active = collisions(player_rect, obstacle_rect_list)
#
# keys = pygame.key.get_pressed()
# if keys[pygame.K_SPACE]:
#     print('Jump!')
#
# if player_rect.colliderect(snail_rect):
#     print('ASD')
#
# mouse_pos = pygame.mouse.get_pos()
# if player_rect.collidepoint(mouse_pos):
#     pygame.mouse.get_pressed()
#
# score_surf = test_font.render('Snail  Jumper', False, (64, 64, 64))
# score_rect = score_surf.get_rect(center=(400, 40))
#
# if randint(0, 2):
#     obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
# else:
#     obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))
#
# def collision_sprite():
#     # return True
#     obstacle_collision = pygame.sprite.spritecollide(player.sprite, obstacle_group, False,
#                                                      collided=pygame.sprite.collide_rect_ratio(.54))
#     if pygame.sprite.spritecollide(player.sprite, obstacle_group, False,
#                                    collided=pygame.sprite.collide_rect_ratio(.54)):
#         obstacle_group.empty()
#         return False
#     else:
#         return True
#
# if difficulty_modifier < 10:
#     size = 0.3
# elif difficulty_modifier > 80:
#     size = 0.7
# else:
#     size = 0.3 + (difficulty_modifier / 200)