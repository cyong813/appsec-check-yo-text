CREATE TABLE Person (
	username VARCHAR (50),
	password VARCHAR (50),
	first_name VARCHAR (50),
	last_name VARCHAR (50),
	PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Content (
	id INT AUTO_INCREMENT,
	username VARCHAR (50),
	timest TIMESTAMP,
	file_path VARCHAR (100),
	content_name VARCHAR (50),
	PRIMARY KEY (id),
	FOREIGN KEY (username) REFERENCES Person (username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Wrong (
	id INT,
	username_from VARCHAR (50),
	PRIMARY KEY (id, username_from),
	FOREIGN KEY (username_from) REFERENCES Person (username),
	FOREIGN KEY (id) REFERENCES Content (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;