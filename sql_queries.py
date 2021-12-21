import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop  = "DROP TABLE IF EXISTS staging_songs_table"
songplay_table_drop       = "DROP TABLE IF EXISTS songplay"
user_table_drop           = "DROP TABLE IF EXISTS users"
song_table_drop           = "DROP TABLE IF EXISTS songs"
artist_table_drop         = "DROP TABLE IF EXISTS artists"
time_table_drop           = "DROP TABLE IF EXISTS times"

# CREATE TABLES
staging_events_table_create  = ("""CREATE TABLE IF NOT EXISTS staging_events_table (
                                events_id         INT identity(0,1) PRIMARY KEY,
                                artist            TEXT,
                                auth              TEXT,
                                first_name        TEXT,
                                gender            TEXT,
                                itemInSession     INT,
                                last_name         TEXT,
                                length            NUMERIC,
                                level             TEXT,
                                location          TEXT,
                                method            TEXT,
                                page              TEXT,
                                registration      TEXT,
                                sessionId         BIGINT,
                                song              TEXT,
                                Status            INT,
                                ts                BIGINT, 
                                userAgent         TEXT,
                                userId            TEXT);""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs_table (
                                num_songs         INT PRIMARY KEY,
                                artist_id         TEXT,
                                artist_latitude   NUMERIC,
                                artist_longitude  NUMERIC,
                                artist_location   TEXT,
                                artist_name       TEXT,
                                song_id           TEXT,
                                title             TEXT,
                                duration          NUMERIC,
                                year              INT);""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay (
                                song_play_id INT identity(0,1) PRIMARY KEY, 
                                start_time   DATE, 
                                user_id      TEXT, 
                                level        TEXT, 
                                song_id      TEXT,
                                artist_id    TEXT, 
                                session_id   INT, 
                                location     TEXT, 
                                user_agent   TEXT);""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                                user_id      TEXT PRIMARY KEY, 
                                first_name   TEXT, 
                                last_name    TEXT, 
                                gender       TEXT, 
                                level        TEXT);""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
                                song_id      TEXT PRIMARY KEY, 
                                title        TEXT, 
                                artist_id    TEXT, 
                                year         INT, 
                                duration     NUMERIC);""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
                                artist_id    TEXT PRIMARY KEY, 
                                name         TEXT, 
                                location     TEXT, 
                                latitude     NUMERIC, 
                                longitude    NUMERIC);""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS times (
                                starttime    DATE PRIMARY KEY, 
                                hour         INT, 
                                day          INT, 
                                week         INT, 
                                month        INT, 
                                year         INT, 
                                weekday      INT);""")


# STAGING TABLES
staging_events_copy = ("""copy staging_events_table 
                          from {}
                          iam_role {}
                          json {};""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""copy staging_songs_table 
                         from {}
                         iam_role {}
                         json 'auto';""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES
songplay_table_insert = ("""INSERT INTO songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            SELECT  TIMESTAMP 'epoch' + ev.ts/1000 * interval '1 second' as start_time,
                                    ev.userId, 
                                    ev.level, 
                                    so.song_id, 
                                    so.artist_id, 
                                    ev.sessionId, 
                                    ev.location, 
                                    ev.userAgent
                            FROM staging_events_table ev, staging_songs_table so""")

user_table_insert = ("""INSERT INTO users(user_id, first_name, last_name, gender, level)
                        SELECT userId,
                               first_name,
                               last_name,
                               gender,
                               level
                        FROM staging_events_table
                        WHERE userId IS NOT NULL
                        AND page = 'NextSong' 
                        AND userId NOT IN (SELECT DISTINCT user_id FROM users)""") #only unique users are taken 
                        

song_table_insert = ("""INSERT INTO songs(song_id, title, artist_id, year, duration)
                        SELECT song_id,
                        	title,
                               artist_id,
                               year,
                               duration                   
                        FROM staging_songs_table
                        WHERE song_id IS NOT NULL""")

artist_table_insert = ("""INSERT INTO artists(artist_id, name, location, latitude, longitude)
                          SELECT artist_id,
                                 artist_name,
                                 artist_location,
                                 artist_latitude,
                                 artist_longitude
                          FROM staging_songs_table
                          WHERE artist_id IS NOT NULL""")

time_table_insert = ("""INSERT INTO times(starttime, hour, day, week, month, year, weekday)
                        SELECT start_time, 
                               EXTRACT (hour from start_time), 
                               EXTRACT (day from start_time), 
                               EXTRACT (week from start_time), 
                               EXTRACT (month from start_time), 
                               EXTRACT (year from start_time), 
                               EXTRACT (weekday from start_time)
                        FROM songplay
                        WHERE start_time IS NOT NULL""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]


