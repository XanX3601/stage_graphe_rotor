from Tkinter import Tk, Canvas, SW, LAST, StringVar, Entry, NORMAL, DISABLED, Button
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
        self.ordre_rotor = StringVar()
        self.input_ordre = Entry(self.fenetre, textvariable=self.ordre_rotor, width=30, state=DISABLED)
        self.bouton_rotationner = Button(self.fenetre, text="Rotationner", command=self.rotationner, state=DISABLED)

    def pack(self):
        self.nom_sommet_courant.trace("w", lambda _, __, ____: self.changer_nom_sommet())
        self.ordre_rotor.trace("w", lambda _, __, ___: self.changer_ordre_rotor())
        self.input_nom.grid(row=0, column=0)
        self.toile.grid(row=0, column=1, rowspan=3)
        self.input_ordre.grid(row=1, column=0)
        self.bouton_rotationner.grid(row=2, column=0)
        self.toile.bind('<Button-1>', self.clique_gauche)
        self.toile.bind('<Button-3>', self.clique_droit)

    def afficher(self):
        self.toile.focus_set()
        self.fenetre.mainloop()

    def selectionner(self,s):
        self.toile.itemconfig(self.id_sommets[s], fill="red")
        self.sommet_courant = s
        self.input_nom.config(state=NORMAL)
        self.input_ordre.config(state=NORMAL)
        self.bouton_rotationner.config(state=NORMAL)
        self.nom_sommet_courant.set(self.toile.itemcget(self.noms_sommets[s], "text"))
        self.ordre_rotor.set(" ".join(map(str, self.graphe.voisins_sortants[s])))

    def deselectionner(self):
        self.toile.itemconfig(self.id_sommets[self.sommet_courant], fill="black")
        self.sommet_courant = None
        self.input_nom.config(state=DISABLED)
        self.input_ordre.config(state=DISABLED)
        self.bouton_rotationner.config(state=DISABLED)
        self.nom_sommet_courant.set('')
        self.ordre_rotor.set('')

    def dessiner_arc(self, s1, s2):
        couleur = "gray65"
        width = 1
        p_s1 = self.positions_sommets[s1]
        p_s2 = self.positions_sommets[s2]
        if self.graphe.get_sommet_pointe(s1) == s2:
            couleur = "orange"
            width = 3
        if (s1,s2) in self.id_arcs:
            if self.graphe.get_sommet_pointe(s1) == s2:
                couleur = "orange"
                width = 3
            self.toile.itemconfig(self.id_arcs[(s1, s2)], width=width, fill=couleur)
        else :
            self.id_arcs[(s1, s2)] = self.toile.create_line(p_s1[0], p_s1[1], p_s2[0], p_s2[1], arrow=LAST, width=width,
                                                        fill=couleur)


    def clique_gauche(self, e=None):
        s = self.est_sur_sommet(e.x, e.y)

        if self.sommet_courant:
            if s == self.sommet_courant:
                self.deselectionner()
            elif s:
                if self.graphe.est_voisin_sortant(s, self.sommet_courant):
                    self.graphe.enlever_arc(self.sommet_courant, s)
                    self.toile.delete(self.id_arcs[(self.sommet_courant, s)])
                    del self.id_arcs[(self.sommet_courant, s)]
                    self.deselectionner()
                else:
                    self.graphe.ajouter_arc(self.sommet_courant, s)
                    self.dessiner_arc(self.sommet_courant, s)
                    self.deselectionner()
            else:
                self.toile.coords(self.id_sommets[self.sommet_courant], e.x-15, e.y-15, e.x+15, e.y+15)
                self.toile.coords(self.noms_sommets[self.sommet_courant], e.x+15, e.y-15)
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
                self.id_sommets[id] = self.toile.create_oval(e.x-15, e.y-15, e.x+15, e.y+15, fill='black')
                self.graphe.ajouter_sommet(id)
                self.positions_sommets[id] = (e.x, e.y)
                self.noms_sommets[id] = self.toile.create_text(e.x+15, e.y-15, text=id, anchor=SW)


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

    def rotationner(self, e=None):
        if self.sommet_courant :
            self.graphe.rotationer(self.sommet_courant)
            for v in self.graphe.voisins_sortants[self.sommet_courant]:
                self.dessiner_arc(self.sommet_courant, v)

    def est_sur_sommet(self, x, y):
        for id, position in self.positions_sommets.items():
            if position[0] - 15 <= x <= position[0] + 15 and position[1] - 15 <= y <= position[1] + 15:
                return id
        return False
    
    def changer_nom_sommet(self):
        if self.sommet_courant:
            self.toile.itemconfig(self.noms_sommets[self.sommet_courant], text=self.nom_sommet_courant.get())

    def changer_ordre_rotor(self):
        if self.sommet_courant:
            try:
                self.graphe.changer_ordre_voisin(self.sommet_courant, list(map(int, self.ordre_rotor.get().split())))
                for v in self.graphe.voisins_sortants[self.sommet_courant]:
                    self.dessiner_arc(self.sommet_courant, v)
            except Exception:
                pass

if __name__ == '__main__':
    i = Interface()
    i.pack()
    i.afficher()
