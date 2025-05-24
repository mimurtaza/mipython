class Cylinder:
    def __init__(self, cross_section: Circle, height: float, density: float = None, mass: float = None):
        self.section = cross_section
        self.height = height
        self.density = density

        if self.height <= 0:
            raise ValueError("Height must be positive.")

        self.volume = self.section.area() * self.height
        self.mass = mass if mass is not None else self.volume * density if density is not None else None

        if self.mass is None:
            raise ValueError("Either 'density' or 'mass' must be provided.")

    def lateral_surface_area(self) -> float:
        ro = self.section.r_outer
        ri = self.section.r_inner
        return 2 * math.pi * (ro + ri) * self.height if self.section.is_hollow() else 2 * math.pi * ro * self.height

    def end_surface_area(self) -> float:
        return 2 * self.section.area()

    def total_surface_area(self) -> float:
        return self.lateral_surface_area() + self.end_surface_area()

    def moment_of_inertia(self, axis: str = 'z') -> float:
        R = self.section.r_outer
        Ri = self.section.r_inner
        m = self.mass

        if axis == 'z':
            return 0.5 * m * (R**2 + Ri**2)
        elif axis in ('x', 'y'):
            return (1/12) * m * (3 * (R**2 + Ri**2) + self.height**2)
        else:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'.")

    def __repr__(self):
        h = self.height
        m = self.mass
        return f"Cylinder({self.section}, H={h:.3f} m, Mass={m:.3f} kg)"

if __name__ == "__main__":
    solid_circle = Circle(outer_radius=0.05)
    hollow_circle = Circle(outer_radius=0.05, inner_radius=0.03)

    solid_cylinder = Cylinder(cross_section=solid_circle, height=0.2, density=7850)
    hollow_cylinder = Cylinder(cross_section=hollow_circle, height=0.2, density=7850)

    print(solid_cylinder)
    print(f"  Area: {solid_circle.area():.6f} m²")
    print(f"  Polar Moment: {solid_circle.polar_moment():.6e} m⁴")
    print(f"  Inertia Z: {solid_cylinder.moment_of_inertia('z'):.6f} kg·m²")

    print(hollow_cylinder)
    print(f"  Area: {hollow_circle.area():.6f} m²")
    print(f"  Polar Moment: {hollow_circle.polar_moment():.6e} m⁴")
    print(f"  Inertia Z: {hollow_cylinder.moment_of_inertia('z'):.6f} kg·m²")
