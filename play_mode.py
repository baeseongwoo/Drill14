import random

from pico2d import *
import game_world
import game_framework
from boy import Boy
from grass import Grass
from bird import Bird, FRAMES_PER_ACTION

BIRD_COUNT = 10

boy = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)

    # 새떼 10마리: 같은 종(같은 크기, 같은 날갯짓 거리)이지만 개체마다 조금씩 다르게
    # 소년(y=90) 머리 위 하늘 영역에서만 날도록 y 범위를 잡음
    for _ in range(BIRD_COUNT):
        bird = Bird(
            x=random.uniform(100, 1500),
            y=random.uniform(250, 560),               # 잔디/소년 위 하늘 영역
            speed_kmph=random.uniform(30.0, 40.0),    # 순항 속도 30~40 km/h
            frame=random.uniform(0, FRAMES_PER_ACTION),  # 날갯짓 박자가 모두 같지 않게
            dir=random.choice((-1, 1)),
        )
        game_world.add_oject(bird, 1)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()
    # delay(0.1)  # 강제적인 프레임 시간 증가 (테스트할 때 주석 해제)

def render():
    clear_canvas()
    game_world.render()
    update_canvas()
