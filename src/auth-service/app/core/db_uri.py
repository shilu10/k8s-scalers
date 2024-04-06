import os 

def generate_db_uri(db_type, user, host, port, password, dbname):
    if db_type == "mysql":
        db_uri = f"mysql://{user}:{password}@{host}:{port}/{dbname}"

    return db_uri
