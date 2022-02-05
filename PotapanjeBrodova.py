#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
from random import randrange
import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade



def provjeriOkoOdabranogIndeksa(prviIndeks, odabraniIndeks,agent):
    dopusteno = True
    if odabraniIndeks + 1 < 10:
        if agent.lista[prviIndeks][odabraniIndeks + 1] != "0":
            dopusteno = False
    if odabraniIndeks - 1 >= 0:
        if agent.lista[prviIndeks][odabraniIndeks - 1] != "0":
            dopusteno = False
    if prviIndeks + 1 < 10:
        if agent.lista[prviIndeks + 1][odabraniIndeks] != "0":
            dopusteno = False
    if prviIndeks - 1 >= 0:
        if agent.lista[prviIndeks - 1][odabraniIndeks] != "0":
            dopusteno = False
    if prviIndeks + 1 < 10 and odabraniIndeks + 1 < 10:
        if agent.lista[prviIndeks + 1][odabraniIndeks + 1] != "0":
            dopusteno = False
    if prviIndeks - 1 >= 0 and odabraniIndeks + 1 < 10:
        if agent.lista[prviIndeks - 1][odabraniIndeks + 1] != "0":
            dopusteno = False
    if prviIndeks + 1 < 10 and odabraniIndeks - 1 >= 0:
        if agent.lista[prviIndeks + 1][odabraniIndeks - 1] != "0":
            dopusteno = False
    if prviIndeks - 1 >= 0 and odabraniIndeks - 1 >= 0:
        if agent.lista[prviIndeks - 1][odabraniIndeks - 1] != "0":
            dopusteno = False
    return dopusteno


def provjeriDostupneSmjerove(prviIndeks, odabraniIndeks, size,agent):
    dostupniSmjerovi = []
    velicinaUvjeti = size - 1
    if prviIndeks + velicinaUvjeti < 10:
        dostupnoDolje = True
        for i in range(1, size):
            dostupnoDolje = provjeriOkoOdabranogIndeksa(prviIndeks + i, odabraniIndeks,agent)
            if dostupnoDolje == False:
                break
        if dostupnoDolje:
            dostupniSmjerovi.append("D")
    if prviIndeks - velicinaUvjeti >= 0:
        dostupnoGore = True
        for i in range(1, size):
            dostupnoGore = provjeriOkoOdabranogIndeksa(prviIndeks - i, odabraniIndeks,agent)
            if dostupnoGore == False:
                break
        if dostupnoGore:
            dostupniSmjerovi.append("U")
    if odabraniIndeks - velicinaUvjeti >= 0:
        dostupnoLijevo = True
        for i in range(1, size):
            dostupnoLijevo = provjeriOkoOdabranogIndeksa(prviIndeks, odabraniIndeks - i,agent)
            if dostupnoLijevo == False:
                break
        if dostupnoLijevo:
            dostupniSmjerovi.append("L")
    if odabraniIndeks + velicinaUvjeti < 10:
        dostupnoDesno = True
        for i in range(1, size):
            dostupnoDesno = provjeriOkoOdabranogIndeksa(prviIndeks, odabraniIndeks + i,agent)
            if dostupnoDesno == False:
                break
        if dostupnoDesno:
            dostupniSmjerovi.append("R")
    return dostupniSmjerovi


def postaviBrod(size, oznaka,agent):
    postavljen = False
    while (postavljen != True):
        prviIndeks = randrange(len(agent.lista))
        if agent.lista[prviIndeks].count("0") > 1:
            sviPrazni = [i for i, polje in enumerate(agent.lista[prviIndeks]) if polje == "0"]
            odabranaLokacija = False
            while (odabranaLokacija == False and sviPrazni):
                odabraniIndeks = random.choice(sviPrazni)
                sviPrazni.remove(odabraniIndeks)
                provjeriKrug = provjeriOkoOdabranogIndeksa(prviIndeks, odabraniIndeks,agent)
                if not provjeriKrug:
                    continue
                dostupniSmjerovi = provjeriDostupneSmjerove(prviIndeks, odabraniIndeks, size,agent)
                if dostupniSmjerovi:
                    odabranaLokacija = True
            if odabranaLokacija:
                postavljen = True
                odabraniSmjer = random.choice(dostupniSmjerovi)
                if odabraniSmjer == "D":
                    for i in range(size):
                        agent.lista[prviIndeks + i][odabraniIndeks] = oznaka
                elif odabraniSmjer == "U":
                    for i in range(size):
                        agent.lista[prviIndeks - i][odabraniIndeks] = oznaka
                elif odabraniSmjer == "R":
                    for i in range(size):
                        agent.lista[prviIndeks][odabraniIndeks + i] = oznaka
                elif odabraniSmjer == "L":
                    for i in range(size):
                        agent.lista[prviIndeks][odabraniIndeks - i] = oznaka


def ProvjeriDaliPogodak(prviIndeks, drugiIndeks, agent):
    poruka = ""
    if agent.lista[prviIndeks][drugiIndeks] != "0":
        oznaka = agent.lista[prviIndeks][drugiIndeks]
        agent.lista[prviIndeks][drugiIndeks] = "X"
        potopljen = True
        for red in agent.lista:
            if red.count(oznaka) != 0:
                potopljen = False
                break
        if potopljen:
            poruka = "Potopljen"
        else:
            poruka = "Pogodak"
        if potopljen:
            gotovo = True
            for red in agent.lista:
                if red.count("J") != 0 or red.count("B") != 0 or red.count("C") != 0 or red.count("S") != 0 or red.count("D") != 0:
                    gotovo = False
                    break
            if gotovo:
                poruka = "Čestitam pobijedio si"
    else:
        poruka = "Promašaj"

    return poruka


def noveMete(prviIndeks,odabraniIndeks,agent):
    if odabraniIndeks + 1 < 10:
        if agent.listaGadanja[prviIndeks][odabraniIndeks + 1] == "0" or agent.listaGadanja[prviIndeks][odabraniIndeks + 1] == "N":
            agent.listaGadanja[prviIndeks][odabraniIndeks + 1]="L"
            agent.listaMogucihMeta.append([prviIndeks,odabraniIndeks+1])
    if odabraniIndeks - 1 >= 0:
        if agent.listaGadanja[prviIndeks][odabraniIndeks - 1] == "0" or agent.listaGadanja[prviIndeks][odabraniIndeks - 1] == "N":
            agent.listaMogucihMeta.append([prviIndeks,odabraniIndeks-1])
            agent.listaGadanja[prviIndeks][odabraniIndeks - 1] = "L"
    if prviIndeks + 1 < 10:
        if agent.listaGadanja[prviIndeks + 1][odabraniIndeks] == "0" or agent.listaGadanja[prviIndeks + 1][odabraniIndeks] == "N":
            agent.listaMogucihMeta.append([prviIndeks+1,odabraniIndeks])
            agent.listaGadanja[prviIndeks+1][odabraniIndeks] = "L"
    if prviIndeks - 1 >= 0:
        if agent.listaGadanja[prviIndeks - 1][odabraniIndeks] == "0" or agent.listaGadanja[prviIndeks - 1][odabraniIndeks] == "N":
            agent.listaMogucihMeta.append([prviIndeks-1,odabraniIndeks])
            agent.listaGadanja[prviIndeks - 1][odabraniIndeks] = "L"


class PrviIgrac(Agent):

    class PonasanjeKA(FSMBehaviour):
        async def on_start(self):
            print("Pokreće se igrač 1")

        async def on_end(self):
            print("Isključuje se igrač 1")

    class PostavljanjeBrodova(State):
        async def run(self):
            print("////////////////////////////////////////////////")
            print("Igrač 1: Postavljam brodove....")
            print("////////////////////////////////////////////////")
            for i in range(10):
                self.agent.lista.append(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"])
                if i % 2 == 0:
                    self.agent.listaGadanja.append(["N", "0", "N", "0", "N", "0", "N", "0", "N", "0"])
                else:
                    self.agent.listaGadanja.append(["0", "N", "0", "N", "0", "N", "0", "N", "0", "N"])
            postaviBrod(5, "J",self.agent)
            postaviBrod(4, "B",self.agent)
            postaviBrod(3, "C",self.agent)
            postaviBrod(3, "S",self.agent)
            postaviBrod(2, "D",self.agent)
            print("   0   1   2   3   4   5   6   7   8   9  ")
            for red in self.agent.lista:
                print(str(self.agent.zaLegendu) + "| " + red[0] + " | " + red[1] + " | " + red[2] + " | " + red[3] + " | " + red[
                    4] + " | " + red[5] + " | " + red[6] + " | " + red[7] + " | " + red[8] + " | " + red[9] + " |")
                self.agent.zaLegendu += 1
            self.agent.zaLegendu = 0
            print("////////////////////////////////////////////////")
            self.set_next_state("PrimajGadanje")
    class PrimajGadanje(State):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                print(f"Igrač 1: Primio sam poruku sadržaja: {msg.body}\n")
                prvaKordinata = msg.body.split(":")[1].split(",")[0]
                drugaKordinata = msg.body.split(":")[1].split(",")[1]
                poruka= ProvjeriDaliPogodak(int(prvaKordinata),int(drugaKordinata),self.agent)
                msg = spade.message.Message(
                    to="agent@rec.foi.hr",
                    body=poruka,
                    metadata={
                        "ontology": "Potapanje Brodova",
                        "language": "hrvatski",
                        "performative": "inform"})
                await self.send(msg)
                if not msg.body=="Čestitam pobijedio si":
                    self.set_next_state("Gadaj")
                else:
                    print("////////////////////////////////////////////////")
                    print("Igrač 1: Noooooooooooo...!")
                    print("////////////////////////////////////////////////")
                    self.set_next_state("KrajIgre")
                print("   0   1   2   3   4   5   6   7   8   9  ")
                for red in self.agent.lista:
                    print(str(self.agent.zaLegendu) + "| " + red[0] + " | " + red[1] + " | " + red[2] + " | " + red[
                        3] + " | " + red[
                              4] + " | " + red[5] + " | " + red[6] + " | " + red[7] + " | " + red[8] + " | " + red[
                              9] + " |")
                    self.agent.zaLegendu += 1
                self.agent.zaLegendu = 0
                print("////////////////////////////////////////////////")

    class Gadaj(State):
        async def run(self):
            izbor = []
            if self.agent.listaMogucihMeta:
                izbor = random.choice(self.agent.listaMogucihMeta)
                self.agent.listaMogucihMeta.remove(izbor)
            else:
                randomOdabran = False
                while not randomOdabran:
                    prviIndeksGadanja = randrange(len(self.agent.listaGadanja))
                    sviMoguci = [i for i, polje in enumerate(self.agent.listaGadanja[prviIndeksGadanja]) if polje == "0"]
                    if sviMoguci:
                        randomOdabran = True
                        drugiIndeksGadanja = random.choice(sviMoguci)
                izbor = [prviIndeksGadanja, drugiIndeksGadanja]
            poruka = "Gađam na kordinate:" + str(izbor[0]) + "," + str(izbor[1])
            self.agent.brojac += 1
            msg = spade.message.Message(
                to="agent@rec.foi.hr",
                body=poruka,
                metadata={
                    "ontology": "Potapanje Brodova",
                    "language": "hrvatski",
                    "performative": "inform"})
            await self.send(msg)
            msg = await self.receive(timeout=5)
            if msg:
                print("////////////////////////////////////////////////")
                print(f"Igrač 1: Primio sam poruku sadržaja: {msg.body}\n")
                if msg.body == "Promašaj":
                    self.agent.listaGadanja[izbor[0]][izbor[1]]="P"
                    self.set_next_state("PrimajGadanje")
                elif msg.body == "Pogodak":
                    self.agent.listaGadanja[izbor[0]][izbor[1]]="X"
                    noveMete(izbor[0], izbor[1],self.agent)
                    self.set_next_state("PrimajGadanje")
                elif msg.body == "Potopljen":
                    self.agent.listaGadanja[izbor[0]][izbor[1]] = "X"
                    self.agent.listaMogucihMeta.clear()
                    self.set_next_state("PrimajGadanje")
                elif msg.body == "Čestitam pobijedio si":
                    self.agent.listaGadanja[int(izbor[0])][int(izbor[1])] = "X"
                    print("Igrač 1: GG, Easy, it was never a matter of if, just when you were going to lose, kid")
                    self.set_next_state("KrajIgre")
                print("   0   1   2   3   4   5   6   7   8   9  ")
                for red in self.agent.listaGadanja:
                    print(str(self.agent.zaLegendu) + "| " + red[0] + " | " + red[1] + " | " + red[2] + " | " + red[
                        3] + " | " + red[
                              4] + " | " + red[5] + " | " + red[6] + " | " + red[7] + " | " + red[8] + " | " + red[
                              9] + " |")
                    self.agent.zaLegendu += 1
                self.agent.zaLegendu = 0
                print("////////////////////////////////////////////////")

    class KrajIgre(State):
        async def run(self):
            print("Igra je završila")
            print("Igrač 1 je gađao "+str(self.agent.brojac)+" puta")
            print("////////////////////////////////////////////////")
            await self.agent.stop()

    async def setup(self):
        print("<------------------------------Legenda------------------------------>")
        print("| N-ne treba gađati (random), P-Promašaj, L-u listi mogućih meta, X-Pogodak, Ostalo-Brodovi|")
        print("<------------------------------------------------------------------->")
        self.brojac = 0
        self.lista = []
        self.listaGadanja = []
        self.zaLegendu = 0
        self.listaMogucihMeta=[]
        fsm = self.PonasanjeKA()

        fsm.add_state(name="PostavljanjeBrodova", state=self.PostavljanjeBrodova(), initial=True)
        fsm.add_state(name="PrimajGadanje", state=self.PrimajGadanje())
        fsm.add_state(name="Gadaj", state=self.Gadaj())
        fsm.add_state(name="KrajIgre", state=self.KrajIgre())

        fsm.add_transition(source="PostavljanjeBrodova", dest="PrimajGadanje")
        fsm.add_transition(source="PrimajGadanje", dest="Gadaj")
        fsm.add_transition(source="PrimajGadanje", dest="KrajIgre")
        fsm.add_transition(source="Gadaj", dest="PrimajGadanje")
        fsm.add_transition(source="Gadaj", dest="KrajIgre")


        self.add_behaviour(fsm)

class DrugiIgrac(Agent):

    class PonasanjeKA(FSMBehaviour):
        async def on_start(self):
            print("Pokreće se igrač 2")

        async def on_end(self):
            print("Isključuje se igrač 2")

    class PostavljanjeBrodova(State):
        async def run(self):
            print("||||||||||||||||||||||||||||||||||||||||||||||||")
            print("Igrač 2: Postavljam brodove....")
            print("||||||||||||||||||||||||||||||||||||||||||||||||")
            for i in range(10):
                self.agent.lista.append(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"])
                self.agent.listaGadanja.append(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"])
            postaviBrod(5, "J",self.agent)
            postaviBrod(4, "B",self.agent)
            postaviBrod(3, "C",self.agent)
            postaviBrod(3, "S",self.agent)
            postaviBrod(2, "D",self.agent)
            print("   0   1   2   3   4   5   6   7   8   9  ")
            for red in self.agent.lista:
                print(str(self.agent.zaLegendu) + "| " + red[0] + " | " + red[1] + " | " + red[2] + " | " + red[3] + " | " + red[
                    4] + " | " + red[5] + " | " + red[6] + " | " + red[7] + " | " + red[8] + " | " + red[9] + " |")
                self.agent.zaLegendu += 1
            self.agent.zaLegendu = 0
            print("||||||||||||||||||||||||||||||||||||||||||||||||")
            self.set_next_state("Gadaj")

    class PrimajGadanje(State):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                print(f"Igrač 2: Primio sam poruku sadržaja: {msg.body}\n")
                prvaKordinata = msg.body.split(":")[1].split(",")[0]
                drugaKordinata = msg.body.split(":")[1].split(",")[1]
                poruka = ProvjeriDaliPogodak(int(prvaKordinata), int(drugaKordinata), self.agent)
                msg = spade.message.Message(
                    to="krasinec@rec.foi.hr",
                    body=poruka,
                    metadata={
                        "ontology": "Potapanje Brodova",
                        "language": "hrvatski",
                        "performative": "inform"})
                await self.send(msg)
                if not msg.body == "Čestitam pobijedio si":
                    self.set_next_state("Gadaj")
                else:
                    print("Igrač 2: Noooooooooooo...!")
                    self.set_next_state("KrajIgre")
                print("   0   1   2   3   4   5   6   7   8   9  ")
                for red in self.agent.lista:
                    print(str(self.agent.zaLegendu) + "| " + red[0] + " | " + red[1] + " | " + red[2] + " | " + red[
                        3] + " | " + red[
                              4] + " | " + red[5] + " | " + red[6] + " | " + red[7] + " | " + red[8] + " | " + red[
                              9] + " |")
                    self.agent.zaLegendu += 1
                self.agent.zaLegendu = 0
                print("||||||||||||||||||||||||||||||||||||||||||||||||")

    class Gadaj(State):
        async def run(self):
            randomOdabran = False
            while not randomOdabran:
                prviIndeksGadanja = randrange(len(self.agent.listaGadanja))
                sviMoguci = [i for i, polje in enumerate(self.agent.listaGadanja[prviIndeksGadanja]) if polje == "0"]
                if sviMoguci:
                    randomOdabran = True
                    drugiIndeksGadanja = random.choice(sviMoguci)
            poruka = "Gađam na kordinate:"+str(prviIndeksGadanja)+","+str(drugiIndeksGadanja)
            self.agent.brojac+=1
            msg = spade.message.Message(
                to="krasinec@rec.foi.hr",
                body=poruka,
                metadata={
                    "ontology": "Potapanje Brodova",
                    "language": "hrvatski",
                    "performative": "inform"})
            await self.send(msg)
            msg = await self.receive(timeout=5)
            if msg:
                print("||||||||||||||||||||||||||||||||||||||||||||||||")
                print(f"Igrač 2: Primio sam poruku sadržaja: {msg.body}\n")
                if msg.body == "Promašaj":
                    self.agent.listaGadanja[int(prviIndeksGadanja)][int(drugiIndeksGadanja)]="P"
                    self.set_next_state("PrimajGadanje")
                elif msg.body == "Pogodak" or msg.body == "Potopljen":
                    self.agent.listaGadanja[int(prviIndeksGadanja)][int(drugiIndeksGadanja)] = "X"
                    self.set_next_state("PrimajGadanje")
                elif msg.body == "Čestitam pobijedio si":
                    self.agent.listaGadanja[int(prviIndeksGadanja)][int(drugiIndeksGadanja)] = "X"
                    print("||||||||||||||||||||||||||||||||||||||||||||||||")
                    print("Igrač 2: Woohooo! Pobijedio sam!")
                    print("||||||||||||||||||||||||||||||||||||||||||||||||")
                    self.set_next_state("KrajIgre")
                print("   0   1   2   3   4   5   6   7   8   9  ")
                for red in self.agent.listaGadanja:
                    print(str(self.agent.zaLegendu) + "| " + red[0] + " | " + red[1] + " | " + red[2] + " | " + red[
                        3] + " | " + red[
                              4] + " | " + red[5] + " | " + red[6] + " | " + red[7] + " | " + red[8] + " | " + red[
                              9] + " |")
                    self.agent.zaLegendu += 1
                self.agent.zaLegendu = 0
                print("||||||||||||||||||||||||||||||||||||||||||||||||")

    class KrajIgre(State):
        async def run(self):
            print("Igra je završila")
            print("Igrač 2 je gađao " + str(self.agent.brojac) + " puta")
            print("||||||||||||||||||||||||||||||||||||||||||||||||")
            await self.agent.stop()

    async def setup(self):
        self.brojac = 0
        self.lista = []
        self.listaGadanja = []
        self.zaLegendu = 0

        fsm = self.PonasanjeKA()

        fsm.add_state(name="PostavljanjeBrodova", state=self.PostavljanjeBrodova(), initial=True)
        fsm.add_state(name="PrimajGadanje", state=self.PrimajGadanje())
        fsm.add_state(name="Gadaj", state=self.Gadaj())
        fsm.add_state(name="KrajIgre", state=self.KrajIgre())

        fsm.add_transition(source="PostavljanjeBrodova", dest="Gadaj")
        fsm.add_transition(source="PrimajGadanje", dest="Gadaj")
        fsm.add_transition(source="PrimajGadanje", dest="KrajIgre")
        fsm.add_transition(source="Gadaj", dest="PrimajGadanje")
        fsm.add_transition(source="Gadaj", dest="KrajIgre")

        self.add_behaviour(fsm)


if __name__ == '__main__':
    #Agent igrač prvi
    prviIgrac = PrviIgrac("krasinec@rec.foi.hr", "krasinec")
    pokretanjePrvi = prviIgrac.start()
    pokretanjePrvi.result()

    #Agent igrač drugi
    drugiIgrac = DrugiIgrac("agent@rec.foi.hr", "tajna")
    pokretanjeDrugi = drugiIgrac.start()
    pokretanjeDrugi.result()



    while prviIgrac.is_alive() or drugiIgrac.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    prviIgrac.stop()
    drugiIgrac.stop()
    quit_spade()
