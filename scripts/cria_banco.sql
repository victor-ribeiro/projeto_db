create database projeto_db;
USE projeto_db;

create table TWEET(
	idTWEET bigint not null primary key,
    created_at datetime not null,
    tweet_text varchar(500) not null,
    in_reply_to_status_id bigint,
    in_reply_to_user_id bigint,
    reply_count bigint not null default 0 ,
    retweet_count int not null default 0,
    favorite_count int not null default 0,
    retweeted boolean not null default 0 /*indica se o tweet foi retweetado*/
    );

create table HASHTAG(
	idHASHTAG bigint primary key auto_increment not null,
    hashtag_text varchar (100) unique,
    tweet_idTweet bigint not null,
    foreign key(tweet_idTweet) references TWEET(idTweet)
);

create table MIDIA (
	idMIDIA bigint primary key not null auto_increment,
    media_url varchar(200),
    tipo_media enum('photo', 'video'),
    tweet_idTweet bigint not null,
    foreign key (tweet_idTweet) references TWEET(idTweet) on delete cascade
);

create table USUARIO (
	idUSUARIO bigint not null primary key,
    name_usuario varchar(200) not null,
    location varchar(300), # nome da cidade do usuario
    verified boolean not null,
    followers_count int not null default 0, # pessoas que seguem o perfil
    friends_count int not null default 0,   # pessoas que o perfil segue
    created_at datetime not null
    );

create table INTERACAO(
	idINTERACAO bigint not null primary key auto_increment,
    usuario_origem bigint not null,
    usuario_destino bigint not null -- foram removidas as restriçoes de chave estrangeira pq os usuários que não interagem não estão na tabela de usuários. posso criar uma rotina que atualiza isso.
);

create table TOPICO(
	idTOPICO bigint primary key not null auto_increment,
    text_topico varchar(200) not null,
    usuario_idUsuario bigint not null,
    foreign key(usuario_idUsuario) references USUARIO(idUsuario) on delete cascade
);

create table LOCAL_POST (
	idLOCAL_POST varchar(200) not null primary key,
    coordinates polygon not null,
    country varchar(100) not null,
    place_type varchar(45) not null
    );

create table POSTAGEM(
	usuario_idUsuario bigint not null,
    tweet_idTweet bigint not null,
    local_idLocal varchar(200) default null,
    foreign key(usuario_idUsuario) references USUARIO(idUsuario) on delete cascade,
    foreign key(tweet_idTweet)     references TWEET(idTweet) on delete cascade,
    foreign key(local_idLocal)     references LOCAL_POST(idLOCAL_POST) on delete cascade
    );