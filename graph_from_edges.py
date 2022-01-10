import json
import edges as edges
from math import isnan
import networkx as nx
import re
from numpy import random, linalg, min, max, array, isnan

from song_library import SongPart


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


def load_graph():
    g: nx.DiGraph = nx.read_graphml('g.graphml')

    # Build a spot for multiple measures
    song_part = []

    for i in range(8):
        # Holder for measures
        measure = []

        # start label is M1_4/4_V1_B0.0_NILS
        def randomPath(label):
            # Skip the NILS measure, it is the origin of the graph
            if(label != 'M1_4/4_V1_B0.0_NILS'):
                # Add the node to the measure container
                measure.append(g.nodes[label]['duration'])

            # Get the list of outgoing edges and their weights
            ssors = g.successors(label)

            # Container of available node choices
            labelChoices = []

            # Paired container of the random weights
            choiceWeights = []

            # Loop through each successor (inbound edge)
            for ss in ssors:
                # Add the node to the values array
                labelChoices.append(ss)

                # Get the weights for the selected successor
                nextWeight = g.edges[label, ss]['weight']

                # Add the weight to the choices weights
                choiceWeights.append(nextWeight)

            # There has to be more than one choice to randomize
            if(len(labelChoices) > 1):
                arr = array(choiceWeights)

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

        song_part.append(measure)
    print(song_part)


if __name__ == '__main__':
    load_graph()
