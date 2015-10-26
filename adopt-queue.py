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
            if os.path.isfile("queue.list"):
                print "existing file"
                self.queuefile = open("queue.list", 'r')
                queuelines = self.queuefile.readlines()

        self.fileid = 1

        if os.path.getsize("queue.list") == 0:
            print "No projects in the queue to process."
        else:
            print "Processing .adopt files..."

            # Let's gather the lines of .adopts that will need to be removed
            lines_to_rem = []

            for l in queuelines:
                print "\t * " + str(l)

                if self.examplemode == True:
                    self.process_file("./exampleadopts/" + l)
                else:
                    f = open("current-adopt.tmp", 'wb')
                    url = urllib2.urlopen(l)
                    f.write(url.read())
                    f.close()
                    if self.process_file("current-adopt.tmp") == False:
                        lines_to_rem.append(l)

                self.fileid = self.fileid + 1

            print "...done."

            # Now let's remove .adopts not required
            # This happens when the status has changed from 'no' to 'yes'

            f = open("queue.list","w")

            print "Removing .adopts that are now maintained:"

            for line in queuelines:
                match = False
                for i in lines_to_rem:
                    if line == i:
                        print "\t * " + str(line)
                        match = True

                if match == False:
                    f.write(line)

            f.close()

            print "...done."

        self.queuefile.close()

    def setup_db(self):
        """Remove a pre-existing database and create a new database and schema."""

        print "Setting up the database..."
        self.db = sqlite3.connect("db.sql")
        self.db.execute("CREATE TABLE projects (ID INT PRIMARY KEY NOT NULL, \
            NAME TEXT NOT NULL, \
            DESCRIPTION TEXT NOT NULL, \
            CATEGORY TEXT NOT NULL, \
            REPO TEXT NOT NULL, \
            DISCUSSION TEXT NOT NULL, \
            LANGUAGES TEXT NOT NULL, \
            CONTACT TEXT NOT NULL, \
            EMAIL TEXT NOT NULL \
            )")

        print "...done."

    def process_file(self, f):
        """Process an individual .adopt file and add it to the database."""

        config = ConfigParser.ConfigParser()
        config.read(f.strip())

        status = config.get('Project', 'maintained')

        if status == "no":
            name = config.get('Project', 'name')
            description = config.get('Project', 'description')
            category = config.get('Project', 'category')
            repo = config.get('Project', 'repo')
            discussion = config.get('Project', 'discussion')
            languages = config.get('Project', 'languages')
            contact = config.get('Contact', 'name')
            email = config.get('Contact', 'email')

            query = "INSERT INTO projects(ID, NAME, DESCRIPTION, CATEGORY, REPO, DISCUSSION, LANGUAGES, CONTACT, EMAIL) VALUES(" \
                + str(self.fileid) + ", " \
                + "'" + name +  "', " \
                + "'" + description +  "', " \
                + "'" + category +  "', " \
                + "'" + repo +  "', " \
                + "'" + discussion +  "', " \
                + "'" + languages +  "', " \
                + "'" + contact +  "', " \
                + "'" + email + "')"
            self.db.execute(query)
            self.db.commit()

            return True
        else:
            return False

if __name__ == '__main__':
    a = Adopt(sys.argv)
