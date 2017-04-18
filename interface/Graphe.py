class Graphe:
    def __init__(self):
        self.voisins_entrants = {}
        self.voisins_sortants = {}

    def ajouter_sommet(self, id):
        self.voisins_entrants[id] = set()
        self.voisins_sortants[id] = set()

    def enelever_sommet(self, id):
        for v in self.voisins_entrants[id]:
            self.voisins_sortants[v].remove(id)
        for v in self.voisins_sortants[id]:
            self.voisins_entrants[v].remove(id)
        del self.voisins_sortants[id]
        del self.voisins_entrants[id]

    def ajouter_arc(self, s1, s2):
        self.voisins_sortants[s1].add(s2)
        self.voisins_entrants[s2].add(s1)

    def enlever_arc(self, s1, s2):
        self.voisins_sortants[s1].remove(s2)
        self.voisins_entrants[s2].remove(s1)

    def estVoisinSortant(self, s1, s2):
        return s1 in self.voisins_sortants[s2]
