from dataclasses import dataclass, field
import math

@dataclass
class Rectangle:
    width: float = 0.0
    height: float = 0.0
    x1: float = 0.0
    y1: float = 0.0
    rotation: float = 0.0

    def __post_init__(self) -> None:
        if self.width < 0.0 or self.height < 0.0:
            raise ValueError("width and height must be nonnegative.")

@dataclass
class Circle:
    x1: float = 0.0
    y1: float = 0.0
    radius: float = 0.0

    def __post_init__(self) -> None:
        if self.radius < 0.0:
            raise ValueError("radius must be nonnegative.")

def main() -> None:
    r = Rectangle(width=3.0, height=4.0)
    c = Circle(x1=0.0, y1=0.0, radius=2.0)
    print(r)
    print(c)

if __name__ == "__main__":
    main()
