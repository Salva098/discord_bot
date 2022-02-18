import mysql.connector as mysql
import os

from discord.ext.commands.core import check
from mysqlx import OperationalError
from objects import users
# id usuario, nivel, experiencia, experiencia maxima

class Level():
    def __init__(self):
        connection=None
        print(os.environ.get('user'))
        try:
            connection = mysql.connect(
            database=os.environ.get('database'),
            user=os.environ.get('user'),
            password=os.environ.get('password'),
            host=os.environ.get('host'),
            port=os.environ.get('port'),
            )

        except OperationalError as e:
            print(f"The error '{e}' occurred")
        self.conn=connection

    def free_games(self,id_server,id_channel):
        cur =self.conn.cursor()
        cur.execute("update servers set free_game ={} where idserver={}".format(str(id_channel),str(id_server)))
        self.conn.commit()
        

    def  check_freegame(self):
        cur =self.conn.cursor()
        cur.execute("select free_game from servers where free_game is NOT NULL;")
        try:
            lista=[]
            numero=cur.fetchall()
            for x in numero:
                lista.append(x[0])
            return lista
        except:
            return None



    def new_user(self,id:int,id_server:int,name_server:str)->bool:
        if not self.check_user(id,id_server):
            try:
                cursor=self.conn.cursor()
                querry="insert into servers (idserver,nserver) values ({},'{}')".format(str(id_server),name_server)
                cursor.execute(querry)
                cursor.close()
                self.conn.commit()
            except:
                
                print("servidor añadido")
            
            try:
               
                self.conn.rollback()
                cursor=self.conn.cursor()
                sql="INSERT INTO usuarios (idusuarios) VALUES ('{}')".format(str(id))
                cursor.execute(sql)
                cursor.close()
                self.conn.commit()
            # INSERT INTO `discord`.`servers` (`idservers`, `server_name`) VALUES ('12', 'asd');
            # return True
                cursor.close()
            except:
                # return False
                pass

            
            try:
                self.conn.rollback()

                cursor=self.conn.cursor()
                
                cursor.execute("INSERT INTO server_usuario (idserver,num_usuario) VALUES ({},{})".format(str(id_server),str(self.num_user(id))))
                cursor.close()
                self.conn.commit()
            except:
                pass
            
            return True
        else:
            return False
    
    def  num_user(self,id:int):
        curse =self.conn.cursor()
        curse.execute("Select max(numusuarios) from usuarios where idusuarios = {} ".format(str(id)))
        return curse.fetchall()[0][0]
    
    def check_id_game(self)->list:   
        curse =self.conn.cursor()
        curse.execute("Select id from extra ")
    
        lista=[]
        for x in curse.fetchall():
            lista.append(x[0])
        return lista

    def insert_id_game(self,id:int):
        cur =self.conn.cursor()
        cur.execute("insert into extra (id) values ({})".format(str(id)))
        self.conn.commit()

    def upload_user(self,user:users,id_server:int):
        cursor =self.conn.cursor()
        cursor.execute("select numusuarios from usuarios,server_usuario where server_usuario.num_usuario=usuarios.numusuarios and usuarios.idusuarios = {} and server_usuario.idserver = {}".format(str(user.id),str(id_server)))
        numero=cursor.fetchall()[0][0]
        cursor.close()
        cursor2=self.conn.cursor()
        cursor2.execute("update usuarios set level={},exp={},exp_max={} where numusuarios={} ".format(user.level,user.exp,user.exp_max,numero))
        self.conn.commit()


    def check_user(self,id:int,id_server:int)->users:
        cur=self.conn.cursor()
        sql="select idusuarios,numusuarios,level,exp,exp_max from usuarios,server_usuario where server_usuario.num_usuario=usuarios.numusuarios and usuarios.idusuarios = {} and server_usuario.idserver = {}".format(str(id),str(id_server))
        cur.execute(sql)

        try:
            usuario=cur.fetchall()[0]
            return users(usuario[0],usuario[1],usuario[2],usuario[3],usuario[4])
        except:

            return None
    
    def increase_exp(self,id:int,id_server:int) -> bool:
        usuario=self.check_user(id,id_server)
        subida=False
        if usuario.exp==usuario.exp_max:
            usuario.level=usuario.level+1
            usuario.exp=0
            usuario.exp_max= usuario.exp_max*2
            subida=True
        else:
            usuario.exp=usuario.exp+1
            subida=False
        
        self.upload_user(usuario,id_server)
        return subida,usuario.level
    

    def disconect(self):
        self.conn.close()
        
    
if __name__ =="__main__":
    hola=Level()
    
    # hola.sql()
    # hola.create_table()
    # hola.new_user(id=1,id_server=3,name_server="b")

    # hola.increase_exp(2,1)
    # hola.free_games(2,1234)
    hola.check_id_game()
    # hola.num_user(2)
    print(hola.check_user(277405999403368470,747428799226052639))
