const fs = require('fs');
const cy = require('cytoscape');
const data = require('./data.json');

const graph = cy({
    data: {
        name: "notesGraph"
    }
});

const beatsAndNotes = /M1_4\/4_V1_B(?<beat>[0-9]\.[0-9]+)_(?<duration>.*)/;

nid = 0;
data.map(m => {
    const ma = beatsAndNotes.exec(m.label);
    if (ma && ma.groups) {
        const { beat, duration } = ma.groups;
        graph.add({ group: 'nodes', data: { id: `N${nid++}`, label: m.label, beat, duration } });
        m.to.map(to => {
            const mato = beatsAndNotes.exec(to.label);
            if (mato && mato.groups) {
                const { beat, duration } = mato;
                graph.add({
                    group: 'nodes',
                    data: {
                        id: `N${nid++}`,
                        label: to.label,
                        beat: (beat) ? beat : 0.0, duration: (duration) ? duration : 0
                    }
                });
            }
        });
    }
});

eid = 0;
data.map(m => {
    const source = graph.filter(`node[label = "${m.label}"]`);
    m.to.map(to => {
        const target = graph.filter(`node[label = "${to.label}"]`);
        if (target.data().label !== 'M1_4/4_V1_B0.0_NILS') {
            graph.add({
                group: 'edges',
                data: {
                    id: eid++,
                    sourceLabel: m.label,
                    source: source.id(),
                    targetLabel: to.label,
                    target: target.id(),
                    weight: Math.random() * (Math.random() > 0.5 ? 1 : -1),
                    tie: !(to.tie && to.tie === 'N/A')
                }
            });
        }
    });
});

let options = {
    name: 'concentric',

    fit: true, // whether to fit the viewport to the graph
    padding: 30, // the padding on fit
    startAngle: 3 / 2 * Math.PI, // where nodes start in radians
    sweep: undefined, // how many radians should be between the first and last node (defaults to full circle)
    clockwise: true, // whether the layout should go clockwise (true) or counterclockwise/anticlockwise (false)
    equidistant: false, // whether levels have an equal radial distance betwen them, may cause bounding box overflow
    minNodeSpacing: 10, // min spacing between outside of nodes (used for radius adjustment)
    boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
    avoidOverlap: true, // prevents node overlap, may overflow boundingBox if not enough space
    nodeDimensionsIncludeLabels: false, // Excludes the label when calculating node bounding boxes for the layout algorithm
    height: undefined, // height of layout area (overrides container height)
    width: undefined, // width of layout area (overrides container width)
    spacingFactor: undefined, // Applies a multiplicative factor (>0) to expand or compress the overall area that the nodes take up
    concentric: function (node) { // returns numeric value for each node, placing higher nodes in levels towards the centre
        return Math.floor(node.data().beat);
    },
    levelWidth: function (nodes) { // the variation of concentric values in each level
        return nodes.maxDegree() / 4;
    },
    animate: false, // whether to transition the node positions
    animationDuration: 500, // duration of animation in ms if enabled
    animationEasing: undefined, // easing of animation if enabled
    animateFilter: function (node, i) { return true; }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
    ready: undefined, // callback on layoutready
    stop: undefined, // callback on layoutstop
    transform: function (node, position) { return position; } // transform a given node position. Useful for changing flow direction in discrete layouts
};

graph.layout(options);

const exported = graph.json();
fs.writeFileSync('graph.json', JSON.stringify(exported), { encoding: 'utf-8' });