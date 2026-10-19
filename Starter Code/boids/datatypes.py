from dataclasses import dataclass, field

@dataclass
class OrderedPair:
    """
    Represents a point or vector in two-dimensional space.

    Attributes:
        x (float): The x-coordinate of the point or vector.
        y (float): The y-coordinate of the point or vector.
    """
    x: float = 0.0
    y: float = 0.0

@dataclass
class Boid:
    """
    Represents our "bird" object.

    Each Boid has position, velocity, and acceleration, each represented by
    an OrderedPair instance.

    Attributes:
        position (OrderedPair): The current position of the boid.
        velocity (OrderedPair): The current velocity of the boid.
        acceleration (OrderedPair): The current acceleration of the boid.
    """
    position: OrderedPair = field(default_factory=OrderedPair)
    velocity: OrderedPair = field(default_factory=OrderedPair)
    acceleration: OrderedPair = field(default_factory=OrderedPair)


@dataclass
class Sky:
    """
    Represents a single time point of the simulation.

    The Sky defines the simulation parameters such as spatial boundaries, speed limits,
    and behavioral factors influencing boid interactions (separation, alignment, cohesion).

    Attributes:
        width (float): The boundary width of the simulation space.
        boids (list[Boid]): A list of Boid objects within the sky.
        max_boid_speed (float): The maximum allowed speed for any boid.
        proximity (float): The distance threshold within which boids influence each other.
        separation_factor (float): The weighting factor for the separation behavior.
        alignment_factor (float): The weighting factor for the alignment behavior.
        cohesion_factor (float): The weighting factor for the cohesion behavior.
    """
    width: float = 0.0
    boids: list[Boid] = field(default_factory=list)
    max_boid_speed: float = 0.0  # fastest speed that a boid can fly
    proximity: float = 0.0       # used to determine if boids are close enough for forces to apply
    separation_factor: float = 0.0
    alignment_factor: float = 0.0
    cohesion_factor: float = 0.0

