connect wardrobedb;


CREATE TABLE articles (Name varchar(255) NOT NULL PRIMARY KEY, Type varchar(128) NOT NULL, Image LONGBLOB, Cost DECIMAL UNSIGNED, TimesWorn BIGINT NOT NULL, Retired BOOLEAN);


