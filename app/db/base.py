import sqlite3
from app.core.logger import logger

def init_db():
    try:
        with sqlite3.connect('userflow_bridge.db') as db:
            cursor = db.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS userflow_bridge ( username TEXT, id INTEGER PRIMARY KEY )'''
            )
            db.commit()
            logger.info('sqlite3 has been created!')
    except sqlite3.Error as e:
        logger.error(f'Error sqlite3: {e}')
    except Exception as e:
        logger.error(f'Error: {e}')

def insert_db(username: str, id: int):
    try:
        with sqlite3.connect('userflow_bridge.db') as db:
            cursor = db.cursor()
            cursor.execute(
                '''INSERT OR IGNORE INTO userflow_bridge ( username, id ) VALUES ( ?, ? )''', (username,id,)
            )
            db.commit()
            logger.info(f'New application form: @{username}, {id}')
    except sqlite3.Error as e:
        logger.error(f'Error sqlite3: {e}')
    except Exception as e:
        logger.error(f'Error: {e}')

def select_db():
    try:
        with sqlite3.connect('userflow_bridge.db') as db:
            cursor = db.cursor()
            cursor.execute(
                '''SELECT * FROM userflow_bridge''',
            )
            result = cursor.fetchall()
            users = []
            for row in result:
                users.append({
                    "username": row[0], 
                    "id": row[1]         
                })
            return users
    except sqlite3.Error as e:
        logger.error(f'Error sqlite3: {e}')
        return []
    except Exception as e:
        logger.error(f'Error: {e}')
        return []

init_db()