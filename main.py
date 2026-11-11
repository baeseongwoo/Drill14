from pico2d import open_canvas, delay, close_canvas
import pico2d
from sdl2 import (SDL_SetWindowSize, SDL_SetWindowPosition, SDL_RenderSetLogicalSize,
                  SDL_WINDOWPOS_CENTERED)
import game_framework

import play_mode as start_mode

CANVAS_W, CANVAS_H = 1600, 600   # 게임 좌표계 크기 (그대로 유지)
WINDOW_SCALE = 0.75              # 실제 창 크기 비율 (1200 x 450)

open_canvas(CANVAS_W, CANVAS_H)
SDL_RenderSetLogicalSize(pico2d.pico2d.renderer, CANVAS_W, CANVAS_H)
SDL_SetWindowSize(pico2d.pico2d.window, int(CANVAS_W * WINDOW_SCALE), int(CANVAS_H * WINDOW_SCALE))
SDL_SetWindowPosition(pico2d.pico2d.window, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED)
game_framework.run(start_mode)
close_canvas()
