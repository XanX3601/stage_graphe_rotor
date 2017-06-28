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
        DiGraph.__init__(self, data, pos, loops, format, weighted,
                         implementation, data_structure, vertex_labels, name,
                         multiedges, convert_empty_dict_labels_to_None,
                         sparse, immutable)

        self._rotor_ordering = rotor_ordering if rotor_ordering is not None \
            else {}

        for vertex in self.vertices():
            if vertex not in self._rotor_ordering:
                self._rotor_ordering[vertex] = deepcopy(
                    self.neighbors_out(vertex))

        if name is None:
            name = 'RotorGraph on {} vert'.format(self.order())
            if self.order() < 2:
                name += 'ex'
            else:
                name += 'ices'
            self.name(name)

    def rotor_ordering(self, vertex=None):
        """
        Return a vertex's rotor ordering

        If no vertex is given, return all rotor ordering

        INPUT:

        - ``vertex`` -- (default: None) a vertex

        OUTPUT:

        list representing the rotor ordering

        If no vertex is given: list containing all lists representing the
        rotor ordering

        EXAMPLE:

        ::

            sage: from sage.rotors.all import RotorGraph
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: R.rotor_ordering(1)
            [2, 3]

        ::

            sage: from sage.rotors.all import RotorGraph
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: [1,2]}, \
                        format='dict_of_lists')
            sage: R.rotor_ordering()
            [[2, 3], [1, 3], [1, 2]]

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3]}, format='dict_of_lists')
            sage: R.rotor_ordering(4)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (4) is not a vertex of the graph
        """
        if vertex is None:
            return deepcopy([self._rotor_ordering[k] for k in sorted(
                self._rotor_ordering)])
        elif not self.has_vertex(vertex):
            raise LookupError(
                "Vertex ({0}) is not a vertex of the graph".format(vertex))
        else:
            return deepcopy(self._rotor_ordering[vertex])

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
            sage: R1 = RotorGraph({1: [], 2: []}, format='dict_of_lists')
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
            sage: R1 = RotorGraph({1: [], 2: []}, format='dict_of_lists')
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
    def __init__(self, rotor_graph, config=None):
        r"""
        """
        self._rotor_graph = rotor_graph
        self._config = config if config is not None else {}
        for vertex in self._rotor_graph.vertices():
            if vertex not in self._config:
                if self.rotor_graph().rotor_ordering(vertex):
                    self._config[vertex] = 0
                else:
                    self._config[vertex] = -1

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
            -1
        """
        return self._config[vertex]

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
        if self._index(vertex) > -1:
            self._config[vertex] += rotation_count
            self._config[vertex] %= len(self.rotor_graph().rotor_ordering(vertex))
        else:
            raise RotationError('The vertex {} can not be rotated'.format(vertex))

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
            sage: RC.rotor_head(1)
            2
            sage: RC.rotor_head(2)
            1
            sage: RC.rotate_vertices([1, 2])
            sage: RC.rotor_head(1)
            3
            sage: RC.rotor_head(2)
            3

        An error can be raised if a vertex which can not be rotated is in the
        given iterable. At this moment, the vertices situated before the
        incorrect one will have been rotated

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotor_head(1)
            2
            sage: RC.rotor_head(2)
            1
            sage: RC.rotate_vertices([1, 3, 2])
            Traceback (most recent call last):
            ...
            RotationError: The vertex 3 can not be rotated
            sage: RC.rotor_head(1)
            3
            sage: RC.rotor_head(2)
            1

        The methods follow the same behaviour if one of the vertex is not
        part of the underlying rotor graph

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [2,3], 2: [1,3], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: RC.rotor_head(1)
            2
            sage: RC.rotor_head(2)
            1
            sage: RC.rotate_vertices([1, 4, 2])
            Traceback (most recent call last):
            ...
            LookupError: Vertex (4) is not a vertex of the underlying rotor
                graph
            sage: RC.rotor_head(1)
            3
            sage: RC.rotor_head(2)
            1
        """
        for vertex in vertices:
            self.rotate_vertex(vertex, rotation_count)

    def fire_vertex(self, vertex, rotor_chips, chips_amount=None,
                    in_place=True):
        r"""
        Fire a vertex

        Fire the given vertex according to the given rotor chips config.

        By default, fire all chips on the given vertex. If a chips amount is
        given, only the first ``chips_amount`` chips will be fire. If the
        number of chips on the vertex is less than the given chips amount,
        they will all be fire.

        By default, the fire is made in place. If not, return a new rotor
        config and a new rotor chips.

        No equality verification is made between the two underlying graph to
        increase performance. If self or rotor_chips do not contain the given
        vertex in its underlying graph, an error is raised.

        EXAMPLES:

        A small example

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1 : [2,3], 2: [], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 2})
            sage: RC.rotor_head(1)
            2
            sage: C.chips(1)
            2
            sage: RC.fire_vertex(1, C)
            sage: RC.rotor_head(1)
            2
            sage: C.chips(1)
            0
            sage: C.chips(2)
            1
            sage: C.chips(3)
            1

        The same example, changing the amount of chips to fire

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1 : [2,3], 2: [], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 2})
            sage: RC.rotor_head(1)
            2
            sage: C.chips(1)
            2
            sage: RC.fire_vertex(1, C, chips_amount=1)
            sage: RC.rotor_head(1)
            3
            sage: C.chips(1)
            1
            sage: C.chips(2)
            1

        The same example but the fire is not made in place

        ::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1 : [2,3], 2: [], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R)
            sage: C = RotorChips(R, {1: 2})
            sage: rc, c = RC.fire_vertex(1, C, in_place=False)
            sage: RC.rotor_head(1)
            2
            sage: rc.rotor_head(1)
            3
            sage: C.chips(1)
            2
            sage: c.chips(1)
            1

        If the rotor config and the rotor chips do not have the same
        underlying rotor graph and they do no share the given vertex

        ::

            sage: from sage.rotors.all import *
            sage: R1 = RotorGraph({1: [2,3], 2: [], 3: []}, \
                        format='dict_of_list')
            sage: R2 = RotorGraph({0: [2,3], 2: [], 3: []}, \
                        format='dict_of_lists')
            sage: RC = RotorConfig(R1)
            sage: C = RotorConfig(R2)
            sage: RC.fire_vertex(1, C)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (1) is not a vertex shared by the two
                underlying rotor graphs
        """
        if not in_place:
            rc, c = deepcopy(self), deepcopy(rotor_chips)
        else:
            rc, c = self, rotor_chips

        if not rc.rotor_graph().has_vertex(vertex) \
                or not c.rotor_graph().has_vertex(vertex):
            raise LookupError("Vertex ({0}) is not a vertex "
                              "shared by the two underlying rotor "
                              "graphs".format(vertex))

        nb_chips_to_fire = c[vertex] if chips_amount is None \
                                        or chips_amount > c[vertex] \
                                     else chips_amount

        rotor_ordering = rc.rotor_graph().rotor_ordering(vertex)

        c.add_chips(vertex, -1 * nb_chips_to_fire)

        if nb_chips_to_fire // len(rotor_ordering) > 0:
            for neighbor in rotor_ordering:
                c.add_chips(neighbor, nb_chips_to_fire // len(rotor_ordering))

        for _ in range(nb_chips_to_fire % len(rotor_ordering)):
            rc.rotate_vertex(vertex)
            c.add_chips(rc[vertex])

        if not in_place:
            return rc, c

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
            sage: RC2 = RotorConfig(R2, config={1:[1]})
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
            sage: RC2 = RotorConfig(R2, config={1:[1]})
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

        for vertex in self.rotor_graph().vertices():
            if vertex not in self._chips:
                self._chips[vertex] = 0

    def chips(self, vertex):
        r"""
        Return the amount of chips on a vertex

        INPUT:

        - ``vertex`` -- a vertex

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [], 2: []}, format='dict_of_lists')
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
        Add chips on a vertex

        INPUT:

        - ``vertex`` -- a vertex

        - ``chips_amount`` -- (default: 1) the number of chips to add

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.chips(1)
            0
            sage: C.add_chips(1)
            sage: C.chips(1)
            1
            sage: C.add_chips(1, 3)
            sage: C.chips(1)
            4
            sage: C.add_chips(1, -2)
            sage: C.chips(1)
            2

        TESTS::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: []}, format='dict_of_lists')
            sage: C = RotorChips(R)
            sage: C.chips(1)
            0
            sage: C.add_chips(1, -5)
            sage: C.chips(1)
            0
            sage: C.add_chips(2, 5)
            Traceback (most recent call last):
            ...
            LookupError: Vertex (2) is not a vertex of the underlying rotor
                graph
        """
        if not self.rotor_graph().has_vertex(vertex):
            self.__missing__(vertex)
        self._chips[vertex] += chips_amount
        if self.chips(vertex) < 0:
            self._chips[vertex] = 0

    def __getitem__(self, vertex):
        r"""
        Return the amount of chips on a vertex

        Do not call this method directly. That is, for ``C.__getitem__(v)``
        write ``G[v]``

        INPUT:

        - ``vertex`` -- a vertex

        EXAMPLES::

            sage: from sage.rotors.all import *
            sage: R = RotorGraph({1: [], 2: []}, format='dict_of_lists')
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


class RotationError(Exception):
    r"""
    Exception type class
    """
    pass
