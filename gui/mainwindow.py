## TODO: 코드 분리,,

from typing import Tuple
import ttkbootstrap as ttk
import tkinter.messagebox as msgbox
from wallbuilder import WallBuilder

INIT_PAGE, WALL_PAGE, START_PAGE, GOAL_PAGE, END_PAGE, LAST_PAGE = range(6)


class MainWindow:
    def __init__(
        self,
        title: str = "Maze Solver",
        size: int = 700,
        row_cnt: Tuple[int] = (3, 11),
        col_cnt: Tuple[int] = (3, 11),
    ) -> "MainWindow":
        self.size = size
        self.row_cnt = row_cnt
        self.col_cnt = col_cnt

        self.root = ttk.Window(themename="journal")
        self.root.title(title)
        self.root.geometry(f"{size}x{size}")

        self.__main_label = ttk.Label(self.root, text="")
        self.__main_label.pack(pady=10)

        self.__main_button = ttk.Button(
            self.root, text="Next", bootstyle="success", command=self.__on_next
        )
        self.__main_button.pack()
        self.__build_init_page()

    # 메인 윈도우를 보여주는 함수
    def show(self):
        self.root.mainloop()

    def __build_init_page(self):
        self.__page = INIT_PAGE
        self.__main_label.config(text="Select the size of the maze.")

        self.__frame = ttk.Frame(self.root, width=(self.size - 200))
        self.__frame.pack(pady=10)

        self.__row = ttk.Combobox(
            self.__frame,
            state="readonly",
            values=[i for i in range(*self.row_cnt)],
        )
        label = ttk.Label(self.__frame, text="X")
        self.__col = ttk.Combobox(
            self.__frame,
            state="readonly",
            values=[i for i in range(*self.col_cnt)],
        )

        self.__row.current(0)
        self.__col.current(0)
        self.__row.pack(padx=10, side=ttk.LEFT)
        label.pack(padx=10, side=ttk.LEFT)
        self.__col.pack(padx=10, side=ttk.LEFT)

    def __build_wall_page(self):
        self.__page = WALL_PAGE
        self.__frame.pack_forget()
        self.__main_label.config(text="Click on the edge of the maze to build a wall.")

        self.__wall_builder = WallBuilder(
            self.root,
            int(self.__row.get()),
            int(self.__col.get()),
            width=(self.size - 200),
            height=(self.size - 200),
        )

    def __build_start_page(self):
        self.__page = START_PAGE
        self.__main_label.config(text="Select the start point.")
        self.__wall_builder.change_click_event()

    def __build_goal_page(self):
        self.__page = GOAL_PAGE
        self.__main_label.config(text="Select the goal point.")
        self.__wall_builder.mark_area(self.start)
        self.__wall_builder.reset_area()

    def __build_end_page(self):
        self.__page = END_PAGE
        self.__main_label.config(text="Select the end point.")
        self.__wall_builder.mark_area(self.goal)
        self.__wall_builder.reset_area()

    def __build_last_page(self):
        self.__page = LAST_PAGE
        self.__main_label.config(text="Click the button to find the path.")
        self.__wall_builder.mark_area(self.end)
        self.__wall_builder.reset_area()
        self.__main_button.config(text="Let's go!")

    def __on_next(self):
        if self.__page == INIT_PAGE:
            self.__build_wall_page()
        elif self.__page == WALL_PAGE:
            self.walls = self.__wall_builder.get_movement_data()
            self.__build_start_page()
        elif self.__page == START_PAGE:
            if self.__wall_builder.area is None:
                msgbox.showerror("Error", "Select the start point.")
            else:
                self.start = self.__wall_builder.area
                self.__build_goal_page()
        elif self.__page == GOAL_PAGE:
            if self.__wall_builder.area is None:
                msgbox.showerror("Error", "Select the goal point.")
            else:
                self.goal = self.__wall_builder.area
                self.__build_end_page()
        elif self.__page == END_PAGE:
            if self.__wall_builder.area is None:
                msgbox.showerror("Error", "Select the end point.")
            else:
                self.end = self.__wall_builder.area
                self.__build_last_page()
        else:
            print(self.walls)
            print(self.start)
            print(self.goal)
            print(self.end)


if __name__ == "__main__":
    mw = MainWindow()
    mw.show()
