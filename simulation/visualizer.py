class Visualizer:
    """Handles ANSI color formatting for terminal output."""
    COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "orange": "\033[38;5;208m",
        "gray": "\033[90m",
        "reset": "\033[0m"
    }

    @classmethod
    def colorize(cls, text: str, color: str | None) -> str:
        """Returns the text wrapped in ANSI color codes if the color exists."""
        if not color:
            return text
        color_code = cls.COLORS.get(color.lower(), "")
        reset_code = cls.COLORS["reset"]
        if color_code:
            return f"{color_code}{text}{reset_code}"
        return text
