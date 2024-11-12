# 클래스별로 파일을 분리하는 게 좋을까요?

from typing import Any
import tkinter.messagebox as msgbox
import ttkbootstrap as ttk
from .wall_builder import WallBuilder
from .design_option import DesignOption


class Page:
    def __init__(
        self,
        root: ttk.Window,
        label: ttk.Label,
        description: str,
        design_option: DesignOption = DesignOption(),
    ) -> "Page":
        self.__root = root
        self.__label = label
        self.__description = description
        self.__design_option = design_option

    @property
    def root(self) -> ttk.Window:
        return self.__root

    @property
    def design_option(self) -> DesignOption:
        return self.__design_option

    def show(self) -> None:
        self.__label.config(text=self.__description)

    def dismiss(self) -> bool:
        return True

    def extract_data(self) -> dict[str, Any]:
        raise NotImplementedError


class InitPage(Page):
    def __init__(
        self, root: ttk.Window, label: ttk.Label, options: dict[str, Any]
    ) -> "InitPage":
        super().__init__(root, label, "Select the size of the maze.")
        self.options = options

    def show(self) -> None:
        super().show()
        self.__frame = ttk.Frame(self.root)
        self.__frame.pack(pady=10)

        self.__row = ttk.Combobox(
            self.__frame,
            state="readonly",
            values=[i for i in range(*self.options["row"])],
        )
        label = ttk.Label(self.__frame, text="X")
        self.__col = ttk.Combobox(
            self.__frame,
            state="readonly",
            values=[i for i in range(*self.options["col"])],
        )

        self.__row.current(0)
        self.__col.current(0)
        self.__row.pack(padx=10, side=ttk.LEFT)
        label.pack(padx=10, side=ttk.LEFT)
        self.__col.pack(padx=10, side=ttk.LEFT)

    def dismiss(self) -> bool:
        self.__frame.pack_forget()
        return True

    def extract_data(self) -> dict[str, Any]:
        return {"row": int(self.__row.get()), "col": int(self.__col.get())}


class WallPage(Page):
    def __init__(self, root: ttk.Window, label: ttk.Label) -> "WallPage":
        super().__init__(root, label, "Click on the edge of the maze to build a wall.")

    def show(self, wall_builder: WallBuilder) -> None:
        super().show()
        self.__wall_builder = wall_builder

    def dismiss(self) -> bool:
        self.__wall_builder.change_click_event()
        return True

    def extract_data(self) -> dict[str, Any]:
        return {"directions": self.__wall_builder.get_movement_data()}


class StartPage(Page):
    def __init__(self, root: ttk.Window, label: ttk.Label) -> "StartPage":
        super().__init__(root, label, "Select the start point.")

    def show(self, wall_builder: WallBuilder) -> None:
        super().show()
        self.__wall_builder = wall_builder

    def dismiss(self) -> bool:
        if self.__wall_builder.selected_area is None:
            msgbox.showerror("Error", "Select the start point.")
            return False
        self.__wall_builder.add_marking(
            *self.__wall_builder.selected_area,
            color=self.design_option.primary_color,
        )
        return True

    def extract_data(self) -> dict[str, Any]:
        data = {"start": self.__wall_builder.selected_area}
        self.__wall_builder.reset_temp_marking()  # TODO: 이게 여기 있는 게 마음에 안 듦
        return data


class GoalPage(Page):
    def __init__(self, root: ttk.Window, label: ttk.Label) -> "GoalPage":
        super().__init__(root, label, "Select the goal point.")

    def show(self, wall_builder: WallBuilder) -> None:
        super().show()
        self.__wall_builder = wall_builder

    def dismiss(self) -> bool:
        if self.__wall_builder.selected_area is None:
            msgbox.showerror("Error", "Select the goal point.")
            return False
        self.__wall_builder.add_marking(
            *self.__wall_builder.selected_area,
            color=self.design_option.secondary_color,
        )
        return True

    def extract_data(self) -> dict[str, Any]:
        data = {"goal": self.__wall_builder.selected_area}
        self.__wall_builder.reset_temp_marking()
        return data


class EndPage(Page):
    def __init__(self, root: ttk.Window, label: ttk.Label) -> "EndPage":
        super().__init__(root, label, "Select the death point.")

    def show(self, wall_builder: WallBuilder) -> None:
        super().show()
        self.__wall_builder = wall_builder

    def dismiss(self) -> bool:
        if self.__wall_builder.selected_area is None:
            msgbox.showerror("Error", "Select the death point.")
            return False
        self.__wall_builder.add_marking(
            *self.__wall_builder.selected_area,
            color=self.design_option.tertiary_color,
        )
        return True

    def extract_data(self) -> dict[str, Any]:
        data = {"end": self.__wall_builder.selected_area}
        self.__wall_builder.reset_temp_marking()
        return data
