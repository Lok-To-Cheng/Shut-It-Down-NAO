SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 576   # screen dimensions
FPS = 60

# Colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Floor heights
FLOOR = [64, 128]

BG_LAYER = 1

# Player
PLAYER_WIDTH, PLAYER_HEIGHT = [128, 256], [128, 256]
PLAYER_X = [128, 128]
PLAYER_Y = [SCREEN_HEIGHT - FLOOR[0] - PLAYER_HEIGHT[0],
            SCREEN_HEIGHT - FLOOR[1] - PLAYER_HEIGHT[1]]
PLAYER_HITBOX = [(PLAYER_X[0] + 48, PLAYER_Y[0] + 16, 32, 112),
                 (PLAYER_X[1] + 96, PLAYER_Y[1] + 32, 64, 224)]
PLAYER_STEP_SIZE = [32, 64]
PLAYER_FRAMEPERSTEP = 3
PLAYER_LAYER = 3

# Enemy
NAO_WIDTH, NAO_HEIGHT = [64, 128], [64, 128]
NAO_Y = [SCREEN_HEIGHT - FLOOR[0] - NAO_HEIGHT[0],
         SCREEN_HEIGHT - FLOOR[1] - NAO_HEIGHT[1]]
NAO_HITBOX = [(16, NAO_Y[0], 32, 64),
              (SCREEN_WIDTH + 32, NAO_Y[1], 64, 128)]
ENEMY_LAYER = 2