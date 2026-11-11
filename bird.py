from pico2d import *

# bird_animation.png 분석 결과 (918 x 506, 투명 배경)
# - 가로 5칸 x 세로 3줄, 마지막 줄은 4칸 -> 총 14 프레임
# - 각 칸의 새 눈(파란 홍채) 중심 x 좌표가 정확히 182 픽셀 간격 -> 프레임 폭 182
# - 세로는 506 / 3 = 약 168.7 픽셀 -> 프레임 높이 169
SHEET_W, SHEET_H = 918, 506
FRAME_W, FRAME_H = 182, 169


class Bird:
    image = None

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = 800, 400

    def update(self):
        pass

    def draw(self):
        # 시트의 왼쪽 위 첫 번째 프레임 (pico2d 는 왼쪽 아래가 원점)
        Bird.image.clip_draw(0, SHEET_H - FRAME_H, FRAME_W, FRAME_H, self.x, self.y)
