import psycopg2
import os

url = os.getenv("DATABASE_URL")

test_url = os.getenv("DATABASE_URL")


def connection(connect_url):
    conn = psycopg2.connect(connect_url)
    return conn


def init_db():
    conn = connection(url)
    curr = conn.cursor()
    queries = tables()

    for query in queries:
        curr.execute(query)
    conn.commit()
    return conn


def init_test_db():
    conn = connection(test_url)
    curr = conn.cursor()
    queries = tables()

    for query in queries:
        curr.execute(query)
    conn.commit()
    return conn


def destroy():
    conn = connection(test_url)
    curr = conn.cursor()
    comments = "DROP TABLE IF EXISTS comments CASCADE"
    incidents = "DROP TABLE IF EXISTS incidents CASCADE"
    users = "DROP TABLE IF EXISTS users CASCADE"
    queries = [comments, incidents, users]
    try:
        for query in queries:
            curr.execute(query)
        conn.commit()
    except:
        print("Fail")


def tables():
    db1 = """CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50),
    username character varying(50) NOT NULL,
    email character varying(50),
    is_admin boolean,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying(500) NOT NULL
    );"""

    db3 = """CREATE TABLE IF NOT EXISTS comments (
    comment_id serial PRIMARY KEY NOT NULL,
    incident_id numeric NOT NULL,
    created_by character varying(20) NOT NULL,
    comment character varying(1000) NOT NULL,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
    );"""

    db2 = """CREATE TABLE IF NOT EXISTS incidents (
    incident_id serial PRIMARY KEY NOT NULL,
    created_by character varying(20) NOT NULL,
    type character varying(20)  NOT NULL,
    description character varying(200) NOT NULL,
    status character varying(50) DEFAULT 0,
    location character varying(200) NULL,
    created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
    );"""

    queries = [db2, db1, db3]
    return queries
