import ConfigParser
import string
import sqlite3
import cherrypy
import urllib2
import os

class AdoptSite(object):
    def __init__(self):
        self.db = sqlite3.connect("db.sql")

    @cherrypy.expose
    def index(self):
        """Display the list of unmaintained projects."""

        html = ""
        head = open("html/header.html", "r")

        html = html + head.read()

        self.db = sqlite3.connect("db.sql")
        rows = self.db.execute("SELECT * FROM projects;")

        if rows.rowcount == -1:
            html = html + "<hr /><strong>No projects.</strong> Why not go and <a href='add/'>add one?</a>.<hr/>"
        else:
            html = html + "<!-- Table --> \
                <table class='table'> \
                <tr> \
                <th>Project</th> \
                <th>Category</th> \
                <th>Description</th> \
                <th>Languages</th> \
                <th>Repo</th> \
                <th>Discussion</th> \
                <th>Contact</th> \
            </tr>"

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
                html = html + line

            html = html + "</table>"

        return html

        foot = open("html/footer.html", "r")

        html = html + foot.read()

        return html

    @cherrypy.expose
    def add(self):
        """Display the form to add a project."""

        # Warning: no error checking
        return """<html>
          <head></head>
          <body>
            <form method="get" action="add_project">
              <input type="text" value="8" name="project" />
              <button type="submit">Add your project</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def add_project(self, project):
        """Add the project to the queue.list."""

        # Warning: no error checking
        f = open("current-adopt-add.tmp", 'wb')
        url = urllib2.urlopen(project)
        f.write(url.read())
        f.close()

        config = ConfigParser.ConfigParser()
        config.read("current-adopt-add.tmp")

        status = config.get('Project', 'maintained')

        if status == "no":
            with open("queue.list", "a") as queue:
                queue.write(project + "\n")

            os.remove("current-adopt-add.tmp")

            return "Added <tt>" + project + "<tt> to the queue. It will be processed and added to the site soon."
        else:
            return "This project is currently maintained. Not added."

if __name__ == '__main__':
    cherrypy.quickstart(AdoptSite())
