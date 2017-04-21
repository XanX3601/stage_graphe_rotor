from copy import deepcopy
from random import randint
from collections import deque
from sys import stderr

voisins_sortants = {1: [4, 5, 2], 2: [3, 4, 5], 3: [1, 4, 5], 4: [1, 2, 3], 5: []}
voisins_entrants = {1: [3, 4], 2: [1, 4], 3: [2, 4], 4: [1, 2, 3], 5: [1, 2, 3]}
arcs = {0: (1, 4), 1: (4, 1), 2: (2, 4), 3: (4, 2), 4: (4, 3), 5: (3, 4), 6: (2, 3), 7: (3, 1), 8: (1, 2), 9: (3, 5), 10: (1, 5), 11: (2, 5)}

#voisins_sortants = {1: [], 2: [3, 1], 3: [2, 1]}
#voisins_entrants = {1: [2, 3], 2: [3], 3: [2]}
#arcs = {0: (2, 1), 1: (3, 1), 3: (2, 3), 4: (3, 2)}

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

    def recursivite(voisins_sortants, voisins_entrants, arcs, compteur):
        print 'APPEL RECURSIF NIVBAU :', compteur
        print
        print 'voisins_entrant', voisins_entrants
        print 'voisins_sortant', voisins_sortants
        print 'arcs', arcs
        print

        if len(voisins_sortants.keys()) == 1:
            return [[]]

        # choisir un arc
        idarc, arc = arcs.items()[0]
        print 'arc choisi :', idarc, arc
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
        st_sans_arc = []
        if peux_acceder(arc[0], s, vs1):
            st_sans_arc = recursivite(vs1, ve1, a1, compteur + 1)

        # Creer G2 en fusionnant arc
        ve2 = deepcopy(voisins_entrants)
        vs2 = deepcopy(voisins_sortants)
        a2 = deepcopy(arcs)
        for i in range(ve2[arc[1]].count(arc[0])):
            del a2[a2.keys()[a2.values().index((arc[0], arc[1]))]]
            vs2[arc[0]].remove(arc[1])
            ve2[arc[1]].remove(arc[0])
            if (arc[1], arc[0]) in a2.values():
                del a2[a2.keys()[a2.values().index((arc[1], arc[0]))]]
                vs2[arc[1]].remove(arc[0])
                ve2[arc[0]].remove(arc[1])
        for v in ve2[arc[0]]:
            vs2[v].remove(arc[0])
            #ve2[arc[0]].remove(v)
            vs2[v].append(arc[1])
            ve2[arc[1]].append(v)
            a2[a2.keys()[a2.values().index((v, arc[0]))]] = (v, arc[1])
        for v in vs2[arc[0]]:
            #vs2[arc[0]].remove(v)
            ve2[v].remove(arc[0])
            del a2[a2.keys()[a2.values().index((arc[0], v))]]

        del ve2[arc[0]]
        del vs2[arc[0]]
        print 'g2 voisins_entrant', ve2
        print 'g2 voisins_sortant', vs2
        print 'g2 arcs', a2
        print

        st_avec_arc = recursivite(vs2, ve2, a2, compteur + 1)
        for st in st_avec_arc:
            st.append(idarc)

        return st_sans_arc + st_avec_arc


    vs = deepcopy(voisins_sortants)
    ve = deepcopy(voisins_entrants)
    a = deepcopy(arcs)
    return recursivite(vs, ve, a, 0)

spanning_trees = list_spanning_tree(5)
for st in spanning_trees:
    vs = {}
    for id_arc in st:
        arc = arcs[id_arc]
        if arc[0] not in vs:
            vs[arc[0]] = []
        vs[arc[0]].append(arc[1])
    print()