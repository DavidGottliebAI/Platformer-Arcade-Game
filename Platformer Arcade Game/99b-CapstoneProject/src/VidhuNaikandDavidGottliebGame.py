# import libraries and API
import pygame
import sys
import random


# create classes

class Character:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.deltay = 0
        self.screen = screen
        self.image = pygame.image.load("Idle (1).png")
        self.is_jump = False

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def gravity(self):
        self.deltay += 1.5
        self.y += self.deltay
        if self.y + self.image.get_height() > self.screen.get_height() and self.deltay >= 0:
            self.deltay = 0
            self.y = self.screen.get_height() - self.image.get_height()

    def is_hit(self, enemy):
        hitbox = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        if hitbox.collidepoint(enemy.x, enemy.y):
            return hitbox.collidepoint(enemy.x, enemy.y)
        if hitbox.collidepoint(enemy.x + enemy.image.get_width(), enemy.y):
            return hitbox.collidepoint(enemy.x + enemy.image.get_width(), enemy.y)
        if hitbox.collidepoint(enemy.x + enemy.image.get_width()//2, enemy.y + enemy.image.get_height()):
            return hitbox.collidepoint(enemy.x + enemy.image.get_width()//2, enemy.y + enemy.image.get_height())


class Health_bar:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.image = pygame.image.load("Health.jpg")
        self.image.set_colorkey((255, 255, 255))

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class Platform:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.speed = 1
        self.screen = screen
        self.image = pygame.image.load("14.png")

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.speed = random.randint(1, 5)
        self.image = pygame.image.load("ZWalk (1).png")

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speed


class Enemies:
    def __init__(self, zombies, character):
        self.zombies = zombies
        self.character = character

    def is_hit(self, platforms):
        for k in range(len(self.zombies) - 1, -1, -1):
            hit_box = pygame.Rect(self.zombies[k].x, self.zombies[k].y, self.zombies[k].image.get_width(), self.zombies[k].image.get_height())
            if hit_box.collidepoint(self.character.x, self.character.y + self.character.image.get_height()//2) or hit_box.collidepoint(self.character.x + self.character.image.get_width(), self.character.y + self.character.image.get_height()//2):
                self.zombies.remove(self.zombies[k])
                platforms.remove(platforms[k])


def generate_level(n, screen):
    if n == 1:
        platform1 = Platform(screen.get_width() // 2 - 500 // 2, screen.get_height() - 150, screen)
        platform2 = Platform(screen.get_width() // 2 + 128, screen.get_height() - 150, screen)
        return [platform1, platform2]
    elif n == 2:
        platform1 = Platform(screen.get_width() // 2 - 700 // 2, screen.get_height() -100, screen)
        platform2 = Platform(screen.get_width() // 2 - 700 // 2, screen.get_height() -300, screen)
        platform3 = Platform(screen.get_width() // 2 - 700 // 2, screen.get_height() -500, screen)
        platform4 = Platform(screen.get_width() // 2 - 700 // 2, screen.get_height() -700, screen)
        platform5 = Platform(screen.get_width() // 2 + 700 // 2, screen.get_height() - 100, screen)
        platform6 = Platform(screen.get_width() // 2 + 700 // 2, screen.get_height() - 300, screen)
        platform7 = Platform(screen.get_width() // 2 + 700 // 2, screen.get_height() - 500, screen)
        platform8 = Platform(screen.get_width() // 2 + 700 // 2, screen.get_height() - 700, screen)
        return [platform1, platform2, platform3, platform4, platform5, platform6, platform7, platform8]
    elif n == 3:
        platform1 = Platform(screen.get_width() // 2 - 500 // 2, screen.get_height() - 100, screen)
        platform2 = Platform(screen.get_width() // 2 + 500 // 2, screen.get_height() - 100, screen)
        platform3 = Platform(screen.get_width() // 2 - 750 // 2, screen.get_height() - 300, screen)
        platform4 = Platform(screen.get_width() // 2 + 750 // 2, screen.get_height() - 300, screen)
        platform5 = Platform(screen.get_width() // 2 - 1000 // 2, screen.get_height() - 500, screen)
        platform6 = Platform(screen.get_width() // 2 + 1000 // 2, screen.get_height() - 500, screen)
        platform7 = Platform(screen.get_width() // 2 - 700 // 2, screen.get_height() - 650, screen)
        platform8 = Platform(screen.get_width() // 2 + 700 // 2, screen.get_height() - 650, screen)
        return [platform1, platform2, platform3, platform4, platform5, platform6, platform7, platform8]



# This is the main game loop

def main():
    pygame.init()
    pygame.display.set_caption("A Knight in the Apocalypse")
    screen = pygame.display.set_mode((1536, 865))
    clock = pygame.time.Clock()
    is_game_over = False
    is_game_win = False
    game_over_image = pygame.image.load("You Died.jpg")
    game_win_image = pygame.image.load("Poggers.jpg")
    paused_image = pygame.image.load("Pause.jpg")
    next_level_image = pygame.image.load("Next_Level.jpg")
    pygame.mixer.music.load("270366_foolboymedia_dramatic-scroller (online-audio-converter.com).mp3")
    jump_sound = pygame.mixer.Sound("270323__littlerobotsoundfactory__jump-03.wav")
    win_sound = pygame.mixer.Sound("495005__evretro__win-video-game-sound.wav")
    win = 0
    lose_sound = pygame.mixer.Sound("538151__fupicat__8bit-fall.wav")
    lose = 0
    ON_TITLE = True
    PAUSED = False
    NEXT_LEVEL = False
    level_num = 1

    buffer_time = 0
    BUFFER_TIME = 40
    took_damage = False
    total_health = []

    right_knight = 0
    right_walk_knight = []
    for x in range(10):
        right_walk_knight.append("Walk ({}).png".format(x + 1))
    left_knight = 0
    left_walk_knight = []
    for x in range(10):
        left_walk_knight.append("Walk Left({}).png".format(x + 1))
    attack_knight = 0
    attack_knight_animation = []
    for x in range(10):
        attack_knight_animation.append("Attack ({}).png".format(x + 1))
    right_enemy = 0
    right_walk_enemy = []
    for x in range(10):
        right_walk_enemy.append("ZWalk ({}).png".format(x + 1))
    left_enemy = 0
    left_walk_enemy = []
    for x in range(10):
        left_walk_enemy.append("ZWalk Left({}).png".format(x + 1))

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if ON_TITLE == True:
            screen.blit(pygame.image.load("Title_Screen.jpg"), (0, 0))
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ON_TITLE = False
                if is_game_over == False:
                    pygame.mixer.music.play()
                    x = 0
                    for k in range(5):
                        health = Health_bar(10 + x, 10, screen)
                        x += health.image.get_width() + 10
                        total_health.append(health)

                    knight = Character(screen.get_width() // 2 - 43 // 2, 0, screen)
                    platforms = []
                    allplatforms = []
                    layout = generate_level(level_num, screen)
                    platforms.extend(layout)

                    for platform in platforms:
                        allplatforms.append(platform)
                    zombies = []
                    for platform in platforms:
                        zombies.append(Enemy(platform.x, platform.y - 61, screen))
                    allzombies = Enemies(zombies, knight)
            else:
                continue

        if NEXT_LEVEL == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                NEXT_LEVEL = False
                total_health.clear()
                if is_game_win == False:
                    x = 0
                    for k in range(5):
                        health = Health_bar(10 + x, 10, screen)
                        x += health.image.get_width() + 10
                        total_health.append(health)

                    knight = Character(screen.get_width() // 2 - 43 // 2, 0, screen)
                    platforms = []
                    allplatforms = []
                    layout = generate_level(level_num, screen)
                    platforms.extend(layout)

                    for platform in platforms:
                        allplatforms.append(platform)
                    zombies = []
                    for platform in platforms:
                        zombies.append(Enemy(platform.x, platform.y - 61, screen))
                    allzombies = Enemies(zombies, knight)
            else:
                continue


        knight.image = pygame.image.load("Idle (1).png")
        pressed_keys = pygame.key.get_pressed()

        if not PAUSED:
            if pressed_keys[pygame.K_p]:
                pygame.mixer.music.stop()
                PAUSED = True
        if PAUSED:
            if pressed_keys[pygame.K_o]:
                pygame.mixer.music.play()
                PAUSED = False
            screen.blit(paused_image,(screen.get_width() // 2 - paused_image.get_width() // 2, screen.get_height() // 2 - 100))
            pygame.display.update()
            continue

        if pressed_keys[pygame.K_RIGHT]:
            knight.x += 5
            knight.image = pygame.image.load(right_walk_knight[right_knight % 10])
            right_knight += 1
            if knight.x > screen.get_width():
                knight.x = 0
        if pressed_keys[pygame.K_LEFT]:
            knight.x -= 5
            knight.image = pygame.image.load(left_walk_knight[left_knight % 10])
            left_knight += 1
            if knight.x + knight.image.get_width() < 0:
                knight.x = screen.get_width() - knight.image.get_width()
        if not knight.is_jump:
            if pressed_keys[pygame.K_UP] and knight.deltay == 0:
                jump_sound.play()
                knight.is_jump = True
        if knight.is_jump:
            knight.deltay = -25
            knight.is_jump = False
        if pressed_keys[pygame.K_SPACE]:
            knight.image = pygame.image.load(attack_knight_animation[attack_knight % 10])
            attack_knight += 1
            allzombies.is_hit(platforms)

        for k in range(len(zombies)):
            if knight.is_hit(zombies[k]) and buffer_time % BUFFER_TIME == 0:
                if len(total_health) >= 1:
                    total_health.remove(total_health[len(total_health) - 1])
                    took_damage = True
                else:
                    is_game_over = True

        if len(zombies) == 0:
            is_game_win = True

        if is_game_over:
            pygame.mixer.music.stop()
            if lose == 0:
                lose_sound.play()
            lose += 1
            screen.blit(game_over_image, (screen.get_width() // 2 - game_over_image.get_width() // 2, screen.get_height() // 2 - 100))
            if pressed_keys[pygame.K_r]:
                level_num = 1
                ON_TITLE = True
                is_game_over = False
                lose = 0
            else:
                pygame.display.update()
                continue


        if took_damage:
            buffer_time += 1
            if buffer_time % 5:
                knight.image = pygame.image.load("Empty.png")
            if buffer_time % BUFFER_TIME == 0:
                took_damage = False

        screen.fill((0, 0, 0))
        knight.gravity()

        for k in range(len(platforms)):
            if allzombies.zombies[k].x + allzombies.zombies[k].image.get_width()//2 > platforms[k].x + platforms[k].image.get_width():
                allzombies.zombies[k].speed = -random.randint(1, 5)
            if allzombies.zombies[k].x + allzombies.zombies[k].image.get_width()//2 < platforms[k].x:
                allzombies.zombies[k].speed = random.randint(1, 5)
            allzombies.zombies[k].move()
            if allzombies.zombies[k].speed > 0:
                allzombies.zombies[k].image = pygame.image.load(right_walk_enemy[right_enemy % 10])
                right_enemy += 1
            else:
                allzombies.zombies[k].image = pygame.image.load(left_walk_enemy[left_enemy % 10])
                left_enemy += 1
            allzombies.zombies[k].draw()

        if is_game_win:
            if level_num == 3:
                pygame.mixer.music.stop()
                if win == 0:
                    win_sound.play()
                win += 1
                screen.blit(game_win_image, (screen.get_width() // 2 - game_win_image.get_width() // 2, screen.get_height() // 2 - 100))
            else:
                screen.blit(next_level_image, (screen.get_width() // 2 - next_level_image.get_width() // 2, screen.get_height() // 2 - 400))
            if pressed_keys[pygame.K_r]:
                level_num = 1
                ON_TITLE = True
                is_game_win = False
                win = 0
                total_health.clear()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and level_num < 3:
                level_num += 1
                NEXT_LEVEL = True
                is_game_win = False
                win = 0
            else:
                pygame.display.update()
                continue

        for k in range(len(allplatforms)):
            if knight.y + knight.image.get_height() > allplatforms[k].y > knight.y and knight.x < allplatforms[k].x + allplatforms[k].image.get_width() and knight.x + knight.image.get_width() > allplatforms[k].x and knight.deltay >=0:
                knight.deltay = 0
                knight.y = allplatforms[k].y - knight.image.get_height()
            allplatforms[k].draw()
        for k in range(len(total_health)):
            total_health[k].draw()

        screen.blit(pygame.image.load("lvl{}.jpg".format(level_num)), (screen.get_width() - 75, 0))


        knight.draw()
        pygame.display.update()


main()