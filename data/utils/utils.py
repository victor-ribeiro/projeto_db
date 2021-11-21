import json
import mysql.connector

class Connector:
    def __init__(self, config) -> None:
        self.config = load_json(config)
        self.conn = None
    def connect(self):
        self.conn = mysql.connector.connect(
            user=self.config['user'],
            password=self.config['password'],
            host=self.config['host'],
            database=self.config['database']
            )
        return self.conn
    def close(self):
        self.conn.close()



def load_json(path):
    try:
        with open(path, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(''' sem arquivo de configuracao. crie um aquivo .json com a formacao abaixo: \n
        {
            "user": "usuario_bd",
            "password": "senha_bd",
            "host":"ip_host", 
            "database":"nome_do_banco"
        }
        ''')

def to_json(data, output):
    with open(output, 'w') as file:
        tmp_json = json.dumps(data, indent=True)
        file.writelines(tmp_json)