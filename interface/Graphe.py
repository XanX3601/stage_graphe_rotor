class Graphe:
    def __init__(self):
        self.voisins_entrants = {}
        self.voisins_sortants = {}
        self.rotors = {}

    def ajouter_sommet(self, id):
        self.voisins_entrants[id] = []
        self.voisins_sortants[id] = []
        self.rotors[id] = -1

    def enelever_sommet(self, id):
        for v in self.voisins_entrants[id]:
            self.voisins_sortants[v].remove(id)
        for v in self.voisins_sortants[id]:
            self.voisins_entrants[v].remove(id)
        del self.voisins_sortants[id]
        del self.voisins_entrants[id]
        del self.rotors[id]

    def ajouter_arc(self, s1, s2):
        self.voisins_sortants[s1].append(s2)
        self.voisins_entrants[s2].append(s1)
        if self.rotors[s1] == -1:
            self.rotors[s1] = 0

    def enlever_arc(self, s1, s2):
        self.voisins_sortants[s1].remove(s2)
        self.voisins_entrants[s2].remove(s1)
        if self.voisins_sortants[s1]:
            self.rotors[s1] = 0
        else:
            self.rotors[s1] = -1

    def rotationer(self, id):
        if self.rotors[id] > -1 :
            self.rotors[id] += 1
            self.rotors[id] %= len(self.voisins_sortants[id])

    def changer_ordre_voisin(self, id, liste):
        if set(liste) == set(self.voisins_sortants[id]):
            self.voisins_sortants[id] = liste
            if liste:
                self.rotors[id] = 0
            else:
                self.rotors[id] = -1

    def est_voisin_sortant(self, s1, s2):
        return s1 in self.voisins_sortants[s2]

    def get_sommet_pointe(self, id):
        if self.rotors[id] > -1:
            return self.voisins_sortants[id][self.rotors[id]]
        else:
            return -1
