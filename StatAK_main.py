import StatAk

direktorij = 'C:\\Users\\miha\\Desktop\\Python projekti\\Python_38\\Projekt_StatAK\\StatAK\\Datoteke\\'  # pot do dokumentov  # nastavi pot do mape kjer so datoteke

print('Dobrodšel v statistični aplikaciji za atletske rezultate.')
print('Izbiraš lahko med različnimi programi v aplikaciji.')
while True:
    izbira1 = int(input('Za vpisovanje rezultatov pritisni 1. Za sortiranje in ustvarjanje/posodabljene datotek za enega atleta pritisni 2.'
                        '\nZa sortiranje in ustvarjanje/posodabljene datotek za več atletov pritisni 3. Če želiš zapustiti aplikacijo pritisni 4: '))
    while izbira1 != 1 and izbira1 != 2 and izbira1 != 3 and izbira1 != 4:
        izbira1 = int(input('Napačen vnos! Ponovi vnos (1 za vpisovanje, 2 za enega atleta, 3 za več atletov, 4 za izhod): '))
    if izbira1 == 1:
        print('Izbiraš lahko med vpisovalcem (za atlete, ki še nimajo datoteke za določeno leto) ali dopisovalcem (za atlete ki že imajo tako datoteko.')
        izbira2 = int(input('Če boš izbral vpisovalca vpiši 1, če pa dopisovalca vpiši 2: '))
        while izbira2 != 1 and izbira2 != 2:
            izbira2 = int(input('Napačen vnos! Ponovi vnos (1 za vpisovanje, 2 za dopisovanje): '))
        if izbira2 == 1: StatAk.Vpisovalec(direktorij)
        else: StatAk.Dopisovalec(direktorij)

    elif izbira1 == 2:
        print('Za enega atleta lahko izbiraš med ustvarjanjem/posodobitvijo datoteke s programi za vse rezultate atleta (pritisni 1),'
              '\nnajboljšimi rezultati v letu (pritisni 2) in osebnimi rekordi (pritisni 3).')
        izbira2 = int(input('Če boš izbral program za vse rezultate vpiši 1, če samo najboljše rezultate v letu pritisni 2 in če osebne rekorde pritisni 3: '))
        while izbira2 != 1 and izbira2 != 2 and izbira2 != 3:
            izbira2 = int(input('Napačen vnos! Ponovi vnos (1 za vpisovanje, 2 za dopisovanje): '))
        if izbira2 == 1: StatAk.Zdruzevalec_solo(direktorij)
        elif izbira2 == 2: StatAk.Rekordi_sezona_solo(direktorij)
        else: StatAk.Osebni_rekordi(direktorij)

    elif izbira1 == 3:
        print('Za več atletov lahko izbiraš med ustvarjanjem/posodobitvijo datoteke s programi za vse rezultate v enem letu (pritisni 1),'
              '\nza vse za vse rezultate v vseh letih(pritisni 2), najboljšimi rezultati v letu (pritisni 3)'
              '\nin klubskimi rekordi (pritisni 4).')
        izbira2 = int(input('Če boš izbral program za vse rezultate v enem letu vpiši 1, če za vse rezultate vpiši 2,\n'
                            'če najboljše rezultate v letu pritisni 3 in klubske rekorde pritisni 4: '))
        while izbira2 != 1 and izbira2 != 2 and izbira2 != 3 and izbira2 != 4:
            izbira2 = int(input('Napačen vnos! Ponovi vnos (1 za vpisovanje, 2 za dopisovanje): '))
        if izbira2 == 1: StatAk.Vsi_sezona(direktorij)
        elif izbira2 == 2: StatAk.Zdruzevalec_multi(direktorij)
        elif izbira2 == 3: StatAk.Rekordi_sezona_multi(direktorij)
        else: StatAk.Klubski_rekordi(direktorij)

    else: break

    p_vnos = input('\nČe želiš uporabiti kak drug program vpiši V, sicer pritisni karkoli: ')
    if p_vnos == 'V' or p_vnos == 'v': continue
    else: break

print('\nAdijo!')
