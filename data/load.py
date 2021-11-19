import os
from utils import utils, entities
from utils import *
from datetime import datetime

def converte_data(dia):
    return datetime.strptime(dia, "%a %b %d %H:%M:%S %z %Y")

def insert(insert_many):
    for i in insert_many:
        print(f"[INSERT] {i._name}", end='\t\t-\t\t')
        i.insert()

def parse_interactions(data, usuario_origem):
    edge_list = []
    # resposta de usuario
    if data['in_reply_to_user_id']:
        interacao = entities.INTERACAO(
            usuario_origem=usuario_origem.idUSUARIO,
            usuario_destino=data['in_reply_to_user_id']
            )
        edge_list.append(interacao)
    # usuario mencionado
    if data['entities']['user_mentions']:
        for mention in data['entities']['user_mentions']:
                interacao = entities.INTERACAO(
                    usuario_origem=usuario_origem.idUSUARIO,
                    usuario_destino=mention['id']
                    )
                edge_list.append(interacao)
    if 'retweeted_status' in data.keys():
        interacao = entities.INTERACAO(
            usuario_origem=usuario_origem.idUSUARIO,
            usuario_destino=data['retweeted_status']['user']['id']
            )
        edge_list.append(interacao)
    return edge_list
  

def parse_media(data, tweet):
    media_list = []
    if 'media' in data['entities'].keys():
        medias = data['entities']['media']
        for media_tmp in medias:
            media = entities.MIDIA(media_url=media_tmp['media_url'], tweet_idTweet=tweet.idTWEET, tipo_media=media_tmp['type'])
            media_list.append(media)
    return media_list
            
CUR_DIR = os.path.abspath("__file__")
ROOT = os.path.dirname(CUR_DIR)
DATA_DIR = os.path.join(ROOT, 'json')

for file in os.listdir(DATA_DIR):
    insert_many = []
    json_data = utils.load_json(os.path.join(DATA_DIR, file))

    for data in json_data:
        # USUARIO
        usuario = entities.USUARIO(
            idUSUARIO=data['user']['id'],
            name_usuario=data['user']['name'],
            location=data['user']['location'],
            verified=data['user']['verified'], 
            followers_count=data['user']['followers_count'], 
            friends_count=data['user']['friends_count'], 
            created_at=converte_data(data['user']['created_at'])
            )
        insert_many.append(usuario)
        # TWEET
        tweet = entities.TWEET(
            idTWEET=data['id'], tweet_text=data['text'], 
            created_at=converte_data(data['created_at']), reply_count=0,
            in_reply_to_status_id=data['in_reply_to_status_id'],
            in_reply_to_user_id=data['in_reply_to_user_id'], 
            retweet_count=data['retweet_count'],
            favorite_count=data['favorite_count'],
            retweeted=data['retweeted']
            )
        insert_many.append(tweet)
        # LOCAL_POST
        if data['place']:
            local = entities.LOCAL_POST(
                idLOCAL_POST=data['place']['id'],
                coordinates=data['place']['bounding_box']['coordinates'],
                country=data['place']['name'],
                place_type=data['place']['place_type']
                )
            insert_many.append(local)
        # POSTAGEM
        try:
            postagem = entities.POSTAGEM(
                usuario_idUsuario=usuario.idUSUARIO, 
                tweet_idTweet=tweet.idTWEET,
                local_idLocal=local.idLOCAL_POST
            )
        except:
            postagem = entities.POSTAGEM(
                usuario_idUsuario=usuario.idUSUARIO, 
                tweet_idTweet=tweet.idTWEET,
                local_idLocal=None
            )
        insert_many.append(postagem)
        # HASHTAG
        if data['entities']['hashtags']:
            for tag in data['entities']['hashtags']:
                hashtag = entities.HASHTAG(hashtag_text=tag['text'], 
                tweet_idTweet=tweet.idTWEET)
                insert_many.append(hashtag)
        # TOPICO
        topico = entities.TOPICO(
            text_topico=data['busca'], 
            usuario_idUsuario=usuario.idUSUARIO)
        insert_many.append(topico)
        # MIDIA
        insert_many.extend(parse_media(data, tweet))
        # INTERACAO
        insert_many.extend(parse_interactions(data, usuario))

    insert(insert_many)
    insert_many[-1].close()