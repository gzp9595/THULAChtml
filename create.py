# create database

import MySQLdb
import MySQLdb.cursors
import ConfigParser

try:
    conf = ConfigParser.ConfigParser()
    conf.read("config.cfg")
    db = MySQLdb.connect(
        host=conf.get('db', 'db_host'),
        user=conf.get('db', 'db_name'),
        passwd=conf.get('db', 'db_password'),
        db=conf.get('db', 'db_database'),
        cursorclass=MySQLdb.cursors.DictCursor)

    cursor = db.cursor()

    cursor.execute("drop table if exists message")
    
    sql = """create table if not exists message(
            userid int not null AUTO_INCREMENT,
            name VARCHAR(45) NULL,
            orgname VARCHAR(45) NULL,
            email VARCHAR(45) NULL,
            address VARCHAR(45) null,
            telephone VARCHAR(45) NULL,
            PRIMARY KEY (`userid`))DEFAULT CHARSET=utf8"""
    cursor.execute(sql)

    db.commit()

except MySQLdb.Error, e:
    print"Mysql Error %d: %s" % (e.args[0], e.args[1])
finally:
    cursor.close()
    db.close()
    conf.
