connect wardrobedb;


CREATE TABLE articles (id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, Name varchar(255) NOT NULL, Type varchar(128) NOT NULL, Image LONGBLOB, Cost DECIMAL UNSIGNED, Retired BOOLEAN);
