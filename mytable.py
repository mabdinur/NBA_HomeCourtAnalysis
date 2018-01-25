class Table:

    def __init__(self, headers:[]):
        self.data = []

    def add_entry(self, row:[]):
        if row is not []:
            self.data.append(row)

    def row(self, team_name:str):
        for row in self.data:
            if team_name.lower() in row[1].lower():
                return row

    def column(self, col_name):
        i = self.data[0].index(col_name)
        column = list()
        for row in self.data:
            col = {row[0] : row[i]}
            column.append(col)
        return column

    def print(self):
        for row in self.data:
            for item in row:
                print(item, "\t", end="")
            print("\n")