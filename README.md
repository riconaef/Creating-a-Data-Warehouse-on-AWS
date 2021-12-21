# Creating-a-Data-Warehouse-on-AWS
**Creating a Data Warehouse to build a relational database with Postgres on AWS**

### Follwoing are the used libraries
configparser, psycopg2

### Project Motivation
A startup called Sparkify, needs to have a relational database to perform queries regarding the songs, users are listening to. The provided data consists of json files, which need to be reordered into new tables.
Following are tables, which were created during the project: 

#### Fact table:
songplays: [staging_events_table (events_id, artist, auth, first_name, gender, itemInSession, last_name, length, level, location, method, page, registration, sessionId, song, Status, ts, userAgent, userId];
#### Dimension tables:
users:     [user_id, first_name, last_name, gender, level]<br />
songs:     [song_id, title, artist_id, year, duration]<br />
artists:   [artist_id, name, location, latitude, longitude]<br />
time:      [start_time, hour, day, week, month, year, weekday]<br />

![alt text](https://github.com/riconaef/Creating-a-Data-Warehouse-on-AWS/blob/main/starschema.png)

### File Descriptions
sql_queries.p<br />
create_tables.p<br />
etl.py<br />
dwh.cfg<br />

To run, first the "create_tables.py" needs to be run, which creates the tables. After, "etl.py" can be run, which fills the table with an etl-pipeline. 


### Licensing, Authors, Acknowledgements
I thank Sparkify for offering the data.
