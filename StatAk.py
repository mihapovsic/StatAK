import os
import csv
import glob
import statakmodul as sm


def Vpisovalec(path):
    """Vpisovanje rezultatov."""

    """Vpisovanje rezultatov za enega atleta in eno leto. Možno je vpisati tako razdalje kot čase. Generira se datoteka atleta oblike spol_ime_priimek_leto.txt.
    Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za vpis atletskih rezultatov!')
    print('Program bo ustvaril datoteko v katero bodo vpisani vsi atletovi rezultati v določenem letu.')
    print('Program je namenjem vnosu individualanih rezultatov, ne štafetnih.')
    print('V program boš najprej vpisal par osnovnih podatkov, preko katerih se ustvari datoteka z rezultati.')
    dokument = True  # indeks s katerim pogledamo če dokument ki ga hočemo ustvariti že obstaja
    while dokument:  # če dokument obstaja gremo v novo zanko, saj načeloma nočemo prepisati datoteke
        # podatki za ustrezno poimenovanje dokumenta(spol_ime_priimek_leto.txt)
        spol = input('Vpiši spol atleta/atletinje(m za moškega in ž za ženskega): ')
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        ime = input('Vpiši ime atleta/atletinje: ')
        priimek = input('Vpiši priimek atleta/atletinje: ')
        rojstvo = int(input('Vpiši leto rojstva atleta/atletinje: '))  # za pravilno razvrstitev v kategorijo
        leto = int(input('Vpiši leto za katero boš vpisoval rezultate: '))
        str_leto = str(leto)
        out_dat = '{}_{}_{}_{}.txt'.format(spol, ime, priimek, str_leto)
        path_out_dat = os.path.join(path, out_dat)  # pot in datoteka, ki jih bomo odprli
        if os.path.isfile(path_out_dat) is False:  # če še ni datoteke na zgoraj navedni poti
            dokument = False  # dokumenta ni bilo, zato začnemo lahko vpisovati, potem pa gremo ven iz while zanke
            sm.vpisovanje(path_out_dat, ime, priimek, rojstvo, leto)  # funkcija za vpisovanje podatkov
            print('Podatki so uspešno vpisani v spodnjo datoteko: ')  # pokaže datoteko v katero smo napisali rezultate
            print(path_out_dat)

        else:  # če pot in datoteka obstajata
            p_vnos = input('Ta atlet ima že ustvarjeno datoteko. Poglej če si se zmotil pri vpisu zgornjih podatkov ali pa uporabi dopisovalec rezultatov!'
                           '\nPritisni V za vnovičen vnos(popravek), P za prepis datoteke oz. karkoli drugega za izhod iz programa: ')
            if p_vnos == 'V' or p_vnos == 'v': continue  # če smo se zmotili pri vnosu podatkov, ponovimo vnos, gremo na začetek while zanke
            elif p_vnos == 'P' or p_vnos == 'p':  # če se nismo zmotili pri vnosu in bomo prepisali že obstojočo datoteko
                sm.vpisovanje(path_out_dat, ime, priimek, rojstvo, leto)  # funkcija za vpisovanje podatkov
                print('Podatki so uspešno vpisani v spodnjo datoteko: ')  # pokaže datoteko v katero smo napisali rezultate
                print(path_out_dat)
                break
            else: break  # če se nismo zmotili pri vnosu in zapustimo program

    input('\nPritisni karkoli za izhod iz programa!')


def Dopisovalec(path):
    """Dopisovanje rezultatov."""

    """Dopisovanje rezultatov za enega atleta in eno leto. Možno je vpisati tako razdalje kot čase. Predhodno mora biti generirana datoteka oblike spol_ime_priimek_leto.txt.
    Ni možno generiranje novih datotek. Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za vpis atletskih rezultatov!')
    print('Atlet mora imeti že ustvarjeno datoteko za posamezno leto za vpisovanje.')
    print('V program boš najprej vpisal par osnovnih podatkov, preko katerih se poišče datoteko z rezultati.')
    dokument = False  # indeks s katerim pogledamo če dokument ki ga hočemo ustvariti že obstaja
    while dokument is False:  # če dokument ne obstaja gremo v novo zanko, saj potrebujemo dokument za dopisovanje
        # podatki za ustrezno poimenovanje dokumenta(spol_ime_priimek_leto.txt)
        spol = input('Vpiši spol atleta/atletinje(m za moškega in ž za ženskega): ')
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        ime = input('Vpiši ime atleta/atletinje: ')
        priimek = input('Vpiši priimek atleta/atletinje: ')
        leto = int(input('Vpiši leto za katero boš vpisoval rezultate: '))
        str_leto = str(leto)
        out_dat = '{}_{}_{}_{}.txt'.format(spol, ime, priimek, str_leto)
        path_out_dat = os.path.join(path, out_dat)  # ime datoteke + pot
        if os.path.isfile(path_out_dat):  # pot in datoteka obstajata
            dokument = True  # našli smo dokument, tako da gremo lahko ven iz zanke
            print('Dokument za vpisovanje je bil najden.')
            sm.dopisovanje(path_out_dat, leto)
            print('Podatki so uspešno dopisani v spodnjo datoteko: ')  # pokaže datoteko v katero so se dopisali rezultati
            print(path_out_dat)

        else:
            p_vnos = input('Ta atlet še nima dokumenta. Če si se zmotil pri vnosu zgornjih podatkov pritisni V, sicer pa pritisni karkoli za izhod in uporabi vpisovalca: ')
            if p_vnos == 'V' or p_vnos == 'v': continue  # če smo se zmotili pri vnosu in bomo ponovno vnesli podatke
            else: break

    input('\nPritisni karkoli za izhod iz programa!')


def Zdruzevalec_solo(path):
    """Združevanje rezultatov za enega atleta za več let."""

    """Združevanje vseh rezultatov za enega atleta in več let. Generira se datoteka atleta oblike ALL_spol_ime_priimek.txt.
    Predhodno mora obstajati datoteka iz vpisovanja (spol_ime_priimek_leto.txt) za vsaj eno leto.
    Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za izpis vseh rezultatov posameznega atleta v eno datoteko!')
    print('Atlet mora imeti že ustvarjene datoteke z rezultati v posameznem letu.')
    print('Po vnosu se ti bo izpisala pot do datotek in vse datoteke, ki jih je program prebral.')
    while True:  # nastavimo zanko, ki teče dokler ne najdemo vsaj enega dokumenta
        spol = input('Vpiši spol atleta/atletinje (m za moškega in ž za ženskega): ')
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        ime = input('Vpiši ime atleta/atletinje: ')
        priimek = input('Vpiši priimek atleta/atletinje: ')
        in_dat = '{}_{}_{}_*.txt'.format(spol, ime, priimek)
        path_in_dat = os.path.join(path, in_dat)  # pot in datoteke, ki jih bomo odprli
        files = [f for f in glob.glob(path_in_dat)]  # poiščemo vse dokumente ki ustrezajo vpis podatkom in jih vpišemo v seznam
        if len(files) > 0: break  # če ima dolžina seznama datotek vsaj en vnos, potem smo našli vsaj en dokument in gremo ven iz zanke
        else:  # seznam datotek je prazen
            print('Ta atlet še nima datotek!')
            p_vnos = input('Če želiš ponovno vnesti začetne podatke vpiši V, sicer pritisni karkoli: ')  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            if p_vnos == 'V' or p_vnos == 'v': continue  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            else:
                input('Pritisni karkoli za izhod iz programa!')
                exit()  # izhod iz programa

    nadseznam = []
    print('\nPrebrane datoteke: ')  # izpišejo se vse prebrane datoteke in poti do njih
    for f in files:
        print(f)  # izpis vseh dokumentov, ki jih bomo prebrali
        with open(f, 'r', encoding='utf-8-sig') as reader:  # odpremo z formatom UTF8
            csv_reader = csv.reader(reader, delimiter='\t')
            seznam = list(csv_reader)  # datoteko pretvorimo v seznam
            for line in seznam[2:]:  # beremo samo od druge vrstice naprej (samo rezultate)
                nadseznam.append(line)  # vsako vrstico zapišemo v nadseznam, po dvojni zanki imamo v nadseznamu seznam vseh rezultatov iz vseh datotek

    koncni_seznam = sm.sortiranje_disciplin(nadseznam)

    out_dat = 'ALL_{}_{}_{}.txt'.format(spol, ime, priimek)
    path_out_dat = os.path.join(path, out_dat)  # pot in datoteka v katero bomo pisali
    with open(path_out_dat, 'w+', newline='', encoding='utf-8-sig') as writer:  # odpremo končno .txt datoteko (defirano v kodi, vrstica 18), hkrati ne dodajamo nove vrstice!(newline='')
        csv_writer = csv.writer(writer, delimiter='\t')  # nastavimo delimiter (tab)
        print('\nNova datoteka z združenimi rezultati: ')  # izpiše se datoteka v katero so združeni rezultati atleta
        print(path_out_dat)
        ime = seznam[0][0]  # ime in priimek
        rojstvo = seznam[0][1]  # leto rojstva
        writer.write('%s\t%s\n\n' % (ime, rojstvo))  # zapišemo v header

        for line in koncni_seznam:  # zapišemo končni seznam v datoteko
            csv_writer.writerow(line)

    input('\nPritisni karkoli za izhod iz programa!')


def Rekordi_sezona_solo(path):
    """Najboljši rezultati enega atleta za eno leto."""

    """Izpis najboljših sezonskih (letnih) rezultatov atleta v vseh disciplinah v katerih je nastopal. Generira se datoteka atleta oblike SR_spol_ime_priimek_leto.txt.
    Predhodno mora obstajati datoteka iz vpisovanja (spol_ime_priimek_leto.txt) za želeno leto. Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za izpis najboljših rezultatov sezone za posameznega atleta!')
    print('Atlet mora imeti že ustvarjeno datoteko z vsemi rezultati v letu.')
    print('V program boš najprej vpisal par osnovnih podatkov, preko katerih se poišče datoteka z rezultati.')
    dokument = False  # indeks s katerim pogledamo če dokument ki ga hočemo ustvariti že obstaja
    while dokument is False:  # če dokument ne obstaja gremo v novo zanko, saj potrebujemo dokument za dopisovanje
        # podatki za ustrezno poimenovanje dokumenta(spol_ime_priimek_leto.txt)
        spol = input('Vpiši spol atleta/atletinje(m za moškega in ž za ženskega): ')
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        ime = input('Vpiši ime atleta/atletinje: ')
        priimek = input('Vpiši priimek atleta/atletinje: ')
        vnos = input('Če želiš izpis najboljših rezultatov sezone za vsa leta, ki so že zapisana v datotekah, pritisni karkoli.\nČe pa želiš izpis le za posamezno leto vpiši V: ')
        if vnos == 'V' or vnos == 'v':
            leto = int(input('Vpiši leto za katero boš iskal najboljše rezultate sezone: '))
            str_leto = str(leto)  # zapišemo string, da lahko ustvarimo ime datoteke (ker z int ga ne moremo)
            in_dat = '{}_{}_{}_{}.txt'.format(spol, ime, priimek, str_leto)  # ime datoteke iz katere črpamo podatke
            path_in_dat = os.path.join(path, in_dat)  # ime datoteke + pot
            if os.path.isfile(path_in_dat):  # pot in datoteka obstajata
                dokument = True  # našli smo dokument, tako da gremo lahko ven iz zanke
                with open(path_in_dat, 'r', encoding='utf-8-sig') as reader:  # odpremo z formatom UTF8
                    csv_reader = csv.reader(reader, delimiter='\t')  # prebermo datoteko
                    seznam = list(csv_reader)  # datoteko pretvorimo v seznam
                    header = seznam[0]  # leto rojstva iz prve vrstice
                    str_header = "  ".join(map(str, header))  # header pretvorimo v string za zapis
                    koncni_seznam = sm.najboljsi_izid_disciplina(seznam)  # pripravimo za zapis s funkcijo ki vrne disciplino in najboljši rezultat v disciplini

                out_dat = 'SR_{}_{}_{}_{}.txt'.format(spol, ime, priimek, str_leto)
                path_out_dat = os.path.join(path, out_dat)  # pot in datoteka v katero bomo pisali
                with open(path_out_dat, 'w+', newline='', encoding='utf-8-sig') as writer:  # odpremo končno .txt datoteko, hkrati ne dodajamo nove vrstice!(newline=''), v UTF8
                    csv_writer = csv.writer(writer, delimiter='\t')  # nastavimo delimiter (tab)
                    writer.write(str_header)  # zapišemo header definiran v vrstici 33
                    writer.write('\n\n')  # dve prazni vrstici med headerjem in rezultati
                    for line in koncni_seznam:  # zapišemo končni seznam v datoteko
                        csv_writer.writerow(line)

                print('Najboljši rezultati v letu {} za atleta {} {} so zapisani v spodnjo datoteko: '.format(str_leto, ime, priimek))  # pokaže datoteko v katero so se dopisali rezultati
                print(path_out_dat)

            else:
                p_vnos = input('Ta atlet še nima dokumenta za navedeno leto. Če si se zmotil pri vnosu zgornjih podatkov pritisni V, sicer pa pritisni karkoli in uporabi vpisovalca za vpis podatkov: ')
                if p_vnos == 'V' or p_vnos == 'v': continue  # če smo se zmotili pri vnosu in bomo ponovno vnesli podatke
                else: exit()  # izhod iz programa

        else:
            in_dat = '{}_{}_{}_*.txt'.format(spol, ime, priimek)  # ime datoteke iz katere črpamo podatke
            path_in_dat = os.path.join(path, in_dat)  # ime datoteke + pot
            files = [f for f in glob.glob(path_in_dat)]  # poiščemo vse dokumente ki ustrezajo vpis podatkom in jih vpišemo v seznam
            if len(files) > 0:  # če ima dolžina seznama datotek vsaj en vnos, potem smo našli vsaj en dokument in nadaljujemo z zanko
                dokument = True  # našli smo dokument, tako da gremo lahko ven iz zanke
                print('Najboljši rezultati za atleta {} {} so zapisani v spodnjih datotekah: '.format(ime, priimek))  # pokaže datoteke v katero so se dopisali rezultati
                for f in files:
                    with open(f, 'r', encoding='utf-8-sig') as reader:  # odpremo z formatom UTF8
                        str_leto = str(f)[-8:-4]  # iz imena datoteke izpišemo datum
                        csv_reader = csv.reader(reader, delimiter='\t')  # prebermo datoteko
                        seznam = list(csv_reader)  # datoteko pretvorimo v seznam
                        header = seznam[0]  # leto rojstva iz prve vrstice
                        str_header = "  ".join(map(str, header))  # header pretvorimo v string za zapis
                        koncni_seznam = sm.najboljsi_izid_disciplina(seznam)  # pripravimo za zapis s funkcijo ki vrne disciplino in najboljši rezultat v disciplini

                    out_dat = 'SR_{}_{}_{}_{}.txt'.format(spol, ime, priimek, str_leto)
                    path_out_name = os.path.join(path, out_dat)  # pot in datoteka v katero bomo pisali
                    with open(path_out_name, 'w+', newline='', encoding='utf-8-sig') as writer:  # odpremo končno .txt datoteko (defirano v kodi, vrstica 18), hkrati ne dodajamo nove vrstice!(newline=''), v UTF8
                        csv_writer = csv.writer(writer, delimiter='\t')  # nastavimo delimiter (tab)
                        writer.write(str_header)  # zapišemo header definiran v vrstici 30
                        writer.write('\n\n')  # dve prazni vrstici med headerjem in rezultati
                        for line in koncni_seznam:  # zapišemo končni seznam v datoteko
                            csv_writer.writerow(line)
                    print(path_out_name)

            else:  # seznam datotek je prazen
                print('Ta atlet še nima datotek!')
                p_vnos = input('Če želiš ponovno vnesti začetne podatke vpiši V, sicer pritisni karkoli za izhod: ')  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
                if p_vnos == 'V' or p_vnos == 'v': continue  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
                else: break

    input('\nPritisni karkoli za izhod iz programa!')


def Osebni_rekordi(path):
    """Osebni rekordi atleta."""

    """Izpis najboljših rezultatov atleta v vseh disciplinah v katerih je nastopal. Generira se datoteka atleta oblike OR_spol_ime_priimek.txt.
    Predhodno mora obstajati datoteka funkcije Zdruzevalec_solo tj. vsi rezultati atleta (ALL_spol_ime_priimek.txt). 
    Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za izpis osebnih rekordov posameznega atleta!')
    print('Atlet mora imeti že ustvarjeno datoteko z vsemi rezultati za vsa leta.')
    print('V program boš najprej vpisal par osnovnih podatkov, preko katerih se poišče datoteka z rezultati.')
    dokument = False  # indeks s katerim pogledamo če dokument ki ga hočemo ustvariti že obstaja
    while dokument is False:  # če dokument ne obstaja gremo v novo zanko, saj potrebujemo dokument za dopisovanje
        # podatki za ustrezno poimenovanje dokumenta(spol_ime_priimek_leto.txt)
        spol = input('Vpiši spol atleta/atletinje(m za moškega in ž za ženskega): ')
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        ime = input('Vpiši ime atleta/atletinje: ')
        priimek = input('Vpiši priimek atleta/atletinje: ')
        in_dat = 'ALL_{}_{}_{}.txt'.format(spol, ime, priimek)  # ime datoteke iz katere črpamo podatke
        path_in_dat = os.path.join(path, in_dat)  # ime datoteke + pot
        if os.path.isfile(path_in_dat):  # pot in datoteka obstajata
            dokument = True  # našli smo dokument, tako da gremo lahko ven iz zanke
            with open(path_in_dat, 'r', encoding='utf-8-sig') as reader:  # odpremo z formatom UTF8
                csv_reader = csv.reader(reader, delimiter='\t')  # prebermo datoteko
                seznam = list(csv_reader)  # datoteko pretvorimo v seznam
                header = seznam[0]  # leto rojstva iz prve vrstice
                str_header = "  ".join(map(str, header))  # header pretvorimo v string za zapis
                koncni_seznam = sm.najboljsi_izid_disciplina(seznam)  # pripravimo za zapis s funkcijo ki vrne disciplino in najboljši rezultat v disciplini

            out_dat = 'OR_{}_{}_{}.txt'.format(spol, ime, priimek)
            path_out_dat = os.path.join(path, out_dat)  # pot in datoteka v katero bomo pisali
            with open(path_out_dat, 'w+', newline='', encoding='utf-8-sig') as writer:  # odpremo končno .txt datoteko, hkrati ne dodajamo nove vrstice!(newline=''), v UTF8
                csv_writer = csv.writer(writer, delimiter='\t')  # nastavimo delimiter (tab)
                writer.write(str_header)  # zapišemo header definiran v vrstici 33
                writer.write('\n\n')  # dve prazni vrstici med headerjem in rezultati
                for line in koncni_seznam:  # zapišemo končni seznam v datoteko
                    csv_writer.writerow(line)

            print('Osebni rekordi za atleta {} {} so zapisani v spodnjo datoteko: '.format(ime, priimek))  # pokaže datoteko v katero so se dopisali rezultati
            print(path_out_dat)

        else:
            p_vnos = input('Ta atlet še nima dokumenta za navedeno leto. Če si se zmotil pri vnosu zgornjih podatkov pritisni V, sicer pa pritisni karkoli in uporabi vpisovalca: ')
            if p_vnos == 'V' or p_vnos == 'v': continue  # če smo se zmotili pri vnosu in bomo ponovno vnesli podatke
            else: break

    input('\nPritisni karkoli za izhod iz programa!')


def Vsi_sezona(path):
    """Vsi rezultati atletov v enem letu."""

    """Izpis vseh rezultatov atletov v vseh disciplinah v enem letu. Generira se datoteka oblike kategorija_spol_leto.txt.
    Predhodno mora obstajati datoteka vpisovanja za vsaj enega atleta (spol_ime_priimek_leto.txt). Izpišejo se tudi najboljši rezultati po posameznih kategorijah
    (ABS, U23, U20, U18, U16, U14, U12). Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za izpis vseh rezultatov posameznega spola v eni sezoni!')
    print('Obstajati mora že vsaj ena ustvarjena datoteke z rezultati atleta v tej sezni.')
    print('Po vnosu spola se ti bo izpisala pot do datotek in vse datoteke, ki jih je program prebral.')
    while True:  # nastavimo zanko, ki teče dokler ne najdemo vsaj enega dokumenta
        spol = input('Vpiši spol za katerega boš izpisal vse rezultate (m za moškega in ž za ženskega): ')
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        leto = int(input('Vpiši leto za katero boš iskal najboljše rezultate sezone: '))
        str_leto = str(leto)  # zapišemo string, da lahko ustvarimo ime datoteke (ker z int ga ne moremo)
        in_dat = '{}_*_{}.txt'.format(spol, str_leto)
        path_in_dat = os.path.join(path, in_dat)  # pot in datoteka, ki jih bomo odprli
        files = [f for f in glob.glob(path_in_dat)]  # poiščemo vse dokumente ki ustrezajo vpis podatkom in jih vpišemo v seznam
        if len(files) > 0:  # če ima dolžina seznama datotek vsaj en vnos, potem smo našli vsaj en dokument in nadaljujemo s programom
            nadseznam = []  # ustvarimo nadseznam v katerega bomo vpisovali vse datoteke
            print('\nPrebrane datoteke: ')  # izpišejo se vse prebrane datoteke in poti do njih
            for f in files:
                print(f)  # izpis vseh dokumentov, ki jih bomo prebrali
                with open(f, 'r', encoding='utf-8-sig') as reader:  # odpremo z formatom UTF8
                    csv_reader = csv.reader(reader, delimiter='\t')
                    seznam = list(csv_reader)  # datoteko pretvorimo v seznam
                    ime = seznam[0][0]  # ime in priimek iz prve vrstice
                    rojstvo = seznam[0][1]  # leto rojstva iz prve vrstice
                    ime_str = "".join(map(str, ime))  # pretvorimo vrstico iz seznama v string (ni problema z izpisom), brez presledka ""
                    rojstvo_str = "".join(map(str, rojstvo))
                    for line in seznam[2:]:  # beremo samo od druge vrstice naprej (samo rezultate)
                        if len(line) > 1:  # če je dolžina vrstice > 1, tj. nek rezultat vpišemo vmes ime in priimek in leto rojstva (spodnji dve vrstici)
                            line.insert(1, rojstvo_str)
                            line.insert(1, ime_str)
                            nadseznam.append(line)
                        else: nadseznam.append(line)  # vsako vrstico ki ni rezultat samo prepišemo

            koncni_seznam = sm.sortiranje_disciplin(nadseznam)

            out_dat = 'UABS_{}_{}.txt'.format(spol, str_leto)  # ustvarimo datotoko, kjer bodo vsi rezultati ne glede na kategorijo
            path_out_dat = os.path.join(path, out_dat)  # pot in datoteka v katero bomo pisali
            with open(path_out_dat, 'w+', newline='', encoding='utf-8-sig') as writer:  # odpremo končno .txt datoteko (defirano v kodi, vrstica 18), hkrati ne dodajamo nove vrstice!(newline=''), v UTF8
                csv_writer = csv.writer(writer, delimiter='\t')  # nastavimo delimiter (tab)
                print('\nNove datoteka z združenimi rezultati: ')  # izpiše se datoteka v katero so združeni rezultati atletov
                print(path_out_dat)
                if spol == 'm': spol_str = 'moške'
                else: spol_str = 'ženske'
                header = 'Vsi rezultati AK Sevnica v letu {} za {}.'.format(str_leto, spol_str)  # prva vrstica dokumenta, odvisna od spola in leta
                writer.write(header + '\n\n')  # zapišemo header definiran zgoraj

                for line in koncni_seznam:  # zapišemo končni seznam v datoteko
                    csv_writer.writerow(line)

            kategorije = {'U23': 23, 'U20': 20, 'U18': 18, 'U16': 16, 'U14': 14, 'U12': 12}  # slovar kategorija : starost ob preskoku kategorije
            for item in kategorije:  # gremo po posamezni kategoriji
                maxstr = (kategorije[item])  # starost pri kateri atlet izpade iz kategorije, vrednost v slovarju
                str_kateg = str(kategorije[item])  # string, za zapis
                with open(path_out_dat, 'r', newline='', encoding='utf-8-sig') as kat_reader:  # preberemo datoteko z absolutnimi rezultati, ki smo je prej generirali
                    # začetek je isti kot pri absolutni kategoriji
                    kat_csv_reader = csv.reader(kat_reader, delimiter='\t')
                    kat_seznam = list(kat_csv_reader)
                    leto = int(str_leto)

                    konec_seznam = sm.kategoriziranje(kat_seznam, leto, maxstr)  # seznam iz katerega so zbrisani rezultati, ki ne ustrezajo kategoriji

                    kat_name = 'U{1}_{0}_{2}.txt'.format(spol, str_kateg, str_leto)  # ime datoteke za pisanje
                    path_kat_dat = os.path.join(path, kat_name)  # pot in datoteka v katero bomo pisali

                    with open(path_kat_dat, 'w+', newline='', encoding='utf-8-sig') as kat_writer:
                        print(path_kat_dat)  # da se vidi v katere datoteke pišemo
                        kat_csv_writer = csv.writer(kat_writer, delimiter='\t')
                        if spol == 'm': spol_str = 'moške'
                        else: spol_str = 'ženske'
                        header = 'Vsi rezultati AK Sevnica v letu {} za {} U{}.'.format(str_leto, spol_str, str_kateg)  # prva vrstica dokumenta, odvisna od spola,leta in kategorije
                        kat_writer.write(header + '\n\n')  # zapišemo header definiran zgoraj

                        for line in konec_seznam:  # zapišemo končni ("konec") seznam v datoteko
                            kat_csv_writer.writerow(line)

                path_out_dat = path_kat_dat  # beremo iz prejšnje (višje) kategorije, ne iz ABS za naslednji cikel zanke

            p_vnos = input('\nČe želiš nadaljevati z novim spolom/letom pritisni V, sicer pritisni enter: ')
            if p_vnos == 'V' or p_vnos == 'v': continue

            else:
                input('\nPritisni karkoli za izhod iz programa!')
                exit()

        else:  # seznam datotek je prazen
            print('Za ta spol in leto še ni datotek!')
            p_vnos = input('Če želiš ponovno vnesti začetne podatke vpiši V, sicer pritisni karkoli: ')  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            if p_vnos == 'V' or p_vnos == 'v': continue  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            else: break

    input('\nPritisni karkoli za izhod iz programa!')


def Zdruzevalec_multi(path):
    """Vsi rezultati vseh atletov."""

    """Izpis vseh rezultatov atletov v vseh disciplinah. Generira se datoteka oblike spol_kategorija_ALL.txt.
    Predhodno mora obstajati datoteka za vsaj eno leto z vsemi rezultati (funkcija Vsi_sezona oblika kategorija_spol_leto.txt). 
    Izpišejo se tudi najboljši rezultati po posameznih kategorijah (ABS, U23, U20, U18, U16, U14, U12). 
    Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za izpis vseh rezultatov posameznega spola v eno datoteko!')
    print('Obstajati mora že ustvarjena datoteke z vsemi rezultati vsaj za eno leto.')
    print('Po vnosu spola se ti bo izpisala pot do datotek in vse datoteke, ki jih je program prebral.')
    spol = input('Vpiši spol za katerega boš izpisal vse rezultate (m za moškega in ž za ženskega): ')
    while True:  # nastavimo zanko, ki teče dokler ne najdemo vsaj enega dokumenta
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        if spol == 'm': spol_str = 'moške'
        else: spol_str = 'ženske'
        vse_kategorije = ['UABS', 'U23', 'U20', 'U18', 'U16', 'U14', 'U12']  # seznam vseh kategorij
        input('V naslednjem koraku izbiraš za katere kategorije bo program izpisal vse rezultate.')  # v naslednjih korakih lahko izbiraš za katere kategorije boš izdelal datoteko z vsemi rezultati
        vnos1 = input('Če želiš izbirati kategorije napiši V sicer (za izpis vseh kategorij) pritisni karkoli: ')
        if vnos1 == 'v' or vnos1 == 'V':
            kategorije = []
            for item in kategorije:
                vnos2 = input('Če boš izbral kategorijo {} pritisni D, sicer pritisni N: '.format(item))
                while vnos2 != 'D' and vnos2 != 'N':
                    print('Napačen vnos. Pritisni D (ne mali d) ali N!')
                    vnos2 = input('Če boš izbral kategorijo {} pritisni D, sicer pritisni N: '.format(item))
                if vnos2 == 'D': kategorije.append(item)
                elif vnos2 == 'N': continue

        else: kategorije = vse_kategorije

        ni_dat = 0  # števec za kategorije, kjer ne najdemo datotek
        for item in kategorije:
            kategorija = item  # kategorija je element seznama kategorij, po katerem gremo v zanki
            in_dat = '{}_{}_*.txt'.format(kategorija, spol)
            path_in_dat = os.path.join(path, in_dat)  # pot in datoteka, ki jih bomo odprli
            files = [f for f in glob.glob(path_in_dat)]  # poiščemo vse dokumente ki ustrezajo vpis podatkom in jih vpišemo v seznam
            if len(files) > 0:  # če ima dolžina seznama datotek vsaj en vnos, potem smo našli vsaj en doukment
                nadseznam = []  # ustvarimo nadseznam v katerega bomo vpisovali vse datoteke
                print('\nPrebrane datoteke: ')  # izpišejo se vse prebrane datoteke in poti do njih
                for f in files:
                    print(f)  # izpis vseh dokumentov, ki jih bomo prebrali
                    with open(f, 'r', encoding='utf-8-sig') as reader:  # odpremo z formatom UTF8
                        csv_reader = csv.reader(reader, delimiter='\t')
                        seznam = list(csv_reader)  # datoteko pretvorimo v seznam
                        for line in seznam[2:]:  # beremo samo od druge vrstice naprej (samo rezultate)
                            nadseznam.append(line)  # prepišemo vrstice v nadseznam

                koncni_seznam = sm.sortiranje_disciplin(nadseznam)

                out_dat = '{1}_{0}_ALL.txt'.format(kategorija, spol)
                path_out_dat = os.path.join(path, out_dat)  # pot in datoteka v katero bomo pisali
                with open(path_out_dat, 'w+', newline='', encoding='utf-8-sig') as writer:  # odpremo končno .txt datoteko, hkrati ne dodajamo nove vrstice!(newline=''), v UTF8
                    csv_writer = csv.writer(writer, delimiter='\t')  # nastavimo delimiter (tab)
                    print('\nNova datoteka z združenimi rezultati: ')  # izpiše se datoteka v katero so združeni rezultati atletov
                    print(path_out_dat)
                    header = 'Najboljši rezultati AK Sevnica za {} {}.'.format(spol_str, kategorija)  # prva vrstica dokumenta, odvisna od spola
                    writer.write(header + '\n\n')  # zapišemo header

                    for line in koncni_seznam:  # zapišemo končni seznam v datoteko
                        csv_writer.writerow(line)

            else:  # seznam datotek je prazen
                ni_dat += 1
                print('\nZa {} v kategoriji {} še ni datotek!\n'.format(spol_str, kategorija))

        if ni_dat == 7:  # če ni datotek za nobeno kategorijo
            input('Za ta spol ni datotek!')
            p_vnos = input('Če želiš ponovno vnesti začetni spol vpiši V, sicer pritisni karkoli: ')  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            if p_vnos == 'V' or p_vnos == 'v': continue  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            else:
                input('Pritisni karkoli za izhod iz programa!')
                exit()  # izhod iz programa

        else: break  # če smo našli vsaj za eno kategorijo datoteko gremo ven iz programa

    input('\nPritisni karkoli za izhod iz programa!')


def Rekordi_sezona_multi(path):
    """Najboljši sezonski (letni) izid v vseh disciplinah."""

    """Izpis najboljših rezultatov atletov v klubu v vseh disciplinah. Generira se datoteka oblike SR_kategorija_spol_leto.txt.
    Predhodno mora obstajati datoteka za vsaj eno leto z vsemi rezultati (funkcija Vsi_sezona oblika kategorija_spol_leto.txt). 
    Izpišejo se tudi najboljši rezultati po posameznih kategorijah (ABS, U23, U20, U18, U16, U14, U12). 
    Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za izpis najboljših rezultatov sezone za posamezen spol!')
    print('Spol mora imeti že ustvarjeno datoteko za vsaj eno kategorijo z vsemi rezultati v letu.')
    dokument = False  # indeks s katerim pogledamo če dokument ki ga hočemo ustvariti že obstaja
    while dokument is False:  # če dokument ne obstaja gremo v novo zanko, saj potrebujemo dokument za dopisovanje
        # podatki za ustrezno poimenovanje dokumenta(spol_ime_priimek_leto.txt)
        spol = input('Vpiši spol atleta/atletinje(m za moškega in ž za ženskega): ')
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        if spol == 'm': spol_str = 'moške'
        else: spol_str = 'ženske'
        leto = int(input('Vpiši leto za katero boš iskal najboljše rezultate sezone: '))
        str_leto = str(leto)  # zapišemo string, da lahko ustvarimo ime datoteke (ker z int ga ne moremo)
        kategorije = ['UABS', 'U23', 'U20', 'U18', 'U16', 'U14', 'U12']
        ni_dat = 0  # števec za kategorije, kjer ne najdemo datotek
        for item in kategorije:
            kategorija = item  # kategorija je v seznamu vseh kategorij po katerih gre zanka
            in_dat = '{}_{}_{}.txt'.format(kategorija, spol, str_leto)  # ime datoteke iz katere črpamo podatke
            path_in_dat = os.path.join(path, in_dat)  # ime datoteke + pot
            if os.path.isfile(path_in_dat):  # pot in datoteka obstajata
                dokument = True  # našli smo dokument, tako da gremo lahko ven iz zanke ko dokončamo pisanje
                with open(path_in_dat, 'r', encoding='utf-8-sig') as reader:  # odpremo z formatom UTF8
                    csv_reader = csv.reader(reader, delimiter='\t')  # prebermo datoteko
                    seznam = list(csv_reader)  # datoteko pretvorimo v seznam
                    seznam = seznam[1:]  # beremo od prve vrstice naprej, ker drugače nam naša funkcija najboljsi_izidi_disciplina vrže error, ker je prva vrstica dolga == 1
                    header = 'Najboljši rezultati AK Sevnica v letu {} za {} {}.'.format(str_leto, spol_str, kategorija)  # prva vrstica dokumenta, odvisna od spola in leta
                    koncni_seznam = sm.najboljsi_izid_disciplina(seznam)  # pripravimo za zapis s funkcijo ki vrne disciplino in najboljši rezultat v disciplini

                out_dat = 'SR_{}_{}_{}.txt'.format(kategorija, spol, str_leto)
                path_out_dat = os.path.join(path, out_dat)  # pot in datoteka v katero bomo pisali
                with open(path_out_dat, 'w+', newline='', encoding='utf-8-sig') as writer:  # odpremo končno .txt datoteko, hkrati ne dodajamo nove vrstice!(newline=''), v UTF8
                    csv_writer = csv.writer(writer, delimiter='\t')  # nastavimo delimiter (tab)
                    writer.write(header)  # zapišemo header definiran v vrstici 33
                    writer.write('\n\n')  # dve prazni vrstici med headerjem in rezultati
                    for line in koncni_seznam:  # zapišemo končni seznam v datoteko
                        csv_writer.writerow(line)

                print('Najboljši rezultati v letu {} za {} {} so zapisani v spodnjo datoteko: '.format(str_leto, spol_str, kategorija))  # pokaže datoteko v katero so se dopisali rezultati
                print(path_out_dat)

            else:  # dokument ne obstaja
                ni_dat += 1
                print('Ta spol v kategoriji {} še nima datoteke za to leto!'.format(kategorija))

        if ni_dat == 7:  # če ni datotek za nobeno kategorijo
            input('Za ta spol ni datotek!')
            p_vnos = input('Če želiš ponovno vnesti začetni spol vpiši V, sicer pritisni karkoli: ')  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            if p_vnos == 'V' or p_vnos == 'v': continue  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            else:
                input('Pritisni enter za karkoli iz programa!')
                exit()  # izhod iz programa

    input('\nPritisni enter za izhod!')


def Klubski_rekordi(path):
    """Najboljši izid v disciplini vseh disciplinah."""

    """Izpis klubskih v vseh disciplinah. Generira se datoteka oblike KR_kategorija_spol.txt.
    Predhodno mora obstajati datoteka z vsemi rezultati (funkcija Zdruzevalec_multi oblika spol_kategorija_ALL.txt). 
    Izpišejo se tudi najboljši rezultati po posameznih kategorijah (ABS, U23, U20, U18, U16, U14, U12). 
    Argument, ki ga funkcija sprejme je pot do direktorija, kjer je datoteka."""

    print('Dobrodošel v program za izpis klubskih rekordov za posamezen spol in kategorijo!')
    print('Spol in kategorija morata imeti že ustvarjeno datoteko z vsemi rezultati.')
    dokument = False  # indeks s katerim pogledamo če dokument ki ga hočemo ustvariti že obstaja
    while dokument is False:  # če dokument ne obstaja gremo v novo zanko, saj potrebujemo dokument za dopisovanje
        # podatki za ustrezno poimenovanje dokumenta(spol_ime_priimek_leto.txt)
        spol = input('Vpiši spol za katerega računaš klubske rekorde(m za moškega in ž za ženskega): ')
        while spol != 'm' and spol != 'ž':
            spol = input('Napačna oznaka, poskusi ponovno: ')
        if spol == 'm': spol_str = 'moške'
        else: spol_str = 'ženske'
        kategorije = ['UABS', 'U23', 'U20', 'U18', 'U16', 'U14', 'U12']
        ni_dat = 0  # števec za kategorije, kjer ne najdemo datotek
        for item in kategorije:
            kategorija = item  # kategorija je element v seznamu kategorije po katerem gre zanka
            in_dat = '{}_{}_ALL.txt'.format(spol, kategorija)  # ime datoteke iz katere črpamo podatke
            path_in_dat = os.path.join(path, in_dat)  # ime datoteke + pot
            if os.path.isfile(path_in_dat):  # pot in datoteka obstajata
                dokument = True  # našli smo dokument, tako da gremo lahko ven iz zanke
                with open(path_in_dat, 'r', encoding='utf-8-sig') as reader:  # odpremo z formatom UTF8
                    csv_reader = csv.reader(reader, delimiter='\t')  # prebermo datoteko
                    seznam = list(csv_reader)  # datoteko pretvorimo v seznam
                    seznam = seznam[1:]  # beremo od prve vrstice naprej, ker drugače nam naša funkcija najboljsi_izidi_disciplina vrže error, ker je prva vrstica dolga == 1
                    koncni_seznam = sm.najboljsi_izid_disciplina(seznam)  # pripravimo za zapis s funkcijo ki vrne disciplino in najboljši rezultat v disciplini

                out_dat = 'KR_{}_{}.txt'.format(kategorija, spol)  # ime datoteke v katero zapisujemo
                path_out_dat = os.path.join(path, out_dat)  # pot in datoteka v katero bomo pisali
                with open(path_out_dat, 'w+', newline='', encoding='utf-8-sig') as writer:  # odpremo končno .txt datoteko, hkrati ne dodajamo nove vrstice!(newline=''), v UTF8
                    csv_writer = csv.writer(writer, delimiter='\t')  # nastavimo delimiter (tab)
                    header = 'Klubski rekordi AK Sevnica za {} {}.'.format(spol_str, kategorija)  # prva vrstica dokumenta, odvisna od spola in leta
                    writer.write(header)  # zapišemo header definiran zgoraj
                    writer.write('\n\n')  # dve prazni vrstici med headerjem in rezultati
                    for line in koncni_seznam:  # zapišemo končni seznam v datoteko
                        csv_writer.writerow(line)

                print('Klubski rekordi za {} {} so zapisani v spodnjo datoteko: '.format(spol_str, kategorija))  # pokaže datoteko v katero so se dopisali rezultati
                print(path_out_dat)

            else:  # dokument ne obstaja
                ni_dat += 1
                print('Ta spol v kategoriji {} še nima datoteke z vsemi podatku!'.format(kategorija))

        if ni_dat == 7:  # če ni datotek za nobeno kategorijo
            input('Za ta spol ni datotek!')
            p_vnos = input('Če želiš ponovno vnesti začetni spol vpiši V, sicer pritisni karkoli: ')  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            if p_vnos == 'V' or p_vnos == 'v': continue  # če se zmotiš pri vnosu, pritisneš V, če ne pritisneš karkoli
            else:
                input('Pritisni enter za izhod iz programa!')
                exit()  # izhod iz programa

    input('\nPritisni karkoli za izhod!')
