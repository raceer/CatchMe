# TEE PELI TÄHÄN
import pygame, random, math

class CatchMe:
    def __init__(self, scr_w: int, scr_h: int):
        pygame.init()
        pygame.display.set_caption("CatchMe")

        self.scr_rez = (scr_w, scr_h)
        self.display_init()
        self.record = 0
        self.game_init()
        
    def game_init(self):         
        self.difficulty = 0.1
        self.difficulty_step = 0.01
        self.play = True
        self.start = True
        self.bg_color = 100

        self.assets_init()
        
        self.player_init()
        self.coin_init()
        self.monster_init()
        self.portal_init()

        self.clock = pygame.time.Clock()
        self.game_loop()

    def assets_init(self):
        assets = {}
        for img in ["hirvio", "kolikko", "ovi", "robo"]:
            assets[img] = pygame.image.load(img + ".png")
        self.assets = assets

    # Display

    def display_init(self):
        self.scr_mid = (self.scr_rez[0] // 2, self.scr_rez[1] // 2)
        self.display = pygame.display.set_mode(self.scr_rez)
        self.bg_color = 100
        self.main_bg_color = [255, 255, 0]

    def background(self):
        value = 100
        self.display.fill([self.bg_color, self.bg_color, self.bg_color])

    def background_ghost(self):        
        black = (0,0,0)
        white = [channel + 255 for channel in black]
        white = (255,255,255)

        self.display.fill(white)
        # Head

        circle_radius = sum(self.scr_mid)/2 / 4

        pygame.draw.circle(self.display, black, (self.scr_mid[0], self.scr_mid[1]*1.1), circle_radius * 5)
        pygame.draw.circle(self.display, black, (self.scr_mid[0], self.scr_mid[1]*1.5), circle_radius * 5)

        # Eyes
        
        pygame.draw.circle(self.display, white, (self.scr_mid[0] * 1.4, self.scr_mid[1]*0.8), circle_radius)
        pygame.draw.circle(self.display, white, (self.scr_mid[0] * 0.6, self.scr_mid[1]*0.8), circle_radius)
    
    def background_change(self):
        distance = self.assets["robo"].get_width() * 5
        
        if abs(self.player_x + self.assets["robo"].get_width() / 2 - self.monster_x + self.assets["hirvio"].get_width() / 2) < distance and abs(self.player_y + self.assets["robo"].get_height() / 2 - self.monster_y + self.assets["hirvio"].get_height() / 2) < distance:
            if self.bg_color > 0:
                if self.bg_color < 3:
                    self.bg_color -= 1
                else:
                    self.bg_color -= 3
        else:
            if self.bg_color < 100:
                self.bg_color += 1

    # Player

    def player_init(self):
        self.controls = {"up": False, "down": False, "left": False, "right": False}
        self.player_x = self.scr_mid[0]
        self.player_y = self.scr_mid[1]
        self.player_speed = 10
        self.point_counter = 0

    def player_move(self):
        if self.controls["up"] and self.player_y > 0:
            self.player_y -= self.player_speed
        if self.controls["down"] and self.player_y < (self.scr_rez[1] - self.assets["robo"].get_height()) * 0.99:
            self.player_y += self.player_speed
        if self.controls["left"] and self.player_x > 0:
            self.player_x -= self.player_speed
        if self.controls["right"] and self.player_x < self.scr_rez[0] - self.assets["robo"].get_width():
            self.player_x += self.player_speed

        self.display.blit(self.assets["robo"], (self.player_x, self.player_y))

    # Coin

    def coin_init(self):
        self.coin_x, self.coin_y = self.random_coordinates(self.assets["kolikko"])
        self.coin_exists = False
    
    def spawn_coin(self):
        self.coin_exists = True
        self.coin_x, self.coin_y = self.random_coordinates(self.assets["kolikko"])

    def display_coin(self):
        self.display.blit(self.assets["kolikko"], (self.coin_x, self.coin_y))

    def display_points(self):
        font = pygame.font.SysFont("Trebuchet", round(sum(self.scr_mid)/2/10))
        text2 = font.render(f"{self.point_counter}", True, (0,0,0))
        text1 = font.render(f"{self.point_counter}", True, (255,255,0))
        self.display.blit(text2, (0,0))
        self.display.blit(text1, (4,0))

    def coin_picked(self):
        if - self.assets["kolikko"].get_width() < self.coin_x - self.player_x < self.assets["robo"].get_width():
            if - self.assets["kolikko"].get_height() < self.coin_y - self.player_y < self.assets["robo"].get_height():
                self.coin_exists = False
                self.point_counter += 1
                self.difficulty += self.difficulty_step

    # Monster

    def monster_init(self):
        def outside_field():
            distance = 100 # how far from the borders
            x = random.randint(- self.assets['hirvio'].get_width() - distance, self.scr_rez[0] + 1 + distance)
            y = random.randint(- self.assets['hirvio'].get_height() - distance, self.scr_rez[1] + 1 + distance)
            if - distance < x < self.scr_rez[0] + distance and -distance < y < self.scr_rez[1] + distance:
                return outside_field()
            return x, y
        self.monster_x, self.monster_y = outside_field()
           
    def monster_move(self):
        self.monster_speed = self.player_speed * self.difficulty
        if self.monster_x < self.player_x:
            self.monster_x += self.monster_speed
        if self.monster_x > self.player_x:
            self.monster_x -= self.monster_speed
        if self.monster_y < self.player_y:
            self.monster_y += self.monster_speed
        if self.monster_y > self.player_y:
            self.monster_y -= self.monster_speed
        self.display.blit(self.assets["hirvio"], (self.monster_x, self.monster_y))

    def monster_touch(self):
        smaller_mult = 0.5
        if - self.assets["hirvio"].get_width() * smaller_mult < self.monster_x - self.player_x < self.assets["robo"].get_width() * smaller_mult:
            if - self.assets["hirvio"].get_height() * smaller_mult < self.monster_y - self.player_y < self.assets["robo"].get_height() * smaller_mult:
                self.play = False 

    # Portal

    def portal_init(self):
        self.portal_exists = False
        self.portals_added = [0]

    def spawn_portal(self):
        self.portal_x, self.portal_y = self.random_coordinates(self.assets["ovi"])
        self.portal_exists = True
        self.portals_added.append(self.point_counter)

    def display_portal(self):
        self.display.blit(self.assets["ovi"], (self.portal_x, self.portal_y))

    def portal_entered(self):
        """Entering portal slows down the monster"""
        if - self.assets["ovi"].get_width() < self.portal_x - self.player_x < self.assets["robo"].get_width():
            if - self.assets["ovi"].get_height() < self.portal_y - self.player_y < self.assets["robo"].get_height():
                self.portal_exists = False
                self.difficulty *= 0.4
                self.difficulty_step *= 1.1
                self.portals_added.append(self.point_counter)
                
    # Game

    def game_loop(self):
        while True: 
            self.check_events()
            if self.start:
                self.render_start()
            elif self.play:
                self.render_game()
            else:
                self.render_end()  

    def render_start(self):
        # Fade out
        self.bg_color = 0
        # Ghost
        self.background_ghost()

        # fonts
        font2 = pygame.font.SysFont("Trebuchet", round(sum(self.scr_mid) / 2 / 3))
        # Key Info Text
        key_color = (255,255,255)
        key_text = font2.render("HIT SPACE!", True, key_color)
        ## Key Info Display
        self.display.blit(key_text, ((self.scr_rez[0] - key_text.get_width()) / 2, (self.scr_rez[1] - key_text.get_height()) / 1.2))

        pygame.display.flip()
        self.clock.tick(60)


    def render_game(self):
        self.background()
        self.display_points()
        
        if not self.coin_exists:
            self.spawn_coin()
        else:
            self.display_coin()
        self.player_move()
        self.monster_move()
        self.monster_touch()
        self.coin_picked()
        self.background_change()

        if not self.portal_exists and self.point_counter != 0 and self.point_counter >= 25 + self.portals_added[-1]:
            self.spawn_portal()
        elif self.portal_exists:
            self.display_portal()
            self.portal_entered()

        pygame.display.flip()
        self.clock.tick(60)

    def render_end(self):
        white = (255, 255, 255)
        black = (0, 0, 0)
        self.display.fill(white)

        if self.record < self.point_counter:
            self.record = self.point_counter

        self.background_ghost()

        # fonts
        font = pygame.font.SysFont("Trebuchet", round(sum(self.scr_mid) / 2 / 5))
        font2 = pygame.font.SysFont("Trebuchet", round(sum(self.scr_mid) / 2 / 7))
        # Key Info Text
        key_color = (255,255,255)
        key_text = font2.render("PRESS R to restart, ESC to exit", True, key_color)
        ## Key Info Display
        self.display.blit(key_text, ((self.scr_rez[0] - key_text.get_width()) / 2, (self.scr_rez[1] - key_text.get_height()) / 1.1))
        # Score Text
        move_score_text = self.scr_rez[1] * 0.18
        text_color = (255, 0, 0)
        text_up = font.render("Catched!", True, text_color)
        text_down = font.render(f"SCORE: {self.point_counter} RECORD: {self.record}", True, text_color)
        ## Score Display
        self.display.blit(text_up, (self.scr_mid[0] - text_up.get_width() / 2, self.scr_mid[1] - text_up.get_height() + move_score_text))
        self.display.blit(text_down, (self.scr_mid[0] - text_down.get_width() / 2, self.scr_mid[1] + move_score_text))

        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_r:
                    self.game_init()
                if event.key == pygame.K_SPACE:
                    self.start = False
                if event.key == pygame.K_UP:
                    self.controls["up"] = True
                if event.key == pygame.K_DOWN:
                    self.controls["down"] = True
                if event.key == pygame.K_LEFT:
                    self.controls["left"] = True
                if event.key == pygame.K_RIGHT:
                    self.controls["right"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.controls["up"] = False
                if event.key == pygame.K_DOWN:
                    self.controls["down"] = False
                if event.key == pygame.K_LEFT:
                    self.controls["left"] = False
                if event.key == pygame.K_RIGHT:
                    self.controls["right"] = False

    # Funcitons

    def random_coordinates(self, item: pygame.image):
        """Returns random x,y coordinates"""
        return random.randint(0, self.scr_rez[0] - item.get_width()), random.randint(0, self.scr_rez[1] - item.get_height())

def main_01():
    mult = 0.5
    game = CatchMe(1920 * mult, 1920 * mult)

if __name__ == "__main__":
    main_01()