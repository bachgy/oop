#VZJDIG
import re
import sys
from datetime import date
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from Design import Ui_MainWindow
from reservationListWindow import  Ui_reservListWindow
from reservationAdd import Ui_addReserv
from ReservationCancel import Ui_ReservCancel
from abc import ABC

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def slotViewReservs(self):
        self.Foglalas_listazo = ReservListApp()
        FoglalasClass = Foglalas
        for x in FoglalasClass.peldanyok:
          self.Foglalas_listazo.listWidget.addItem(str(x))
        self.Foglalas_listazo.show()

    def slotCreateReserv(self):
        # print("Foglalás készítése")
        self.Foglalas_keszito = ReservAddApp()
        SzallodaiSzobak = Szoba
        for x in SzallodaiSzobak.szobaszam:
            # print(x)
            self.Foglalas_keszito.cmbSzobak.addItem(str(x))
        self.Foglalas_keszito.show()


    def slotDeleteReserv(self):
        self.Foglalas_torlo = reservCancelApp()
        FoglalasClass = Foglalas
        for x in FoglalasClass.peldanyok:
            self.Foglalas_torlo.listWidget.addItem(str(x))
        self.Foglalas_torlo.show()

class ReservAddApp(QMainWindow, Ui_addReserv):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def slot_tmp(self):
        kiv_szobaszam = self.cmbSzobak.currentText()
        SzallodaClass = szalloda
        for x in SzallodaClass.szobak:
            if kiv_szobaszam in x:
                print(x)

    def leiras_megkereses_kivalaszott_szobaszam_alapjan(self):
        kiv_szobaszam = self.cmbSzobak.currentText()
        SzallodaClass = szalloda
        for x in SzallodaClass.szobak:
            if kiv_szobaszam in x:
                return (x)
    def btnClick(self):
        SzobaFoglalas = Foglalas
        SzallodaClass = szalloda
        NemLehetsegesFoglalasok = []
        for x in Foglalas.peldanyok:
            NemLehetsegesFoglalasok.append((str(x.datum), str(x.szobaszam)))

        if (self.txtGuestName.toPlainText()) == "":
            QMessageBox.information(None, "Információ", "Nem töltötte ki a vendég neve mezőt!")
        else:
            if (self.calendarWidget.selectedDate().toPyDate()) < date.today():
                QMessageBox.information(None, "Információ", "A múltba nem lehetséges foglalni!")
            else:
                if (str(self.calendarWidget.selectedDate().toPyDate()),self.cmbSzobak.currentText()) in NemLehetsegesFoglalasok:
                    QMessageBox.information(None, "Információ", "Nem lehetséges, mert ezen a dátumon ebben a szobában már van foglalás")
                else:
                    SzobaFoglalas.hozzaad(self.cmbSzobak.currentText(),self.txtGuestName.toPlainText(),str(self.calendarWidget.selectedDate().toPyDate()))
                    QMessageBox.information(None, "Információ",f"Sikeres foglalás\n" + "A szoba jellemzői:\n" + self.leiras_megkereses_kivalaszott_szobaszam_alapjan())
                    self.close()

class ReservListApp(QMainWindow, Ui_reservListWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class reservCancelApp(QMainWindow, Ui_ReservCancel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def slotCancelReserv(self):
        FoglalasClass = Foglalas
        regexKif = r"Sorszám: (\d+)"
        torlendoElemIndexe = re.search(regexKif,self.listWidget.currentItem().text())
        print(torlendoElemIndexe.group(1))
        del FoglalasClass.peldanyok[int(torlendoElemIndexe.group(1))]
        QMessageBox.information(None, "Információ", "A kiválasztott fogalalás törlése megtörtént!")
        self.close()

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []  # Szobák tárolása

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba.leiras())

    def __str__(self):
        return f"{self.nev} Szálloda, Szobák száma: {len(self.szobak)}"

class Foglalas:

    peldanyok = []
    datumok = []
    szobak = []

    def __init__(self, szobaszam, vendeg_nev, mely_napra):
        self.szobaszam = szobaszam
        self.vendeg_nev = vendeg_nev
        self.datum = mely_napra
        Foglalas.peldanyok.append(self)
        Foglalas.datumok.append(mely_napra)
        Foglalas.szobak.append(self.szobak)
        self.index = Foglalas.peldanyok.index(self)
    def __str__(self):
        #return f"Foglalás: {self.vendeg_nev} - {self.szoba.leiras()}, Dátum: {self.datum}"
        return f"Sorszám: {self.index} Név: {self.vendeg_nev}, Szobaszám: {self.szobaszam}, Dátum: {self.datum}"
    @classmethod
    def hozzaad(cls, szoba, vendeg_nev, mely_napra):
        return cls(szoba, vendeg_nev, mely_napra)


class Szoba(ABC):

    szobaszam = []
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam
        Szoba.szobaszam.append(szobaszam)

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

szalloda = Szalloda("Grand Hotel GDE")

egyagyas = EgyagyasSzoba(10000, 101, True,True)
ketagyas_1 = KetagyasSzoba(18000, 102, False, True)
ketagyas_2 = KetagyasSzoba(16000, 201, True, True)

szalloda.szoba_hozzaad(egyagyas)
szalloda.szoba_hozzaad(ketagyas_1)
szalloda.szoba_hozzaad(ketagyas_2)

Foglalas.hozzaad(egyagyas.szobaszam, "Nagy Béla", '2024-06-13')
Foglalas.hozzaad(egyagyas.szobaszam, "teszt", '2024-06-10')
Foglalas.hozzaad(ketagyas_1.szobaszam, "Kovács Anna", '2024-06-18')
Foglalas.hozzaad(ketagyas_2.szobaszam, "Teszt Elek", '2024-06-12')
Foglalas.hozzaad(egyagyas.szobaszam, "Egyágyas István", '2024-06-20')

if __name__ == "__main__":
     app = QApplication(sys.argv)
     window = MainApp()
    # window = ReservAddApp()
     window.show()
     sys.exit(app.exec())