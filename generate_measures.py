from email import message
import sys
import argparse
import json
import edges as edges
import cytoscape_graph as cg
from math import isnan
import networkx as nx
import re
from pydash import flatten_deep, flatten, flat_map
from numpy import random, linalg, min, max, array, isnan, asarray
from song_library import SongPart

# parser = argparse.ArgumentParser(
#     description='generate measure files from a graph')
# parser.add_argument(
#     '--graph', metavar='string', nargs='+', type='string',
#     help='a graphml file to load the notes from')
# args = parser.parse_args()


def load_from_json():
    file = open("music_rhythm_edges.json")
    myEdges = edges.edges_from_dict(json.loads(file.read()))
    g = nx.DiGraph()

    # Loop through edge JSON objects to get the data
    for edge in enumerate(myEdges):
        (_id, edge_data) = edge

        d = edge_data.data

        # Add the edges from the JSON file
        g.add_edge(u_of_edge=d.from_label, v_of_edge=d.to_label,
                   weight=d.weight, source=d.source, target=d.target)

    # Regular expression to split out the beats and duration
    x = re.compile('M1_4\/4_V1_B([0-9]\.[0-9]+)_(.*)')
    for idx, attrs in g.nodes.items():
        # Find all matches in the label string
        fa = x.findall(idx)

        # Unbox the beat and duration from the matches
        beat, duration = fa[0]

        # Set the custom attributes in the node
        g.nodes[idx]['beat'] = beat
        g.nodes[idx]['duration'] = duration

    # Assign a random weight because they are all 0 for the moment
    for u, v in enumerate(g.edges.data(True, None, None)):
        # Unbox the source and target from the edge
        source, target, attrs = v
        # Randomly assign a floating point value fothe the weight
        g[source][target]['weight'] = random.uniform(-1, 1)

    # Get the list of outgoing edges
    for u in enumerate(g.nodes.keys()):
        _id, label = u
        successors = g.successors(label)

        for s in successors:
            ed = g[label][s]

    # Write out to a GraphML file for other tools
    nx.write_graphml(g, 'g.graphml')

    # Tidy up the file handle
    file.close()


def load_from_cytoscape():
    file = open("js_utils/graph.json")
    graph = cg.cytoscape_graph_from_dict(json.loads(file.read()))
    g = nx.DiGraph()

    for node in graph.elements.nodes:
        g.add_node(node.data.label,
                   id=node.data.id,
                   beat=node.data.beat,
                   duration=node.data.duration,
                   y=node.position.y,
                   x=node.position.x)
    for edge in graph.elements.edges:
        g.add_edge(u_of_edge=edge.data.source_label,
                   v_of_edge=edge.data.target_label,
                   weight=edge.data.weight,
                   tie=edge.data.tie)

    # Write out to a GraphML file for other tools
    nx.write_graphml(g, 'g.graphml')

    file.close()


def generate_measures(measures_len):
    g: nx.DiGraph = nx.read_graphml('g.graphml')

    # Build a spot for multiple measures
    song_part = []

    for i in range(measures_len):
        # Holder for measures
        measure = []

        # start label is M1_4/4_V1_B0.0_NILS
        def randomPath(label):
            # Skip the NILS measure, it is the origin of the graph
            if(label != 'M1_4/4_V1_B0.0_NILS'):
                # look up the duration label and get a number
                dur = len_beats(g.nodes[label]['duration'])

                flat_dur = flatten_deep(array(dur, dtype=object).flat)

                # Add the node to the measure container
                measure.append(flat_dur)

            # Get the list of outgoing edges and their weights
            ssors = g.successors(label)

            # Container of available node choices
            labelChoices = []

            # Paired container of the random weights
            choiceWeights = []

            # Loop through each successor (inbound edge)
            for ss in ssors:
                # Get the weights for the selected successor
                nextWeight = g.edges[label, ss]['weight']

                # If the weight is -1, don't add the successor
                if nextWeight > -1:
                    # Add the node to the values array
                    labelChoices.append(ss)

                    # Add the weight to the choices weights
                    choiceWeights.append(float(nextWeight))

            # There has to be more than one choice to randomize
            if(len(labelChoices) > 1):
                arr = array(choiceWeights, dtype=float)

                # Normalize the -1 to 1 range to 0 to 1
                def NormalizeData(data):
                    return (data - min(data)) / (max(data) - min(data))

                # Normalize our weights to a range of [0, 1]
                normWeights = NormalizeData(arr)

                # Rescale the weights to sum to 1
                scaledWeights = normWeights / normWeights.sum()

                # Randomly select the next note based on their
                # normalized and scaled weights
                rr = random.choice(a=labelChoices, size=1,
                                   replace=False, p=scaledWeights)

                # Get the label of the first (of one) choice
                picked = str(rr[0])
                return randomPath(picked)

            elif (len(labelChoices) == 1):
                # ^ If there are no options, choose the only option

                # We want to stop endless loops here
                if(labelChoices[0] == 'M1_4/4_V1_B0.0_NILS'):
                    return

                # Recursively call the next choice in the list of edges
                return randomPath(labelChoices[0])
            else:
                # If there are no further nodes, we end here as well
                return

        # Kick off the navigation with the source node
        randomPath('M1_4/4_V1_B0.0_NILS')

        # Flatten the list because of triplets
        l = flatten_deep(array(measure, dtype=object).flat)

        # Do a beats conversion (1 whole note is 4 beats)
        multiplied = [element * 4 for element in l]

        measureTotal = sum([abs(element) for element in multiplied])

        # If the sum is less than 4, append a rest for the difference
        if(measureTotal < 4.0):
            multiplied.append((4.0 - measureTotal) * -1)

        song_part.append(multiplied)
    return song_part


def rebalance_graph(
    wn_weight=0.1, hn_weight=0.1, qn_weight=0.1, en_weight=0.1, sn_weight=0.1,
    wr_weight=0.1, hr_weight=0.1, qr_weight=0.1, er_weight=0.1, sr_weight=0.1,
    dhn_weight=0.1, dqn_weight=0.1, den_weight=0.1, dsn_weight=0.1,
    dhr_weight=0.1, dqr_weight=0.1, der_weight=0.1, dsr_weight=0.1,
    triplets=0.1
):
    g: nx.DiGraph = nx.read_graphml('g.graphml')
    for u, v, w in g.edges.data('weight'):
        dur = g.nodes[v]['duration']
        if dur == '1N':
            g.edges[u, v]['weight'] = wn_weight
        if dur == '1/2N':
            g.edges[u, v]['weight'] = hn_weight
        if dur == '1/4N':
            g.edges[u, v]['weight'] = qn_weight
        if dur == '1/8N':
            g.edges[u, v]['weight'] = en_weight
        if dur == '1/16N':
            g.edges[u, v]['weight'] = sn_weight
        if dur == '1R':
            g.edges[u, v]['weight'] = wr_weight
        if dur == '1/2R':
            g.edges[u, v]['weight'] = hr_weight
        if dur == '1/4R':
            g.edges[u, v]['weight'] = qr_weight
        if dur == '1/8R':
            g.edges[u, v]['weight'] = er_weight
        if dur == '1/16R':
            g.edges[u, v]['weight'] = sr_weight
        if dur == '1/2.N':
            g.edges[u, v]['weight'] = dhn_weight
        if dur == '1/4.N':
            g.edges[u, v]['weight'] = dqn_weight
        if dur == '1/8.N':
            g.edges[u, v]['weight'] = den_weight
        if dur == '1/16.N':
            g.edges[u, v]['weight'] = dsn_weight
        if dur == '1/2.R':
            g.edges[u, v]['weight'] = dhr_weight
        if dur == '1/4.R':
            g.edges[u, v]['weight'] = dqr_weight
        if dur == '1/8.R':
            g.edges[u, v]['weight'] = der_weight
        if dur == '1/16.R':
            g.edges[u, v]['weight'] = dsr_weight
        if dur != 0 and 'T' in dur:
            if 'R' in dur:
                g.edges[u, v]['weight'] = triplets
            else:
                g.edges[u, v]['weight'] = triplets + 0.001

    nx.write_graphml(g, 'g.graphml')


def len_beats(duration):
    if(duration == '1N'):
        return [1]
    if(duration == '1/2N'):
        return [(1/2)]
    if(duration == '1/2.N'):
        return [(1/2)+(1/4)]
    if(duration == '1/4N'):
        return [(1/4)]
    if(duration == '1/4TN'):
        return [(((1/4) * 2)/3)]
    if(duration == '1/4T+1/4TN'):
        return [(((1/4) * 2)/3), (((1/4) * 2)/3)]
    if(duration == '1/4.N'):
        return [(1/4)+(1/8)]
    if(duration == '1/8N'):
        return [(1/8)]
    if(duration == '1/8.N'):
        return [(1/8)+(1/16)]
    if(duration == '1/8TN'):
        return [((0.125 * 2)/3)]
    if(duration == '1/8T+1/8TN'):
        return [((0.125 * 2)/3), ((0.125 * 2)/3)]
    if(duration == '1/16N'):
        return [(1/16)]
    if(duration == '1/16.N'):
        return [(1/16)+(1/32)]
    if(duration == '1R'):
        return [-1]
    if(duration == '1/2R'):
        return [-(1/2)]
    if(duration == '1/2.R'):
        return [((1/2)+(1/4)) * -1]
    if(duration == '1/4R'):
        return [-(1/4)]
    if(duration == '1/4TR'):
        return [(((1/4)*2)/3) * -1]
    if(duration == '1/4T+1/4TR'):
        return [(((1/4)*2)/3) * -1, (((1/4)*2)/3) * -1]
    if(duration == '1/4.R'):
        return [((1/4)+(1/8) * -1)]
    if(duration == '1/8R'):
        return [-(1/8)]
    if(duration == '1/8.R'):
        return [(((1/8)+(1/16)) * -1)]
    if(duration == '1/8TR'):
        return [((((1/8) * 2)/3) * -1)]
    if(duration == '1/8T+1/8TR'):
        return [((((1/8) * 2)/3) * -1), ((((1/8) * 2)/3) * -1)]
    if(duration == '1/16R'):
        return [(1/16) * -1]
    if(duration == '1/16.R'):
        return [((1/16)+(1/32) * -1)]
    else:
        return [0]


if __name__ == '__main__':
    load_from_cytoscape()
    rebalance_graph(
        wn_weight=-1.0, hn_weight=-1.0, qn_weight=0.51, en_weight=-0.51, sn_weight=-0.91,
        wr_weight=-1.0, hr_weight=-1.0, qr_weight=0.52, er_weight=-0.52, sr_weight=-0.92,
        dhn_weight=-0.53, dqn_weight=0.253, den_weight=0.53, dsn_weight=-0.53,
        dhr_weight=-1.0, dqr_weight=-0.253, der_weight=0.754, dsr_weight=-0.754,
        triplets=-1.0
    )
    with open('s:\\dev\\measure_4.json', 'w') as outfile1:
        out4 = generate_measures(4)
        json.dump(out4, outfile1)
    with open('s:\\dev\\verse_4.json', 'w') as outfile1:
        out4 = generate_measures(4)
        json.dump(out4, outfile1)
    with open('s:\\dev\\chorus_4.json', 'w') as outfile1:
        out4 = generate_measures(4)
        json.dump(out4, outfile1)
    with open('s:\\dev\\preverse_4.json', 'w') as outfile1:
        out4 = generate_measures(4)
        json.dump(out4, outfile1)
    with open('s:\\dev\\prechorus_4.json', 'w') as outfile1:
        out4 = generate_measures(4)
        json.dump(out4, outfile1)

    with open('s:\\dev\\measure_8.json', 'w') as outfile1:
        out8 = generate_measures(8)
        json.dump(out8, outfile1)
    with open('s:\\dev\\verse_8.json', 'w') as outfile1:
        out8 = generate_measures(8)
        json.dump(out8, outfile1)
    with open('s:\\dev\\chorus_8.json', 'w') as outfile1:
        out8 = generate_measures(8)
        json.dump(out8, outfile1)
    with open('s:\\dev\\preverse_8.json', 'w') as outfile1:
        out8 = generate_measures(8)
        json.dump(out8, outfile1)
    with open('s:\\dev\\prechorus_8.json', 'w') as outfile1:
        out8 = generate_measures(8)
        json.dump(out8, outfile1)

    with open('s:\\dev\\measure_16.json', 'w') as outfile1:
        out16 = generate_measures(16)
        json.dump(out16, outfile1)
    with open('s:\\dev\\verse_16.json', 'w') as outfile2:
        out16 = generate_measures(16)
        json.dump(out16, outfile2)
    with open('s:\\dev\\chorus_16.json', 'w') as outfile2:
        out16 = generate_measures(16)
        json.dump(out16, outfile2)
    with open('s:\\dev\\preverse_16.json', 'w') as outfile2:
        out16 = generate_measures(16)
        json.dump(out16, outfile2)
    with open('s:\\dev\\prechorus_16.json', 'w') as outfile2:
        out16 = generate_measures(16)
        json.dump(out16, outfile2)

    with open('s:\\dev\\measure_32.json', 'w') as outfile1:
        out32 = generate_measures(32)
        json.dump(out32, outfile1)
    with open('s:\\dev\\verse_32.json', 'w') as outfile3:
        out64 = generate_measures(32)
        json.dump(out64, outfile3)
    with open('s:\\dev\\chorus_32.json', 'w') as outfile3:
        out64 = generate_measures(32)
        json.dump(out64, outfile3)
    with open('s:\\dev\\preverse_32.json', 'w') as outfile3:
        out64 = generate_measures(32)
        json.dump(out64, outfile3)
    with open('s:\\dev\\prechorus_32.json', 'w') as outfile3:
        out64 = generate_measures(32)
        json.dump(out64, outfile3)

    with open('s:\\dev\\measure_64.json', 'w') as outfile1:
        out64 = generate_measures(64)
        json.dump(out64, outfile1)
    with open('s:\\dev\\verse_64.json', 'w') as outfile4:
        out64 = generate_measures(64)
        json.dump(out64, outfile4)
    with open('s:\\dev\\chorus_64.json', 'w') as outfile4:
        out64 = generate_measures(64)
        json.dump(out64, outfile4)
    with open('s:\\dev\\preverse_64.json', 'w') as outfile4:
        out64 = generate_measures(64)
        json.dump(out64, outfile4)
    with open('s:\\dev\\prechorus_64.json', 'w') as outfile4:
        out64 = generate_measures(64)
        json.dump(out64, outfile4)
