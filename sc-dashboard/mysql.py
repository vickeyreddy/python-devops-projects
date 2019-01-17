import MySQLdb

class MySQL(object):

    def __init__(self, host=None, port=3306, user=None, passwd=None, dbname=None):

        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = dbname

        conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd)
        try:
            cursor = conn.cursor()
            print("Creating DB if it doesn't exist")
            cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % (self.db))
            conn.commit()

        except MySQLdb.Error, e:
            try:
                print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                conn.rollback()
            except IndexError:
                print("MySQL Error: %s" % str(e))
                conn.rollback()
        finally:
            print("Closing Database Connection!!")
            conn.close()

    def create_table(self, table=None, tquery=None):
	    self.table = table
	    self.tquery = tquery
        conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
        try:
            cursor = conn.cursor()
            print("Creating Table if it doesn't exist")
            cursor.execute("CREATE TABLE IF NOT EXISTS %s(%s)" % (self.table,self.tquery))
            conn.commit()
        except MySQLdb.Error, e:
            try:
                print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                conn.rollback()
            except IndexError:
                print("MySQL Error: %s" % str(e))
                conn.rollback()
        finally:
                print("Closing Database Connection!!")
                conn.close()

    def insert_data(self, squery=None):
        self.squery = squery
        conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
        try:
            cursor = conn.cursor()
            print("Inserting Records to Database")
            cursor.execute(self.squery)
            conn.commit()

        except MySQLdb.Error, e:
            try:
                print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                conn.rollback()
            except IndexError:
                print("MySQL Error: %s" % str(e))
                conn.rollback()
        finally:
                print("Closing Database Connection!!")
                conn.close()
