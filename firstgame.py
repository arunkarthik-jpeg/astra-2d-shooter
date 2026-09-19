import pygame
import random

pygame.init()

# ============================================
# SETTINGS
# ============================================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

clock = pygame.time.Clock()


# ============================================
# GAME STATES
# ============================================

MENU = 0
PLAYING = 1
GAME_OVER = 2

game_state = MENU


# ============================================
# LOAD IMAGES
# ============================================

player_images = [
    pygame.image.load(
        "assets/new_player1.png"
    ).convert_alpha(),

    pygame.image.load(
        "assets/new_player2.png"
    ).convert_alpha()
]

enemy_image = pygame.image.load(
    "assets/new_enemy.png"
).convert_alpha()


# ============================================
# PLAYER CLASS
# ============================================

class Player:

    def __init__(self):

        self.width = 50
        self.height = 50

        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 100

        # Pixels per second
        self.speed = 300

        # --------------------------------
        # Animation
        # --------------------------------

        self.images = []

        for image in player_images:

            image = pygame.transform.scale(
                image,
                (self.width, self.height)
            )

            self.images.append(image)

        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.image = self.images[0]

        # --------------------------------
        # Collision rectangle
        # --------------------------------

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self, dt):

        # =================================
        # MOVEMENT
        # =================================

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:

            self.x -= self.speed * dt

        if keys[pygame.K_RIGHT]:

            self.x += self.speed * dt


        # =================================
        # SCREEN BOUNDARIES
        # =================================

        if self.x < 0:

            self.x = 0

        if self.x > WIDTH - self.width:

            self.x = WIDTH - self.width


        # =================================
        # UPDATE RECTANGLE
        # =================================

        self.rect.x = self.x
        self.rect.y = self.y


        # =================================
        # ANIMATION
        # =================================

        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:

            self.animation_timer = 0

            self.animation_index += 1

            if self.animation_index >= len(self.images):

                self.animation_index = 0

            self.image = self.images[
                self.animation_index
            ]

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )


# ============================================
# ENEMY CLASS
# ============================================

class Enemy:

    def __init__(self):

        self.width = 50
        self.height = 50

        # Random horizontal position

        self.x = random.randint(
            0,
            WIDTH - self.width
        )

        # Start above screen

        self.y = random.randint(
            -600,
            -50
        )

        # Pixels per second

        self.speed = 300

        # Image

        self.image = pygame.transform.scale(
            enemy_image,
            (self.width, self.height)
        )

        # Collision rectangle

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self, dt):

        # Move downward

        self.y += self.speed * dt

        # Update rectangle

        self.rect.x = self.x
        self.rect.y = self.y

        # Check if enemy left screen

        if self.y > HEIGHT:

            return True

        return False

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )


# ============================================
# RESET GAME
# ============================================

def reset_game():

    global player
    global enemies
    global score
    global spawn_timer

    # Create player

    player = Player()

    # Create initial enemies

    enemies = []

    for i in range(3):

        enemies.append(
            Enemy()
        )

    # Reset score

    score = 0

    # Reset spawn timer

    spawn_timer = 0


# ============================================
# CREATE INITIAL OBJECTS
# ============================================

player = Player()

enemies = []

for i in range(3):

    enemies.append(
        Enemy()
    )


# ============================================
# GAME VARIABLES
# ============================================

running = True

score = 0

spawn_timer = 0

spawn_delay = 1.0

max_enemies = 5


# ============================================
# FONTS
# ============================================

title_font = pygame.font.Font(
    None,
    90
)

font = pygame.font.Font(
    None,
    40
)

game_over_font = pygame.font.Font(
    None,
    80
)


# ============================================
# MAIN GAME LOOP
# ============================================

while running:

    # ========================================
    # DELTA TIME
    # ========================================

    dt = clock.tick(60) / 1000


    # ========================================
    # EVENTS
    # ========================================

    for event in pygame.event.get():

        # ----------------------------
        # CLOSE WINDOW
        # ----------------------------

        if event.type == pygame.QUIT:

            running = False


        # ----------------------------
        # KEYBOARD
        # ----------------------------

        if event.type == pygame.KEYDOWN:


            # ============================
            # MENU
            # ============================

            if game_state == MENU:

                if event.key == pygame.K_SPACE:

                    reset_game()

                    game_state = PLAYING


            # ============================
            # GAME OVER
            # ============================

            elif game_state == GAME_OVER:

                if event.key == pygame.K_r:

                    reset_game()

                    game_state = PLAYING


    # ========================================
    # PLAYING STATE
    # ========================================

    if game_state == PLAYING:


        # ====================================
        # UPDATE PLAYER
        # ====================================

        player.update(dt)


        # ====================================
        # ENEMY SPAWNING
        # ====================================

        spawn_timer += dt

        if spawn_timer >= spawn_delay:

            if len(enemies) < max_enemies:

                enemies.append(
                    Enemy()
                )

            spawn_timer = 0


        # ====================================
        # UPDATE ENEMIES
        # ====================================

        for enemy in enemies[:]:

            passed = enemy.update(dt)

            # Enemy left screen

            if passed:

                score += 1

                enemies.remove(
                    enemy
                )


        # ====================================
        # DIFFICULTY
        # ====================================

        enemy_speed = (
            300 +
            (score // 5) * 60
        )

        for enemy in enemies:

            enemy.speed = enemy_speed


        # ====================================
        # COLLISION
        # ====================================

        for enemy in enemies:

            if player.rect.colliderect(
                enemy.rect
            ):

                game_state = GAME_OVER


    # ========================================
    # CLEAR SCREEN
    # ========================================

    screen.fill(
        (0, 0, 0)
    )


    # ========================================
    # MENU
    # ========================================

    if game_state == MENU:

        # Title

        title = title_font.render(
            "DODGE THE BLOCKS",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                WIDTH // 2,
                200
            )
        )

        screen.blit(
            title,
            title_rect
        )


        # Start instruction

        instruction = font.render(
            "Press SPACE to Start",
            True,
            (255, 255, 255)
        )

        instruction_rect = instruction.get_rect(
            center=(
                WIDTH // 2,
                350
            )
        )

        screen.blit(
            instruction,
            instruction_rect
        )


    # ========================================
    # PLAYING
    # ========================================

    elif game_state == PLAYING:

        # Player

        player.draw(
            screen
        )


        # Enemies

        for enemy in enemies:

            enemy.draw(
                screen
            )


        # Score

        score_text = font.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            score_text,
            (20, 20)
        )


    # ========================================
    # GAME OVER
    # ========================================

    elif game_state == GAME_OVER:

        # Player

        player.draw(
            screen
        )


        # Enemies

        for enemy in enemies:

            enemy.draw(
                screen
            )


        # Game Over text

        game_over_text = game_over_font.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        game_over_rect = game_over_text.get_rect(
            center=(
                WIDTH // 2,
                250
            )
        )

        screen.blit(
            game_over_text,
            game_over_rect
        )


        # Score

        score_text = font.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        score_rect = score_text.get_rect(
            center=(
                WIDTH // 2,
                330
            )
        )

        screen.blit(
            score_text,
            score_rect
        )


        # Restart instruction

        restart_text = font.render(
            "Press R to Restart",
            True,
            (255, 255, 255)
        )

        restart_rect = restart_text.get_rect(
            center=(
                WIDTH // 2,
                400
            )
        )

        screen.blit(
            restart_text,
            restart_rect
        )


    # ========================================
    # UPDATE SCREEN
    # ========================================

    pygame.display.update()


# ============================================
# QUIT
# ============================================

pygame.quit()