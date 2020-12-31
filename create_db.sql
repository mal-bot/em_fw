
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS student;
CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32)
);

DROP TABLE IF EXISTS category;
CREATE TABLE category (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
	name VARCHAR (32),
	category_id BIGINT UNSIGNED,
	FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS course;
CREATE TABLE course (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
	name VARCHAR (32),
	category_id BIGINT UNSIGNED NOT NULL,
	FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO student
    (name)
VALUES
    ('student_1'),
    ('student_2');

INSERT INTO category
    (name, category_id)
VALUES
    ('category_1', NULL),
    ('category_2', 1);


INSERT INTO course
    (name, category_id)
VALUES
    ('course_1', 1),
    ('course_2', 2);



COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
