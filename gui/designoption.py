class DesignOption:
    def __init__(
        self,
        primary_color: str = "blue",
        secondary_color: str = "gray",
        primary_border_width: int = 4,
        secondary_border_width: int = 2,
    ):
        self.__primary_color = primary_color
        self.__secondary_color = secondary_color
        self.__primary_border_width = primary_border_width
        self.__secondary_border_width = secondary_border_width

    def get_color(self, is_primary: bool) -> str:
        return self.__primary_color if is_primary else self.__secondary_color

    def get_border_width(self, is_primary: bool) -> int:
        return (
            self.__primary_border_width if is_primary else self.__secondary_border_width
        )
