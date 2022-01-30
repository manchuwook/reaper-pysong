# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cytoscape_graph_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Type, cast, Callable
from enum import Enum


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class RendererClass:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'RendererClass':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        return RendererClass(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


class Classes(Enum):
    EDGE = "edge"


class EdgeData:
    id: int
    source_label: str
    source: str
    target_label: str
    target: str
    weight: float
    stop: bool
    tie: bool

    def __init__(self, id: int, source_label: str, source: str, target_label: str, target: str, weight: float, stop: bool, tie: bool) -> None:
        self.id = id
        self.source_label = source_label
        self.source = source
        self.target_label = target_label
        self.target = target
        self.weight = weight
        self.stop = stop
        self.tie = tie

    @staticmethod
    def from_dict(obj: Any) -> 'EdgeData':
        assert isinstance(obj, dict)
        id = int(from_str(obj.get("id")))
        source_label = from_str(obj.get("sourceLabel"))
        source = from_str(obj.get("source"))
        target_label = from_str(obj.get("targetLabel"))
        target = from_str(obj.get("target"))
        weight = from_float(obj.get("weight"))
        stop = from_bool(obj.get("stop"))
        tie = from_bool(obj.get("tie"))
        return EdgeData(id, source_label, source, target_label, target, weight, stop, tie)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(str(self.id))
        result["sourceLabel"] = from_str(self.source_label)
        result["source"] = from_str(self.source)
        result["targetLabel"] = from_str(self.target_label)
        result["target"] = from_str(self.target)
        result["weight"] = to_float(self.weight)
        result["stop"] = from_bool(self.stop)
        result["tie"] = from_bool(self.tie)
        return result


class EdgeGroup(Enum):
    EDGES = "edges"


class Pan:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def from_dict(obj: Any) -> 'Pan':
        assert isinstance(obj, dict)
        x = from_float(obj.get("x"))
        y = from_float(obj.get("y"))
        return Pan(x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["x"] = to_float(self.x)
        result["y"] = to_float(self.y)
        return result


class Edge:
    data: EdgeData
    position: Pan
    group: EdgeGroup
    removed: bool
    selected: bool
    selectable: bool
    locked: bool
    grabbable: bool
    pannable: bool
    classes: Classes

    def __init__(self, data: EdgeData, position: Pan, group: EdgeGroup, removed: bool, selected: bool, selectable: bool, locked: bool, grabbable: bool, pannable: bool, classes: Classes) -> None:
        self.data = data
        self.position = position
        self.group = group
        self.removed = removed
        self.selected = selected
        self.selectable = selectable
        self.locked = locked
        self.grabbable = grabbable
        self.pannable = pannable
        self.classes = classes

    @staticmethod
    def from_dict(obj: Any) -> 'Edge':
        assert isinstance(obj, dict)
        data = EdgeData.from_dict(obj.get("data"))
        position = Pan.from_dict(obj.get("position"))
        group = EdgeGroup(obj.get("group"))
        removed = from_bool(obj.get("removed"))
        selected = from_bool(obj.get("selected"))
        selectable = from_bool(obj.get("selectable"))
        locked = from_bool(obj.get("locked"))
        grabbable = from_bool(obj.get("grabbable"))
        pannable = from_bool(obj.get("pannable"))
        classes = Classes(obj.get("classes"))
        return Edge(data, position, group, removed, selected, selectable, locked, grabbable, pannable, classes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(EdgeData, self.data)
        result["position"] = to_class(Pan, self.position)
        result["group"] = to_enum(EdgeGroup, self.group)
        result["removed"] = from_bool(self.removed)
        result["selected"] = from_bool(self.selected)
        result["selectable"] = from_bool(self.selectable)
        result["locked"] = from_bool(self.locked)
        result["grabbable"] = from_bool(self.grabbable)
        result["pannable"] = from_bool(self.pannable)
        result["classes"] = to_enum(Classes, self.classes)
        return result


class NodeData:
    label: str
    beat: float
    duration: str
    id: str

    def __init__(self, label: str, beat: float, duration: str, id: str) -> None:
        self.label = label
        self.beat = beat
        self.duration = duration
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> 'NodeData':
        assert isinstance(obj, dict)
        label = from_str(obj.get("label"))
        beat = from_float(obj.get("beat"))
        duration = from_str(obj.get("duration"))
        id = from_str(obj.get("id"))
        return NodeData(label, beat, duration, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["label"] = from_str(self.label)
        result["beat"] = to_float(self.beat)
        result["duration"] = from_str(self.duration)
        result["id"] = from_str(self.id)
        return result


class NodeGroup(Enum):
    NODES = "nodes"


class Node:
    data: NodeData
    position: Pan
    group: NodeGroup
    removed: bool
    selected: bool
    selectable: bool
    locked: bool
    grabbable: bool
    pannable: bool
    classes: str

    def __init__(self, data: NodeData, position: Pan, group: NodeGroup, removed: bool, selected: bool, selectable: bool, locked: bool, grabbable: bool, pannable: bool, classes: str) -> None:
        self.data = data
        self.position = position
        self.group = group
        self.removed = removed
        self.selected = selected
        self.selectable = selectable
        self.locked = locked
        self.grabbable = grabbable
        self.pannable = pannable
        self.classes = classes

    @staticmethod
    def from_dict(obj: Any) -> 'Node':
        assert isinstance(obj, dict)
        data = NodeData.from_dict(obj.get("data"))
        position = Pan.from_dict(obj.get("position"))
        group = NodeGroup(obj.get("group"))
        removed = from_bool(obj.get("removed"))
        selected = from_bool(obj.get("selected"))
        selectable = from_bool(obj.get("selectable"))
        locked = from_bool(obj.get("locked"))
        grabbable = from_bool(obj.get("grabbable"))
        pannable = from_bool(obj.get("pannable"))
        classes = from_str(obj.get("classes"))
        return Node(data, position, group, removed, selected, selectable, locked, grabbable, pannable, classes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(NodeData, self.data)
        result["position"] = to_class(Pan, self.position)
        result["group"] = to_enum(NodeGroup, self.group)
        result["removed"] = from_bool(self.removed)
        result["selected"] = from_bool(self.selected)
        result["selectable"] = from_bool(self.selectable)
        result["locked"] = from_bool(self.locked)
        result["grabbable"] = from_bool(self.grabbable)
        result["pannable"] = from_bool(self.pannable)
        result["classes"] = from_str(self.classes)
        return result


class Elements:
    nodes: List[Node]
    edges: List[Edge]

    def __init__(self, nodes: List[Node], edges: List[Edge]) -> None:
        self.nodes = nodes
        self.edges = edges

    @staticmethod
    def from_dict(obj: Any) -> 'Elements':
        assert isinstance(obj, dict)
        nodes = from_list(Node.from_dict, obj.get("nodes"))
        edges = from_list(Edge.from_dict, obj.get("edges"))
        return Elements(nodes, edges)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nodes"] = from_list(lambda x: to_class(Node, x), self.nodes)
        result["edges"] = from_list(lambda x: to_class(Edge, x), self.edges)
        return result


class CytoscapeGraph:
    elements: Elements
    data: RendererClass
    zooming_enabled: bool
    user_zooming_enabled: bool
    zoom: float
    min_zoom: float
    max_zoom: float
    panning_enabled: bool
    user_panning_enabled: bool
    pan: Pan
    box_selection_enabled: bool
    renderer: RendererClass

    def __init__(self, elements: Elements, data: RendererClass, zooming_enabled: bool, user_zooming_enabled: bool, zoom: float, min_zoom: float, max_zoom: float, panning_enabled: bool, user_panning_enabled: bool, pan: Pan, box_selection_enabled: bool, renderer: RendererClass) -> None:
        self.elements = elements
        self.data = data
        self.zooming_enabled = zooming_enabled
        self.user_zooming_enabled = user_zooming_enabled
        self.zoom = zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.panning_enabled = panning_enabled
        self.user_panning_enabled = user_panning_enabled
        self.pan = pan
        self.box_selection_enabled = box_selection_enabled
        self.renderer = renderer

    @staticmethod
    def from_dict(obj: Any) -> 'CytoscapeGraph':
        assert isinstance(obj, dict)
        elements = Elements.from_dict(obj.get("elements"))
        data = RendererClass.from_dict(obj.get("data"))
        zooming_enabled = from_bool(obj.get("zoomingEnabled"))
        user_zooming_enabled = from_bool(obj.get("userZoomingEnabled"))
        zoom = from_float(obj.get("zoom"))
        min_zoom = from_float(obj.get("minZoom"))
        max_zoom = from_float(obj.get("maxZoom"))
        panning_enabled = from_bool(obj.get("panningEnabled"))
        user_panning_enabled = from_bool(obj.get("userPanningEnabled"))
        pan = Pan.from_dict(obj.get("pan"))
        box_selection_enabled = from_bool(obj.get("boxSelectionEnabled"))
        renderer = RendererClass.from_dict(obj.get("renderer"))
        return CytoscapeGraph(elements, data, zooming_enabled, user_zooming_enabled, zoom, min_zoom, max_zoom, panning_enabled, user_panning_enabled, pan, box_selection_enabled, renderer)

    def to_dict(self) -> dict:
        result: dict = {}
        result["elements"] = to_class(Elements, self.elements)
        result["data"] = to_class(RendererClass, self.data)
        result["zoomingEnabled"] = from_bool(self.zooming_enabled)
        result["userZoomingEnabled"] = from_bool(self.user_zooming_enabled)
        result["zoom"] = to_float(self.zoom)
        result["minZoom"] = to_float(self.min_zoom)
        result["maxZoom"] = to_float(self.max_zoom)
        result["panningEnabled"] = from_bool(self.panning_enabled)
        result["userPanningEnabled"] = from_bool(self.user_panning_enabled)
        result["pan"] = to_class(Pan, self.pan)
        result["boxSelectionEnabled"] = from_bool(self.box_selection_enabled)
        result["renderer"] = to_class(RendererClass, self.renderer)
        return result


def cytoscape_graph_from_dict(s: Any) -> CytoscapeGraph:
    return CytoscapeGraph.from_dict(s)


def cytoscape_graph_to_dict(x: CytoscapeGraph) -> Any:
    return to_class(CytoscapeGraph, x)
