import tkinter as tk
from designoption import DesignOption

DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500
VERTICAL, HORIZONTAL = 0, 1


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

        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.pack()

        self.__init_walls()
        self.draw_walls()
        self.canvas.bind("<Button-1>", self.__on_click)

    # 현재 벽 상태를 그리는 함수
    def draw_walls(self) -> None:
        self.canvas.delete("all")

        # 수직 벽 그리기
        for row in range(self.rows):
            for col in range(self.cols + 1):
                self.__draw_vertical_wall(row, col, self.walls[VERTICAL][row][col])

        # 수평 벽 그리기
        for row in range(self.rows + 1):
            for col in range(self.cols):
                self.__draw_horizontal_wall(row, col, self.walls[HORIZONTAL][row][col])

    def __draw_vertical_wall(self, row, col, is_blocked):
        x1 = x2 = (col + 1) * self.width // (self.cols + 2)
        y1 = (row + 1) * self.height // (self.rows + 2)
        y2 = (row + 2) * self.height // (self.rows + 2)
        self.canvas.create_line(
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
        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=self.design_option.get_color(is_blocked),
            width=self.design_option.get_border_width(is_blocked),
        )

    def __init_walls(self):
        self.walls = {
            VERTICAL: [
                [(i == 0 or i == self.cols) for i in range(self.cols + 1)]
                for _ in range(self.rows)
            ],
            HORIZONTAL: [
                [(i == 0 or i == self.rows)] * (self.cols) for i in range(self.rows + 1)
            ],
        }

    def __on_click(self, event):
        x_offset = event.x * (self.cols + 2) / self.width
        y_offset = event.y * (self.rows + 2) / self.height
        x, y = round(x_offset), round(y_offset)

        if abs(x - x_offset) < abs(y - y_offset):  # 수직 벽 선택
            self.walls[VERTICAL][int(y_offset) - 1][x - 1] = not self.walls[VERTICAL][
                int(y_offset) - 1
            ][x - 1]
        else:  # 수평 벽 선택
            self.walls[HORIZONTAL][y - 1][int(x_offset) - 1] = not self.walls[
                HORIZONTAL
            ][y - 1][int(x_offset) - 1]

        self.draw_walls()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wall Builder")
    root.geometry("700x700")

    wb = WallBuilder(root, 5, 5)
    root.mainloop()
