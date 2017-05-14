# TODO doc de la bibliotheque rotor
from sage.graphs.all import DiGraph


class RotorGraph(DiGraph):
    # TODO doc de la classe RotorGraph
    def __init__(self, data=None, pos=None, loops=None, format=None,
                 weighted=None, implementation='c_graph',
                 data_structure="sparse", vertex_labels=True, name=None,
                 multiedges=None, convert_empty_dict_labels_to_None=None,
                 sparse=True, immutable=False, rotor_orders=None):
        # TODO doc de la methode __init__
        DiGraph.__init__(self, data, pos, loops, format, weighted, implementation, data_structure, vertex_labels, name,
                         multiedges, convert_empty_dict_labels_to_None, sparse, immutable)
        self._rotor_orders = {}
        if rotor_orders:
            for vertex, rotor_order in rotor_orders.items():
                if self.has_vertex(vertex):
                    self._rotor_orders[vertex] = []
                    for neighbor in rotor_order:
                        if self.has_vertex(neighbor) and neighbor in self.neighbors_out(vertex):
                            self._rotor_orders[vertex].append(neighbor)
        for vertex in [v for v in self.vertices() if v not in self._rotor_orders]:
            self._rotor_orders[vertex] = self.neighbors_out(vertex)

    def default_config(self):
        return ChipsConfig()


class RotorConfig:
    # TODO doc de la classe RotorConfig
    def __init__(self, rotor_graph, rotor_indexes):
        # TODO doc de la methode __init__
        self._rotor_graph = rotor_graph
        self._rotor_indexes = rotor_indexes


class ChipsConfig:
    # TODO doc de la classe ChipsConfig
    def __init__(self, rotor_graph, chips):
        # TODO doc de la methode __init__
        self._rotor_graph = rotor_graph
        self._chips = {}
        if isinstance(chips, list):
            vertices = self._rotor_graph.vertices()
            for i in range(len(vertices)):
                if i < len(chips):
                    self._chips[vertices[i]] = chips[i]
                else:
                    self._chips[vertices[i]] = 0
        elif isinstance(chips, dict):
            for vertex, chipsCount in chips.items():
                self._chips[vertex] = chipsCount
            for vertex in [v for v in self._rotor_graph.vertices() if v not in self._chips]:
                self._chips[vertex] = 0
        else:
            for vertex in self._rotor_graph.vertices():
                self._chips[vertex] = 0

    def values(self):
        # TODO doc de la methode values
        return [self._chips[v] for v in self._rotor_graph.vertices()]

    def chips_count(self, vertex=None):
        # TODO doc de la methode chips_count
        if vertex != None:
            return self._chips[vertex]
        else:
            return sum(self.values())

    def add_chips_to_vertex(self, quantity, vertex):
        # TODO doc de la methode add_chips_to_vertex
        self._chips[vertex] += quantity

    def sub_chips_to_vertex(self, quantity, vertex):
        # TODO doc de la methode sub_chips_to_vertex
        self._chips[vertex] -= quantity

    def add_chips_to_vertices(self, quantity, vertices):
        # TODO doc de la methode add_chips_to_vertices
        for vertex in vertices:
            self._chips[vertex] += quantity

    def sub_chips_to_vertices(self, quantity, vertices):
        # TODO doc de la methode sub_chips_to_vertices
        for vertex in vertices:
            self._chips[vertex] += quantity

    def add_chips(self, chips):
        # TODO doc de la methode add_chips
        for vertex, quantity in chips.items():
            self._chips[vertex] += quantity

    def subb_chips(self, chips):
        # TODO doc de la methode sub_chips
        for vertex, quantity in chips.items():
            self._chips[vertex] -= quantity

    def __len__(self):
        # TODO doc de la methode __len__
        return self.chips_count()
