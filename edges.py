# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = edges_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Edge:
    source: str
    target: str
    from_label: str
    to_label: str
    weight: int

    def __init__(self, source: str, target: str, from_label: str, to_label: str, weight: int) -> None:
        self.source = source
        self.target = target
        self.from_label = from_label
        self.to_label = to_label
        self.weight = weight

    @staticmethod
    def from_dict(obj: Any) -> 'Edge':
        assert isinstance(obj, dict)
        source = from_str(obj.get("source"))
        target = from_str(obj.get("target"))
        from_label = from_str(obj.get("fromLabel"))
        to_label = from_str(obj.get("toLabel"))
        weight = from_int(obj.get("weight"))
        return Edge(source, target, from_label, to_label, weight)

    def to_dict(self) -> dict:
        result: dict = {}
        result["source"] = from_str(self.source)
        result["target"] = from_str(self.target)
        result["fromLabel"] = from_str(self.from_label)
        result["toLabel"] = from_str(self.to_label)
        result["weight"] = from_int(self.weight)
        return result


class ID:
    oid: str

    def __init__(self, oid: str) -> None:
        self.oid = oid

    @staticmethod
    def from_dict(obj: Any) -> 'ID':
        assert isinstance(obj, dict)
        oid = from_str(obj.get("$oid"))
        return ID(oid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["$oid"] = from_str(self.oid)
        return result


class EdgesData:
    id: ID
    data: Edge

    def __init__(self, id: ID, data: Edge) -> None:
        self.id = id
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> 'EdgesData':
        assert isinstance(obj, dict)
        id = ID.from_dict(obj.get("_id"))
        data = Edge.from_dict(obj.get("data"))
        return EdgesData(id, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = to_class(ID, self.id)
        result["data"] = to_class(Edge, self.data)
        return result


def edges_from_dict(s: Any) -> List[EdgesData]:
    return from_list(EdgesData.from_dict, s)


def edges_to_dict(x: List[EdgesData]) -> Any:
    return from_list(lambda x: to_class(EdgesData, x), x)
