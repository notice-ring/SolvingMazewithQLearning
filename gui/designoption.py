class DesignOption:
    def __init__(
        self,
        primary_color: str = "blue",
        secondary_color: str = "gray",
        accent_color: str = "red",
        primary_border_width: int = 4,
        secondary_border_width: int = 2,
    ) -> "DesignOption":
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.primary_border_width = primary_border_width
        self.secondary_border_width = secondary_border_width
        self.accent_color = accent_color

    def get_color(self, is_primary: bool) -> str:
        return self.primary_color if is_primary else self.secondary_color

    def get_accent_color(self, is_accent: bool) -> str:
        return self.accent_color if is_accent else self.secondary_color

    def get_border_width(self, is_primary: bool) -> int:
        return self.primary_border_width if is_primary else self.secondary_border_width
