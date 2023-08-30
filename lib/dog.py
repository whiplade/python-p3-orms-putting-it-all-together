import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []
    def __init__(self, name, breed) -> None:
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(self):
        CURSOR.execute('''
                        CREATE TABLE IF NOT EXISTS dogs (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            breed TEXT
                        )
                       ''')
        CONN.commit()
        

    @classmethod
    def drop_table(self):
        CURSOR.execute('''
                        DROP TABLE IF EXISTS dogs
                       ''')
        CONN.commit()
    
    def save(self):
        CURSOR.execute('''
                        INSERT INTO dogs (name, breed)
                        VALUES (?, ?)
                        ''',    
                        (self.name, self.breed)
                      )
        
        self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog 
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        all = CURSOR.execute('''
                            SELECT * FROM dogs
                            ''').fetchall()

        cls.get_all = [cls.new_from_db(row) for row in all]

        return cls.get_all
    
    @classmethod
    def find_by_name(cls, name):
        dog = CURSOR.execute( """
                                SELECT *
                                FROM dogs
                                WHERE name = ?
                                LIMIT 1
                            """, 
                            (name,)).fetchone()

        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        dog = CURSOR.execute( """
                                SELECT *
                                FROM dogs
                                WHERE id = ?
                                LIMIT 1
                              """, 
                            (id,)).fetchone()

        return cls.new_from_db(dog)
    
    