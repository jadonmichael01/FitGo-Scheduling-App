import harperdb

url = "https://cloud-1-jadonmichael.harperdbcloud.com"

username = "jadonmichael"
password = "jadonmichael"

database = harperdb.HarperDB(
    url=url,
    username=username,
    password=password
)

SCHEMA = "fitness_repo"
TABLE = "workouts"
TABLE_TODAY = "workout_today"

def delete_workout(workout_id):
    return database.delete(SCHEMA, TABLE, [workout_id])

def insert_workout(workout_data):
    return database.insert(SCHEMA, TABLE, [workout_data])

def get_all_workouts():
    return database.sql(f"select video_id, channel, title, duration from {SCHEMA}.{TABLE}")

def get_todays_workout():
    return database.sql(f"select * from {SCHEMA}.{TABLE_TODAY} where id = 0")

def update_todays_workout(workout_data, insert=False):
    workout_data['id'] = 0
    if insert:
        return database.insert(SCHEMA, TABLE_TODAY, [workout_data])
    return database.update(SCHEMA, TABLE_TODAY, [workout_data])







