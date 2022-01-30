import fs = require('fs');
import { Core, NodeDefinition, NodeSingular, EdgeSingular, ElementDefinition } from 'cytoscape';
import cytoscape = require('cytoscape');

/** @type {*} */
const beatsAndNotes = /M1_4\/4_V1_B(?<beat>[0-9]\.[0-9]+)_(?<duration>.*)/;

/**
 * Basic graph structure object
 *
 * @export
 * @interface NoteData
 */
export interface NoteData {
    /**
     * Label of the note in the format of
     * M1_x/x_V1_Bx.x_x/xN|R|T|TN|TR
     * @type {string}
     * @memberof NoteData
     */
    label: string;
    /**
     * Source label
     *
     * @type {string}
     * @memberof NoteData
     */
    from: string;
    /**
     * Target nodes
     *
     * @type {To[]}
     * @memberof NoteData
     */
    to: To[];
}
/**
 *
 *
 * @export
 * @interface To
 */
export interface To {
    /**
     * Target label of node
     *
     * @type {string}
     * @memberof To
     */
    label: string;
    /**
     * Percent chance of selecting this item
     *
     * @type {string}
     * @memberof To
     */
    nextPercentage: string;
    /**
     * Whether to tie to the next note
     *
     * @type {Tie}
     * @memberof To
     */
    tie: Tie;
}
/**
 * A tie option
 *
 * @export
 * @enum {number}
 */
export enum Tie {
    /**
     *
     */
    NA = "N/A",
}

class GraphConverter {
    graph: cytoscape.Core;

    constructor(data: NoteData[]) {
        this.graph = cytoscape({
            data: { name: "notesGraph" }
        });

        let nid = 0;

        const addId = (m: ElementDefinition): ElementDefinition => {
            m.data.id = `N${nid++}`;
            return m;
        };

        data.flatMap(m => {
            const ma = beatsAndNotes.exec(m.label);
            let eds: ElementDefinition[] = [];
            if (ma && ma.groups) {
                const { beat, duration } = ma.groups;
                eds.push({
                    group: 'nodes',
                    data: {
                        label: m.label,
                        beat: (beat) ? +beat : 0.0,
                        duration: (duration) ? duration : 0
                    }, classes: "nodes"
                });
            }

            m.to.map(to => {
                const mato = beatsAndNotes.exec(to.label);
                if (mato && mato.groups) {
                    const beat = mato.groups["beat"];
                    const duration = mato.groups["duration"];
                    const def: ElementDefinition = {
                        group: 'nodes',
                        data: {
                            label: to.label,
                            beat: (beat) ? +beat : 0.0,
                            duration: (duration) ? duration : 0
                        }, classes: "nodes"
                    };
                    return def;
                }
            }).filter(this.isElement())
                .map(m => eds.push(m));

            return eds;
        }).map(addId).forEach(x => this.graph.add(x));

        let eid = 0;
        data.flatMap(m => {
            const source = this.graph.filter(`node[label = "${m.label}"]`);
            return m.to.map(to => {
                const target = this.graph.filter(`node[label = "${to.label}"]`);
                const targetId = target.id();
                if (targetId === undefined) {
                    console.log(to.label);
                    return;
                }
                const def: ElementDefinition = {
                    group: 'edges',
                    data: {
                        id: `${eid++}`,
                        sourceLabel: m.label,
                        source: source.id(),
                        targetLabel: to.label,
                        target: targetId,
                        weight: Math.random() * (Math.random() > 0.5 ? 1 : -1),
                        stop: (target.data('label') === 'M1_4/4_V1_B0.0_NILS'),
                        tie: !(to.tie && to.tie === 'N/A')
                    }, classes: 'edge'
                };
                return def;
            });
        }).filter(this.isElement())
            .forEach(x => this.graph.add(x));

        let options: BeatConcentricLayoutOptions = {
            name: 'concentric',
            fit: true, padding: 30,
            startAngle: 3 / 2 * Math.PI,
            sweep: undefined, clockwise: true,
            equidistant: true, minNodeSpacing: 10,
            boundingBox: undefined, avoidOverlap: true,
            nodeDimensionsIncludeLabels: false,
            height: undefined, width: undefined,
            animate: false, animationDuration: 500,
            animationEasing: undefined,
            ready: undefined, stop: undefined,
            spacingFactor: undefined,
            animateFilter: function (node: NodeSingular, i) {
                return true;
            },
            concentric: function (node) {
                // Each beat (simplified) is a valence
                const ndb = Math.floor(node.data('beat') as number);
                return ndb;
            },
            levelWidth: function (nodes) {
                // Get a count of the nodes by beat and find the largest number of nodes
                const x = nodes.reduce((acc, value) => {
                    const vd: number = Math.floor(value.data('beat') ?? '0.0');
                    const accum: { [key: string]: number; } = acc;
                    if (!accum[vd]) { accum[vd] = 1; } else { accum[vd]++; }
                    return accum;
                }, {});

                // The count of beats (simplified)
                const k = Object.keys(x).length;

                // The beats that has the largest number of members
                const mv = Object.values<number>(x).sort((a, b) => b - a)[0];

                // List count and members
                console.log(k, mv);

                // I don't understand this
                return k;
            },
            transform: function (node: NodeSingular, position) {
                return position;
            }
        };

        this.graph.layout(options).run();
    }

    writeFile = (destination: string) => {
        const exported = this.graph.json();
        fs.writeFileSync(
            destination,
            JSON.stringify(exported),
            { encoding: 'utf-8' }
        );
    };

    private isElement(): (
        value: ElementDefinition | undefined,
        index: number,
        array: (ElementDefinition | undefined)[]
    ) => value is ElementDefinition {
        return (element): element is ElementDefinition => Boolean(element);
    }
}

interface BeatConcentricLayoutOptions extends Omit<Omit<cytoscape.ConcentricLayoutOptions, 'levelWidth'>, 'concentric'> {
    // returns numeric value for each node, placing higher nodes in levels towards the centre
    concentric(node: { degree(): number, data(name: string): any; }): number;
    // the variation of concentric values in each level
    levelWidth?(node: cytoscape.NodeCollection): number;
}

let json = fs.readFileSync('./data.json', { encoding: 'utf-8' });
let data: NoteData[] = JSON.parse(json);

const gc = new GraphConverter(data);
gc.writeFile('graph.json');