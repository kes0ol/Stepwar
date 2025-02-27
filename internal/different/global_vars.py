import pygame

'''Файл для констант'''
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

UNIT_SWORDSMAN = 'swordsman'
UNIT_ARCHER = 'archer'
UNIT_CAVALRY = 'cavalry'
UNIT_DRAGON = 'dragon'
UNIT_CASTLE = 'castle'

QUANTITY_SWORDSMAN = 5
QUANTITY_ARCHER = 2
QUANTITY_CAVALRY = 0
QUANTITY_DRAGON = 0

BOARD_EMPTY = 0
BOARD_MY_UNIT = 1
BOARD_ENEMY = 2
BOARD_ENEMY_CASTLE = 3
BOARD_MY_CASTLE = 4

FIELD_GRASS = 0
FIELD_MOUNTAIN = 1
FIELD_HILL = 2
FIELD_RIVER = 3

FPS = 60

my_units_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
shop_group = pygame.sprite.Group()
landscape_group = pygame.sprite.Group()

action_in_progress = False

current_user = None
