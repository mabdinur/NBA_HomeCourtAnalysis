import _sqlite3

class Tabledb:
    ins_sql = {"ratings": "INSERT INTO ratings(rank,team,conf,div,wins,losses,winloss,mov,ortg,drtg,nrtg,mov_a,ortg_a,drtg_a,nrtg_a,year) Values",
               "team_splits": "INSERT INTO team_splits(team,location,type,rating,year,win,loss,fg,fga,three_pt,three_pa,ft,fta,orb,trb,ast,stl,blk,tov,pf,pts) Values"}

    create_sql = {"ratings": """Create table ratings (id  INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER, rank INTEGER, 
                             team VARCHAR(255), conf CHAR(1), div 	VARCHAR(2), wins    INTEGER,
                             losses  INTEGER,winloss  DECIMAL(4,3),mov DECIMAL(4,2), ortg DECIMAL(5,2),
                             drtg DECIMAL(5,2), nrtg DECIMAL(5,2),mov_a DECIMAL(4,2), ortg_a DECIMAL(5,2), 
                             drtg_a DECIMAL(5,2), nrtg_a DECIMAL(4,2) )""",
                  #G	W	L	FG	FGA	3P	3PA	FT	FTA	ORB	TRB	AST	STL	BLK	TOV	PF	PTS
               "team_splits": """Create table team_splits
                           ( id  INTEGER PRIMARY KEY AUTOINCREMENT, team TEXT,year INTEGER, location TEXT,type TEXT, rating DECIMAL(4,1),
                             win INTEGER, loss INTEGER, fg DECIMAL(3,1), fga DECIMAL(4,1), three_pt DECIMAL(3,1), 
                             three_pa DECIMAL(3,1), ft DECIMAL(3,1), fta DECIMAL(3,1), orb DECIMAL(3,1), trb DECIMAL(3,1),
                             ast DECIMAL(3,1), stl DECIMAL(3,1), blk DECIMAL(3,1), tov DECIMAL(3,1), pf DECIMAL(3,1), 
                             pts DECIMAL(4,1))"""}


    def __init__(self, db_name = "NBA_Data_TEST2" ):
        self.conn = _sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create(self, table_name, sql_str=""):
        if sql_str == "":
            sql_str = Tabledb.create_sql[table_name]

        try:
            sql_str1 = "DROP table " + table_name
            self.cur.execute(sql_str1)
            self.conn.commit()
        except:
            pass

        self.cur.execute(sql_str)
        self.conn.commit()

    def insert(self, data:[], table_name):
        data = tuple(data)
        print(data)
        sql_str = Tabledb.ins_sql[table_name] + str(data)
        #print(sql_str)
        self.cur.execute(sql_str)
        self.conn.commit()

    def select(self, table_name, col_names = "*", where_clause=""):
        sel_str = "SELECT DISTINCT " + col_names + " FROM " + table_name + " " + where_clause
        foo = self.cur.execute(sel_str)
        return foo.fetchall()


