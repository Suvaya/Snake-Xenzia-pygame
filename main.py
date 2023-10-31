import pygame
import time
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

collision_sound = pygame.mixer.Sound('assets/eat.mp3')
bonus_sound = pygame.mixer.Sound('assets/Bwonus.mp3')
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Font
font = pygame.font.SysFont(None, 48)

# Food Class
class Dot:
    def __init__(self):
        self.size = 10  # Size of the dot
        self.respawn()  # Initialize and spawn the dot

    def respawn(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = random.randint(60, SCREEN_HEIGHT - self.size)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_img = font.render(self.text, True, BLACK)
        text_rect = text_img.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_img, text_rect)

# Snake class
class Snake:
    def __init__(self):
        self.size = 20  # Size of each snake segment
        self.base_speed = 10  # Initial speed: 10 pixels per second
        self.speed = self.base_speed  # Current speed
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # Initial snake position
        self.direction = (0, 0)  # Initial direction (not moving)
        self.last_update_time = time.time()
        self.score = 0
        self.dot = Dot()
        self.grow = False
        self.speed_increase_count = 0  # Keep track of speed increases

    def move(self, dx, dy):
        # Ensure the snake can't reverse its direction
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def update(self):
        current_time = time.time()
        if current_time - self.last_update_time >= 1 / self.speed:
            new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
            self.body.insert(0, new_head)

            if self.grow:
                self.grow = False
            else:
                self.body.pop()

            self.last_update_time = current_time
            self.check_collision()

            if self.score % 5 == 0 and self.score > 0 and self.speed_increase_count < self.score / 5:
                self.increase_speed(2)
                self.speed_increase_count += 1
                bonus_sound.play()
    def check_collision(self):
        # Check if the snake collides with the screen boundaries
        if (
                self.body[0][0] < 0
                or self.body[0][0] >= SCREEN_WIDTH
                or self.body[0][1] < 0
                or self.body[0][1] >= SCREEN_HEIGHT
        ):
            self.game_over()

        # Check if the snake's head collides with its body
        for segment in self.body[1:]:
            if self.body[0] == segment:
                self.game_over()

        # Check if the snake eats the dot
        if (
                self.body[0][0] < self.dot.x + self.dot.size
                and self.body[0][0] + self.size > self.dot.x
                and self.body[0][1] < self.dot.y + self.dot.size
                and self.body[0][1] + self.size > self.dot.y
        ):
            self.score += 1
            self.dot.respawn()
            self.grow = True
            collision_sound.play()

        if self.body[0][1] <= 55:
            self.game_over()

    def increase_speed(self, amount):
        self.speed += amount

    def game_over(self):
        menu.active_screen = GameEndScreen(self.score)

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, WHITE, (segment[0], segment[1], self.size, self.size))

#Game Screen
class GameScreen:
    def __init__(self):
        self.background_color = BLACK
        self.snake = Snake()

    def draw(self, screen):
        screen.fill(self.background_color)
        self.snake.draw(screen)
        pygame.draw.rect(screen, WHITE, (self.snake.dot.x, self.snake.dot.y, self.snake.dot.size, self.snake.dot.size))  # Draw the dot

        # Display the snake's speed at the top left corner
        speed_text = font.render("Speed: {}".format(self.snake.speed), True, WHITE)
        screen.blit(speed_text, (10, 10))

        # Display the score at the top right corner
        score_text = font.render("Score: {}".format(self.snake.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topright = (SCREEN_WIDTH - 10, 10)
        screen.blit(score_text, score_rect)

        # Draw a rectangular boundary
        boundary_rect = pygame.Rect(0, 60, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, WHITE, boundary_rect, 2)  # Draw a white rectangle with a thickness of 2 pixels


# Help screen
class HelpScreen:
    def __init__(self):
        self.text = ["Help Screen", "", "Use arrow keys to move", "Each score of 5 increase speed by 2"]
        self.restart_button = Button("Restart", SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2 + 120, 250, 100, WHITE)

    def draw(self, screen):
        screen.fill(BLACK)
        for i, line in enumerate(self.text):
            text_img = font.render(line, True, WHITE)
            text_rect = text_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * 50))
            screen.blit(text_img, text_rect)

# Game End screen
class GameEndScreen:
    def __init__(self, score):
        self.text = ["Game Over", "Score: " + str(score)]
        self.restart_button = Button("Restart", SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2 + 120, 250, 100, WHITE)

    def draw(self, screen):
        screen.fill(BLACK)
        for i, line in enumerate(self.text):
            text_img = font.render(line, True, WHITE)
            text_rect = text_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * 50))
            screen.blit(text_img, text_rect)

        self.restart_button.draw(screen)


# Menu class
class Menu:
    def __init__(self):
        self.screen = screen
        self.buttons = [
            Button("Start Game", SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2 - 50, 250, 100, WHITE),
            Button("Help", SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2 + 60, 250, 100, WHITE)
        ]
        self.active_screen = None
        self.snake = None

    def run(self):
        run = True
        while run:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.text == "Start Game":
                                self.active_screen = GameScreen()
                                self.snake = self.active_screen.snake
                                self.snake.score = 0
                            elif button.text == "Help":
                                self.active_screen = HelpScreen()

                            # Remove the button from the list
                            self.buttons.remove(button)

                    # Handle restart button from the GameEndScreen
                    if self.active_screen is not None and isinstance(self.active_screen, GameEndScreen):
                        if self.active_screen.restart_button.rect.collidepoint(event.pos):
                            self.active_screen = GameScreen()
                            self.snake = self.active_screen.snake
                            self.snake.score = 0

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.snake.move(0, -self.snake.size)
                if keys[pygame.K_DOWN]:
                    self.snake.move(0, self.snake.size)
                if keys[pygame.K_LEFT]:
                    self.snake.move(-self.snake.size, 0)
                if keys[pygame.K_RIGHT]:
                    self.snake.move(self.snake.size, 0)

            if self.snake:
                self.snake.update()

            for button in self.buttons:
                button.draw(self.screen)

            if self.active_screen:
                self.active_screen.draw(self.screen)

            pygame.display.update()

        pygame.quit()


# Game End class
class GameEnd:
    def __init__(self):
        self.screen = screen
        self.active_screen = GameEndScreen()

    def run(self):
        run = True
        while run:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.active_screen.draw(self.screen)

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    menu = Menu()
    menu.run()
