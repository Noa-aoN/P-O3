def check_spelbord(bord):
    for rij in bord:
        test = ""
        for i in rij:
            test = test + i
        if "XXXX" in test or "OOOO" in test:
            return True
    for i in range(len(bord[0])):
        kolom = []
        for rij in bord:
            kolom.append(rij[i])
        test = ""
        for i in kolom:
            test = test + i
        if "XXXX" in test or "OOOO" in test:
            return True
    beginposities_schuin = [[0,0],[0,1],[0,2],[0,3],[1,0],[2,0]]
    for beginpos in beginposities_schuin:
        test = ""
        i= 0
        while i+beginpos[1] != len(bord[0]) and i+beginpos[0] != len(bord):
            test = test+bord[beginpos[0]+i][beginpos[1]+i]
            i+=1
        if "XXXX" in test or "OOOO" in test:
            return True
    beginposities_andere_schuin = list(map(lambda pos: [pos[0],len(bord[0])-pos[1]-1],beginposities_schuin))
    for beginpos in beginposities_andere_schuin:
        test = ""
        i= 0
        while beginpos[1]-i != -1 and i+beginpos[0] != len(bord):
            test = test+bord[beginpos[0]+i][beginpos[1]-i]
            i+=1
        if "XXXX" in test or "OOOO" in test:
            return True
    return False



def vind_y(x,bord):
    kolom = []
    for rij in bord:
        kolom.append(rij[x])
    i = 5
    while i>=0:
        if kolom[i] == " ":
            return i
        i -= 1
    return -1


bord = [[" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "]]
for i in bord:
    print(i)
gewonnen = False
speler = 1
while gewonnen == False:
    if speler == 1:
        print("speler 1 is aan de beurt")
    else:
        print("speler 2 is aan de beurt")
    x = int(input("in welke kolom wilt ge uw ding zetten:"))-1
    while not 0<=x<=6:
        print("pipo doe eens fatsoenlijk")
        x = int(input("in welke kolom wilt ge uw ding zetten:"))-1
    while vind_y(x,bord)==-1:
        print("sorry deze kolom is al vol probeer opnieuw")
        x = int(input("in welke kolom wilt ge uw ding zetten:")) - 1
        while not 0 <= x <= 6:
            print("pipo doe eens fatsoenlijk")
            x = int(input("in welke kolom wilt ge uw ding zetten:")) - 1
    if speler == 1:
        y = vind_y(x,bord)
        bord[y][x] = "X"
    else:
        y = vind_y(x, bord)
        bord[y][x] = "O"
    gewonnen = check_spelbord(bord)
    if gewonnen:
        print("speler",speler,"wint!")
    if speler == 1:
        speler = 2
    else:
        speler = 1
    for i in bord:
        print(i)
input("Press enter to exit ;)")