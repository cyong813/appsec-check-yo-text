CREATE TABLE Person (
	username VARCHAR (50),
	password VARCHAR (64),
	first_name VARCHAR (50),
	last_name VARCHAR (50),
	PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Content (
	id INT AUTO_INCREMENT,
	username VARCHAR (50),
	timest TIMESTAMP,
	file_path VARCHAR (100),
	content_name VARCHAR (50),
	file_text VARCHAR (2500),
	PRIMARY KEY (id),
	FOREIGN KEY (username) REFERENCES Person (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Wrong (
	id INT,
	incorrect_word VARCHAR (25),
	PRIMARY KEY (id, incorrect_word),
	FOREIGN KEY (id) REFERENCES Content (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;