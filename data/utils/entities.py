from os import error

from .utils import *

class ENTITIE:
    _name = None
    def __init__(self):
        pass
    def insert(self, _conn):
        attr_names  = tuple([*self.__dict__.keys()])
        attr_values = tuple([f'%({k})s' for k in attr_names])
        query = f"INSERT INTO {self._name} {attr_names} VALUES {attr_values}".replace('\'', '')
        try:
            # parser da query de insercao
            cursor = _conn.cursor()
            cursor.execute(query, self.__dict__)
            _conn.commit()
            # fecha as conexao com o banco
            cursor.close()
            print('ok')
        except mysql.connector.errors.IntegrityError:
            print(f"[ERROR] erro de integridade:{self._name}")
        except mysql.connector.errors.OperationalError:
            self._conn = Connector('utils/config.json').connect()
            cursor = _conn.cursor()
            cursor.execute(query, self.__dict__)
            _conn.commit()
            # fecha as conexao com o banco
            cursor.close()
            print('ok')

class HASHTAG(ENTITIE):
    _name='HASHTAG'
    def __init__(self, hashtag_text:str, tweet_idTweet: int) -> None:
        super().__init__()
        self.hashtag_text  = hashtag_text[:100] 
        self.tweet_idTweet = tweet_idTweet
        
class INTERACAO(ENTITIE):
    _name = "INTERACAO"
    def __init__(self, usuario_origem: int, usuario_destino: int) -> None:
        super().__init__()
        self.usuario_origem  = usuario_origem
        self.usuario_destino = usuario_destino
        
class LOCAL_POST(ENTITIE):
    _name='LOCAL_POST'
    def __init__(self, idLOCAL_POST: int, coordinates, country: str, place_type: str) -> None:
        super().__init__()
        self.idLOCAL_POST = idLOCAL_POST
        self.country      = country
        self.place_type   = place_type
        self.coordinates  = coordinates[0]
        self.coordinates.append(self.coordinates[0])
    def transform_coord(self):
        return tuple(tuple(coord) for coord in self.coordinates)
    def insert(self, _conn) -> None:
        try:
            coord_insert = ''.join(tuple(str(coord) for coord in self.transform_coord()))
            self.coordinates = f'ST_GeomFromText("polygon({coord_insert.replace(", ", " ").replace(")(", ", ")})")'
            query = f"INSERT INTO {self._name} (idLOCAL_POST, country, place_type, coordinates) VALUES ('{self.idLOCAL_POST}', '{self.country}', '{self.place_type}', {self.coordinates})"
            _conn = Connector('utils/config.json').connect()
            cursor = _conn.cursor()
            cursor.execute(query)
            _conn.commit()
            # fecha as conexao com o banco
            cursor.close()
        except mysql.connector.errors.IntegrityError:
            print(f"[ERROR] erro de integridade:{self._name}")
        except mysql.connector.errors.OperationalError:
            self._conn = Connector('utils/config.json').connect()
            cursor = _conn.cursor()
            cursor.execute(query, self.__dict__)
            _conn.commit()
            # fecha as conexao com o banco
            cursor.close()
            print('ok')

class MIDIA(ENTITIE):
    _name='MIDIA'
    def __init__(self, media_url: str, tipo_media, tweet_idTweet: int) -> None:
        super().__init__()
        self.media_url     = media_url[:200]
        self.tipo_media    = tipo_media
        self.tweet_idTweet = tweet_idTweet

class POSTAGEM(ENTITIE):
    _name='POSTAGEM'
    def __init__(self,usuario_idUsuario: int, tweet_idTweet: int, local_idLocal: int) -> None:
        super().__init__()
        self.usuario_idUsuario = usuario_idUsuario
        self.tweet_idTweet     = tweet_idTweet
        self.local_idLocal     = local_idLocal

class TOPICO(ENTITIE):
    _name='TOPICO'
    def __init__(self, text_topico: str, usuario_idUsuario: int) -> None:
        super().__init__()
        self.text_topico = text_topico[:200]
        self.usuario_idUsuario = usuario_idUsuario        


class TWEET(ENTITIE):
    _name='TWEET'
    def __init__(self, idTWEET: int, created_at, tweet_text: str, in_reply_to_status_id: int, 
    in_reply_to_user_id: int, reply_count: int, retweet_count: int, favorite_count: int, retweeted: bool) -> None:
        super().__init__()
        self.idTWEET = idTWEET
        self.created_at = created_at
        self.tweet_text = tweet_text[:500]
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.retweeted = retweeted

class USUARIO(ENTITIE):
    _name = "USUARIO"
    def __init__(self, idUSUARIO: int, name_usuario: str, location: str, verified: bool, followers_count: int, friends_count: int, created_at) -> None:
        super().__init__()
        self.idUSUARIO=idUSUARIO
        self.name_usuario=name_usuario[:200]
        self.location = location[:300]
        self.verified = verified
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.created_at = created_at

if __name__ == '__main__':
    interacao = INTERACAO(usuario_origem=2, usuario_destino=3)
    print(interacao.insert())