import start_game
from animation import AnimationChain, MovableAnimatedSprite
from global_vars import ANIMATION_ATTACK, ANIMATION_IDLE, ANIMATION_MOVE, ANIMATION_END_MOVE, ANIMATION_BEGIN_MOVE, \
    RANGE_ATTACK, MELEE_ATTACK, ANIMATION_DEATH


class Unit(MovableAnimatedSprite):
    def __init__(self, animations, x, y, group, scale_to, default_animation, mirror_animation=False):
        super().__init__(animations, x, y, group, scale_to, default_animation, mirror_animation)
        self.default_stock = 0

        self.default_step = 0
        self.step = 0
        self.do_damage = True
        self.is_dead = False

        self.distance_attack = 0
        self.attack_type = MELEE_ATTACK
        self.hp = 0
        self.damage = 0
        self.damage_plus = 0
        self.name = ''
        self.title = ''

    def __repr__(self):
        return f"[{id(self)} | {super().__repr__()}]"

    def init_stats(self, step, distance_attack, attack_type, hp, damage, name, title, stock):
        self.default_step = step
        self.step = step
        self.distance_attack = distance_attack
        self.attack_type = attack_type
        self.hp = hp
        self.damage = damage
        self.name = name
        self.title = title
        self.default_stock = stock

    def update(self, *args, **kwargs):
        self.next_frame()
        self.move_tick()
        self.gc_tick()

    def make_step(self, cell_coords, choose_cell, screen, callback=None, callback_args=None):
        x_now, y_now = cell_coords
        select_x, select_y = choose_cell
        self.damage_plus = 0

        if screen.board.field[select_y][select_x] == 2 and self.attack_type == RANGE_ATTACK:
            self.damage_plus = 15

        screen.board.board[y_now][x_now], screen.board.board[select_y][select_x] = screen.board.board[select_y][
            select_x], screen.board.board[y_now][x_now]

        x = (select_x - x_now) * screen.board.cell_size
        y = (select_y - y_now) * screen.board.cell_size
        px = self.rect.x + x
        py = self.rect.y + y

        mirror = x < 0
        animation_chain = AnimationChain()
        animation_chain.add_step(ANIMATION_BEGIN_MOVE, mirror=mirror)
        steps = max([abs(select_x - x_now), abs(select_y - y_now)])
        tx = x / steps
        ty = y / steps
        for i in range(1, steps + 1):
            animation_chain.add_step(ANIMATION_MOVE, self.move, [tx, ty], mirror=mirror)
        animation_chain.add_step(ANIMATION_END_MOVE, self.set_position, [px, py], mirror=mirror)
        animation_chain.add_step(ANIMATION_IDLE, callback, callback_args)

        self.start_animation_chain(animation_chain)
        self.step = 0

    def make_attack(self, choose_cell, screen, callback=None, callback_args=None):
        select_x, select_y = choose_cell
        animation_chain = AnimationChain()

        x = select_x * screen.board.cell_size + screen.board.left
        y = select_y * screen.board.cell_size + screen.board.top

        mirror = x < self.rect.x
        args = [screen, (x, y), (select_x, select_y), self]
        animation_chain.add_step(ANIMATION_ATTACK, start_game.give_damage, args, mirror=mirror)
        animation_chain.add_step(ANIMATION_IDLE, callback, callback_args)

        self.start_animation_chain(animation_chain)
        self.do_damage = False

    def make_death(self):
        animation_chain = AnimationChain()

        animation_chain.add_step(ANIMATION_IDLE)
        animation_chain.add_step(ANIMATION_DEATH)
        animation_chain.add_step(ANIMATION_DEATH, self.kill, [])

        self.start_animation_chain(animation_chain)

    def recieve_damage(self, actor):
        self.hp -= actor.get_damage()
        if self.hp <= 0:
            self.is_dead = True
            self.make_death()

    def get_damage(self):
        return self.damage + self.damage_plus

    def refresh(self):
        self.step = self.default_step
        self.do_damage = True
