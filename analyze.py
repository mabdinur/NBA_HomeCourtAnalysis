from dbread import Tabledb
import matplotlib.pyplot as plt
from nba_math import trueshooting


class HomeAway:

    def __init__(self, dbname=""):
        if dbname == "":
            self.db = Tabledb()
        else:
            self.db = Tabledb(dbname)

    def __extract(self, table_name="team_splits", columns="location,type,rating,year,win,loss", where=""):
        try:
            data = self.db.select(table_name, columns, where)
            return data
        except:
            print("ERROR", "HOMEAWAY __Extract can't select table cuz it DNE")
            return None

    def calculate_winloss(self):
        data = self.__extract("team_splits", "location,year,win,loss" )
        home = dict()
        away = dict()
        for row in data:
            wl = round(row[2]/(row[2]+row[3]),3)

            if row[0].lower() == "home":
                dict1 = home
                home[row[1]] = self.__append_to_list(dict1, row[1], wl)
            else:
                dict1= away
                away[row[1]] = self.__append_to_list(dict1, row[1], wl)

        print(home)
        print(away)
        home = self.__avg_dictlists(home)
        away = self.__avg_dictlists(away)
        return home,away

    def calculate_winloss_dif(self):
        data = self.__extract("team_splits", "location,year,win,loss" )
        home = dict()
        away = dict()
        for row in data:
            wl = round(row[2]/(row[2]+row[3]),3)

            if row[0].lower() == "home":
                dict1 = home
                home[row[1]] = self.__append_to_list(dict1, row[1], wl)
            else:
                dict1= away
                away[row[1]] = self.__append_to_list(dict1, row[1], wl)

        print(home)
        print(away)
        home = self.__avg_dictlists(home)
        away = self.__avg_dictlists(away)

        diff = dict()
        for key1 in away.keys():
            diff[key1] = home[key1] - away[key1]

        return diff,diff
    def __calc_rating(self, where):
        data = self.__extract("team_splits", "location,year,type,rating", where)

        home = dict()
        away = dict()
        for row in data:
            if row[0].lower() == "home":
                home[row[1]] = row[3]
            elif row[0].lower() == "road":
                away[row[1]] = row[3]
        return home, away

    def calculate_defrating(self):
        return self.__calc_rating("WHERE type = \'def\'")

    def calculate_offrating(self):
        return self.__calc_rating("WHERE type = \'off\'")

    def calculate_margin_victory(self):
        defence = self.calculate_defrating()
        offence = self.calculate_offrating()
        home = dict()
        away = dict()
        for year in defence[0].keys():
            margin = offence[0][year] - defence[0][year]
            dict1 = home
            home[year] = self.__append_to_list(dict1, year, margin)

            margin = offence[1][year] - defence[1][year]
            dict1 = away
            away[year] = self.__append_to_list(dict1, year, margin)

        home = self.__avg_dictlists(home)
        away = self.__avg_dictlists(away)
        return home,away

    def calculate_trueshooting(self):
        data = self.__extract("team_splits", "location,year,fga,fta,pts,team", "WHERE type = \'off\'")

        home = dict()
        away = dict()

        for row in data:
            if row[0].lower() == "home":
                ts = trueshooting(row[2], row[3], row[4])
                temp_dict = home
                home[row[1]] = self.__append_to_list(temp_dict, row[1], ts)
            elif row[0].lower() == "road":
                ts = trueshooting(row[2], row[3], row[4])
                temp_dict = away
                away[row[1]] = self.__append_to_list(temp_dict, row[1], ts)

        home = self.__avg_dictlists(home)
        away = self.__avg_dictlists(away)
        print(home)
        print(away)
        return home, away

    def __append_to_list(self, dict1:dict,key, item):
        if key not in dict1:
            dict1[key] = [item]
        else:
            #print(dict1[key], item)
            dict1[key].append(item)
        return dict1[key]

    def __avg_dictlists(self, dict1):
        for key in dict1.keys():
            temp_list = dict1[key]
            #print(dict1[key])
            #print(key)
            #print(type(temp_list))
            dict1[key] = sum(temp_list)/len(temp_list)
        return dict1




class Visualize:

    def __init__(self):
        self.ha = HomeAway()


    def ___create_line_graph(self, home, away, team="SAS", data_type="Win/Loss Percentage"):
        x1, y1 = zip(*home.items())
        x2, y2 = zip(*away.items())
        fig = plt.figure()
        for a in x1,y1:
            print(a)

        plt.scatter(x1, y1,marker="X", c="r", alpha=0.5, label="Home" )
        plt.scatter(x2, y2, marker="o", c="b", alpha=0.5, label= "Away")
        plt.legend(loc="lower right")
        self.__set_axis(y1,y2,x1,x2,data_type)
        plt.xlabel("Year")
        plt.ylabel(data_type)
        plt.title(team + " " + data_type)
        fig.canvas.set_window_title("NBA Analysis")
        plt.show()
        #fig.savefig(team + " " + data_type)

    def __set_axis(self,y1,y2,x1,x2,data_type):
        true_ymin = min(y1 + y2)
        true_ymax = max(y1 + y2)

        if "shooting" in data_type.lower():
            plt.ylim([true_ymin - 0.1, true_ymax + 0.1])
            print("yay shoot")
        elif "margin" in data_type.lower():
            plt.ylim([true_ymin - 1, true_ymax + 1])
        elif "%" in data_type.lower():
            plt.ylim([0, 1])
        else:
            plt.ylim([true_ymin - 1, true_ymax + 1])

        plt.xlim([min(x1 + x2) - 1, max(x1 + x2) + 1])

    def show_winloss(self,team):
        home,away = self.ha.calculate_winloss()
        self.___create_line_graph(home, away,team,"Win/Loss(%)")

    def show_margin_victory(self,team=""):
        home, away = self.ha.calculate_margin_victory()
        self.___create_line_graph(home, away,team,"Margin of Victory")

    def show_trueshooting(self,team=""):
        home, away = self.ha.calculate_trueshooting()
        self.___create_line_graph(home, away,team,"True shooting (%)")

    def show_diff_win_loss(self, team=""):
        diff1, diff2 = self.ha.calculate_winloss_dif()
        self.___create_line_graph(diff1, diff2, team, "Home - Away Win Percentage (%)")







vs = Visualize()
#vs.show_winloss("ALL Teams")
#vs.show_trueshooting("ALL Teams")
#vs.show_margin_victory("ALL Teams")
vs.show_diff_win_loss()
#ha = HomeAway()
#print(ha.calculate_margin_victory())




