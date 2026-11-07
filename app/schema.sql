CREATE TABLE IF NOT EXISTS users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK (role IN ('lecturer', 'student')),
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    lecturer_id BIGINT NOT NULL REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS assessments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id BIGINT NOT NULL REFERENCES courses(id),
    name TEXT NOT NULL,
    weight NUMERIC NOT NULL CHECK (weight > 0 AND weight < 'Infinity'::numeric),
    UNIQUE (id, course_id)
);

CREATE TABLE IF NOT EXISTS enrollments (
    course_id BIGINT REFERENCES courses(id),
    student_id BIGINT REFERENCES users(id),
    PRIMARY KEY (course_id, student_id)
);

CREATE TABLE IF NOT EXISTS grades (
    assessment_id BIGINT,
    student_id BIGINT,
    course_id BIGINT NOT NULL,
    value NUMERIC NOT NULL CHECK (value BETWEEN 1 AND 6 AND scale(value) <= 2),
    PRIMARY KEY (assessment_id, student_id),
    FOREIGN KEY (assessment_id, course_id) REFERENCES assessments(id, course_id),
    FOREIGN KEY (course_id, student_id) REFERENCES enrollments(course_id, student_id)
);
