import pygame

FILL_TYPE_NONE = 0
FILL_TYPE_BORDER = 1

COORD_CENTER = 0
COORD_LEFTBOTTOM = 1
COORD_LEFTTOP = 2
COORD_MIDTOP = 3

DB_DIR = "db"
DB_FILENAME = "db.sqlite"

ANIMATION_IDLE = "idle"
ANIMATION_ATTACK = "attack"
ANIMATION_BEGIN_MOVE = "begin_move"
ANIMATION_MOVE = "move"
ANIMATION_END_MOVE = "end_move"
ANIMATION_DEATH = "death"

MELEE_ATTACK = "melee"
RANGE_ATTACK = "range"

my_units_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
shop_group = pygame.sprite.Group()
landscape_group = pygame.sprite.Group()

action_in_progress = False

current_user = None
