from typing import List, Tuple
import tkinter as tk
from designoption import DesignOption

DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500
VERTICAL, HORIZONTAL = 0, 1
WALL, AREA = 0, 1


class WallBuilder:
    def __init__(
        self,
        root: tk.Tk,
        rows: int,
        cols: int,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        design_option: DesignOption = DesignOption(),
    ) -> "WallBuilder":
        self.root = root
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.design_option = design_option
        self.__marked = []
        self.area = None

        self.__canvas = tk.Canvas(root, width=width, height=height)
        self.__canvas.pack()

        self.__init_datas()
        self.draw()

        self.__event = WALL
        self.__canvas.bind("<Button-1>", self.__on_wall_click)

    # 클릭 이벤트(벽을 그리는지, 공간을 선택하는지)를 바꾸는 함수
    def change_click_event(self):
        self.__canvas.unbind("<Button-1>")
        if self.__event == WALL:
            self.__event = AREA
            self.__canvas.bind("<Button-1>", self.__on_area_click)
        else:
            self.__event = WALL
            self.__canvas.bind("<Button-1>", self.__on_wall_click)

    # 현재 상태를 그리는 함수
    def draw(self) -> None:
        self.__canvas.delete("all")

        # 수직 벽 그리기
        for row in range(self.rows):
            for col in range(self.cols + 1):
                self.__draw_vertical_wall(row, col, self.walls[VERTICAL][row][col])

        # 수평 벽 그리기
        for row in range(self.rows + 1):
            for col in range(self.cols):
                self.__draw_horizontal_wall(row, col, self.walls[HORIZONTAL][row][col])

        # 선택한 곳 그리기
        if self.area:
            self.__draw_circle(*self.area, is_accent=True)

        # 이미 선택한 곳 그리기
        for r, c in self.__marked:
            self.__draw_circle(r, c)

    # 벽 정보를 MazeWorld에 맞게 변환하는 함수
    def get_movement_data(self) -> List[List[List[int]]]:
        result = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                if not self.walls[HORIZONTAL][row][col]:  # 위쪽 벽 없음
                    result[row][col].append(0)
                if not self.walls[HORIZONTAL][row + 1][col]:  # 아래쪽 벽 없음
                    result[row][col].append(1)
                if not self.walls[VERTICAL][row][col]:  # 왼쪽 벽 없음
                    result[row][col].append(2)
                if not self.walls[VERTICAL][row][col + 1]:  # 오른쪽 벽 없음
                    result[row][col].append(3)

        return result

    # 공간 선택을 초기화하는 함수
    def reset_area(self) -> None:
        self.area = None
        self.draw()

    # 이미 선택한 공간을 추가하는 함수
    def mark_area(self, area: Tuple[int]) -> None:
        self.__marked.append(area)
        self.draw()

    def __draw_vertical_wall(self, row, col, is_blocked):
        x1 = x2 = (col + 1) * self.width // (self.cols + 2)
        y1 = (row + 1) * self.height // (self.rows + 2)
        y2 = (row + 2) * self.height // (self.rows + 2)
        self.__canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=self.design_option.get_color(is_blocked),
            width=self.design_option.get_border_width(is_blocked),
        )

    def __draw_horizontal_wall(self, row, col, is_blocked):
        x1 = (col + 1) * self.width // (self.cols + 2)
        y1 = y2 = (row + 1) * self.height // (self.rows + 2)
        x2 = (col + 2) * self.width // (self.cols + 2)
        self.__canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=self.design_option.get_color(is_blocked),
            width=self.design_option.get_border_width(is_blocked),
        )

    def __draw_circle(self, row, col, is_accent=False):
        x = (row + 0.5) * self.width // (self.cols + 2)
        y = (col + 0.5) * self.height // (self.rows + 2)
        self.__canvas.create_oval(
            x - 10,
            y - 10,
            x + 10,
            y + 10,
            outline=self.design_option.get_accent_color(is_accent),
            width=self.design_option.get_border_width(is_accent),
        )

    def __init_datas(self):
        self.walls = {
            VERTICAL: [
                [(i == 0 or i == self.cols) for i in range(self.cols + 1)]
                for _ in range(self.rows)
            ],
            HORIZONTAL: [
                [(i == 0 or i == self.rows)] * (self.cols) for i in range(self.rows + 1)
            ],
        }
        self.area = None

    def __on_wall_click(self, event):
        x_offset = event.x * (self.cols + 2) / self.width
        y_offset = event.y * (self.rows + 2) / self.height
        x, y = round(x_offset), round(y_offset)
        if x <= 1 or x >= self.cols + 1 or y <= 1 or y >= self.rows + 1:
            return

        if abs(x - x_offset) < abs(y - y_offset):  # 수직 벽 선택
            self.walls[VERTICAL][int(y_offset) - 1][x - 1] = not self.walls[VERTICAL][
                int(y_offset) - 1
            ][x - 1]
        else:  # 수평 벽 선택
            self.walls[HORIZONTAL][y - 1][int(x_offset) - 1] = not self.walls[
                HORIZONTAL
            ][y - 1][int(x_offset) - 1]

        self.draw()

    def __on_area_click(self, event):
        x_offset = event.x * (self.cols + 2) / self.width
        y_offset = event.y * (self.rows + 2) / self.height
        x, y = int(x_offset), int(y_offset)

        if x <= 0 or x >= self.cols + 1 or y <= 0 or y >= self.rows + 1:
            return
        if (x, y) in self.__marked:
            return

        self.area = (x, y)
        self.draw()
