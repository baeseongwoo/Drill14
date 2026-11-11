from pico2d import *

import game_framework

# bird_animation.png 분석 결과 (918 x 506, 투명 배경)
# - 가로 5칸 x 세로 3줄, 마지막 줄은 4칸 -> 총 14 프레임
# - 각 칸의 새 눈(파란 홍채) 중심 x 좌표가 정확히 182 픽셀 간격 -> 프레임 폭 182
# - 세로는 506 / 3 = 약 168.7 픽셀 -> 프레임 높이 169
SHEET_W, SHEET_H = 918, 506
FRAME_W, FRAME_H = 182, 169
COLS, ROWS = 5, 3
FRAMES_PER_ACTION = 14  # 날갯짓 1회(위 -> 아래 -> 위)를 구성하는 프레임 수

# 화면의 물리 단위 (LEC16 과 동일: 10 pixel = 30 cm)
PIXEL_PER_METER = (10.0 / 0.3)

# 새 크기: 날개를 편 옆모습 한 프레임이 실제로 1.5 m 정도인 대형 새(독수리급)로 가정
BIRD_SIZE_M = 1.5
BIRD_DRAW_W = BIRD_SIZE_M * PIXEL_PER_METER          # 50 pixel
BIRD_DRAW_H = BIRD_DRAW_W * FRAME_H / FRAME_W         # 원본 비율 유지 (약 46 pixel)

# Bird Fly Speed : 대형 새의 순항 속도 약 35 km/h
FLY_SPEED_KMPH = 35.0
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)                # 약 9.72 m/s
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)     # 약 324 pixel/s

# Bird Action Speed
# 소년의 '보폭(STRIDE_LENGTH_M)'에 해당하는 값: 날갯짓 1회 동안 앞으로 나아가는 거리
DISTANCE_PER_FLAP_M = 3.5
# 1초에 날갯짓을 몇 번 하는가? (약 2.8회/초 -> 대형 새의 실제 날갯짓 빈도 2~3Hz 범위)
FLAPS_PER_SECOND = FLY_SPEED_MPS / DISTANCE_PER_FLAP_M
# 1초에 프레임을 몇 개 넘겨야 하는가? (약 38.9 프레임/초)
FLY_FRAMES_PER_SECOND = FLAPS_PER_SECOND * FRAMES_PER_ACTION


def frame_rect(index):
    """index 번째 프레임의 시트 내 (left, bottom) 좌표.
    시트는 왼쪽 위부터 오른쪽으로, 줄이 끝나면 다음 줄로 진행(행 우선).
    pico2d 는 왼쪽 아래가 원점이므로 위에서부터 센 줄 번호를 뒤집어 계산한다."""
    col = index % COLS
    row = index // COLS  # 0: 맨 윗줄
    left = col * FRAME_W
    bottom = int(SHEET_H - (row + 1) * SHEET_H / ROWS)  # 337, 168, 0
    return left, bottom


class Bird:
    image = None

    def __init__(self, x=100, y=400, speed_kmph=FLY_SPEED_KMPH, frame=0.0, dir=1):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = frame  # 실수로 누적, 그릴 때 int() 로 변환
        self.dir = dir  # 1: 오른쪽, -1: 왼쪽

        # 새마다 속도가 다를 수 있으므로, 같은 공식으로 개체별 값을 계산
        speed_mps = speed_kmph * 1000.0 / 60.0 / 60.0
        self.speed_pps = speed_mps * PIXEL_PER_METER
        self.frames_per_second = speed_mps / DISTANCE_PER_FLAP_M * FRAMES_PER_ACTION

    def update(self):
        self.frame = (self.frame + self.frames_per_second * game_framework.frame_time) % FRAMES_PER_ACTION
        # 이동 거리 = 속도 x 프레임 시간 -> 컴퓨터 성능과 무관하게 같은 속도
        self.x += self.dir * self.speed_pps * game_framework.frame_time

        # 화면 끝에 닿으면 방향 전환 (몸 절반만큼 여유를 두어 화면 밖으로 나가지 않게)
        half_w = BIRD_DRAW_W / 2
        if self.x > get_canvas_width() - half_w:
            self.x = get_canvas_width() - half_w
            self.dir = -1
        elif self.x < half_w:
            self.x = half_w
            self.dir = 1

    def draw(self):
        left, bottom = frame_rect(int(self.frame))
        if self.dir == 1:  # 시트의 새는 오른쪽을 보고 있음
            Bird.image.clip_draw(left, bottom, FRAME_W, FRAME_H, self.x, self.y,
                                 BIRD_DRAW_W, BIRD_DRAW_H)
        else:  # 왼쪽으로 날 때는 좌우 반전
            Bird.image.clip_composite_draw(left, bottom, FRAME_W, FRAME_H, 0, 'h',
                                           self.x, self.y, BIRD_DRAW_W, BIRD_DRAW_H)
