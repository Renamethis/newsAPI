GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;
CREATE TABLE IF NOT EXISTS news(
    id varchar(512) not null primary key,
    uri varchar(256) not null,
    title varchar(256) not null,
    content varchar(5000) not null,
    tags varchar(256)[] not null,
    pdate date not null
);
