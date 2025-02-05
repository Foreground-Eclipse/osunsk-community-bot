import sqlite3

dbPath = "./internal/storage/community.db"

def initializeDatabaseSchema(): 
    try:
        sqliteConnection = sqlite3.connect(dbPath)
        cursor = sqliteConnection.cursor()

        query = "create table if not exists commands (ID  INTEGER primary key AUTOINCREMENT, name text NOT NULL, content text, picture text, owner text NOT NULL)"
        cursor.execute(query)
    except Exception as e :
        return e
    finally :
        if sqliteConnection:
            sqliteConnection.close()

def addcom(name: str, text: str, picture: str, owner :str) -> bool:
    try:
        sqliteConnection = sqlite3.connect(dbPath)
        cursor = sqliteConnection.cursor()
        query = "insert into commands(name,content,picture,owner) values (?, ?, ?, ?)"
        cursor.execute(query, (name,text,picture,owner))
        sqliteConnection.commit()
    except Exception as e:
        print(e)
        return False
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def checkIfCommandNameTaken(name:str) -> bool:
    try:
        sqliteConnection = sqlite3.connect(dbPath)
        cursor = sqliteConnection.cursor()
        query = "select * from commands where name = ?"
        arr = cursor.execute(query, (name,))
        result = arr.fetchall()
        return True if len(result) > 0 else False
    except Exception as e:
        print(e)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def getCommandOwner(name: str) -> str:
    try:
        sqliteConnection = sqlite3.connect(dbPath)
        cursor = sqliteConnection.cursor()
        query = "select owner from commands where name = ?"
        arr = cursor.execute(query, (name,))
        result = arr.fetchall()
        result = [item[0] for item in result]
        return result[0]
    except Exception as e:
        print(e)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def deleteCommand(name: str):
    try:
        sqliteConnection = sqlite3.connect(dbPath)
        cursor = sqliteConnection.cursor()
        query = "delete  from commands where name = ?"
        cursor.execute(query, (name,))
        sqliteConnection.commit()
        
    except Exception as e:
        print(e)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def getAllCommandNames():
    try:
        sqliteConnection = sqlite3.connect(dbPath)
        cursor = sqliteConnection.cursor()
        query = "select name from commands"
        cursor.execute(query)
        names = cursor.fetchall()
        names = [item[0] for item in names]
        return names
        
    except Exception as e:
        print(e)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def getInfoByCommandName(name:str):
    try:
        sqliteConnection = sqlite3.connect(dbPath)
        cursor = sqliteConnection.cursor()
        query = "select name, content, picture from commands where name = ?"
        cursor.execute(query, (name,))
        info = cursor.fetchall()
        
        return info
        
    except Exception as e:
        print(e)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def getCommandsWithLimit(page : int):
    try:
        sqliteConnection = sqlite3.connect(dbPath)
        cursor = sqliteConnection.cursor()
        query = "select name, content, picture from commands limit 24 offset ? "
        cursor.execute(query, (page*24,))
        info = cursor.fetchall()
        return info
        
    except Exception as e:
        print(e)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


