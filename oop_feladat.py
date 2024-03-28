#VZJDIG
from abc import  ABC


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []  # Szobák tárolása

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba)

    def __str__(self):
        return f"{self.nev} Szálloda, Szobák száma: {len(self.szobak)}"

class Foglalas:
    def __init__(self, szoba, vendeg_nev, napok_szama):
        self.szoba = szoba
        self.vendeg_nev = vendeg_nev
        self.napok_szama = napok_szama

    def __str__(self):
        return f"Foglalás: {self.vendeg_nev} - {self.szoba.leiras()}, Napok száma: {self.napok_szama}"

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    def leiras(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, reggeli, erkely):
        super().__init__(ar, szobaszam)
        self.reggeli = reggeli
        self.erkely = erkely

    def leiras(self):
        return f"Egyágyas szoba, Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft/éj, {'Reggeli' if self.reggeli else 'Nincs reggeli'}, {'Erkélyes' if self.erkely else 'Nincs erkély'}"


class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, reggeli, erkely):
        super().__init__(ar, szobaszam)
        self.reggeli = reggeli
        self.erkely = erkely

    def leiras(self):
        return f"Ketágyas szoba, Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft/éj, {'Reggeli' if self.reggeli else 'Nincs reggeli'}, {'Erkélyes' if self.erkely else 'Nincs erkély'}"

szalloda = Szalloda("Grande Hotel")

egyagyas = EgyagyasSzoba(10000, 101, True,True)
ketagyas = KetagyasSzoba(18000, 102, False, True)

szalloda.szoba_hozzaad(egyagyas)
szalloda.szoba_hozzaad(ketagyas)

foglalas1 = Foglalas(egyagyas, "Kis József", 2)
foglalas2 = Foglalas(ketagyas, "Nagy Anna", 3)
foglalas3 = Foglalas(ketagyas, "Nagy Annaaaaa", 1)

print(szalloda)
print(foglalas1)
print(foglalas2)
print(foglalas3)