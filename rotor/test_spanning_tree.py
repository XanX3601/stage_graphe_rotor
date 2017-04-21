from copy import deepcopy
from random import randint
from collections import deque

voisins_sortants = {1: [], 2: [1, 3], 3: [1, 2]}
voisins_entrants = {1: [2, 3], 2: [3], 3: [2]}
arcs = {0: (2, 1), 1: (2, 3), 2: (3, 2), 3: (3, 1)}

def peux_acceder(s1, s2):
    filo = deque()
    filo.append(s1)
    deja_vue = [s1]

    while filo:
        courant = filo.pop()
        for v in voisins_sortants[courant]:
            if v not in deja_vue:
                if v == s2:
                    return True
                deja_vue.append(v)
                filo.append(v)


def list_spanning_tree(s):
    def peux_acceder(s1, s2, vs):
        filo = deque()
        filo.append(s1)
        deja_vue = [s1]

        while filo:
            courant = filo.pop()
            for v in vs[courant]:
                if v not in deja_vue:
                    if v == s2:
                        return True
                    deja_vue.append(v)
                    filo.append(v)
        return False

    def recursivite(voisins_sortants, voisins_entrants, arcs):
        print 'voisins_entrant', voisins_entrants
        print 'voisins_sortant', voisins_sortants
        print 'arcs', arcs
        print
        # choisir un arc
        idarc, arc = arcs.items()[randint(0, len(arcs)-1)]
        print idarc, arc
        print

        # Creer G1 en enlevant arc
        ve1 = deepcopy(voisins_entrants)
        vs1 = deepcopy(voisins_sortants)
        a1 = deepcopy(arcs)
        del a1[idarc]
        ve1[arc[1]].remove(arc[0])
        vs1[arc[0]].remove(arc[1])
        print 'g1 voisins_entrant', ve1
        print 'g1 voisins_sortant', vs1
        print 'g1 arcs', a1
        print
        # appel recursif sur G1
        st_sans_arc = [[]]
        if peux_acceder(arc[0], s, vs1):
            pass
            #st_sans_arc = recursivite(vs1, ve1, a1)

        # Creer G2 en fusionnant arc
        ve2 = deepcopy(voisins_entrants)
        vs2 = deepcopy(voisins_sortants)
        a2 = deepcopy(arcs)
        for v in ve2[arc[0]]:
            if not v == arc[1]:
                ve2[arc[1]].append(v)
                a2[a2.keys()[a2.values().index((v, arc[0]))]] = (v, arc[1])
            else:
                del a2[a2.keys()[a2.values().index((arc[1], arc[0]))]]
        print 'g2 voisins_entrant', ve2
        print 'g2 voisins_sortant', vs2
        print 'g2 arcs', a2
        print







    vs = deepcopy(voisins_sortants)
    ve = deepcopy(voisins_entrants)
    a = deepcopy(arcs)
    return recursivite(vs, ve, a)

list_spanning_tree(1)