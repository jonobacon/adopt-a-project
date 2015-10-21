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

        print "Generated HTML..."
        self.generate_webpage()
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

    def generate_webpage(self):
        """Generate a simple web page listing the projects."""

        generated = open("generated.html", "w")
        h = open("html/header.html", "r")
        generated.write(h.read())


        rows = self.db.execute("SELECT * FROM projects;")


        for r in rows:
            line = "<tr>"
            line = line + "<td>" + r[1] + "</td>"
            line = line + "<td>" + r[3] + "</td>"
            line = line + "<td>" + r[2] + "</td>"
            line = line + "<td>" + r[6] + "</td>"
            line = line + "<td><a href='" + r[4] + "'>Repo</a></td>"
            line = line + "<td><a href='" + r[5] + "'>Discussion</a></td>"
            line = line + "<td><a href='mailto:" + r[8] + "'>" + r[7] + "</a></td>"
            line = line + "</tr>\n"
            generated.write(line)

        f = open("html/footer.html", "r")
        generated.write(f.read())
        generated.close()



if __name__ == '__main__':
    a = Adopt(sys.argv)
