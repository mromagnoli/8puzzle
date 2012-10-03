CREATE TABLE puzzle (
       id    	INTEGER PRIMARY KEY AUTOINCREMENT,
       hash 	VARCHAR(100) NOT NULL,
       tablero	CHAR(9) NOT NULL,
       padre_id	INTEGER NOT NULL
);
