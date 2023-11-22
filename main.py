import arcade as a
import random
import time

import animate
from animate import Animate

SCREEN_TITLE = 'Bomber'
CELL_WIDTH = 60
CELL_HEIGHT = 60
ROW_COUNT = 11  # MUST BE ODD NUMBER
COLUMN_COUNT = 11  # MUST BE ODD NUMBER
SCREEN_WIDTH = COLUMN_COUNT * CELL_WIDTH
SCREEN_HEIGHT = ROW_COUNT * CELL_HEIGHT
BOMBERMAN_SPEED = 5
PLAYER1_BOMB_COUNT = 1
PLAYER2_BOMB_COUNT = 1
PlAYER1_POWER = 3
PLAYER2_POWER = 3


def difference(coordinate, distance):
    return coordinate * distance + distance / 2


def justify_x(position_x):
    for x in range(COLUMN_COUNT):
        cell_center_x = difference(x, CELL_WIDTH)
        if position_x - cell_center_x <= CELL_WIDTH / 2:
            return cell_center_x


def justify_y(position_y):
    for y in range(ROW_COUNT):
        cell_center_y = difference(y, CELL_HEIGHT)
        if position_y - cell_center_y <= CELL_HEIGHT / 2:
            return cell_center_y


class Game(a.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # Textures
        self.bg = a.load_texture('Blocks/BackgroundTile.png')
        # sprite lists
        self.solid_blocks = a.SpriteList()
        self.explodable_blocks = a.SpriteList()
        self.bombs_player1 = a.SpriteList()
        self.bombs_player2 = a.SpriteList()
        self.explosions = a.SpriteList()
        # Sprites
        self.bomberman = Bomberman(PLAYER1_BOMB_COUNT, PlAYER1_POWER)
        self.bomberman2 = Bomberman(PLAYER2_BOMB_COUNT, PLAYER2_POWER)

        self.win1 = a.load_texture('win/win1.png')
        self.win2 = a.load_texture('win/win2.png')

        self.game = True

    def draw_background(self):
        for y in range(ROW_COUNT):
            for x in range(COLUMN_COUNT):
                a.draw_texture_rectangle(
                    x * CELL_WIDTH + CELL_WIDTH / 2,
                    y * CELL_HEIGHT + CELL_HEIGHT / 2,
                    CELL_WIDTH,
                    CELL_HEIGHT,
                    self.bg
                )

    def setup(self):
        for y in range(ROW_COUNT):
            for x in range(COLUMN_COUNT):
                if y % 2 == 1 and x % 2 == 1:
                    solid_block = SolidBlock()
                    solid_block.center_x = x * CELL_WIDTH + CELL_WIDTH / 2
                    solid_block.center_y = y * CELL_HEIGHT + CELL_HEIGHT / 2
                    self.solid_blocks.append(solid_block)
                else:
                    if (not (x == 0 and y <= 2) and not (y == 0 and x <= 2)
                            and not (y == COLUMN_COUNT - 1 and x >= ROW_COUNT - 3) and not (
                                    x == ROW_COUNT - 1 and y >= COLUMN_COUNT - 3)):
                        rand_number = random.randint(1, 2)
                        if rand_number == 1:
                            exp_block = ExplodableBlock()
                            exp_block.center_x = x * CELL_WIDTH + CELL_WIDTH / 2
                            exp_block.center_y = y * CELL_HEIGHT + CELL_HEIGHT / 2
                            self.explodable_blocks.append(exp_block)
        # set location for bomberman
        x = SCREEN_WIDTH / COLUMN_COUNT - CELL_WIDTH / 2
        y = SCREEN_HEIGHT / ROW_COUNT - CELL_HEIGHT / 2
        self.bomberman.set_position(x, y)
        self.bomberman.costume_change()
        # set location for bomberman2
        x2 = SCREEN_WIDTH - CELL_WIDTH / 2
        y2 = SCREEN_HEIGHT - CELL_HEIGHT / 2
        self.bomberman2.set_position(x2, y2)
        self.bomberman2.costume_change()

    def on_draw(self):
        self.clear((255, 255, 255))
        self.draw_background()
        self.solid_blocks.draw()
        self.explodable_blocks.draw()
        self.bomberman.draw()
        self.bomberman2.draw()
        self.bombs_player1.draw()
        self.bombs_player2.draw()
        self.explosions.draw()

        if self.bomberman.win:
            a.draw_texture_rectangle(
                center_x=SCREEN_WIDTH / 2,
                center_y=SCREEN_HEIGHT / 2,
                width=SCREEN_WIDTH,
                height=SCREEN_HEIGHT,
                texture=self.win1
            )
            self.game = False

        if self.bomberman2.win:
            a.draw_texture_rectangle(
                center_x=SCREEN_WIDTH / 2,
                center_y=SCREEN_HEIGHT / 2,
                width=SCREEN_WIDTH,
                height=SCREEN_HEIGHT, texture=self.win2

            )
            self.game = False

    def on_key_press(self, symbol: int, modifiers: int):
        if self.game:
            if symbol == a.key.LEFT:
                self.bomberman.to_left()
            elif symbol == a.key.RIGHT:
                self.bomberman.to_right()
            elif symbol == a.key.UP:
                self.bomberman.to_up()
            elif symbol == a.key.DOWN:
                self.bomberman.to_down()
            self.bomberman.costume_change()
            if symbol == a.key.SPACE:
                if len(self.bombs_player1) < self.bomberman.bomb_count:
                    bomb = Bomb(self.bomberman.power)
                    bomb.center_x = justify_x(self.bomberman.center_x)
                    bomb.center_y = justify_y(self.bomberman.center_y)
                    self.bombs_player1.append(bomb)

            if symbol == a.key.A:
                self.bomberman2.to_left()
            elif symbol == a.key.D:
                self.bomberman2.to_right()
            elif symbol == a.key.W:
                self.bomberman2.to_up()
            elif symbol == a.key.S:
                self.bomberman2.to_down()
            self.bomberman2.costume_change()
            if symbol == a.key.Q:
                if len(self.bombs_player2) < self.bomberman2.bomb_count:
                    bomb = Bomb(self.bomberman2.power)
                    bomb.center_x = justify_x(self.bomberman2.center_x)
                    bomb.center_y = justify_y(self.bomberman2.center_y)
                    self.bombs_player2.append(bomb)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == a.key.LEFT or symbol == a.key.RIGHT or symbol == a.key.UP or symbol == a.key.DOWN:
            self.bomberman.to_stop()
        if symbol == a.key.A or symbol == a.key.D or symbol == a.key.W or symbol == a.key.S:
            self.bomberman2.to_stop()

    def update(self, delta_time: float):
        if self.game:
            self.bomberman.update_animation(delta_time)
            self.bomberman2.update_animation(delta_time)
            self.bomberman.update()
            self.bomberman2.update()
            self.bombs_player1.update()
            self.bombs_player2.update()
            self.bombs_player1.update_animation(delta_time)
            self.bombs_player2.update_animation(delta_time)
            self.explosions.update()
            self.explosions.update_animation(delta_time)
            for flame in self.explosions:
                explosions = a.check_for_collision_with_list(flame, self.explodable_blocks)
                if len(explosions) > 0:
                    for block in explosions:
                        block.kill()

                hit_list = a.check_for_collision_with_list(flame, self.solid_blocks)
                if len(hit_list) > 0:
                    flame.kill()

                if a.check_for_collision(flame, self.bomberman):
                    self.bomberman.color = (0, 0, 0)
                    self.bomberman2.win = True

                if a.check_for_collision(flame, self.bomberman2):
                    self.bomberman2.color = (0, 0, 0)
                    self.bomberman.win = True


class SolidBlock(a.Sprite):
    def __init__(self):
        super().__init__('Blocks/SolidBlock.png', 1)


class ExplodableBlock(a.Sprite):
    def __init__(self):
        super().__init__('Blocks/ExplodableBlock.png', 1)


class Bomberman(Animate):
    def __init__(self, bomb_count, power=3):
        super().__init__('Bomberman/Front/Bman_F_f00.png', 0.5)
        self.bomb_count = bomb_count
        self.direction = 4  # left - 1; right - 2; up - 3; down - 4
        self.motion = False
        self.power = power
        self.win = False
        # Front
        self.walk_down_frames = []
        # Back
        self.walk_up_frames = []
        # Right
        self.walk_right_frames = []
        # Left
        self.walk_left_frames = []
        for i in range(8):
            self.walk_left_frames.append(a.load_texture(f'Bomberman/Side/Bman_S_f0{i}.png', flipped_horizontally=True))
            self.walk_down_frames.append(a.load_texture(f'Bomberman/Front/Bman_F_f0{i}.png'))
            self.walk_up_frames.append(a.load_texture(f'Bomberman/Back/Bman_B_f0{i}.png'))
            self.walk_right_frames.append(a.load_texture(f'Bomberman/Side/Bman_S_f0{i}.png'))

    def costume_change(self):
        if self.direction == 1:
            self.textures = self.walk_left_frames
        elif self.direction == 2:
            self.textures = self.walk_right_frames
        elif self.direction == 3:
            self.textures = self.walk_up_frames
        elif self.direction == 4:
            self.textures = self.walk_down_frames

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0

        self.collisions(window.solid_blocks)
        self.collisions(window.explodable_blocks)

    def collisions(self, sprite_list):
        block_hit = a.check_for_collision_with_list(self, sprite_list)
        for block in block_hit:
            if self.left < block.right and self.direction == 1:
                self.left = block.right
            if self.right > block.left and self.direction == 2:
                self.right = block.left
            if self.top > block.bottom and self.direction == 3:
                self.top = block.bottom
            if self.bottom < block.top and self.direction == 4:
                self.bottom = block.top

    def to_up(self):
        if not self.motion:
            self.motion = True
            self.direction = 3
            self.change_y = BOMBERMAN_SPEED

    def to_down(self):
        if not self.motion:
            self.direction = 4
            self.change_y = -BOMBERMAN_SPEED
            self.motion = True

    def to_left(self):
        if not self.motion:
            self.direction = 1
            self.change_x = -BOMBERMAN_SPEED
            self.motion = True

    def to_right(self):
        if not self.motion:
            self.direction = 2
            self.change_x = BOMBERMAN_SPEED
            self.motion = True

    def to_stop(self):
        self.change_x = 0
        self.change_y = 0
        self.motion = False


class Bomb(Animate):
    def __init__(self, power=3):
        super().__init__('Bomb/Bomb_f00.png', 0.7)
        for i in range(3):
            self.append_texture(a.load_texture(f'Bomb/Bomb_f0{i}.png'))
        self.bomb_timer = time.time()
        self.power = power

    def update(self):
        if time.time() - self.bomb_timer > 3:
            self.kill()
            exp = Explosion()
            exp.center_x = self.center_x
            exp.center_y = self.center_y

            left = True
            right = True
            top = True
            bottom = True

            window.explosions.append(exp)
            for i in range(1, self.power):
                if left:
                    exp1 = Explosion()
                    exp1.center_x = exp.center_x - CELL_WIDTH * i
                    exp1.center_y = exp.center_y
                    window.explosions.append(exp1)
                    hit_solid_block = exp1.check()
                    if hit_solid_block:
                        left = False
                if right:
                    exp2 = Explosion()
                    exp2.center_x = exp.center_x + CELL_WIDTH * i
                    exp2.center_y = exp.center_y
                    window.explosions.append(exp2)
                    if exp2.check():
                        right = False
                if bottom:
                    exp3 = Explosion()
                    exp3.center_x = exp.center_x
                    exp3.center_y = exp.center_y - CELL_HEIGHT * i
                    window.explosions.append(exp3)
                    if exp3.check():
                        bottom = False
                if top:
                    exp4 = Explosion()
                    exp4.center_x = exp.center_x
                    exp4.center_y = exp.center_y + CELL_HEIGHT * i
                    window.explosions.append(exp4)
                    if exp4.check():
                        top = False


class Explosion(animate.Animate):
    def __init__(self):
        super().__init__('Flame/Flame_f00.png', 0.7)
        for i in range(5):
            self.append_texture(a.load_texture(f'Flame/Flame_f0{i}.png'))
        self.explosion_timer = time.time()

    def update(self):
        if time.time() - self.explosion_timer > 2:
            self.kill()

    def check(self):
        hit = a.check_for_collision_with_list(self, window.solid_blocks)
        return len(hit) > 0


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
a.run()
