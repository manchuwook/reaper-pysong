import { INoteSequence } from '@magenta/music';
import { NoteSequence } from '@magenta/music/node';
import { sequenceProtoToMidi } from '@magenta/music/node/core';
const JSDOM = require("jsdom").JSDOM;

import * as fs from 'fs';
import * as path from 'path';

// export interface Checkpoint {
//     id: string; model: string;
//     description: string; url: string;
//     sizeMB: number | string;
// }

/**
 *  Simulate browser environment for nodejs.
 */
module.exports.browserenv = function () {
    const cfg = { url: "http://localhost" };
    const dom = new JSDOM("", cfg);
    global.window = dom.window;
    global.document = dom.window.document;

    // Object.keys(global.window).forEach((x) => {
    //     if (typeof global[x] === "undefined") {
    //         global[x] = global.window[x];
    //     }
    // });

    global.Element = window.Element;
    global.Image = window.Image;
    // maybe more of: global.Whatever = window.Whatever

    global.navigator = new Navigator();
};

export class MidiGenerator {
    ns: INoteSequence = new NoteSequence();

    constructor() {
        // const inFile = fs.readFileSync('./checkpoints.json', { encoding: 'utf-8' });
        // const checkpoints: Checkpoint[] = JSON.parse(inFile);
        // const checkpoint: Checkpoint = checkpoints.filter(f => f.id === 'mel_4bar_med_q2')[0];

        this.ns.notes.push(<NoteSequence.INote>[
            { pitch: 60, startTime: 0.0, endTime: 0.5 },
            { pitch: 60, startTime: 0.5, endTime: 1.0 },
            { pitch: 67, startTime: 1.0, endTime: 1.5 },
            { pitch: 67, startTime: 1.5, endTime: 2.0 },
            { pitch: 69, startTime: 2.0, endTime: 2.5 },
            { pitch: 69, startTime: 2.5, endTime: 3.0 },
            { pitch: 67, startTime: 3.0, endTime: 4.0 },
            { pitch: 65, startTime: 4.0, endTime: 4.5 },
            { pitch: 65, startTime: 4.5, endTime: 5.0 },
            { pitch: 64, startTime: 5.0, endTime: 5.5 },
            { pitch: 64, startTime: 5.5, endTime: 6.0 },
            { pitch: 62, startTime: 6.0, endTime: 6.5 },
            { pitch: 62, startTime: 6.5, endTime: 7.0 },
            { pitch: 60, startTime: 7.0, endTime: 8.0 },
        ]);
    }

    write = () => {
        const midi = sequenceProtoToMidi(this.ns);
        fs.writeFileSync('s:\\dev\\genfile.mid', midi, { encoding: 'utf-8' });
    };
}

const mg = new MidiGenerator();
mg.write();
