import ConfigParser
import sqlite3
import os

class Adopt():
    def __init__(self):
        print "Starting up."

        os.remove("db.sql")
        self.setup_db()

        self.queuefile = open("queue.list", 'r')
        self.fileid = 1

        print "Processing .adopt files..."
        for l in self.queuefile:
            self.process_file(l)
            self.fileid = self.fileid + 1

        print "...done."

        self.queuefile.close()

    def setup_db(self):
        """Remove a pre-existing database and create a new database and schema."""

        print "Setting up the database..."
        self.db = sqlite3.connect("db.sql")
        self.db.execute("CREATE TABLE project (ID INT PRIMARY KEY NOT NULL, \
            STATUS INT NOT NULL, \
            NAME TEXT NOT NULL, \
            DESCRIPTION TEXT NOT NULL, \
            CATEGORY TEXT NOT NULL, \
            REPO TEXT NOT NULL, \
            LANGUAGES TEXT NOT NULL, \
            CONTACT TEXT NOT NULL, \
            EMAIL TEXT NOT NULL \
            )")

        print "...done."

    def process_file(self, f):
        """Process an individual .adopt file and add it to the database."""

        config = ConfigParser.ConfigParser()
        config.read(f.strip())

        status = config.get('Project', 'status')
        name = config.get('Project', 'name')
        description = config.get('Project', 'description')
        category = config.get('Project', 'category')
        repo = config.get('Project', 'repo')
        languages = config.get('Project', 'languages')
        contact = config.get('Contact', 'name')
        email = config.get('Contact', 'email')

        query = "INSERT INTO project(ID, STATUS, NAME, DESCRIPTION, CATEGORY, REPO, LANGUAGES, CONTACT, EMAIL) VALUES(" \
            + str(self.fileid) + ", " \
            + str("0") + ", " \
            + "'" + name +  "', " \
            + "'" + description +  "', " \
            + "'" + category +  "', " \
            + "'" + repo +  "', " \
            + "'" + languages +  "', " \
            + "'" + contact +  "', " \
            + "'" + email + "')"
        self.db.execute(query)
        self.db.commit()

if __name__ == '__main__':
    a = Adopt()
