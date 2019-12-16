import datetime
import csv
from decimal import Decimal  # za nastavitev na dve decimalni mesti
from re import compile  # za pravilen format

TWOPLACES = Decimal(10) ** -2  # nastavimo, da se decimalke zaokrožijo na dve
regexp = compile(r'^\d{2},\d{2}$')  # nastavitev formata, ko iščemo krajevne rezultate (meti, skoki), da so v obliki mm.cm


def definirano_sort_discplin(seznam_disciplin):
    """Vrne pravilno sortiran seznam disciplin."""

    """Funkcija dobi seznam disciplin, ki jih sortira po ključu, ki je definiran v slovarju. Vrne presortiran seznam."""

    # slovar, ki definira po kakem vrstnem redu se discipline razporedijo
    disc_dic = {'60 m': 1, '80 m': 2, '100 m': 3, '150 m': 4, '200 m': 5, '300 m': 6, '400 m': 7, '600 m': 8, '800 m': 9,
                '1000 m': 10, '1500 m': 11, '1 milja': 12, '2000 m': 13, '3000 m': 14, '5000 m': 15, '10000 m': 16, '60 m ovire': 17,
                '80 m ovire': 18, '100 m ovire': 19, '110 m ovire': 20, '200 m ovire': 21, '300 m ovire': 22, '400 m ovire': 23,
                '1500 m zapreke': 24, '2000 m zapreke': 25, '3000 m zapreke': 26, '10 km': 27, 'Polmaraton': 28, 'Maraton': 29,
                'Skok v daljino': 30, 'Troskok': 31, 'Skok v višino': 32, 'Skok s palico': 33, 'Suvanje krogle': 34,
                'Suvanje krogle 4 kg': 35, 'Met diska': 36, 'Met kladiva': 37, 'Met kopja': 38, 'Met kopja 700 g': 39, 'Met kopja 600 g': 40,
                'Met kopja 400 g': 41, 'Deseteroboj': 42, 'Sedmeroboj': 43, 'Četveroboj': 44, 'Met vorteksa': 45, 'Met žogice': 46}
    seznam_disciplin.sort(key=disc_dic.__getitem__)  # presortiranje
    return seznam_disciplin


def sortiranje_disciplin(nadseznam):
    """Sortiranje rezultatov iz seznama, ki vsebuje različne discipline. Vrne se sortiran seznam."""

    """Funkcija ki za argument sprejme seznam(nadseznam) v katerem so pod disciplinami zapisani rezultati
    (lahko tudi večkratni zapisi iste discipline) in vrne sortiran seznam za vsako disciplino, ki se pojavi v nadseznamu.
    Deluje tako za časovne kot za krajevne rezultate, s tem da morajo biti v pravem formatu (hh:mm:ss;st za časovne (teki)
    in mm.cm za krajevne (skoki, meti)."""

    vse_discipline = []  # seznam z vsemi disciplinami
    for line in nadseznam:  # gremo po vrsticah in če je dolžina == 1, to pomeni da je vrstica z diciplino in jo zapišemo
        if len(line) == 1:
            line_string = "".join(map(str, line))  # zapišemo vrstico brez [] okoli brez presledka ""
            vse_discipline.append(line_string)  # zapis v seznam

    set_dis = set(vse_discipline)  # set disciplin, tako da se zbrišemo podvojene discipline
    discipline = list(set_dis)  # spravimo set v seznam disciplin
    discipline = definirano_sort_discplin(discipline)  # sortiramo seznam disciplin, tako da je pravilen izpis
    len_dis = len(discipline)
    koncni_seznam = []  # končni seznam ki ga bomo zapisali
    for i in range(len_dis):  # gremo po seznamu disciplin in za vsako disciplino izvedemo zanko
        koncni_seznam.append([discipline[i]])  # najprej zapišemo disciplino
        k1 = 0  # indeks
        list_k = []  # seznam indeksov
        for line in nadseznam:  # gremo po nadseznamu po vsrticah in vsakič ko najdemo disiciplino zapišemo indeks k1 v seznam indeksov
            string = " ".join(map(str, line))  # pretvorimo vrstico iz seznama v string (ni problema z izpisom)
            if string == discipline[i]: list_k.append(k1)
            k1 += 1
        len_k = len(list_k)  # preštejemo kolikokrat smo v nadseznamu našli disciplino
        sortiran_seznam_raz = []  # ustvarimo seznam, ki ga bomo sortirali (krajevni)
        sortiran_seznam_cas = []  # ustvarimo seznam, ki ga bomo sortirali (časovni)
        for j in range(len_k):  # zanka gre čez nadseznam tolikokrat kolikokorat smo našli disciplino v nadseznamu
            k2 = list_k[j] + 1  # indeks, ki kaže na naslednjo vrstico od te v kateri je zapisana disciplina (torej vrstica s prvim rezultatom)
            for line in nadseznam[k2:]:  # začnemo z branjem v zgoraj navedeni vrstici
                if len(line) > 1:  # upoštevamo le vrstico z dolžino daljšo od 1 (torej vrstice z rezultati)
                    del line[0]  # zbrišemo prvi indeks (torej npr. 1., 3., 6., ...) ker bomo morali znova presortirat
                    if regexp.match(line[2]):  # če se format zapisa rezultata ujema z navedenim pod vrhom modula (regexp) ga zapišemo v krajevni del
                        sortiran_seznam_raz.append(line)
                    else: sortiran_seznam_cas.append(line)  # če se format ne ujema je časovni rezultat
                else: break  # če je dolžina 1 ali 0 prekinemo zanko
        sortiran_seznam_cas.sort(key = lambda sortiran_seznam_cas: sortiran_seznam_cas[2])  # sortiramo seznam, da je po vrstnem redu navzgor, za časovne rezultate
        sortiran_seznam_raz.sort(key = lambda sortiran_seznam_raz: sortiran_seznam_raz[2], reverse = True)  # sortiramo seznam, da je po vrstnem redu navzdol, za krajevne rezultate
        sortiran_seznam = sortiran_seznam_cas + sortiran_seznam_raz  # združimo oba dela v en seznam
        m = 1  # indeks za naslednjo zanko
        for line in sortiran_seznam:  # gremo po sortiranem seznamu, kjer so po vsrti zbrani rezultati posamezne discipline
            m_string = str(m) + '.'  # pripravimo string, s katerim bomo zapisali vrstni red (torej 1., 2., 3., ...)
            line.insert(0, m_string)  # vstavimo zgoraj navedeni string na začetek vrstice
            m += 1
        for line in sortiran_seznam:  # pripnemo sortiran seznam za posamezno disciplino v konci seznam za vse discipline
            koncni_seznam.append(line)
        koncni_seznam.append([])  # da je prazna vrstica med disciplinami

    return koncni_seznam


def kategorija(starost):
    """Razvrsti atleta v pravilno kategorijo glede na starost. Vrne se kategorija."""

    """Sprejme en argument (starost) in vrne kategorijo (U12, U14, U16, U18, U20, U23 in ABS(absolutno). Funkcija na koncu
    vrne pravilno kategorijo."""

    kateg = 'ABS'
    if starost < 12: kateg = 'U12'
    elif starost < 14: kateg = 'U14'
    elif starost < 16: kateg = 'U16'
    elif starost < 18: kateg = 'U18'
    elif starost < 20: kateg = 'U20'
    elif starost < 23: kateg = 'U23'
    return kateg


def veljavnost_datuma():
    """Funkcija ki preveri datum."""

    """Če datum ne obstaja, tako dolgo vpisuješ datum, da vneseš mogoč datum. Vrne pravilno vnešen datum."""

    datum = input('Zapiši datum tekmovanja (dd.mm.yyyy): ')  # vnos
    while True:  # preverimo ali je datum pravilen
        try: datetime.datetime.strptime(datum, '%d.%m.%Y')  # pregleda format vnosa
        except ValueError:  # preverim ali datum obstaja
            print('Datum {} ni veljaven.'.format(datum))  # če ni pravilen fromat ali obsteječ datum
            datum = input('Zapiši datum tekmovanja (dd.mm.yyyy): ')  # ponovno vneseš datum
        else: break  # če ni napake gremo iz zanke
    return datum


def preveri_datum(leto):
    """Zapišeš datum tekmovanja in če datum ni pravilen ponoviš vnos. Vrne pravilno vnešen datum."""

    """Funkcija je podobna funkciji veljavnost_datum, s tem da moraš vnesti int argument leto. Zapišeš datum tekmovanja,
     preveri se, če se vpisano leto ujema z vpisanim letom, za katerega vnašaš podatke, na koncu pa preveri še če je
    datum veljaven, tj. če obstaja. Vrne pravilno (obstoječ in pravo leto) vnešen datum."""

    datum = input('Zapiši datum tekmovanja (dd.mm.yyyy): ')  # vnos
    while True:  # preverimo ali je datum pravilen
        try:
            format_datum = datetime.datetime.strptime(datum, '%d.%m.%Y')  # pregleda format vnosa
            datum_year = format_datum.year
            while datum_year != leto:  # ali se vnešen datum ujema z vnešenim na začetku (leto)
                datum = input('Napačno leto. Ponovno zapiši datum tekmovanja (dd.mm.yyyy): ')  # če se leto ne ujema, ponovimo vnos
                format_datum = datetime.datetime.strptime(datum, '%d.%m.%Y')
                datum_year = format_datum.year
        except ValueError:  # preverim ali datum obstaja
            print('Datum {} ni veljaven.'.format(datum))  # če ni pravilen fromat ali obsteječ datum
            datum = input('Zapiši datum tekmovanja (dd.mm.yyyy): ')  # ponovno vneseš datum
        else: break  # če ni napake gremo iz zanke
    return datum


def vpisovanje_razdalja(f, n_rez, leto):
    """Funkcija za vpisovanje dolžinskih rezultatov za eno disiciplino."""

    """Sprejme tri argumente, datoteko v katero vpisuješ, število rezultatov za to disciplino in leto za katero vpisuješ rezultate.
    Funkcija samo vpisuje, ne vrne ničesar."""

    seznam = []  # ustvarimo seznam seznamov ali nadseznam (seznam vseh rezultatov, v posamezne rezultat imamo časovni rezultat, datum in kraj)
    for i in range(n_rez):
        print('Začel boš z vpisovanjem %d. dosežka.' % (i + 1))
        seznam2 = []  # podseznam v katerega se vpisuje trenutni dosežek
        datum = preveri_datum(leto)  # preverimo datum
        kraj = input('Zapiši kraj tekmovanja: ')  # vpišemo kraj tekmovanja
        dvorana = input('Če je tekmovanje potekalo v dvorani napisi D, sicer pa pritisni SPACE in ENTER: ')  # označimo če je tekma potekala v dvorani
        while dvorana != 'D' and dvorana != ' ':  # če vnos ni D ali space
            print('Neveljaven vnos!\n')
            dvorana = input('Če je tekmovanje potekalo v dvorani napisi D, sicer pa pritisni SPACE in ENTER: ')
        m = int(input('Vpiši metre: '))
        cm = int(input('Vpiši centimetre: '))
        while cm > 99:
            print('Neveljaven zapis. Meter nima več kot 100 stotink ...\n')
            cm = int(input('Vpiši centimetre: '))
        rez = cm + 100 * m  # rezultat pretvorimo v eno številko
        # pripnemo rezultat, datum, kraj in dvorano v podseznam
        seznam2.append(rez)
        seznam2.append(datum)
        seznam2.append(kraj)
        seznam2.append(dvorana)
        seznam.append(seznam2)  # ustvarimo nov dosežek v seznamu (rezultat(razdalja), kraj, datum, dvorana) v svojo vrstico
    seznam.sort(reverse=True)  # uredimo seznam po vrsti (po razdalji navzdol)
    # prepišemo urejen seznam v datoteko
    for i in range(n_rez):
        seznam3 = seznam[i]  # odpremo i-ti podseznam (i-ti dosežek)
        # ustvarimo spremenljivke za vpis v dokument iz podseznama
        datum2 = seznam3[1]
        kraj2 = seznam3[2]
        dvorana2 = seznam3[3]
        raz2 = seznam3[0]
        cm = raz2 % 100
        m = int(raz2 / 100)
        f.write('%d.\t%02d,%02d\t%s\t%s\t%s\n' % (i + 1, m, cm, datum2, kraj2, dvorana2))


def vpisovanje_cas(f, n_rez, leto):
    """Funkcija za vpisovanje časovnih rezultatov za eno disciplino."""

    """Sprejme tri argumente, datoteko v katero vpisuješ, število rezultatov za to disciplino in leto za katero vpisuješ rezultate.
    Funkcija samo vpisuje, ne vrne ničesar."""

    seznam = []  # ustvarimo seznam seznamov ali nadseznam (seznam vseh rezultatov, v posamezne rezultat imamo časovni rezultat, datum in kraj)
    for i in range(n_rez):
        print('Začel boš z vpisovanjem %d. dosežka.' % (i + 1))
        seznam2 = []  # podseznam v katerega se vpisuje trenutni dosežek
        datum = preveri_datum(leto)  # preverimo datum
        kraj = input('Zapiši kraj tekmovanja: ')  # vpišemo kraj tekmovanja
        dvorana = input('Če je tekmovanje potekalo v dvorani napisi D, sicer pa pritisni SPACE in ENTER: ')  # označimo če je tekma potekala v dvorani
        while dvorana != 'D' and dvorana != ' ':  # če vnos ni D ali space
            print('Neveljaven vnos!\n')
            dvorana = input('Če je tekmovanje potekalo v dvorani napisi D, sicer pa pritisni SPACE in ENTER: ')
        h = int(input('Vpiši ure: '))
        minu = int(input('Vpiši minute: '))
        # ce nekdo vpiše prevec minut, sekund ali stotink:
        while minu > 59:
            print('Neveljaven zapis. Ura nima več kot 60 minut ...\n')
            minu = int(input('Vpiši minute: '))
        sek = int(input('Vpiši sekunde: '))
        while sek > 59:  # preveč sekund
            print('Neveljaven zapis. Minuta nima več kot 60 sekund ...\n')
            sek = int(input('Vpiši sekunde: '))
        sto = int(input('Vpiši stotinke: '))
        while sto > 99:  # preveč stotink
            print('Neveljaven zapis. Sekunda nima več kot 100 stotink ...\n')
            sto = int(input('Vpiši stotinke: '))
        rez = sto + 100 * sek + 6000 * minu + 360000 * h  # pretvorimo v eno stevilko, nato spravimo vse podatke v podseznam
        # pripnemo rezultat, datum, kraj in dvorano v podseznam
        seznam2.append(rez)
        seznam2.append(datum)
        seznam2.append(kraj)
        seznam2.append(dvorana)
        seznam.append(seznam2)  # ustvarimo nov dosežek v seznamu (čas, kraj, datum, dvorana)
    seznam.sort()  # uredimo seznam po vrsti (po casu navzgor)
    # prepišemo urejen seznam v datoteko
    for i in range(n_rez):
        seznam3 = seznam[i]  # odpremo i-ti podseznam (i-ti dosežek)
        # ustvarimo spremenljivke za vpis v dokument iz podseznama
        datum2 = seznam3[1]
        kraj2 = seznam3[2]
        dvorana2 = seznam3[3]
        t2 = seznam3[0]
        sto = t2 % 100
        t3 = int(t2 / 100)
        sek = t3 % 60
        t4 = int(t3 / 60)
        minu = t4 % 60
        h = int(t4 / 60)
        f.write('%d.\t%02d:%02d:%02d;%02d\t%s\t%s\t%s\n' % (i + 1, h, minu, sek, sto, datum2, kraj2, dvorana2))


def vpisovanje(path_dat, ime, priimek, rojstvo, leto):
    """Funkcija za vpisovanje rezultatov, ki združuje časovne in dolžinske rezultate."""

    """Ta funkcija združuje dolžinske in časovne rezultate. Uporabi se lahko za več disciplin. Argumenti so pot do:
    pot do datoteke in ime datoteke (path_dat), ime atleta, priimek atleta, leto rojstva atleta in leto za katero se 
    vpisuje rezultat. Funkcija samo vpisuje v datoteko, ne vrne ničesar."""

    with open(path_dat, 'w+', encoding='utf-8-sig') as f:  # odpremo odkument
        starost = leto - rojstvo
        kateg = kategorija(starost)  # razvrstimo v kategorije
        f.write('%s %s\t%d\t%d\t%s\n' % (ime, priimek, rojstvo, leto, kateg))  # zapišemo prvo vrstico (header)
        print('Na začetku moraš določiti koliko disciplin boš vpisal in koliko rezultatov v posamezni disciplini.')
        print('Potem boš določil ali boš vpisoval časovne rezultate (teki) ali dolžinske (meti, skoki).')
        print('Program bo vpisoval discipline v enakem vrstnem redu kot se jih bo vnašalo.')
        print('Nato v program vpišeš koliko ur, minut, sekund in stotink je bilo potrebnih za rezultat (če je rezultat krajši od ure ali minute, vpiši 0).'
              '\nOz. v primeru dolžinskih rezultatov vpišeš metre in centimetre.')
        st_dis = int(input('Za koliko različnih disciplin boš vpisoval rezultat?: '))  # določi število disciplin
        for j in range(st_dis):  # gremo po zanki tolikokrat koliko različnih disciplin bomo vpisovali
            disciplina = input('\nZapiši %d. disciplino za katero boš vpisoval rezultate: ' % (j + 1))
            f.write('\n%s\n' % disciplina)
            enote = input('Če je disciplina tek pritisni ENTER, sicer (meti, skoki) vpiši M: ')  # ali boš vpisoval teke ali mete in skoke
            n_rez = int(input('Koliko rezultatov v disciplini boš vpisal?: '))  # število vpisanih rezultatov v disciplini
            if enote == 'M' or enote == 'm':  # rezultati za mete in skoke
                vpisovanje_razdalja(f, n_rez, leto)  # funkcija ki vpiše dolžinske rezultate v datoteko
            else:  # rezultati za teke
                vpisovanje_cas(f, n_rez, leto)  # funkcija ki vpiše časovne rezultate v datoteko
        f.write('\n')  # dodamo prazno vrstico na koncu


def ostevilcenje(seznam):
    """Funkcija, ki vzame neoštevilčen seznam, ga oštevilči in zapiše v skupen seznam(nadseznam), ki ga vrne."""

    """Prvi argument je neoštevilčen, urejen seznam rezultatov v posamezni disciplini, ki ga oštevilčimo (1., 2., 3., ...
     in zapišemo v seznam rezultatov vseh disciplin (nadseznam). Funkcija vrne nadseznam"""

    k_seznam = []  # ustvarimo prazen seznam, za oštevilčenje
    lenght = len(seznam)  # dolžina seznama (torej koliko rezultatov je v disciplini)
    for i in range(lenght):  # gremo po rezultatih v disciplini
        indx = ('%d' + '.') % (i + 1)  # indeksiramo vrstni red (1., 2., 3., ...)
        tmp_seznam = [indx] + seznam[i]  # ustvarimo oštevilčene rezultate
        k_seznam.append(tmp_seznam)  # pripnemo oštevilčene rezultate v skupen seznam
    k_seznam.append([])  # dodamo prazno vrstico za vmesni prostor
    return k_seznam   # vrnemo dopolnjeni nadseznam


def zdruzevanje_razdalja(n_rez, seznam, leto):
    """Funkcija, ki združi in sortira že obstoječe in novo vpisane dolžinske rezultate. Vrne sortiran seznam."""

    """Funkcija združi in sortira že obstoječe in novo vpisane dolžinske rezultate (meti in skoki). Za argumente je 
    potrebno vpisati število novih vnosov v tej disciplini (n_rez), seznam že obstoječih rezultatov (brez oštevilčenja) 
    in leto za katero vnašamo rezultate. Tako sortiran seznam funkcija vrne."""

    for i in range(n_rez):
        seznam2 = []  # seznam za en rezultat
        print('Začel boš z vpisovanjem %d dosežka.' % (i + 1))
        datum = preveri_datum(leto)  # preverimo datum
        kraj = input('Zapiši kraj tekmovanja: ')
        dvorana = input('Če je tekmovanje potekalo v dvorani napisi D, sicer pa pritisni SPACE in ENTER: ')  # označimo če je tekma potekala v dvorani
        while dvorana != 'D' and dvorana != ' ':  # če vnos ni D ali space
            print('Neveljaven vnos!\n')
            dvorana = input('Če je tekmovanje potekalo v dvorani napisi D, sicer pa pritisni SPACE in ENTER: ')
        m = int(input('Vpiši metre: '))
        cm = int(input('Vpiši centimetre: '))
        while cm > 99:
            print('Neveljaven zapis. Meter nima več kot 100 stotink ...\n')
            cm = int(input('Vpiši centimetre: '))
        rez = float(m + cm / 100)  # rezultat pretvorimo v eno številko
        rez = Decimal(rez).quantize(TWOPLACES)  # da se vedno zaokroži na dve decimalki, poglej takoj pod import
        # pripnemo rezultat, datum, kraj in dvorano v skupen seznam
        seznam2.append(rez)
        seznam2.append(datum)
        seznam2.append(kraj)
        seznam2.append(dvorana)
        seznam.append(seznam2)  # dodamo seznam z vsemi podatki rezultata v seznam vseh rezultatov za posamezno disciplino
    seznam.sort(reverse=True)  # sortiramo seznam
    return seznam


def dopisovanje_razdalja(f, nadseznam, reader, writer, disciplina, leto):
    """Funkcija za vpisovanje dolžinskih rezultatov za eno disiciplino."""

    """Sprejme tri argumente, datoteko v katero vpisuješ, število rezultatov za to disciplino in leto za katero vpisuješ
     rezultate. Funkcija samo vpisuje v datoteko, ne vrača ničesar."""

    seznam = []  # ustvarimo seznam seznamov (seznam obstjeečih dosežkov, v posamezne dosežku imamo rezultat, datum in kraj)
    found = False  # iščemo disciplino, ko jo najdemo je found == True
    for line in reader:  # gremo po datoteki od druge vrstice naprej (prvo smo prebrali z next(reader)
        nadseznam.append(line)  # dodamo vrstico v nadseznam
        if line == [disciplina]:  # ko je vrstica enaka disciplini, se found spremeni v True, torej našli smo našo disciplino
            found = True
            print('Program te bo vprašal najprej koliko metrov si potreboval za svoj dosežek in nato centimetrov ter vse to bo združil v en rezultat.')  # za časovne rezultate
            for row in reader:  # gremo po vrsticah od najdene discipline navzdol
                lenght = len(row)  # parameter dolžine vrstice
                if lenght > 1:  # če je dolžina vrstice daljša od 1 (torej več kot en podatek) to pomeni, da je v vrstici rezultat
                    del row[0]  # zbrišemo prvi indeks vrstice (torej 1. , 2., 3., ...), saj bomo rezultate ponovno presortirali
                    seznam.append(row)  # zapišemo rezultate v seznam
                else:  # ko je vrstica dolžine 1 ali manj je zmanjkalo že vpisanih rezultatov, zato se sproži dopisovalec
                    n_rez = int(input('Koliko rezultatov v disciplini boš vpisal?: '))  # število vpisanih rezultatov v disciplini
                    sort_seznam = zdruzevanje_razdalja(n_rez, seznam, leto)  # združeni že vpisani rezultati v seznamu in novi rezultati
                    ostevilcen_seznam = ostevilcenje(sort_seznam)  # naredimo oštevičen seznam
                    nadseznam.append(ostevilcen_seznam)  # pripnemo ostevičen seznam v nadsezam
                    break  # gremo ven iz dopisovalca za posamezno disciplino, nato program dopiše še ostale vrstice za našo disciplino

    if found:  # šli smo čez celo datoteko, našli disciplino, preuredili rezultate za njo in prepisali rezultate za ostale discipline
        f.seek(0)  # kazalnik na začetek dokumenta
        f.truncate()  # izpraznimo datoteko
        writer.writerows(nadseznam)  # zapišemo nadseznam v datoteko

    return found


def zdruzevanje_cas(n_rez, seznam, leto):
    """Funkcija, ki združi in sortira že obstoječe in novo vpisane časovne rezultate. Vrne sortiran seznam."""

    """Funkcija združi in sortira že obstoječe in novo vpisane časovne rezultate (teki). Za argumente je potrebno vpisati
    število novih vnosov v tej disciplini (n_rez), seznam že obstoječih rezultatov (brez oštevilčenja) in leto za katero
    vnašamo rezultate. Tako sortiran seznam funkcija vrne."""

    for i in range(n_rez):
        seznam2 = []  # seznam za en rezultat
        print('Začel boš z vpisovanjem %d dosežka.' % (i + 1))
        datum = preveri_datum(leto)  # preverimo datum
        kraj = input('Zapiši kraj tekmovanja: ')
        dvorana = input('Če je tekmovanje potekalo v dvorani napisi D, sicer pa pritisni SPACE in ENTER: ')  # označimo če je tekma potekala v dvorani
        while dvorana != 'D' and dvorana != ' ':  # če vnos ni D ali space
            print('Neveljaven vnos!\n')
            dvorana = input('Če je tekmovanje potekalo v dvorani napisi D, sicer pa pritisni SPACE in ENTER: ')
        h = int(input('Vpiši ure: '))
        minu = int(input('Vpiši minute: '))
        # ce nekdo vpiše prevec minut, sekund ali stotink
        while minu > 59:
            print('Neveljaven zapis. Ura nima več kot 60 minut ...\n')
            minu = int(input('Vpiši minute: '))
        sek = int(input('Vpiši sekunde: '))
        while sek > 59:
            print('Neveljaven zapis. Minuta nima več kot 60 sekund ...\n')
            sek = int(input('Vpiši sekunde: '))
        sto = int(input('Vpiši stotinke: '))
        while sto > 99:
            print('Neveljaven zapis. Sekunda nima več kot 100 stotink ...\n')
            sto = int(input('Vpiši stotinke: '))
        mikro = 10000 * sto  # potrebujemo mikorosekunde, ker delamo z datetime formatom
        t_m = datetime.time(h, minu, sek, mikro)  # čas z mikrosekundam
        t = t_m.replace(microsecond=round(t_m.microsecond, -4))  # čas v stotinkah (odšetejmo zadnje štiri decimalke)
        rez = t.strftime('%H:%M:%S;%f')[:-4]  # zapišemo čas kot rezultat v pravilen format (v stotinkah)
        # pripnemo rezultat, datum, kraj in dvorano v skupen seznam
        seznam2.append(rez)
        seznam2.append(datum)
        seznam2.append(kraj)
        seznam2.append(dvorana)
        seznam.append(seznam2)  # dodamo seznam z vsemi podatki rezultata v seznam vseh rezultatov za posamezno disciplino
        seznam.sort()
    return seznam  # sortiramo seznam


def dopisovanje_cas(f, nadseznam, reader, writer, disciplina, leto):
    """Funkcija za dopisovanje časovnih rezultatov za eno disiciplino"""

    """Sprejme tri argumente, datoteko v katero vpisuješ, število rezultatov za to disciplino in leto za katero vpisuješ
     rezultate. Funkcija samo vpisuje, ne vrača ničesar."""

    seznam = []  # ustvarimo seznam seznamov (seznam vseh dosežkov, v posamezne dosežku imamo rezultat, datum in kraj)
    found = False  # iščemo disciplino, ko jo najdemo je found == True
    for line in reader:  # gremo po datoteki od druge vrstice naprej (prvo smo prebrali z next(reader)
        nadseznam.append(line)  # dodamo vrstico v nadseznam
        if line == [disciplina]:  # ko je vrstica enaka disciplini, se found spremeni v True, torej našli smo našo disciplino
            found = True
            print('Program te bo vprašal najprej koliko ur si potreboval za svoj dosežek, nato minut, sekund in na koncu stotink in vse to bo združil v en rezultat.')  # za časovne rezultate
            for row in reader:  # gremo po vrsticah od najdene discipline navzdol
                lenght = len(row)  # parameter dolžine vrstice
                if lenght > 1:  # če je dolžina vrstice daljša od 1 (torej več kot en podatek) to pomeni, da je v vrstici rezultat
                    del row[0]  # zbrišemo prvi indeks vrstice (torej 1. , 2., 3., ...), saj bomo rezultate ponovno presortirali
                    seznam.append(row)  # zapišemo rezultate v seznam
                else:  # ko je vrstica dolžine 1 ali manj je zmanjkalo že vpisanih rezultatov, zato se sproži dopisovalec
                    n_rez = int(input('Koliko rezultatov v disciplini boš vpisal?: '))  # število vpisanih rezultatov v disciplini
                    seznam = zdruzevanje_cas(n_rez, seznam, leto)  # združimo nove in stare rezultate v en seznam
                    ostevilcen_seznam = ostevilcenje(seznam)  # naredimo oštevičen seznam
                    for new_line in ostevilcen_seznam:
                        nadseznam.append(new_line)  # pripnemo ostevilčen seznam v nadsezam
                    break  # gremo ven iz dopisovalca za posamezno disciplino, nato program dopiše še ostale vrstice za našo disciplino

    if found:  # šli smo čez celo datoteko, našli disciplino, preuredili rezultate za njo in prepisali rezultate za ostale discipline
        f.seek(0)  # kazalnik na začetek dokumenta
        f.truncate()  # izpraznimo datoteko
        writer.writerows(nadseznam)  # zapišemo nadseznam v datoteko

    return found


def dopisovanje(path_dat, leto):
    """Funkcija dopisovanja rezultatov v datoteko."""

    """Funkcija vzame pot do datoteke in ime datoteke v katero vpisujemo in nato dopisuje bodisi časovne bodisi krajevne
    rezultate v datoteko in zraven sortira rezultate v pravilen vrstni red. Možno je tudi dodajanje novih disciplin."""

    print('Na začetku moraš določiti koliko disciplin boš vpisal in koliko rezultatov v posamezni disciplini.')
    print('Potem boš določil ali boš vpisoval časovne rezultate (teki) ali dolžinske (meti, skoki).')
    print('Program bo vpisoval discipline v enakem vrstnem redu kot so bili vnešeni z vpisovalce\noz. če se jih bo dodali na novo kakor se jih bo vnašalo.')
    print('Nato v program vpišeš koliko ur, minut, sekund in stotink je bilo potrebnih za rezultat (če je rezultat krajši od ure ali minute, vpiši 0).\n'
          'Oz. v primeru dolžinskih rezultatov vpišeš metre in centimetre.')
    st_dis = int(input('Za koliko različnih disciplin boš vpisoval rezultat?: '))  # določi število disciplin, ki jih bomo vpisovali
    for j in range(st_dis):  # zanka po disciplinah, v tem programu bo malo drugačen pristop, za vsako disciplino se bo odprlo datoteko in zapisalo posodobljene podatke
        with open(path_dat, 'r+', newline='', encoding='utf-8-sig') as f:  # odpremo odkument v r+, da se ne zbriše napisano (w) ali da ne dodajamo na koncu(a)
            reader = csv.reader(f, delimiter='\t')  # bralec datoteke
            writer = csv.writer(f, delimiter='\t')  # zapisovalec datoteke
            line1 = next(reader)  # preberemo prvo vrstico
            nadseznam = [line1]  # ustvarimo nadseznam, ki ga bomo zapisovali v datoteko
            disciplina = input('\nZapiši %d. disciplino za katero boš vpisoval rezultate: ' % (j + 1))  # zapišemo disciplino za kateri bomo dopisovali rezultate
            enote = input('Če je disciplina tek pritisni ENTER, sicer (meti, skoki) vpiši M: ')  # ali boš vpisoval teke ali mete in skoke
            if enote == 'M' or enote == 'm': found = dopisovanje_razdalja(f, nadseznam, reader, writer, disciplina, leto)  # uporabimo funkcijo za dopisovanje v datoteko, odvisno od izbire
            else: found = dopisovanje_cas(f, nadseznam, reader, writer, disciplina, leto)

            if found is False:  # discipline še ni v datoteki, torej je ali napaka pri vnosu ali pa jo dodamo
                dodati = input('Ta disciplina še ni vpisana. Jo želiš dodati(pritisni D za da in karkoli za ne): ')
                if dodati == 'D' or dodati == 'd':  # če se jo želi dodati
                    nadseznam.append([disciplina])
                    seznam = []  # prazen seznam, v katerega bomo pisali rezultate
                    n_rez = int(input('Koliko rezultatov v disciplini boš vpisal?: '))
                    if enote == 'M' or enote == 'm': sort_seznam = zdruzevanje_razdalja(n_rez, seznam, leto)  # funkcija za vpisovanje, je del dopisovanje_razdalje, vendar rabimo samo del za vpisovnje,
                    # ne rabimo še primerjavo z ostalimi rezultati v disciplini (ker jih ni)
                    else: sort_seznam = zdruzevanje_cas(n_rez, seznam, leto)
                    ostevilcen_seznam = ostevilcenje(sort_seznam)  # naredimo oštevičen seznam
                    for line in ostevilcen_seznam:
                        nadseznam.append(line)  # pripnemo ostevičen seznam v nadsezam
                    f.seek(0)  # kazalnik na začetek datoteke
                    f.truncate()  # spraznimo datoteko
                    writer.writerows(nadseznam)  # zapišemo nadseznam
                    continue  # gremo v drug krog zanke, ko dodamo
                else:
                    break  # če nočemo nič dodajat in gremo direkt iz zanke


def najboljsi_izid_disciplina(seznam):
    """Funkcija s katero razberemo najboljši rezultat v disciplini."""

    """Ta funckija sprejme že sortiran seznam rezultatov. Nato prebere vrstice z disciplinami in jih nato združi s prvo
    vrstico rezultatov (= najboljši rezultat) v eno vrstico. Vrne seznam v katarem so vse discipline in vnešenega seznama
    in najboljši rezultati."""

    i = 0  # vrstični indeks
    izpis_seznam = []  # pripravimo za seznam za izpis
    for line in seznam[:-1]:  # gremo po seznamu do predzadnje vrstice (zadnja je prazna)
        lenght = len(line)  # dolžina vrstice
        if lenght == 1:  # če je dolžina == 1, potem je to vrstica z disciplino
            del seznam[i + 1][0]  # zbrišemo oštevičenje naslednje vrstice (vrstica z najboljšim rezultatom)
            string = "".join(map(str, line))  # spravimo vrstico v string
            seznam[i + 1].insert(0, string)  # združimo vrstcio z disciplino (spredaj) in najboljši rezultat
            izpis_seznam.append(seznam[i + 1])  # pripnemo tako združeno vrstico v končni seznam (za izpis)
        i += 1

    return izpis_seznam


def kategoriziranje(seznam, leto, mejna_starost):
    """Funkcija, ki briše rezultate atletov starejših od določene kategorije oz. starosti."""

    """Funkcija sprejme seznam v katerem so sortirani rezultati v absolutni kategoriji, leto za katero delamo kategorizacijo
    in zgornjo mejno starost kategorije (tj. starost ob prestopu, torej za U12 je ta starost 12. Vrne se sortiran seznam,
    kjer so izbrisani rezultati, ki ne ustrezajo tej kategoriji."""

    tmp_seznam = []  # začasen seznam
    for line in seznam:
        if len(line) > 1:  # ko je rezultat
            rojstvo = int(line[2])  # preberemo leto rojstva
            starost = leto - rojstvo  # izračunamo starost
            if starost >= mejna_starost: del line  # če je starost izven kategorije izbrišemo vrstico
            else: tmp_seznam.append(line)  # sicer prepišemo
        else: tmp_seznam.append(line)

    j = 1  # indeksa zanke
    urejen_seznam = []  # končni seznam
    for line in tmp_seznam[1:]:
        if len(tmp_seznam[j]) == 1 and len(tmp_seznam[j + 1]) == 0:  # če je disiciplina brez rezultata brišemo str disciplino in eno vrstico zgoraj
            del urejen_seznam[-1]
        else: urejen_seznam.append(line)  # sicer samo prepišemo
        j += 1

    konec_seznam = []
    disciplina_seznam = []
    m = 0
    while m in range(len(urejen_seznam)):  # po indeksu seznama
        if len(urejen_seznam[m]) == 1:   # ko imamo disciplino jo zapišemo
            konec_seznam.append(urejen_seznam[m])
            for row in urejen_seznam[m+1:]:   # zapišemo vse rezultate v disiciplini, brez originalnega oštevilčenja (row[0])
                if len(row) > 1:
                    del row[0]
                    disciplina_seznam.append(row)
                    m += 1
                else: break
            disciplina_seznam = ostevilcenje(disciplina_seznam)  # ponovno oštevilčimo seznam
            for line in disciplina_seznam:  # zapišemo v končni seznam
                konec_seznam.append(line)
        disciplina_seznam = []   # spraznimo seznam za naslednjo disciplino
        m += 1

    return konec_seznam
