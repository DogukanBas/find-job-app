import psycopg2

class DataBaseConnector : 
    singleton = None
    def __init__(self) : 
        self.database = "IsBul"
        self.user = "postgres"
        self.password = "608608"
        self.connect()
        self.cursor = self.connection.cursor()

    def connect(self) : 
        try : 
            self.connection = psycopg2.connect(
                database = self.database,
                user = self.user,
                password = self.password
            )
        except (Exception, psycopg2.Error) as error : 
            print("Error while connecting to PostgreSQL", error)
    
    def close(self) : 
        if self.connection : 
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
    
   

    