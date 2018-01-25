from collect_data import Scrape

def create_table(url, table_id):
    teams = ["ATL","BRK","BOS","CHA","CHI","CLE","DAL","DEN","DET","GSW",
             "HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOH","NYK",
             "OKC","ORL","PHI","PHO","POR","SAC","SAS","TOR","UTA","WAS",
             "VAN", "NOH", "NOK", "SEA", "WSB", "NJN", "CHH"]

    expansion_teams = ["NOP", "NOK", "MEM", "VAN","TOR", "OKC", "SEA", "WAS", "WSB", "BRK", "NJN", "CHH", "CHA", "NOH"]

    for year in range(2001, 2018):
        for team in teams:
            url_i = url.replace("$$$$", str(year)).replace("^^^^", team)
            if team in expansion_teams:
                url_i = find_expansion_url(year, team, url_i)

            if url_i != "Not Valid":
                sc = None
                try:
                    sc = Scrape(url_i, team)
                    print(url_i)
                    sc.get_table(table_id, year)
                    print(year, "This year was added")
                except:
                    print(year, "ERROR")

#mn = Tabledb()
#mn.select()

def find_team():
    pass

def find_expansion_url(year:int, team:str, url):

    if year < 1989:
        return "Not Valid"
    elif team.upper() == "MEM" and year > 2001:
        return url
    elif team.upper() == "VAN" and 1995 > year > 2002:
        return url
    elif team.upper() == "NOP" and year > 2013 :
        return url
    elif team.upper() == "NOH" and 2007 < year < 2014:
        return url
    elif team.upper() == "NOK" and  2004 < year < 2008:
        return url
    elif team.upper() == "NOP" and 2002 < year < 2005:
        return url
    elif team.upper() == "TOR" and year > 1996:
        return url
    elif team.upper() == "OKC" and year > 2008:
        return url
    elif team.upper() == "SEA" and year < 2009:
        return url
    elif team.upper() == "WAS" and year > 1997:
        return url
    elif team.upper() == "WSB" and year < 1998:
        return url
    elif team.upper() == "NJN" and year < 2014:
        return url
    elif team.upper() == "BRK" and year > 2013:
        return url
    elif team.upper() == "CHH" and 1988 < year < 2003:
        return url
    elif team.upper() == "CHA" and year > 2004:
        return url
    else:
        return "Not Valid"



#create_table("https://www.basketball-reference.com/leagues/NBA_" + "$$$$" + "_ratings.html", "ratings")
create_table("https://www.basketball-reference.com/teams/^^^^/" + "$$$$" + "/splits/", "team_splits")
