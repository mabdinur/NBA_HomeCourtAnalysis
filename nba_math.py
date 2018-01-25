
def offrating(fgt, orb, tov, fta, pts):
    poss = float(fgt) + float(orb) - float(tov) + 0.4*float(fta)
    return (float(pts)/poss)*100


def defrating(fgt, orb, tov, fta, pts):
    return float(pts)*100/(float(fgt) + float(orb) - float(tov) + 0.4*float(fta))


def trueshooting(fga, fta, pts):
    tsa = float(fga) + 0.44*float(fta)
    return float(pts)/(2*tsa)

