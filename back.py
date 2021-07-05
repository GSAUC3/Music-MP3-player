import sqlite3
x='songs.db'
def connect():
    conn=sqlite3.connect(x)
    c=conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS playlist (
        song_id INTEGER NOT NULL PRIMARY KEY,
        song text NOT NULL,
        path text NOT NULL,
        fav INTEGER
    )
    """)
    conn.commit()
    conn.close()

def insert(song,path,fav=0):
    conn=sqlite3.connect(x)
    c=conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO playlist (song,path,fav) VALUES (?,?,?)
    """,(song,path,fav))
    conn.commit()
    conn.close()

def fav(song,f):
    conn=sqlite3.connect(x)
    c=conn.cursor()
    c.execute("""
        UPDATE playlist SET fav=? WHERE song=?""",(f,song))
    conn.commit()
    conn.close()
    


def show():
    conn=sqlite3.connect(x)
    c=conn.cursor()
    c.execute("""
    SELECT * FROM playlist
    """)
    s=c.fetchall()
    conn.commit()
    conn.close()
    return s

def find(song=None,sid=None):
    conn=sqlite3.connect(x)
    c=conn.cursor()
    c.execute("""
    SELECT * FROM playlist WHERE song=? OR song_id=?
    """,(song,sid))
    s=c.fetchall()
    conn.commit()
    conn.close()
    return s

def remove(song):
    conn=sqlite3.connect(x)
    c=conn.cursor()
    c.execute("DELETE FROM playlist WHERE song=?",(song,))

    conn.commit()
    conn.close()

def  playfavs():
    conn=sqlite3.connect(x)
    c=conn.cursor()
    c.execute("SELECT * FROM playlist WHERE fav=1")
    favss=c.fetchall()
    conn.commit()
    conn.close()
    return favss

connect()
# remove(2)
# print(show())