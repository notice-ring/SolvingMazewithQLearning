from typing import List, Tuple
import tkinter as tk
from design_option import DesignOption

VERTICAL, HORIZONTAL = 0, 1
WALL_MODE, AREA_MODE = 0, 1


class WallBuilder:
    def __init__(
        self,
        root: tk.Tk,  # 루트 TK 객체
        rows: int,  # 열 수
        cols: int,  # 행 수
        width: int,  # 너비
        height: int,  # 높이
        design_option: DesignOption = DesignOption(),
    ) -> "WallBuilder":
        self.__root = root
        self.__rows = rows
        self.__cols = cols
        self.__width = width
        self.__height = height
        self.__design_option = design_option

        # 캔버스 생성
        self.__canvas = tk.Canvas(root, width=width, height=height)
        self.__canvas.pack()

        # 초기 데이터 설정
        self.__markings: List["Marking"] = []  # 영역 표시
        self.__temp_marking: "Marking" = None  # 임시 영역 표시(클릭시 변경되는 영역)
        self.__walls = {  # 벽 정보
            VERTICAL: [
                [(i == 0 or i == cols) for i in range(cols + 1)] for _ in range(rows)
            ],
            HORIZONTAL: [[(i == 0 or i == rows)] * cols for i in range(rows + 1)],
        }

        # 클릭 이벤트 설정
        self.__click_event: int = WALL_MODE  # 이벤트 모드(벽 그리기, 영역 선택)
        self.__canvas.bind("<Button-1>", self.__on_wall_click)

        # 현재 상태를 그리기
        self.draw()

    @property
    def selected_area(self) -> Tuple[int]:
        if self.__temp_marking:
            return self.__temp_marking.row, self.__temp_marking.col
        return None

    # 현재 상태를 그리는 함수
    def draw(self) -> None:
        self.__canvas.delete("all")

        # 수직 벽 그리기
        for row in range(self.__rows):
            for col in range(self.__cols + 1):
                self.__draw_vertical_wall(row, col, self.__walls[VERTICAL][row][col])

        # 수평 벽 그리기
        for row in range(self.__rows + 1):
            for col in range(self.__cols):
                self.__draw_horizontal_wall(
                    row, col, self.__walls[HORIZONTAL][row][col]
                )

        # 선택한 곳 그리기
        if self.__temp_marking:
            self.__draw_marking(self.__temp_marking)

        # 영역 표시
        for marking in self.__markings:
            self.__draw_marking(marking)

    # 임시 영역 선택 초기화
    def reset_temp_marking(self) -> None:
        self.__temp_marking = None
        self.draw()

    # 영역 표시 추가
    def add_marking(self, row: int, col: int, color: str) -> None:
        self.__markings.append(Marking(row, col, color))
        self.draw()

    # 이벤트 모드(벽 그리기, 영역 선택)를 변경하는 함수
    def change_click_event(self) -> None:
        self.__canvas.unbind("<Button-1>")
        if self.__click_event == WALL_MODE:
            self.__click_event = AREA_MODE
            self.__canvas.bind("<Button-1>", self.__on_area_click)
        else:
            self.__click_event = WALL_MODE
            self.__canvas.bind("<Button-1>", self.__on_wall_click)

    # MazeWorld에 필요한 벽 데이터를 추출하는 함수
    def get_movement_data(self) -> List[List[List[int]]]:
        result = [[[] for _ in range(self.__cols)] for _ in range(self.__rows)]

        for row in range(self.__rows):
            for col in range(self.__cols):
                if not self.__walls[HORIZONTAL][row][col]:  # 위쪽 벽 없음
                    result[row][col].append(0)
                if not self.__walls[HORIZONTAL][row + 1][col]:
                    result[row][col].append(1)
                if not self.__walls[VERTICAL][row][col]:
                    result[row][col].append(2)
                if not self.__walls[VERTICAL][row][col + 1]:
                    result[row][col].append(3)

        return result

    def __draw_vertical_wall(self, row, col, enabled):
        x1 = x2 = (col + 1) * self.__width // (self.__cols + 2)
        y1 = (row + 1) * self.__height // (self.__rows + 2)
        y2 = (row + 2) * self.__height // (self.__rows + 2)
        self.__canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=self.__design_option.get_primary_color(not enabled),
            width=self.__design_option.get_border_width(not enabled),
        )

    def __draw_horizontal_wall(self, row, col, enabled):
        x1 = (col + 1) * self.__width // (self.__cols + 2)
        y1 = y2 = (row + 1) * self.__height // (self.__rows + 2)
        x2 = (col + 2) * self.__width // (self.__cols + 2)
        self.__canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=self.__design_option.get_primary_color(not enabled),
            width=self.__design_option.get_border_width(not enabled),
        )

    def __draw_marking(self, marking):
        x = (marking.col + 0.5) * self.__width // (self.__cols + 2)
        y = (marking.row + 0.5) * self.__height // (self.__rows + 2)
        self.__canvas.create_oval(
            x - 10,
            y - 10,
            x + 10,
            y + 10,
            outline=marking.color,
            width=self.__design_option.circle_width,
        )

    def __on_wall_click(self, event):
        x_offset = event.x * (self.__cols + 2) / self.__width
        y_offset = event.y * (self.__rows + 2) / self.__height
        x, y = round(x_offset), round(y_offset)

        if x <= 1 or x >= self.__cols + 1 or y <= 1 or y >= self.__rows + 1:
            return

        if abs(x - x_offset) < abs(y - y_offset):
            direction = VERTICAL
            x, y = x - 1, int(y_offset) - 1
        else:
            direction = HORIZONTAL
            x, y = int(x_offset) - 1, y - 1

        self.__walls[direction][y][x] = not self.__walls[direction][y][x]
        self.draw()

    def __on_area_click(self, event):
        x_offset = event.x * (self.__cols + 2) / self.__width
        y_offset = event.y * (self.__rows + 2) / self.__height
        x, y = int(x_offset), int(y_offset)

        if x <= 0 or x >= self.__cols + 1 or y <= 0 or y >= self.__rows + 1:
            return
        for marking in self.__markings:
            if marking.row == y and marking.col == x:
                return

        self.__temp_marking = Marking(y, x, self.__design_option.disabled_color)
        self.draw()


class Marking:
    def __init__(self, row: int, col: int, color: str) -> "Marking":
        self.row = row
        self.col = col
        self.color = color
