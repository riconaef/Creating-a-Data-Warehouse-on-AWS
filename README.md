# Creating-a-Data-Warehouse-on-AWS
**Creating a Data Warehouse to build a relational database with Postgres on AWS**

### Follwoing are the used libraries
configparser, psycopg2

### Project Motivation
A startup called Sparkify, needs to have a relational database to perform queries regarding the songs, users are listening to. The provided data consists of json files, which need to be reordered into new tables.
Following are tables, which were created during the project: 

#### Fact table:
songplays: [songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent]

#### Dimension tables:
users:     [user_id, first_name, last_name, gender, level]
songs:     [song_id, title, artist_id, year, duration]
artists:   [artist_id, name, location, latitude, longitude]
time:      [start_time, hour, day, week, month, year, weekday]

![alt text](https://github.com/riconaef/Creating-a-Data-Warehouse-on-AWS/blob/main/starschema.png)

### File Descriptions
sql_queries.p; 
create_tables.p; 
etl.py
dwh.cfg


To run, first the "create_tables.py" needs to be run, which creates the tables. After, "etl.py" can be run, which fills the table with an etl-pipeline. 


### Licensing, Authors, Acknowledgements
I thank Sparkify for offering the data.
