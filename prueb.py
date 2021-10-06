import sqlite3

conexion =sqlite3.connect("bd1.bd")
try:

    cursor=conexion.execute("select * from personas where id = 1")
    print(cursor.fetchall()[0])
    for filas in cursor:
        print(filas[0])



# 
    # conexion.execute("insert into personas (id,nombre)values (?,?)",(3,"Pedro"))
    # conexion.commit()
    # # conexion.execute("""
    #  create table personas(
    #      id integer primary key,
    #      nombre string 
    #  )
    # """)
    print("tabla creada")
except sqlite3.OperationalError:
    print("tabla ya creada")
conexion.close()