from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
from dbread import Tabledb
from nba_math import defrating as defr, offrating as offr
#from mytable import Table


class Scrape(object):

    def __init__(self, url, team=""):
        request = urlopen(url)
        page_html = request.read()
        self.soup = BeautifulSoup(page_html, "html.parser")
        request.close()
        self.team = team

    def get_table(self, table_name, year):
        tb = self.soup.find("table", id=table_name)
        #data_set = []
        #data = self.get_header(tb)
        tbdb = Tabledb()
        #head = self.get_header(tb)
        #ratings_table = Table(head)

        for row in tb.find_all("tr"):
            #print(row)
            if table_name == "team_splits":
                data = self.__row_home_away(row)
            else:
                data = self.__all_rows(row)

            #ratings_table.add_entry(data)
            self.append_table(tbdb, data + [year], table_name)
            #data_set.append(data)

        #ratings_table.print()
        tbdb.select(table_name)
        #print(data_set)
        #print(tb)
    def __all_rows(self,row):
        data = []
        for entry in row.find_all():
            if entry.name == "td" or entry.name == "th":
                data.append(entry.text)
        return data

    def __row_home_away(self,row):
        data = self.__all_rows(row)
        if "Home" in data or "Road" in data:
            return data
        else:
            return []

    def __format_row(self, data, id):
        if id == "team_splits":
           return data[1:19]
        else:
            return data

    def get_header(self, table):
        header = list()
        if table:
            row1 = table.find("tr")
            for entry in row1.find_all("th"):
                    header.append(entry.text)
        return header

    def append_table(self, dbtb:Tabledb, data:list, table_name):
        try:
            if len(data) < 2:
                return
            elif "Team" in data:
                return
            elif table_name == "team_splits":
                defence = defr(data[20], data[25], data[30], data[24], data[32])
                offence = offr(data[6], data[11], data[16], data[10], data[18])
                data1 = [self.team] +[data[1]] +  ["off"] + [offence] + [data[33]] + data[3:19]
                dbtb.insert(data1, table_name)
                data2 = [self.team] + [data[1]] + ["def"] + [defence] + [data[33]] + data[3:5] + data[19:33]
                dbtb.insert(data2, table_name)
            else:
                dbtb.insert(data, table_name)
        except:
            dbtb.create(table_name)