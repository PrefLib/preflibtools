from os import path

from preflibtools.instances.preflibinstance.instance import PrefLibInstance


class WeightedDiGraph(object):
    """This class is used to represent weighted directed graphs.

    :ivar node_mapping: The dictionary representing the graph mapping each node to its neighbourhood (set of nodes
        to which it is connected). A node can be of any hashable type.
    :ivar weights: The dictionary mapping every node to its weight.
    """

    def __init__(self):
        self.node_mapping = dict()
        self.weights = dict()

    def neighbours(self, node):
        """Returns all the neighbours of a given node.

        :param node: The node whose neighbours we want to know.

        :return: The set of the neighbours of the node.
        :rtype: set
        """
        return self.node_mapping[node]

    def outgoing_edges(self, node):
        """Returns all the edges leaving a given node.

        :param node: The node whose edges we want to get.

        :return: The set of the tuples (node, neighbour, edgeWeight) representing (weighted) edges.
        :rtype: set of tuples
        """
        return {(node, n, self.weights[(node, n)]) for n in self.node_mapping[node]}

    def add_node(self, node):
        """Adds a node to the graph if the node does not already exist.

        :param node: The node to add.
        """
        if node not in self.node_mapping:
            self.node_mapping[node] = set()

    def add_edge(self, node1, node2, weight):
        """Adds an edge to the graph. If the nodes do not exist in the graph, those are also added.

        :param node1: The departure node of the edge.
        :param node2: The arrival node of the edge.
        :param weight: The weight of the edge.
        """
        self.add_node(node1)
        self.add_node(node2)
        self.node_mapping[node1].add(node2)
        self.weights[(node1, node2)] = weight

    def edges(self):
        """Returns the set of all the edges of the graph.

        :return: A set of tuples (node, neighbour, weight) representing (weighted) edges.
        :rtype: set of tuples
        """
        return {
            (n1, n2, self.weights[(n1, n2)])
            for n1 in self.node_mapping
            for n2 in self.node_mapping[n1]
        }

    def nodes(self):
        """Returns the set of all the nodes of the graph.

        :return: The set of all the nodes of the graph.
        :rtype: set
        """
        return self.node_mapping.keys()

    def __str__(self):
        """Returns the string used when printing the graph"""
        return "Graph with {} vertices and {} edges :\n".format(
            len(self.node_mapping), len(self.edges())
        )


class MatchingInstance(PrefLibInstance, WeightedDiGraph):
    """This is the class representing a PrefLib instance for matching preferences. It basically 
    contains the data and information written within a PrefLib file.

    """

    def __init__(self, file_path=""):
        PrefLibInstance.__init__(self)
        WeightedDiGraph.__init__(self)
        self.num_edges = 0
        self.file_path = file_path

        # If a filePath is given as argument, we parse it immediately
        if len(file_path) > 0:
            self.parse_file(file_path)

    def type_validator(self, data_type):
        return data_type == "wmd"

    def parse(self, lines, autocorrect=False, header_only=False):
        """Parses the strings, assuming that the latter describes a graph.

        :param lines: A list of string, each string being one line of the instance to parse.
        :type lines: list
        :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
        :type autocorrect: bool
        :param header_only: A boolean indicating whether we should stop after having read the header. Default is False.
        :type header_only: bool
        """
        # The first few lines contain the metadata
        i = 0
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("#"):
                if line.startswith("# NUMBER EDGES"):
                    self.num_edges = int(line[15:].strip())
                else:
                    self.parse_metadata(line, autocorrect=autocorrect)
            else:
                break
        self.num_voters = self.num_alternatives

        if header_only:
            return

        for line in lines[i:]:
            (vertex1, vertex2, weight) = line.strip().replace(" ", "").split(",")
            self.add_edge(int(vertex1), int(vertex2), float(weight))
        self.num_edges = sum(len(edge_set) for edge_set in self.node_mapping.values())

    def parse_old(self, lines, autocorrect=False):
        """Parses the strings, assuming that the latter describes a graph.

        :param lines: A list of string, each string being one line of the instance to parse.
        :type lines: list
        :param autocorrect: A boolean indicating whether we should try to automatically correct the potential errors
            in the file. Default is False.
        :type autocorrect: bool
        """

        self.num_alternatives = int(lines[0].strip().split(",")[0])
        self.num_voters = int(lines[0].strip().split(",")[1])
        for i in range(1, self.num_alternatives + 1):
            alt_name = lines[i].split(",")[1].strip()
            if autocorrect and alt_name in self.alternatives_name.values():
                tmp = 1
                while alt_name + "__" + str(tmp) in self.alternatives_name.values():
                    tmp += 1
                self.alternatives_name[i] = alt_name + "__" + str(tmp)
            else:
                self.alternatives_name[i] = alt_name

        # Skip the lines that describe the data
        graph_first_line = self.num_alternatives + 1
        for line in lines[graph_first_line:]:
            (vertex1, vertex2, weight) = line.strip().split(",")
            weight = float(weight)
            vertex1 = int(vertex1)
            vertex2 = int(vertex2)
            self.add_edge(vertex1, vertex2, weight)
        self.num_edges = sum(len(edge_set) for edge_set in self.node_mapping.values())

    def write(self, filepath):
        """Writes the instance into a file whose destination has been given as argument, assuming the instance
        represents a graph. If no file extension is provided the data type of the instance is used.

        Also sets `self.file_name` correctly (according to `filepath`), if `self.file_name` is empty.

        :param filepath: The destination where to write the instance.
        :type filepath: str
        """
        if len(path.splitext(filepath)[1]) == 0:
            filepath += "." + str(self.data_type)
        # set self.filename if it is undefined
        if not self.file_name:
            self.set_file_name(filepath)
        with open(filepath, "w", encoding="utf-8") as file:
            # Writing metadata in the file header
            self.write_metadata(file)
            file.write(
                "# NUMBER ALTERNATIVES: {}\n# NUMBER EDGES: {}\n".format(
                    self.num_alternatives,
                    self.num_edges,
                )
            )
            for alt, name in self.alternatives_name.items():
                file.write("# ALTERNATIVE NAME {}: {}\n".format(alt, name))

            # Writing the actual graph
            nodes = sorted(list(self.nodes()))
            for n in nodes:
                out_edges = sorted(list(self.outgoing_edges(n)), key=lambda x: x[1])
                for vertex1, vertex2, weight in out_edges:
                    file.write("{}, {}, {}\n".format(vertex1, vertex2, weight))

    def __str__(self):
        return "Matching-Instance: {} <{}, {}>".format(
            self.file_name, self.num_voters, self.num_alternatives
        )
