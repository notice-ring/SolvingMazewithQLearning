class DesignOption:
    def __init__(
        self,
        primary_color: str = "blue",  # 메인 컬러
        secondary_color: str = "green",  # 보조 컬러
        tertiary_color: str = "red",  # 세번째 컬러
        disabled_color: str = "gray",  # 비활성화된 컬러
        border_width: int = 4,  # 테두리 두께
        disabled_border_width: int = 2,  # 비활성화된 테두리 두께
        circle_width: int = 3,  # 원 테두리 두께
    ) -> "DesignOption":
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.tertiary_color = tertiary_color
        self.disabled_color = disabled_color
        self.border_width = border_width
        self.disabled_border_width = disabled_border_width
        self.circle_width = circle_width

    def get_primary_color(self, disabled: bool = False) -> str:
        return self.disabled_color if disabled else self.primary_color

    def get_secondary_color(self, disabled: bool = False) -> str:
        return self.disabled_color if disabled else self.secondary_color

    def get_tertiary_color(self, disabled: bool = False) -> str:
        return self.disabled_color if disabled else self.tertiary_color

    def get_border_width(self, disabled: bool = False) -> int:
        return self.disabled_border_width if disabled else self.border_width
