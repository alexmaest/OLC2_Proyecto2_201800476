class Error():
    def __init__(self, description, enviroment, row, column, type):
        self.description = description
        self.enviroment = enviroment
        self.row = row
        self.column = column
        self.type = type