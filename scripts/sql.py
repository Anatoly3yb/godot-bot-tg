import sqlite3 as sq

class sqlDB:
    dbPath: str = "database/stats.db"

    with sq.connect(dbPath) as db:
        c = db.cursor()
    

    def getData(self, tableName: str) -> list:
        self.c.execute("SELECT * FROM %s" % (tableName))

        result: list = []
        for idx in self.c.fetchone():
            result.append(idx)

        return result


    def getDatas(self, tableName: str, limit: int) -> list:
            self.c.execute("SELECT * FROM %s LIMIT %s" % (tableName, limit))

            result: list = []
            for item in self.c.fetchall():
                result.append(item)

            return result

    def getFilterDatas(self, tableName: str, filterName: str, limit: int) -> list:
        self.c.execute("SELECT * FROM %s WHERE sub='%s' LIMIT %s" % (tableName, filterName, limit))

        result: list = []
        for item in self.c.fetchall():
            result.append(item)
        
        return result


    def incrementValue(self, tableName: str, paramName: str, rowid: int = 1) -> None:
        self.c.execute("UPDATE %s SET %s = %s+1 WHERE rowid = %s" % (tableName, paramName, paramName, rowid))
        self.db.commit()


    def decrementValue(self, tableName: str, paramName: str, rowid: int = 1) -> None:
        self.c.execute("UPDATE %s SET %s = %s-1 WHERE rowid = %s" % (tableName, paramName, paramName, rowid))
        self.db.commit()


    def setDatas(self, tableName: str, valuesArr: list) -> None:
        self.c.execute("INSERT INTO %s VALUES (?, ?, ?)" %tableName, (valuesArr[0], valuesArr[1], valuesArr[2]))
        self.db.commit()
    
    def clearDatasUser(self, tableName: str, userId: int) -> None:
        self.c.execute("DELETE FROM %s WHERE userId =%s" % (tableName, userId))
        self.db.commit()