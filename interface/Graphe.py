from multiprocessing.dummy import Pool, Lock
from time import time

class Graphe:
    def __init__(self):
        self.voisins_entrants = {}
        self.voisins_sortants = {}
        self.rotors = {}
        self.trains = {}

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
        if id in self.trains:
            del self.trains[id]

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

if __name__ == '__main__':
    g = Graphe()
    g.ajouter_sommet(1)
    g.ajouter_sommet(2)
    g.ajouter_sommet(3)
    g.ajouter_arc(2, 1)
    g.ajouter_arc(2, 3)
    g.ajouter_arc(3, 1)
    g.ajouter_arc(3, 2)
    g.ajouter_train(2, 100000)
    g.ajouter_train(3, 100000)
    if g.get_sommet_pointe(2) == 1:
        g.rotationer(2)
    if g.get_sommet_pointe(3) == 1:
        g.rotationer(3)
    start = time()
    print g.simuler()
    stop = time()
    print stop - start
    print g.voisins_sortants
    print g.rotors
    print g.trains
