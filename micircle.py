import math

class Circle:
    def __init__(self, outer_radius: float, inner_radius: float = 0.0):
        self.r_outer = outer_radius
        self.r_inner = inner_radius
        self._validate()

    def _validate(self):
        if self.r_outer <= 0:
            raise ValueError("Outer radius must be positive.")
        if self.r_inner < 0:
            raise ValueError("Inner radius cannot be negative.")
        if self.r_inner >= self.r_outer:
            raise ValueError("Inner radius must be smaller than outer radius.")

    def area(self) -> float:
        return math.pi * (self.r_outer**2 - self.r_inner**2)

    def second_moment(self) -> float:
        """Second moment of area about x or y axis [m⁴]"""
        return (math.pi / 4) * (self.r_outer**4 - self.r_inner**4)

    def polar_moment(self) -> float:
        """Polar moment of area about center [m⁴]"""
        return (math.pi / 2) * (self.r_outer**4 - self.r_inner**4)

    def is_hollow(self) -> bool:
        return self.r_inner > 0

    def __repr__(self):
        hollow = "Hollow" if self.is_hollow() else "Solid"
        return f"{hollow} Circle(R_outer={self.r_outer:.3f}, R_inner={self.r_inner:.3f})"
