import ConfigParser
import sqlite3
import os
import urllib2
import sys

class Adopt():
    def __init__(self, argv):

        self.examplemode = False

        print "Starting up."

        self.args = sys.argv

        for a in self.args:
            if a == "-e":
                self.examplemode = True

        if os.path.isfile("db.sql"):
            os.remove("db.sql")

        self.setup_db()

        if self.examplemode == True:
            self.queuefile = open("exampleadopts/local-queue", 'r')
        else:
            self.queuefile = open("sample-queue", 'r')

        self.fileid = 1

        print "Processing .adopt files..."
        for l in self.queuefile:
            print "\t * " + str(l)

            if self.examplemode == True:
                self.process_file("./exampleadopts/" + l)
            else:
                f = open("current-adopt.tmp", 'wb')
                url = urllib2.urlopen(l)
                f.write(url.read())
                f.close()
                self.process_file("current-adopt.tmp")

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

    def generate_webpage(self):
        """Generate a simple web page listing the projects."""
        pass


if __name__ == '__main__':
    a = Adopt(sys.argv)
