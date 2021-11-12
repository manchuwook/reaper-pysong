# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = song_library_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, Any, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class TypeEnum(Enum):
    """Song structure type"""
    BREAKDOWN = "Breakdown"
    """Notes are more drawn out or minimally dispersed"""
    BRIDGE = "Bridge"
    """Let's the listener know they are towards the end of the song """
    CHORUS = "Chorus"
    """Contains the hook and is typically repetitive"""
    DROP = "Drop"
    """Post-crescendo excited action"""
    INSTRUMENTAL = "Instrumental"
    """Section with no vocals"""
    INTRO = "Intro"
    """Beginning of the song, introducing themes and for a buildup"""
    OUTRO = "Outro"
    """Descending action of the song"""
    PRE_BREAKDOWN = "Pre-Breakdown"
    PRE_CHORUS = "Pre-Chorus"
    """Transition from another part through voicing"""
    PRE_INSTRUMENTAL = "Pre-Instrumental"
    """Build-up to the instrumental section"""
    PRE_INTRO = "Pre-Intro"
    """Sound effects or soundbyte"""
    PRE_OUTRO = "Pre-Outro"
    """Indicate that the song is ending"""
    PRE_VERSE = "Pre-Verse"
    """Transition from the intro or chorus to the verse"""
    VERSE = "Verse"
    """Repeated section of a song that typically features a new set of lyrics on each repetition"""


class SongPart:
    """The song part in terms of the structure component and length"""
    name: Optional[str]
    """The name of the song style"""
    bars: Optional[int]
    """The number of bars (measures) in the song part.  Multiples of 4"""
    color: str
    """Lowercase color name used to generate hues"""
    index: Optional[str]
    """Index of the related region"""
    max: Optional[int]
    """Maximum number of bars"""
    min: Optional[int]
    """Minimum number of bars"""
    type: TypeEnum
    """Song structure type"""
    variation: Optional[bool]
    """part is a variation on a theme"""

    def __init__(self, name: Optional[str], bars: Optional[int], color: str, index: Optional[str], max: Optional[int], min: Optional[int], type: TypeEnum, variation: Optional[bool]) -> None:
        self.name = name
        self.bars = bars
        self.color = color
        self.index = index
        self.max = max
        self.min = min
        self.type = type
        self.variation = variation

    @staticmethod
    def from_dict(obj: Any) -> 'SongPart':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        bars = from_union([from_int, from_none], obj.get("bars"))
        color = from_str(obj.get("color"))
        index = from_union([from_str, from_none], obj.get("index"))
        max = from_union([from_int, from_none], obj.get("max"))
        min = from_union([from_int, from_none], obj.get("min"))
        type = TypeEnum(obj.get("type"))
        variation = from_union([from_bool, from_none], obj.get("variation"))
        return SongPart(name, bars, color, index, max, min, type, variation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["bars"] = from_union([from_int, from_none], self.bars)
        result["color"] = from_str(self.color)
        result["index"] = from_union([from_str, from_none], self.index)
        result["max"] = from_union([from_int, from_none], self.max)
        result["min"] = from_union([from_int, from_none], self.min)
        result["type"] = to_enum(TypeEnum, self.type)
        result["variation"] = from_union(
            [from_bool, from_none], self.variation)
        return result


class SongLibraryElement:
    """Song consisting of a name and structures"""
    name: Optional[str]
    """Pattern or Song Structure Name"""
    structure: Optional[List[SongPart]]
    """A collection of structural song parts"""

    def __init__(self, name: Optional[str], structure: Optional[List[SongPart]]) -> None:
        self.name = name
        self.structure = structure

    @staticmethod
    def from_dict(obj: Any) -> 'SongLibraryElement':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        structure = from_union([lambda x: from_list(
            SongPart.from_dict, x), from_none], obj.get("structure"))
        return SongLibraryElement(name, structure)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["structure"] = from_union([lambda x: from_list(
            lambda x: to_class(SongPart, x), x), from_none], self.structure)
        return result


def song_library_from_dict(s: Any) -> List[SongLibraryElement]:
    return from_list(SongLibraryElement.from_dict, s)


def song_library_to_dict(x: List[SongLibraryElement]) -> Any:
    return from_list(lambda x: to_class(SongLibraryElement, x), x)
