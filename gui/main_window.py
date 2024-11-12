from typing import Any
from collections.abc import Callable
import ttkbootstrap as ttk
from .wall_builder import WallBuilder
from .pages import InitPage, WallPage, StartPage, GoalPage, EndPage
import time

WINDOW_SIZE = 700
MINROW = MINCOL = 3
MAXROW = MAXCOL = 11


class MainWindow:
    def __init__(
        self,
        title: str = "Maze Solver",  # 창 제목
        size: int = 700,  # 창 크기
        row_cnt: tuple[int, int] = (MINROW, MAXROW),  # 미로 열 개수 상/하한
        col_cnt: tuple[int, int] = (MINCOL, MAXCOL),  # 미로 행 개수 상/하한
        on_finish: Callable[[dict[str, Any]], None] = None,  # 완료시 호출할 함수
    ) -> "MainWindow":
        self.__size = size
        self.__row_cnt = row_cnt
        self.__col_cnt = col_cnt
        self.__on_finish = on_finish
        self.__result = {}

        # 윈도우 생성
        self.__root = ttk.Window(themename="journal")
        self.__root.title(title)
        self.__root.geometry(f"{size}x{size}")

        # 기본 틀 생성
        self.__main_label = ttk.Label(self.__root, text="")
        self.__main_label.pack(pady=10)

        self.__main_button = ttk.Button(
            self.__root, text="Next", bootstyle="success", command=self.__on_next
        )
        self.__main_button.pack()

        # 페이지 설정
        self.__pages = [
            InitPage(self.__root, self.__main_label, {"row": row_cnt, "col": col_cnt}),
            WallPage(self.__root, self.__main_label),
            StartPage(self.__root, self.__main_label),
            GoalPage(self.__root, self.__main_label),
            EndPage(self.__root, self.__main_label),
        ]
        self.__now_page = 0
        self.__wall_builder = None

        # 첫 페이지 실행
        self.__pages[self.__now_page].show()

    # 메인 윈도우를 보여주는 함수
    def show(self):
        self.__root.mainloop()

    def __on_next(self):
        page = self.__pages[self.__now_page]

        if not page.dismiss():
            return

        # TODO: Wall Builder 부분이 만들고 넘기는 부분이 너무 중구난방임.
        data = page.extract_data()
        if self.__now_page == 0:
            self.__wall_builder = WallBuilder(
                self.__root,
                int(data["row"]),
                int(data["col"]),
                width=(self.__size - 200),
                height=(self.__size - 200),
            )
        else:
            self.__result.update(data)

        if self.__now_page == len(self.__pages) - 1:
            self.__root.quit()
            self.__root.destroy()
            self.__on_finish(self.__result)
            return

        self.__now_page += 1
        self.__pages[self.__now_page].show(self.__wall_builder)
