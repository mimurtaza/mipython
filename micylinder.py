import math

class Cylinder:
    def __init__(self, outer_radius: float, height: float, density: float = None, mass: float = None, inner_radius: float = 0.0):
        """
        Parameters:
            outer_radius (float): Outer radius [m]
            height (float): Height of the cylinder [m]
            density (float): Material density [kg/m³] (optional if mass is given)
            mass (float): Total mass [kg] (optional if density is given)
            inner_radius (float): Inner radius [m]; zero for solid cylinder
        """
        self.r_outer = outer_radius
        self.r_inner = inner_radius
        self.height = height

        self._validate_geometry()

        self.volume = math.pi * (self.r_outer**2 - self.r_inner**2) * self.height
        self.density = density
        self.mass = mass if mass is not None else self.volume * density if density is not None else None

        if self.mass is None:
            raise ValueError("Either 'density' or 'mass' must be provided.")

    def _validate_geometry(self):
        if self.r_outer <= 0 or self.height <= 0:
            raise ValueError("Outer radius and height must be positive.")
        if self.r_inner < 0:
            raise ValueError("Inner radius cannot be negative.")
        if self.r_inner >= self.r_outer:
            raise ValueError("Inner radius must be less than outer radius.")

    def is_hollow(self) -> bool:
        return self.r_inner > 0

    def cross_sectional_area(self) -> float:
        return math.pi * (self.r_outer**2 - self.r_inner**2)

    def lateral_surface_area(self) -> float:
        if self.is_hollow():
            return 2 * math.pi * (self.r_outer + self.r_inner) * self.height
        return 2 * math.pi * self.r_outer * self.height

    def end_surface_area(self) -> float:
        return 2 * self.cross_sectional_area()

    def total_surface_area(self) -> float:
        end_caps = 2 * math.pi * (self.r_outer**2 - self.r_inner**2)
        lateral = self.lateral_surface_area()
        return lateral + end_caps

    def moment_of_inertia(self, axis: str = 'z') -> float:
        """
        Mass moment of inertia [kg·m²]
        """
        m = self.mass
        R = self.r_outer
        Ri = self.r_inner

        if axis == 'z':
            return 0.5 * m * (R**2 + Ri**2)
        elif axis in ('x', 'y'):
            return (1/12) * m * (3 * (R**2 + Ri**2) + self.height**2)
        else:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'.")

    def second_moment_of_area(self, axis: str = 'x') -> float:
        """
        Second moment of area (aka area moment of inertia) [m⁴]
        Used in bending: I_x or I_y (circular symmetry → equal)

        I_x = I_y = (π/4) * (R_o⁴ - R_i⁴)
        """
        R = self.r_outer
        Ri = self.r_inner
        if axis not in ('x', 'y'):
            raise ValueError("Axis must be 'x' or 'y'")
        return (math.pi / 4) * (R**4 - Ri**4)

    def polar_moment_of_area(self) -> float:
        """
        Polar moment of area J [m⁴]
        Used in torsion: J = I_x + I_y = (π/2) * (R_o⁴ - R_i⁴)
        """
        R = self.r_outer
        Ri = self.r_inner
        return (math.pi / 2) * (R**4 - Ri**4)

    def __repr__(self):
        hollow_flag = "Hollow" if self.is_hollow() else "Solid"
        return f"{hollow_flag} Cylinder(R_outer={self.r_outer:.3f} m, R_inner={self.r_inner:.3f} m, H={self.height:.3f} m, Mass={self.mass:.3f} kg)"

if __name__ == "__main__":
    solid = Cylinder(outer_radius=0.05, height=0.2, density=7800)
    hollow = Cylinder(outer_radius=0.05, inner_radius=0.03, height=0.2, density=7800)

    print(solid)
    print(f"  Second Moment (I_x): {solid.second_moment_of_area('x'):.6e} m⁴")
    print(f"  Polar Moment (J): {solid.polar_moment_of_area():.6e} m⁴")

    print(hollow)
    print(f"  Second Moment (I_x): {hollow.second_moment_of_area('x'):.6e} m⁴")
    print(f"  Polar Moment (J): {hollow.polar_moment_of_area():.6e} m⁴")
