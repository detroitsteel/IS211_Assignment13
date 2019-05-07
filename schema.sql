drop table students;
CREATE TABLE students(
id INTEGER PRIMARY KEY,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL);

CREATE TABLE quiz(
id INTEGER PRIMARY KEY,
subject TEXT,
q_cnt INTEGER,
q_date DATE);

CREATE TABLE quizScore(
id INTEGER PRIMARY KEY,
stu_id INTEGER,
q_id INTEGER,
score INTEGER);

INSERT INTO students VALUES (1, 'John', 'Smith');
INSERT INTO quiz VALUES (1, 'Python Basics', 5, '02/05/2015');
INSERT INTO quizScore VALUES (1, 1, 1, 85);

