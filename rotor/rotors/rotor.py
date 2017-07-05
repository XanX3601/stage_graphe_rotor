r"""
Rotors Graph

Classes and methods for rotor graph

<Paragraph description>

AUTHORS:

- CHRETIEN Clement, PETITEAU Thomas (2017-07-07): initial version

EXAMPLES::

<Lots and lots of examples>
"""

from sage.graphs.all import DiGraph
from sage.structure.all import SageObject

from copy import deepcopy


class RotorGraph(DiGraph):
    r"""
    A Rotor Graph class
    """
    def __init__(self, data=None, pos=None, loops=None, format=None,
                 weighted=None, implementation='c_graph',
                 data_structure="sparse", vertex_labels=True, name=None,
                 multiedges=None, convert_empty_dict_labels_to_None=None,
                 sparse=True, immutable=False, rotor_ordering=None):
        r"""
        """
        # Call super __init__
        DiGraph.__init__(self, data, pos, loops, format, weighted,
                         implementation, data_structure, vertex_labels, name,
                         multiedges, convert_empty_dict_labels_to_None,
                         sparse, immutable)

        # init self._rotor_ordering
        self._rotor_ordering = {} if rotor_ordering is None else rotor_ordering

        # Verification of what the user gave in rotor_ordering
        for vertex in self._rotor_ordering:
            if not self.has_vertex(vertex):
                raise LookupError('Vertex ({}) is not a vertex '
                                  'of the graph'.format(vertex))
            ordering = self._rotor_ordering[vertex]
            neighbors_out = self.neighbors_out(vertex)
            if not all([n in neighbors_out for n in ordering]):
                raise ValueError('Invalid rotor ordering for vertex {}:'
                                 ' A rotor ordering can only contain '
                                 'neighbors out of the vertex'.format(vertex))

        # Put default value to vertices which do not have a rotor ordering
        for vertex in self.vertices():
            if vertex not in self._rotor_ordering:
                self._rotor_ordering[vertex] = self.neighbors_out(vertex)

        # Handle multi edges
        if self.has_multiple_edges():
            print 'Multiple edges have been deleted and replaced by an ' \
                  'unique edge. Rotor ordering may have been changed on some ' \
                  'vertices. Please ensure they correspond to what you expected'
            multiple_edges = self.multiple_edges(labels=False)
            for edge in set(multiple_edges):
                vertex, neighbor = edge
                ordering = self._rotor_ordering[vertex]
                if multiple_edges.count(edge) > ordering.count(neighbor):
                    for _ in range(multiple_edges.count(edge)-ordering.count(edge)-1):
                        self._rotor_ordering[vertex].append(neighbor)
            self.remove_multiple_edges()

        if name is None:
            name = 'RotorGraph on {} vert'.format(self.order())
            if self.order() < 2:
                name += 'ex'
            else:
                name += 'ices'
            self.name(name)

    def rotor_ordering(self, vertex=None):
        r"""
        Return a vertex's rotor ordering

        If no vertex is given, return all rotor ordering

        INPUT:

        - ``vertex`` -- (default: None) a vertex

        OUTPUT:

        list representing the rotor ordering

        If no vertex is given: list containing all lists representing the
        rotor ordering

        EXAMPLE:

        When a vertex is given

        ::

            sage: from sage.rotors.all import RotorGraph
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: R.rotor_ordering(1)
            [2, 3]
            sage: R.rotor_ordering(3)
            []

        When no vertex is given

        ::

            sage: from sage.rotors.all import RotorGraph
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: R.rotor_ordering()
            {1: [2, 3], 2: [1, 3], 3: []}

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: R.rotor_ordering(4)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (4) is not a vertex of the graph
        """
        if vertex is None:
            return {v: self.rotor_ordering(v) for v in self.vertices()}
        elif not self.has_vertex(vertex):
            raise LookupError(
                "Vertex ({0}) is not a vertex of the graph".format(vertex))
        else:
            return deepcopy(self._rotor_ordering[vertex])

    def sinks(self):
        r"""
        Override of the method sinks of from DiGraph class.

        In a rotor graph, a sink is a vertex having an empty rotor ordering

        OUTPUT:

        list containing all the sinks of the self

        EXAMPLES:

        An example using the default rotor ordering

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3]}, format='dict_of_lists')
            sage: R.sinks()
            [3]

        Another example without any sink

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2], 2: [3], 3: [1]}, \
                        format='dict_of_lists')
            sage: R.sinks()
            []

        A similar example where the rotor ordering are not the default ones

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2], 2: [3], 3: [1]}, \
                        format='dict_of_lists', rotor_ordering={3: []})
            sage: R.sinks()
            [3]
        """
        return [vertex for vertex in self.vertices()
                if not self.rotor_ordering(vertex)]

    def reverse(self):
        """
        Override for the method reverse od DiGraph class

        Returns a copy of rotor graph with edges reversed in direction and the
        rotor ordering reversed too.

        The reverse of the rotor ordering is made like so: if a vertex A has a
        vertex B in its rotor ordering then, once reversed, A will be in B's
        rotor ordering.

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: D = RotorGraph({ 0: [1,2,3], 1: [0,2], 2: [3], 3: [4], 4: [0,5], 5: [1] })
            sage: D.reverse()
            Reverse of (RotorGraph on 6 vertices): Rotor graph on 6 vertices
        """
        rotor_ordering = {}
        for vertex in self.vertices():
            if vertex not in rotor_ordering:
                rotor_ordering[vertex] = []
            for neighbor in self.rotor_ordering(vertex):
                if neighbor not in rotor_ordering:
                    rotor_ordering[neighbor] = []
                rotor_ordering[neighbor].append(vertex)

        H = RotorGraph(multiedges=self.allows_multiple_edges(),
                       loops=self.allows_loops())
        H.add_vertices(self)
        H.add_edges( [ (v,u,d) for (u,v,d) in self.edge_iterator() ] )
        H._rotor_ordering = rotor_ordering
        name = self.name()
        if name is None:
            name = ''
        H.name("Reverse of (%s)"%name)
        return H

    def _repr_(self):
        """
        Override the _repr_ function from GenericGraph class

        Return a string representation of self.

        EXAMPLES::

            sage: from sage.rotors.all import RotorGraph
            sage: R = RotorGraph({1: [2], 2: [1]}, format='dict_of_lists')
            sage: R._repr_()
            'RotorGraph on 2 vertices: Rotor graph on 2 vertices'
        """
        name = ""
        if self.allows_loops():
            name += "looped "
        if self.allows_multiple_edges():
            name += "multi-"
        name += "rotor graph on {} vert".format(self.order())
        if self.order() == 1:
            name += "ex"
        else:
            name += "ices"
        name = name.capitalize()
        if self.name() != '':
            name = self.name() + ": " + name
        return name

    def __eq__(self, other):
        r"""
        Compare self and other for equality

        Do not call this method directly. That is, for ``G.__eq__(H)``
        write ``G == H``

        Two rotor graphs are considered equal if following hold:
         - they respect the holds used to define equality beetween graphs
         - the rotor ordering is the same for every vertices

        INPUT:

        - ``other`` -- a rotor graph

        OUTPUT:

        True if self and other are equal, False otherwise

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R1 = RotorGraph({1: [2], 2: []}, format='dict_of_lists')
            sage: R2 = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: R1 == R2
            False
            sage: R1 = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: R2 = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: R1 == R2
            True
            sage: R1 = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists', rotor_ordering={1: [3,2]})
            sage: R1 == R2
            False

        .. SEEALSO::

            :meth:`sage.graph.DiGraph.__eq__`
        """
        return DiGraph.__eq__(self, other) and \
               self._rotor_ordering == other._rotor_ordering

    def __ne__(self, other):
        r"""
        Compare self and other for inequality

        Do not call this method directly. That is, for ``G.__ne__(H)``
        write ``G != H``

        Two rotor graph are consider inequal if they do not respect one of
        the following hold:
         - they respect the holds used to define equality beetween graphs
         - the rotor ordering is the same for every vertices

        INPUT:

        - ``other`` -- a rotor graph

        OUTPUT:

        True if self and other are not equal, False otherwise

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R1 = RotorGraph({1: [2], 2: []}, format='dict_of_lists')
            sage: R2 = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: R1 != R2
            True
            sage: R1 = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: R2 = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: R1 != R2
            False
            sage: R1 = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists', rotor_ordering={1: [3,2]})
            sage: R1 != R2
            True

        .. SEEALSO::

            :meth:`sage.graph.DiGraph.__ne__`
        """
        return not self == other


class RotorConfig(SageObject):
    r"""
    Configuration on rotor graph
    """
    def __init__(self, rotor_graph, config=None, format='rotor_head'):
        r"""
        """
        self._rotor_graph = rotor_graph
        self._config = {}

        # Check user's input according to format
        if config is not None:
            if format == 'rotor_head':
                for vertex in config:
                    if not self.rotor_graph().has_vertex(vertex):
                        self.__missing__(vertex)
                    rotor_ordering = self.rotor_graph().rotor_ordering(vertex)
                    if not rotor_ordering:
                        if config[vertex] is not None:
                            raise ValueError('Rotor ordering of vertex ({}) is '
                                             'empty, its rotor head can not be '
                                             'vertex ({})'.format(vertex,
                                                                  config[vertex]))
                        self._config[vertex] = None
                    elif rotor_ordering:
                        if config[vertex] is None:
                            raise ValueError('Rotor ordering of vertex ({}) is not'
                                             'empty, its rotor head can not be'
                                             'None'.format(vertex))
                        if config[vertex] not in rotor_ordering:
                            raise ValueError('Vertex ({}) is not in the rotor '
                                             'ordering of vertex '
                                             '({})'.format(config[vertex], vertex))
                        self._config[vertex] = rotor_ordering.index(config[vertex])
            elif format == 'rotor_index':
                for vertex in config:
                    if not self.rotor_graph().has_vertex(vertex):
                        self.__missing__(vertex)
                    rotor_ordering = self.rotor_graph().rotor_ordering(vertex)
                    if not rotor_ordering:
                        if config[vertex] is not None:
                            raise ValueError('Rotor ordering of vertex ({}) is '
                                             'empty, the index of its rotor head '
                                             'can not be {}'.format(vertex,
                                                                    config[vertex]))
                        self._config[vertex] = None
                    elif rotor_ordering:
                        try:
                            rotor_head = rotor_ordering[config[vertex]]
                            self._config[vertex] = config[vertex]
                        except IndexError as index_error:
                            raise IndexError('rotor head index of vertex ({}) out '
                                             'of range'.format(vertex))

        # Put default value for not given vertex
        for vertex in self.rotor_graph().vertices():
            if vertex not in self._config:
                rotor_ordering = self.rotor_graph().rotor_ordering(vertex)
                if not rotor_ordering:
                    self._config[vertex] = None
                else:
                    self._config[vertex] = 0

    def _index(self, vertex):
        r"""
        Return the rotor's head index in rotor ordering

        Return -1 if the given vertex do not have any neighbors out

        INPUT:

        - ``vertex`` - a vertex

        OUTPUT:

        rotor's head index in rotor ordering

        EXAMPLES:

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,2], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC._index(1)
            0
            sage: RC._index(3)
        """
        return self._config[vertex]

    def to_dictionary(self):
        r"""
        Return a dictionary representing the rotor configuration

        Return a dict object representing self. It associate at every vertex
        from the underlying rotor graph its rotor head.

        OUTPUT:

        a dictionary associating every vertex to its rotor head

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: 1}
        """
        return {vertex: self[vertex] for vertex in self._config}

    def rotor_graph(self):
        r"""
        Return the configuration's underlying rotor

        OUTPUT:

        RotorGraph

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotor_graph()
            RotorGraph on 3 vertices: Rotor graph on 3 vertices
        """
        return self._rotor_graph

    def rotor_head(self, vertex):
        r"""
        Return the rotor's head

        Return the rotor's head for which the given vertex is the end

        INPUT:

        - ``vertex`` -- a vertex

        OUTPUT:

        a vertex being the rotor's head

        None if the given vertex is not a rotor's end

        EXAMPLES:

        When the given vertex is pointing to a vertex

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotor_head(2)
            1
            sage: RC.rotor_head(1)

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotor_head(2)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        if not self.rotor_graph().has_vertex(vertex):
            self.__missing__(vertex)
        rotor_order = self.rotor_graph().rotor_ordering(vertex)
        return rotor_order[self._index(vertex)] if rotor_order else None

    def rotate_vertex(self, vertex, rotation_count=1):
        r"""
        Rotate the vertex

        Rotate the vertex for the specified amount of rotation

        INPUT:

        - ``vertex`` -- a vertex

        - ``rotation_count`` -- (default: 1) the amount of rotation to apply

        EXAMPLES:

        Rotating a vertex which can be rotated

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1:[2,3,4], 2: [], 3: [], 4:[]}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotor_head(1)
            2
            sage: RC.rotate_vertex(1)
            sage: RC.rotor_head(1)
            3
            sage: RC.rotate_vertex(1, 2)
            sage: RC.rotor_head(1)
            2

        Rotating a vertex which cannot be rotated

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1:[2,3,4], 2: [], 3: [], 4:[]}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotate_vertex(2)
            Traceback (most recent call last):
            ...
            RotationError: The vertex 2 can not be rotated

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotate_vertex(4)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (4) is not a vertex of the underlying rotor
                graph
        """
        if not self.rotor_graph().has_vertex(vertex):
            self.__missing__(vertex)
        if self.rotor_head(vertex) is not None:
            self._config[vertex] += rotation_count
            self._config[vertex] %= \
                len(self.rotor_graph().rotor_ordering(vertex))
        else:
            raise RotationError('The vertex {} can not be '
                                'rotated'.format(vertex))

    def rotate_vertices(self, vertices, rotation_count=1):
        r"""
        Rotate the vertices

        Rotate the vertices from the given iterable

        INPUT:

        - ``vertices`` -- iterable on vertices

        - ``rotation_count`` -- (default: 1) the amount of rotation to apply
        to each vertex

        EXAMPLES:

        If rotating only vertices which can be rotated

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: 1}
            sage: RC.rotate_vertices([1, 2])
            sage: RC.to_dictionary()
            {1: 3, 2: 3, 3: 1}

        An error can be raised if a vertex which can not be rotated is in the
        given iterable. At this moment, the vertices situated before the
        incorrect one will have been rotated

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: None}
            sage: RC.rotate_vertices([1, 3, 2])
            Traceback (most recent call last):
            ...
            RotationError: The vertex 3 can not be rotated
            sage: RC.to_dictionary()
            {1: 3, 2: 1, 3: None}

        The methods follow the same behaviour if one of the vertex is not
        part of the underlying rotor graph

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: None}
            sage: RC.rotate_vertices([1, 4, 2])
            Traceback (most recent call last):
            ...
            LookupError: Vertex (4) is not a vertex of the underlying rotor
                graph
            sage: RC.to_dictionary()
            {1: 3, 2: 1, 3: None}
        """
        for vertex in vertices:
            self.rotate_vertex(vertex, rotation_count)

    def fire_vertex(self, vertex, rotor_chips, chips_amount=None, in_place=True):
        r"""
        Fire a vertex

        Move all the chips placed on the vertex. The movement of a chips is made
        in two steps:
         1 - rotate the vertex
         2 - go on the new rotor head

        The order in which the chips are moved does not matter.

        Firing a sink have no effect.

        By default, all the chips placed on the vertex are moved. An amount of
        chips can be given in order to change this behaviour.

        By default, the operations if fire are made in place. If not, a new
        rotor config and a new rotor chips are returned.

        INPUT:

        - ``vertex`` -- a vertex

        - ``rotor_chips`` -- a rotor chips object giving the amount of chips on
        the vertices

        - ``chips_amount`` -- (default: None) The amount of chips to fire, all
        if let by default

        - ``in_place`` -- (default: True) boolean precising if the fire
        operation are to be made in place or not

        OUTPUT:

        None if made in place

        a rotor config object and a rotor chips object if not made in place

        EXAMPLES:

        A fire on a simple exemple made in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 2})
            sage: RC.to_dictionary()
            {1: 2, 2: None, 3: None}
            sage: C.to_dictionary()
            {1: 2, 2: 0, 3: 0}
            sage: RC.fire_vertex(1, C)
            sage: RC.to_dictionary()
            {1: 2, 2: None, 3: None}
            sage: C.to_dictionary()
            {1: 0, 2: 1, 3: 1}

        The same exemple firing obly one chips

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 2})
            sage: RC.to_dictionary()
            {1: 2, 2: None, 3: None}
            sage: C.to_dictionary()
            {1: 2, 2: 0, 3: 0}
            sage: RC.fire_vertex(1, C, 1)
            sage: RC.to_dictionary()
            {1: 3, 2: None, 3: None}
            sage: C.to_dictionary()
            {1: 1, 2: 0, 3: 1}

        The same exemple not made in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 2})
            sage: RC.to_dictionary()
            {1: 2, 2: None, 3: None}
            sage: C.to_dictionary()
            {1: 2, 2: 0, 3: 0}
            sage: rc, c = RC.fire_vertex(1, C, in_place=False)
            sage: rc.to_dictionary()
            {1: 2, 2: None, 3: None}
            sage: c.to_dictionary()
            {1: 0, 2: 1, 3: 1}

        .. WARNING::

            Be aware that, if not made in place, the rotor config and the rotor
            chips returned share the same rotor graph: the underlying rotor
            graph of self.
            If self and rotor chips do not share themselves the same rotor graph
            the results can be different from the ones expected if no error is
            raised.
        """
        if not in_place:
            rc = RotorConfig(self.rotor_graph(),
                             {v: self._index(v) for v in self._config},
                             format='rotor_index')
            c = RotorChips(self.rotor_graph(), {v: rotor_chips[v] for v in
                                                self.rotor_graph().vertices()})
        else:
            rc, c = self, rotor_chips

        if rc[vertex] is not None:
            nb_chips_to_move = c[vertex] if chips_amount is None else chips_amount
            rotor_ordering = rc.rotor_graph().rotor_ordering(vertex)

            c[vertex] -= nb_chips_to_move

            if nb_chips_to_move // len(rotor_ordering) > 0:
                for neighbor in rotor_ordering:
                    c[neighbor] += nb_chips_to_move // len(rotor_ordering)

            for i in range(nb_chips_to_move % len(rotor_ordering)):
                rc.rotate_vertex(vertex)
                c[rc[vertex]] += 1

            if not in_place:
                return rc, c

    def fire_vertices(self, vertices, rotor_chips, chips_amount=None, in_place=True):
        r"""
        Fire vertices

        Fire vertices from an iterable container

        Move all the chips placed on the vertices. The movement of a chips is
        made in two steps:
         1 - rotate the vertex
         2 - go on the new rotor head

        The order in which the chips are moved does not matter.

        Although, the order in which the vertices are given can change the
        result.

        By default, all the chips placed on the vertices are moved. If precised,
        only a certain amount of chips is moved on every vertices.

        By default, the operations if fire are made in place. If not, a new
        rotor config and a new rotor chips are returned.

        INPUT:

        - ``vertices`` -- an iterable container containing vertices

        - ``rotor_chips`` -- a rotor chips object giving the amount of chips on
        the vertices

        - ``chips_amount`` -- (default: None) The amount of chips to fire, all
        chips if let by default

        - ``in_place`` -- (default: True) boolean precising if the fire
        operation are to be made in place or not

        OUTPUT:

        None if made in place

        a rotor config object and a rotor chips object if not made in place

        EXAMPLES:

        A simple example made in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1:2, 2: 2})
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: None}
            sage: C.to_dictionary()
            {1: 2, 2: 2, 3: 0}
            sage: RC.fire_vertices([1,2], C)
            sage: RC.to_dictionary()
            {1: 2, 2: 3, 3: None}
            sage: C.to_dictionary()
            {1: 1, 2: 0, 3: 3}

        The same exemple with a precise amount of chips to fire on each vertex

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1:2, 2: 2})
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: None}
            sage: C.to_dictionary()
            {1: 2, 2: 2, 3: 0}
            sage: RC.fire_vertices([1,2], C, 2)
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: None}
            sage: C.to_dictionary()
            {1: 1, 2: 1, 3: 2}

        The same example not made in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1:2, 2: 2})
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: None}
            sage: C.to_dictionary()
            {1: 2, 2: 2, 3: 0}
            sage: rc, c = RC.fire_vertices([1,2], C, in_place=False)
            sage: rc.to_dictionary()
            {1: 2, 2: 3, 3: None}
            sage: c.to_dictionary()
            {1: 1, 2: 0, 3: 3}
        """
        if not in_place:
            rc = RotorConfig(self.rotor_graph(),
                             {v: self._index(v) for v in self._config},
                             format='rotor_index')
            c = RotorChips(self.rotor_graph(), {v: rotor_chips[v] for v in
                                                self.rotor_graph().vertices()})
        else:
            rc, c = self, rotor_chips

        for vertex in vertices:
            rc.fire_vertex(vertex, c, chips_amount)

        if not in_place:
            return rc, c

    def stabilize(self, rotor_chips, in_place=True):
        r"""
        Stabilize the rotor configuration and the chips configuration

        Fire all the chips until the stabilization state is reached.

        A stabilize state only exists if the underlying rotor graph contains at
        least one sink and if, in the reversed rotor graph, a path from a sink
        to a vertex V exists from every vertex. Theses paths only takes in
        count of the rotor ordering and not the neighbors.

        By default, the stabilization is made in place. If not, a new rotor
        config and a new rotor chips are returned

        INPUT:

        - ``rotor_chips`` -- the rotor chips object to stabilize with self

        - ``in_place`` -- (default: True) boolean precising if the stabilization
        operation are to be made in place or not

        OUTPUT:

        None if made in place

        a rotor config object and a rotor chips object if not made in place

        EXAMPLES:

        A simple example made in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3]}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 2, 2: 2})
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: None}
            sage: C.to_dictionary()
            {1: 2, 2: 2, 3: 0}
            sage: RC.stabilize(C)
            sage: RC.to_dictionary()
            {1: 3, 2: 3, 3: None}
            sage: C.to_dictionary()
            {1: 0, 2: 0, 3: 4}

        The same example not made in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3]}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 2, 2: 2})
            sage: RC.to_dictionary()
            {1: 2, 2: 1, 3: None}
            sage: C.to_dictionary()
            {1: 2, 2: 2, 3: 0}
            sage: rc, c = RC.stabilize(C, in_place=False)
            sage: rc.to_dictionary()
            {1: 3, 2: 3, 3: None}
            sage: c.to_dictionary()
            {1: 0, 2: 0, 3: 4}

        If the rotor graph has no sink, an error is raised

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2], 2: [3], 3: [1]}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 1})
            sage: RC.stabilize(C)
            Traceback (most recent call last):
            ...
            LookupError: Underlying rotor graph has no sink

        A similar error is raised if at least one vertex is not accessible by a
        sink in the reversed rotor graph.

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2], 2: [1, 3], 3: [4]}, \
                        format='dict_of_lists', rotor_ordering={2: [1]})
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 1})
            sage: RC.stabilize(C)
            Traceback (most recent call last):
            ...
            ValueError: All vertex can not access to a sink
        """
        # TODO change reverse
        from collections import deque

        if not self.rotor_graph().sinks():
            raise LookupError('Underlying rotor graph has no sink')

        reverse_rotor_graph = self.rotor_graph().reverse()

        accessible_vertex_from_sink = set()
        for sink in self.rotor_graph().sinks():
            depth_search = reverse_rotor_graph.depth_first_search(sink, neighbors=lambda vertex: reverse_rotor_graph.rotor_ordering(vertex))
            accessible_vertex_from_sink |= set(depth_search)

        if accessible_vertex_from_sink != set(self.rotor_graph().vertices()):
            raise ValueError('All vertex can not access to a sink')

        if not in_place:
            rc = RotorConfig(self.rotor_graph(),
                             {v: self._index(v) for v in self._config},
                             format='rotor_index')
            c = RotorChips(self.rotor_graph(), {v: rotor_chips[v] for v in
                                                self.rotor_graph().vertices()})
        else:
            rc, c = self, rotor_chips

        fifo = deque([vertex for vertex in rc.rotor_graph().vertices()
                      if c[vertex]>0])

        while fifo:
            current_vertex = fifo.pop()
            rc.fire_vertex(current_vertex, c)
            for neighbor in rc.rotor_graph().rotor_ordering(current_vertex):
                if c[neighbor] > 0:
                    fifo.appendleft(neighbor)

        if not in_place:
            return rc, c

    def show(self):
        r"""
        Show the rotor configuration

        Call the plot object from underlying graph and highlight in red all the
        edges that link a vertex to the associated rotor head
        """
        self.rotor_graph().plot(edge_colors={'red':[(v, self[v]) for v in self._config if self[v] is not None]}).show()

    def __getitem__(self, vertex):
        r"""
        Return the rotor's head

        Do not call this method directly. That is, for ``R.__getitem__(v)``
        write ``R[v]``

        Return the rotor's head for which the given vertex is the end

        INPUT:

        - ``vertex`` -- a vertex

        OUTPUT:

        a vertex being the rotor's head

        None if the given vertex is not a rotor's end

        EXAMPLES:

        When the given vertex is pointing to a vertex

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC[2]
            1
            sage: RC[1]

        .. SEEALSO::

            :meth:`sage.rotors.RotorConfig.rotor_head`

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC[2]
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        return self.rotor_head(vertex)

    def __setitem__(self, vertex, rotor_head):
        """
        Set the rotor's head

        Do not call this method directly. That is, for ``R.__setitem__(v, x)``
        write ``R[v] = x``

        Change the rotor head to the first value's instance in the rotor
        ordering list from the given vertex

        INPUT:

        - ``vertex`` -- a vertex

        - ``rotor_head`` -- a vertex in the given vertex's ordering list

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotor_head(1)
            2
            sage: RC[1] = 3
            sage: RC[1]
            3

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC[2] = 5
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        if not self.rotor_graph().has_vertex(vertex):
            self.__missing__(vertex)
        self._config[vertex] = self.rotor_graph().rotor_ordering(
            vertex).index(rotor_head)

    def __missing__(self, vertex):
        r"""
        Provide default value for non existing vertex

        Do not call this method directly. That is, for ``R.__missing__(v)``
        write ``R[v]``

        Raises a LookupError stating the given vertex do not belong to the
        underlying rotor graph

        INPUT:

        - ``vertex`` -- a vertex which is not in the underlying rotor graph

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC[2]
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        raise LookupError("Vertex ({0}) is not a vertex of the "
                          "underlying rotor graph".format(vertex))

    def __eq__(self, other):
        r"""
        Compare self and other for equality

        Do not call this method directly. That is, for ``G.__eq__(H)``
        write ``G == H``

        Two rotor configurations are considered equal if following hold:
         - the underlying rotor graphs are both equal
         - every rotors are in the same position

        INPUT:

        - ``other`` -- a rotor configuration

        OUTPUT:

        True if self and other are equal, False otherwise

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R1 = RotorGraph({1: [2, 3], 2: [1], 3: []}, \
                        format='dict_of_lists')
            sage: R2 = RotorGraph({1: []}, format='dict_of_lists')
            sage: RC1 = RotorConfig(R1)
            sage: RC2 = RotorConfig(R2)
            sage: RC1 == RC2
            False
            sage: R2 = RotorGraph({1: [2, 3], 2: [1], 3: []}, \
                        format='dict_of_lists')
            sage: RC2 = RotorConfig(R2, config={1:3})
            sage: RC1 == RC2
            False
            sage: RC2 = RotorConfig(R2)
            sage: RC1 == RC2
            True

        .. SEEALSO::

            :meth:`sage.rotors.RotorGraph.__ne__`
        """
        if not isinstance(other, RotorConfig):
            return False
        return self.rotor_graph() == other.rotor_graph() and \
               self._config == other._config

    def __ne__(self, other):
        r"""
        Compare self and other for inequality

        Do not call this method directly. That is, for ``G.__ne__(H)``
        write ``G != H``

        Two rotor configurations are considered non equal if they do not
        respect one of the following hold:
         - the underlying rotor graphs are both equal
         - every rotors are in the same position

        INPUT:

        - ``other`` -- a rotor configuration

        OUTPUT:

        True if self and other are not equal, False otherwise

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R1 = RotorGraph({1: [2, 3], 2: [1], 3: []}, \
                        format='dict_of_lists')
            sage: R2 = RotorGraph({1: []}, format='dict_of_lists')
            sage: RC1 = RotorConfig(R1)
            sage: RC2 = RotorConfig(R2)
            sage: RC1 != RC2
            True
            sage: R2 = RotorGraph({1: [2, 3], 2: [1], 3: []}, \
                        format='dict_of_lists')
            sage: RC2 = RotorConfig(R2, config={1:3})
            sage: RC1 != RC2
            True
            sage: RC2 = RotorConfig(R2)
            sage: RC1 != RC2
            False

        .. SEEALSO::

            :meth:`sage.rotors.RotorGraph.__ne__`
        """
        return not self == other


class RotorChips(SageObject):
    r"""
    A configuration of chips on a rotor graph
    """
    def __init__(self, rotor_graph, chips=None):
        r"""
        """
        self._rotor_graph = rotor_graph

        self._chips = {} if chips is None else chips

        # check user's input
        for vertex in self._chips:
            if not self.rotor_graph().has_vertex(vertex):
                self.__missing__(vertex)
            elif self._chips[vertex] < 0:
                raise ValueError('Invalid chips amount ({}) for vertex ({}): '
                                 'chips amount can\'t be '
                                 'negative'.format(self._chips[vertex], vertex))

        # Set defaut value
        for vertex in self.rotor_graph().vertices():
            if vertex not in self._chips:
                self._chips[vertex] = 0

    def to_dictionary(self):
        r"""
        Return a dictionary representing the chips configuration

        Return a dict object representing the chips configuration. It associated
        to every vertex from the underlying rotor graph the number of chip on it

        OUTPUT:

        a dictionary associating the number of chips on a vertex to every vertex

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                    format='dict_of_lists')
            sage: C = RotorChips(R, {1: 1, 2: 3})
            sage: C.to_dictionary()
            {1: 1, 2: 3, 3: 0}
        """
        return {vertex: self[vertex] for vertex in self._chips}

    def chips(self, vertex):
        r"""
        Return the amount of chips on a vertex

        INPUT:

        - ``vertex`` -- a vertex

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2], 2: []}, format='dict_of_lists')
            sage: C = RotorChips(R, {1: 2})
            sage: C.chips(1)
            2

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.chips(2)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        if not self.rotor_graph().has_vertex(vertex):
            self.__missing__(vertex)
        return self._chips[vertex]

    def add_chips(self, vertex, chips_amount=1):
        r"""
        Add chips to a vertex

        Add a amount of chips on a vertex

        INPUT:

        - ``vertex`` -- a vertex

        - ``chips_amount`` -- (default: 1) the amount of chips to add

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.chips(1)
            0
            sage: C.add_chips(1)
            sage: C.chips(1)
            1
            sage: C.add_chips(1, 5)
            sage: C.chips(1)
            6

        TESTS:

        Tests if given vertex is not a vertex of the underlying rotor graph

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.add_chips(4)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (4) is not a vertex of the underlying rotor
                graph

        Test if the amount of chips could become negative

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.add_chips(1, -2)
            Traceback (most recent call last):
            ...
            ValueError: Amount of chips of vertex (1) can not be negative
        """
        if not self.rotor_graph().has_vertex(vertex):
            self.__missing__(vertex)
        elif self[vertex] + chips_amount < 0:
            raise ValueError('Amount of chips of vertex ({}) can not '
                             'be negative'.format(vertex))
        self._chips[vertex] += chips_amount

    def sub_chips(self, vertex, chips_amount=1):
        r"""
        Subtract chips to a vertex

        subtract a amount of chips on a vertex

        INPUT:

        - ``vertex`` -- a vertex

        - ``chips_amount`` -- (default: 1) the amount of chips to subtract

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: C = RotorChips(R, {1: 5})
            sage: C.chips(1)
            5
            sage: C.sub_chips(1)
            sage: C.chips(1)
            4
            sage: C.sub_chips(1, 3)
            sage: C.chips(1)
            1

        TESTS:

        Tests if given vertex is not a vertex of the underlying rotor graph

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.sub_chips(4)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (4) is not a vertex of the underlying rotor
                graph

        Test if the amount of chips could become negative

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.sub_chips(1)
            Traceback (most recent call last):
            ...
            ValueError: Amount of chips of vertex (1) can not be negative
        """
        if not self.rotor_graph().has_vertex(vertex):
            self.__missing__(vertex)
        elif self[vertex] - chips_amount < 0:
            raise ValueError('Amount of chips of vertex ({}) can not '
                             'be negative'.format(vertex))
        self._chips[vertex] -= chips_amount

    def rotor_graph(self):
        r"""
        Return the chips's underlying rotor

        OUTPUT:

        RotorGraph

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.rotor_graph()
            RotorGraph on 3 vertices: Rotor graph on 3 vertices
        """
        return self._rotor_graph

    def __getitem__(self, vertex):
        r"""
        Return the amount of chips on a vertex

        Do not call this method directly. That is, for ``C.__getitem__(v)``
        write ``G[v]``

        INPUT:

        - ``vertex`` -- a vertex

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2], 2: []}, format='dict_of_lists')
            sage: C = RotorChips(R, {1: 2})
            sage: C[1]
            2

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C[2]
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        return self.chips(vertex)

    def __setitem__(self, vertex, chips_amount):
        r"""
        Set the amount of chips on a vertex

        Do not call this method directly. That is, for ``C.__setitem__(v, a)``
        write ``C[v] = a``

        INPUT:

        - ``vertex`` -- a vertex

        - ``chips_amount`` -- the amount of chips

        EXAMPLES:

        Changing the amount of chips on a vertex

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C[1]
            0
            sage: C[1] = 3
            sage: C[1]
            3

        Raise an error if the amount given is negative

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C[1] = -5
            Traceback (most recent call last):
            ...
            ValueError: An amount of chips can not be negative

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C[2] = 2
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        if not self.rotor_graph().has_vertex(vertex):
            self.__missing__(vertex)
        if chips_amount < 0:
            raise ValueError('An amount of chips can not be negative')
        self._chips[vertex] = chips_amount

    def __missing__(self, vertex):
        r"""
        Provide default value for non existing vertex

        Do not call this method directly. That is, for ``C.__missing__(v)``
        write ``C[v]``

        Raises a LookupError stating the given vertex do not belong to the
        underlying rotor graph

        INPUT:

        - ``vertex`` -- a vertex which is not in the underlying rotor graph

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C[2]
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        raise LookupError("Vertex ({0}) is not a vertex of the "
                          "underlying rotor graph".format(vertex))

    def __add__(self, other):
        r"""
        Addition for rotor chips

        Do not call this method directly. That is, for ``C.__add__(other)``
        write ``C + other``

        A rotor chips can be add to an integer or to another rotor chips.

        Adding two rotor chips results in a new rotor chips having self's
        underlying rotor graph as rotor graph and the amounts of chips of self
        plus the ones of other placed on vertices

        Adding a rotor chips and an integer is the same as adding an amount of
        chips equal to the integer to every vertices of the rotor chips

        INPUT:

        - ``other`` -- a rotor chips object or an integer

        OUPUT:

        A new rotor chips

        EXAMPLES:

        Adding a rotor chips to another one

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2]}, format='dict_of_lists')
            sage: C1 = RotorChips(R, {1: 2})
            sage: C2 = RotorChips(R, {1: 1, 2: 1})
            sage: C3 = C1 + C2
            sage: C3.to_dictionary()
            {1: 3, 2: 1}

        Adding an integer to a rotor chips

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2]}, format='dict_of_lists')
            sage: C1 = RotorChips(R)
            sage: C2 = C1 + 5
            sage: C2.to_dictionary()
            {1: 5, 2: 5}
        """
        from sage.rings.integer import Integer

        if isinstance(other, RotorChips):
            return RotorChips(self.rotor_graph(),
                              {v: self[v]+other[v]
                               for v in self.rotor_graph().vertices()})
        elif isinstance(other, int) or isinstance(other, Integer):
            return RotorChips(self.rotor_graph(),
                              {v: self[v]+other
                               for v in self.rotor_graph().vertices()})
        raise TypeError('unsupported operand type(s) for +: \'RotorChips\' and '
                        '\'{}\''.format(type(other)))

    def __radd__(self, other):
        r"""
        Right addition for rotor chips

        Do not call this method directly. That is, for ``C.__radd__(other)``
        write ``other + C``

        Return the result of self + other.

        This method is only called if python can not performed ``other + C``
        by using ``other.__add__(C)`` or if other do not have such a method.

        INPUT:

        - ``other`` -- a rotor chips object or an integer

        OUPUT:

        A new rotor chips

        .. SEEALSO::

            :meth: `sage.rotor.RotorChips.__add__`
        """
        return self + other

    def __iadd__(self, other):
        r"""
        In place addition for rotor chips

        Do not call this method directly. That is, for ``C.__iadd__(other)``
        write ``C += other``

        An integer or another rotor chips can be added to a rotor chips.

        Add an integer to a rotor chips is the same as adding an amount of chips
        equal to the integer on all the vertex of the rotor chips

        Add another rotor chips to a rotor chips is the same as adding to every
        vertex of self, the amount of chips on other's corresponding vertex

        INPUT:

        - ``other`` -- a rotor chips object or an integer

        OUPUT:

        A new rotor chips

        EXAMPLES:

        Adding a rotor chips to another one in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2]}, format='dict_of_lists')
            sage: C1 = RotorChips(R)
            sage: C2 = RotorChips(R, {1: 2, 2: 2})
            sage: C1 += C2
            sage: C1.to_dictionary()
            {1: 2, 2: 2}

        Adding an integer to a rotor chips in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2]}, format='dict_of_lists')
            sage: C1 = RotorChips(R)
            sage: C1 += 2
            sage: C1.to_dictionary()
            {1: 2, 2: 2}
        """
        from sage.rings.integer import Integer
        if isinstance(other, RotorChips):
            for vertex in self.rotor_graph().vertices():
                self[vertex] += other[vertex]
            return self
        elif isinstance(other, int) or isinstance(other, Integer):
            for vertex in self.rotor_graph().vertices():
                self[vertex] += other
            return self
        raise TypeError('unsupported operand type(s) for +: \'RotorChips\' and '
                        '\'{}\''.format(type(other)))

    def __sub__(self, other):
        r"""
        Substraction for rotor chips

        Do not call this method directly. That is, for ``C.__sub__(other)``
        write ``C - other``

        An integer or a rotor chips can be subtracted to a rotor chips.

        Subtracting a rotor chips to another results in a new rotor chips having
        self's underlying rotor graph as rotor graph and the amounts of chips of
         self minus the ones of other placed on vertices.

        Subtracting an integer chips and an integer is the same as substracting
        an amount of chips equal to the integer to every vertices of the rotor
        chips.

        INPUT:

        - ``other`` -- a rotor chips object or an integer

        OUPUT:

        A new rotor chips

        EXAMPLES:

        Subtracting a rotor chips to another one

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2]}, format='dict_of_lists')
            sage: C1 = RotorChips(R, {1: 2, 2: 1})
            sage: C2 = RotorChips(R, {1: 1, 2: 1})
            sage: C3 = C1 - C2
            sage: C3.to_dictionary()
            {1: 1, 2: 0}

        Adding an integer to a rotor chips

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2]}, format='dict_of_lists')
            sage: C1 = RotorChips(R, {1: 5, 2: 5})
            sage: C2 = C1 - 2
            sage: C2.to_dictionary()
            {1: 3, 2: 3}
        """
        from sage.rings.integer import Integer

        if isinstance(other, RotorChips):
            return RotorChips(self.rotor_graph(),
                              {v: self[v]-other[v]
                               for v in self.rotor_graph().vertices()})
        elif isinstance(other, int) or isinstance(other, Integer):
            return RotorChips(self.rotor_graph(),
                              {v: self[v]-other
                               for v in self.rotor_graph().vertices()})
        raise TypeError('unsupported operand type(s) for -: \'RotorChips\' and '
                        '\'{}\''.format(type(other)))

    def __rsub__(self, other):
        r"""
        Right subtraction for rotor chips

        Do not call this method directly. That is, for ``C.__rsub__(other)``
        write ``other - C``

        Return the result of self - other

        This method is only called if python can not performed ``other - C``
        by using ``other.__sub__(C)`` or if other do not have such a method.

        .. SEEALSO::

            :meth: `sage.rotor.RotorChips.__sub__`
        """
        return self - other

    def __isub__(self, other):
        r"""
        In place sbtraction for rotor chips

        Do not call this method directly. That is, for ``C.__isunb__(other)``
        write ``C -= other``

        An integer or another rotor chips can be subtracted to a rotor chips.

        Subtract an integer to a rotor chips is the same as subtracting an
        amount of chips equal to the integer on all the vertex of the rotor
        chips.

        Subtract another rotor chips to a rotor chips is the same as subtracting
        to every vertex of self, the amount of chips on other's corresponding
        vertex.

        INPUT:

        - ``other`` -- a rotor chips object or an integer

        OUPUT:

        A new rotor chips

        EXAMPLES:

        Subtracting a rotor chips to another one in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2]}, format='dict_of_lists')
            sage: C1 = RotorChips(R, {1: 5, 2: 5})
            sage: C2 = RotorChips(R, {1: 2, 2: 2})
            sage: C1 -= C2
            sage: C1.to_dictionary()
            {1: 3, 2: 3}

        Adding an integer to a rotor chips in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2]}, format='dict_of_lists')
            sage: C1 = RotorChips(R, {1: 4, 2: 4})
            sage: C1 -= 2
            sage: C1.to_dictionary()
            {1: 2, 2: 2}
        """
        from sage.rings.integer import Integer

        if isinstance(other, RotorChips):
            for vertex in self.rotor_graph().vertices():
                self[vertex] -= other[vertex]
            return self
        elif isinstance(other, int) or isinstance(other, Integer):
            for vertex in self.rotor_graph().vertices():
                self[vertex] -= other
            return self
        raise TypeError('unsupported operand type(s) for -: \'RotorChips\' and '
                        '\'{}\''.format(type(other)))


class RotationError(Exception):
    r"""
    Exception type class
    """
    pass
