from Tkinter import Tk, Canvas, SW, LAST, StringVar, Entry, NORMAL, DISABLED
from Graphe import Graphe

class Interface:
    def __init__(self):
        self.fenetre = Tk()
        self.toile = Canvas(self.fenetre, width=800, height=800)
        self.graphe = Graphe()
        self.id = 1
        self.id_sommets = {}
        self.positions_sommets = {}
        self.noms_sommets = {}
        self.sommet_courant = None
        self.id_arcs = {}
        self.nom_sommet_courant = StringVar()
        self.input_nom = Entry(self.fenetre, textvariable=self.nom_sommet_courant, width=30, state=DISABLED)

    def pack(self):
        self.nom_sommet_courant.trace("w", lambda _, __, ____: self.changer_nom_sommet())
        self.input_nom.grid(row=0, column=0)
        self.toile.grid(row=0, column=1)
        self.toile.bind('<Button-1>', self.clique_gauche)
        self.toile.bind('<Button-3>', self.clique_droit)


    def afficher(self):
        self.fenetre.mainloop()

    def selectionner(self,s):
        self.toile.itemconfig(self.id_sommets[s], fill="red")
        self.sommet_courant = s
        self.input_nom.config(state=NORMAL)
        self.nom_sommet_courant.set(self.toile.itemcget(self.noms_sommets[s], "text"))

    def deselectionner(self):
        self.toile.itemconfig(self.id_sommets[self.sommet_courant], fill="black")
        self.sommet_courant = None
        self.input_nom.config(state=DISABLED)
        self.nom_sommet_courant.set('')

    def clique_gauche(self, e=None):
        s = self.est_sur_sommet(e.x, e.y)

        if self.sommet_courant:
            if s == self.sommet_courant:
                self.deselectionner()
            elif s:
                if self.graphe.estVoisinSortant(s, self.sommet_courant):
                    self.graphe.enlever_arc(self.sommet_courant, s)
                    self.toile.delete(self.id_arcs[(self.sommet_courant, s)])
                    del self.id_arcs[(self.sommet_courant, s)]
                    self.deselectionner()
                else:
                    self.graphe.ajouter_arc(self.sommet_courant, s)
                    p_s1 = self.positions_sommets[self.sommet_courant]
                    p_s2 = self.positions_sommets[s]
                    self.id_arcs[(self.sommet_courant, s)] = self.toile.create_line(p_s1[0], p_s1[1], p_s2[0], p_s2[1], arrow=LAST, width=3, fill='gray65')
                    self.deselectionner()
            else:
                self.toile.coords(self.id_sommets[self.sommet_courant], e.x-10, e.y-10, e.x+10, e.y+10)
                self.toile.coords(self.noms_sommets[self.sommet_courant], e.x+10, e.y-10)
                self.positions_sommets[self.sommet_courant] = (e.x, e.y)

                for v in self.graphe.voisins_entrants[self.sommet_courant]:
                    p_v = self.positions_sommets[v]
                    self.toile.coords(self.id_arcs[(v, self.sommet_courant)], p_v[0], p_v[1], e.x, e.y)
                for v in self.graphe.voisins_sortants[self.sommet_courant]:
                    p_v = self.positions_sommets[v]
                    self.toile.coords(self.id_arcs[(self.sommet_courant, v)], e.x, e.y, p_v[0], p_v[1])

                self.deselectionner()
        else:
            if s:
                self.selectionner(s)
            else:
                id = self.id
                self.id += 1
                self.id_sommets[id] = self.toile.create_oval(e.x-10, e.y-10, e.x+10, e.y+10, fill='black')
                self.graphe.ajouter_sommet(id)
                self.positions_sommets[id] = (e.x, e.y)
                self.noms_sommets[id] = self.toile.create_text(e.x+10, e.y-10, text=id, anchor=SW)


    def clique_droit(self,e=None):
        s = self.est_sur_sommet(e.x, e.y)

        if s:
            if s == self.sommet_courant:
                self.deselectionner()

            for v in self.graphe.voisins_entrants[s]:
                self.toile.delete(self.id_arcs[(v, s)])
                del self.id_arcs[(v, s)]
            for v in self.graphe.voisins_sortants[s]:
                self.toile.delete(self.id_arcs[(s, v)])
                del self.id_arcs[(s, v)]

            self.toile.delete(self.id_sommets[s])
            self.toile.delete(self.noms_sommets[s])
            del self.noms_sommets[s]
            del self.id_sommets[s]
            del self.positions_sommets[s]
            self.graphe.enelever_sommet(s)

    def est_sur_sommet(self, x, y):
        for id, position in self.positions_sommets.items():
            if position[0] - 10 <= x <= position[0] + 10 and position[1] - 10 <= y <= position[1] + 10:
                return id
        return False
    
    def changer_nom_sommet(self):
        if self.sommet_courant:
            self.toile.itemconfig(self.noms_sommets[self.sommet_courant], text=self.nom_sommet_courant.get())

if __name__ == '__main__':
    i = Interface()
    i.pack()
    i.afficher()
