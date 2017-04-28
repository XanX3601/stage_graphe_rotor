from collections import deque

voisins_sortants = {1: [5, 4, 2], 2: [4, 3, 5], 3: [1, 4, 5], 4: [1, 2, 3], 5:[]}

def list_spanning_trees(voisins_sortants, puit):
    def _accessibilite(s1, s2, mode=0):
        fifo = deque()
        deja_vue = set()
        
        fifo.append(s1)
        deja_vue.add(s1)
        
        while fifo:
            courant = fifo.pop()
            for arc in sommets[courant]:
                if (arc in arcs_normaux and mode==0) or arc in arcs_fusionnes:
                    arc = arcs[arc]
                    if arc[1] not in deja_vue:
                        deja_vue.add(arc[1])
                        if arc[1] == s2:
                            return True
                        if arc[1] not in fifo:
                            fifo.append(arc[1])
        return False

    def _recursivite():
        if not arcs_normaux:
            return [[]]
        id_arc = arcs_normaux.pop()
        arc = arcs[id_arc]

        # Appel a gauche
        st_sans_arc = []
        if _accessibilite(arc[0], puit):
            st_sans_arc = _recursivite()

        # Appel a droite
        arcs_fusionnes.add(id_arc)
        arcs_retires = set()
        for a in sommets[arc[0]]:
            if a in arcs_normaux:
                arcs_normaux.remove(a)
                arcs_retires.add(a)
        st_avec_arc = []
        if not _accessibilite(arc[1], arc[0], mode=FUSIONNE):
            st_avec_arc = _recursivite()
        for a in arcs_retires:
            arcs_normaux.add(a)
        arcs_normaux.add(id_arc)
        arcs_fusionnes.remove(id_arc)

        for st in st_avec_arc:
            st.append(id_arc)

        return st_sans_arc + st_avec_arc

    NORMAL = 0
    SUPPRIME = 1
    FUSIONNE = 2
    arcs = {}
    arcs_normaux = set()
    arcs_fusionnes = set()
    sommets = {}
    for s, v_sortants in voisins_sortants.items():
        sommets[s] = set()
        for v in v_sortants:
            arcs[len(arcs)+1] = (s, v)
            arcs_normaux.add(len(arcs))
            sommets[s].add(len(arcs))
    print(arcs)
    print(len(_recursivite()))

list_spanning_trees(voisins_sortants, 5)
