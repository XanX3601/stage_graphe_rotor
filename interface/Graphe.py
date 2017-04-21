from multiprocessing.dummy import Pool, Lock
from copy import deepcopy
from collections import deque
from sys import stderr

class Graphe:
    def __init__(self):
        self.voisins_entrants = {}
        self.voisins_sortants = {}
        self.rotors = {}
        self.trains = {}
        self.arcs = {}
        self.id_arc = 0

    def ajouter_sommet(self, id):
        self.voisins_entrants[id] = []
        self.voisins_sortants[id] = []
        self.rotors[id] = -1

    def enelever_sommet(self, id):
        for v in self.voisins_entrants[id]:
            self.voisins_sortants[v].remove(id)
            if (v, id) in self.arcs.values():
                del self.arcs[self.arcs.keys()[self.arcs.values().index((v, id))]]
        for v in self.voisins_sortants[id]:
            self.voisins_entrants[v].remove(id)
            if (id, v) in self.arcs.values():
                del self.arcs[self.arcs.keys()[self.arcs.values().index((id, v))]]
        del self.voisins_sortants[id]
        del self.voisins_entrants[id]
        del self.rotors[id]
        if id in self.trains:
            del self.trains[id]

    def ajouter_arc(self, s1, s2, id_arc=-1):
        self.voisins_sortants[s1].append(s2)
        self.voisins_entrants[s2].append(s1)
        if id_arc != -1:
            self.arcs[id_arc] = (s1, s2)
        else:
            self.arcs[self.id_arc] = (s1, s2)
            self.id_arc += 1
        if self.rotors[s1] == -1:
            self.rotors[s1] = 0

    def enlever_arc(self, s1, s2):
        self.voisins_sortants[s1].remove(s2)
        self.voisins_entrants[s2].remove(s1)
        del self.arcs[self.arcs.keys()[self.arcs.values().index((s1, s2))]]
        if self.voisins_sortants[s1]:
            self.rotors[s1] = 0
        else:
            self.rotors[s1] = -1

    def ajouter_train(self, id, train=1):
        if id not in self.trains:
            self.trains[id] = train
        else:
            self.trains[id] += train

    def enelever_train(self, id, train=1):
        if id in self.trains:
            self.trains[id] -= train
            if self.trains[id] <= 0:
                del self.trains[id]

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

    def peut_acceder(self, s1, s2):
        filo = deque()
        filo.append(s1)
        deja_vue = [s1]

        while filo:
            courant = filo.pop()
            for v in self.voisins_sortants[courant]:
                if v not in deja_vue:
                    if v == s2:
                        return True
                    deja_vue.append(v)
                    filo.append(v)
        return False

    def simuler(self):
        def circuler(id):
            while self.voisins_sortants[id]:
                verrous[id].acquire()
                self.enelever_train(id)
                self.rotationer(id)
                verrous[id].release()
                id = self.get_sommet_pointe(id)
                verrous[id].acquire()
                self.ajouter_train(id)
                verrous[id].release()
            return id
        verrous = {}
        for id in self.rotors.keys():
            verrous[id] = Lock()
        trains = []
        for id, nb_trains in self.trains.items():
            for i in xrange(nb_trains):
                trains.append(id)
        pool = Pool(2)
        return pool.map(circuler, trains)

    def liste_spanning_tree(self, s):
        def _recursivite(g):
            if len(g.rotors) == 1:
                return [[]]
            arc = g.arcs[g.arcs.keys()[0]]

            g1 = deepcopy(g)
            g1.enlever_arc(arc[0], arc[1])
            st_sans_arc = []
            if g1.peut_acceder(arc[0], s):
                st_sans_arc = _recursivite(g1)

            g2 = deepcopy(g)
            for v in g2.voisins_entrants[arc[0]]:
                if v != arc[1]:
                    g2.ajouter_arc(v, arc[1], g2.arcs.keys()[g2.arcs.values().index((v, arc[0]))])
            g2.enelever_sommet(arc[0])
            st_avec_arc = _recursivite(g2)

            id_arc = g.arcs.keys()[g.arcs.values().index(arc)]
            for i in xrange(len(st_avec_arc)):
                st_avec_arc[i].append(id_arc)
            return st_avec_arc + st_sans_arc

        if not self.voisins_sortants[s]:
            liste_arcs_supprimes = []
            for v in self.voisins_sortants[s]:
                self.enlever_arc(s, v)
                liste_arcs_supprimes += [(s, v)]
        print(_recursivite(self))


if __name__ == '__main__':
    g = Graphe()
    g.ajouter_sommet(1)
    g.ajouter_sommet(2)
    g.ajouter_sommet(3)
    g.ajouter_sommet(4)
    g.ajouter_sommet(5)
    g.ajouter_arc(1, 2)
    g.ajouter_arc(2, 3)
    g.ajouter_arc(3, 1)
    g.ajouter_arc(4, 2)
    g.ajouter_arc(4, 3)
    g.ajouter_arc(4, 1)
    g.ajouter_arc(1, 4)
    g.ajouter_arc(2, 4)
    g.ajouter_arc(3, 4)
    g.ajouter_arc(1, 5)
    g.ajouter_arc(2, 5)
    g.ajouter_arc(3, 5)
    print(g.arcs)
    g.liste_spanning_tree(1)