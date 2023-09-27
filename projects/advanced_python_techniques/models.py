from helpers import cd_to_datetime, datetime_to_str
from typing import List, Optional

from logger import get_logger

logger = get_logger(__name__)


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(
        self,
        designation: str = "",
        name: Optional[str] = None,
        diameter: float = float('nan'),
        hazardous: bool = False,
    ):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation for this NearEarthObject.
        :param name: The IAU name for this NearEarthObject.
        :param diameter: The diameter of this NearEarthObject in kilometers.
        :param hazardous: Whether or not this NearEarthObject is potentially hazardous.
        """
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous
        self.approaches: List = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.designation + " " + self.name

    def __str__(self):
        """Return `str(self)`."""
        return f"A NearEarthObject is {self.fullname}, which is {self.diameter:.3f} km in " \
               f"diameter and {'is' if self.hazardous else 'is not'} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """Return a dictionary of NearEarthObject's attributes"""
        serialize = {}
        serialize['designation'] = self.designation
        serialize['name'] = self.name
        serialize['diameter_km'] = self.diameter
        serialize['potentially_hazardous'] = self.hazardous

        return serialize


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(
        self,
        designation: str = "",
        time: str = "",
        distance: float = 0.0,
        velocity: float = 0.0
    ):
        """Create a new `CloseApproach`.

        :param time: The time of the close approach in calendar date format.
        :param distance: The distance between the NEO and Earth at the time of
            the close approach in astronomical units (AU).
        :param velocity: The velocity of the NEO at the time of the close approach
            in kilometers per second (km/s).
        """
        self._designation = designation
        self.time = cd_to_datetime(calendar_date=time)
        self.distance = distance
        self.velocity = velocity
        self.neo = None

    @property
    def time_str(self) -> str:
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.neo.name:
            return self._designation + " " + self.neo.name
        return self._designation

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, {self.fullname} approaches Earth at a distance "\
               f"of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        logger.info("Running __repr__")
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        """Return a dictionary of CloseApproach's attributes"""
        serialize = {}
        serialize['datetime_utc'] = self.time_str
        serialize['distance_au'] = self.distance
        serialize['velocity_km_s'] = self.velocity
        serialize['neo'] = self.neo.serialize()

        return serialize


if __name__ == '__main__':
    logger.info("Running models.py directly")
    logger.info("Creating NearEarthObject")
    neo = NearEarthObject(
        designation="2020 FK",
        name="One REALLY BIG fake asteroid",
        diameter=12.345,
        hazardous=True
    )
    assert neo.designation == "2020 FK"
    logger.info(neo.designation)
    assert neo.name == "One REALLY BIG fake asteroid"
    logger.info(neo.name)
    assert neo.diameter == 12.345
    logger.info(neo.diameter)
    assert neo.hazardous is True
    logger.info(neo.hazardous)
    logger.info("Creating CloseApproach")
    ca = CloseApproach(
        time="2020-Jan-01 12:00",
        distance=0.25,
        velocity=56.78
    )
    assert ca.time_str == "2020-01-01 12:00"
    logger.info(ca.time_str)
    assert ca.distance == 0.25
    logger.info(ca.distance)
    assert ca.velocity == 56.78
    logger.info(ca.velocity)
    logger.info(ca)
