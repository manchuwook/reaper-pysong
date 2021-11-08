# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = coordinate_from_dict(json.loads(json_string))

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


def from_bool(x: Any) -> Any:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
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
    CHORUS = "Chorus"
    DROP = "Drop"
    INSTRUMENTAL = "Instrumental"
    INTRO = "Intro"
    OUTRO = "Outro"
    PRE_BREAKDOWN = "Pre-Breakdown"
    PRE_CHORUS = "Pre-Chorus"
    PRE_INSTRUMENTAL = "Pre-Instrumental"
    PRE_INTRO = "Pre-Intro"
    PRE_OUTRO = "Pre-Outro"
    PRE_VERSE = "Pre-Verse"
    VERSE = "Verse"
    BRIDGE = "Bridge"


class Part:
    name: Optional[str]
    """The song part in terms of the structure component and length"""

    bars: Optional[int]
    """The number of bars (measures) in the song part.  Multiples of 4"""

    color: str
    """Lowercase color name used to generate hues"""

    max: Optional[int]
    """Maximum number of bars"""

    min: Optional[int]
    """Minimum number of bars"""

    type: TypeEnum
    """Song structure type"""

    index: int
    """Region Number"""

    source: bool
    """Use this as the source for pooled items"""

    def __init__(self, name: Optional[str], bars: Optional[int], color: str, max: Optional[int], min: Optional[int], type: TypeEnum, index: Optional[int], source: Optional[bool]) -> None:
        self.name = name
        self.bars = bars
        self.color = color
        self.max = max
        self.min = min
        self.type = type
        self.index = index
        self.source = source

    @staticmethod
    def from_dict(obj: Any) -> 'Part':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        bars = from_union([from_int, from_none], obj.get("bars"))
        color = from_str(obj.get("color"))
        max = from_union([from_int, from_none], obj.get("max"))
        min = from_union([from_int, from_none], obj.get("min"))
        type = TypeEnum(obj.get("type"))
        index = obj.get("index")
        source = obj.get("source")
        return Part(name, bars, color, max, min, type, index, source)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["bars"] = from_union([from_int, from_none], self.bars)
        result["color"] = from_str(self.color)
        result["max"] = from_union([from_int, from_none], self.max)
        result["min"] = from_union([from_int, from_none], self.min)
        result["type"] = to_enum(TypeEnum, self.type)
        result["index"] = self.index
        result["source"] = self.source
        return result


class SongStructure:
    """Collection of pre-made song structures"""
    """Pattern or Song Structure Name"""
    name: Optional[str]
    """A collection of structural song parts"""
    structure: Optional[List[Part]]

    def __init__(self, name: Optional[str], structure: Optional[List[Part]]) -> None:
        self.name = name
        self.structure = structure

    @staticmethod
    def from_dict(obj: Any) -> 'SongStructure':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        structure = from_union([lambda x: from_list(
            Part.from_dict, x), from_none], obj.get("structure"))
        return SongStructure(name, structure)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["structure"] = from_union([lambda x: from_list(
            lambda x: to_class(Part, x), x), from_none], self.structure)
        return result


def structures_from_dict(s: Any) -> List[SongStructure]:
    return from_list(SongStructure.from_dict, s)


def structure_to_dict(x: List[SongStructure]) -> Any:
    return from_list(lambda x: to_class(SongStructure, x), x)
