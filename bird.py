from pico2d import *

# bird_animation.png 분석 결과 (918 x 506, 투명 배경)
# - 가로 5칸 x 세로 3줄, 마지막 줄은 4칸 -> 총 14 프레임
# - 각 칸의 새 눈(파란 홍채) 중심 x 좌표가 정확히 182 픽셀 간격 -> 프레임 폭 182
# - 세로는 506 / 3 = 약 168.7 픽셀 -> 프레임 높이 169
SHEET_W, SHEET_H = 918, 506
FRAME_W, FRAME_H = 182, 169
COLS, ROWS = 5, 3
FRAMES_PER_ACTION = 14  # 날갯짓 1회(위 -> 아래 -> 위)를 구성하는 프레임 수


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

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = 800, 400
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % FRAMES_PER_ACTION

    def draw(self):
        left, bottom = frame_rect(int(self.frame))
        Bird.image.clip_draw(left, bottom, FRAME_W, FRAME_H, self.x, self.y)
