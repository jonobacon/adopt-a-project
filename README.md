# Adopt A Project

This repo contains some code based on a simple idea I had recently for helping to connect unmaintained Open Source projects to people who may be interested in taking over them.

The idea works like this:

 * An unmaintained project creates an `.adopt` file that lives in it's source tree that is available somewhere online. This is a simple configuration file that includes details about the project and at least one contact person to help with the transition to a new maintainer.
 * The project can then use a simple web form to submit a direct link to the `.adopt` file to add it to the database. This web form is stored on the server in `queue.list`.
 * A script (`adopt-queue.py`) then processes `queue.list`, reads in all the `.adopt` files and generates a sqlite3 database that provides a searchable list of projects.
 * We then expose a simple web interface where someone can browse the list of projects or search by attributes such as programming language.
 * When the project is eventually converted to a *maintained* state (and is thus reflected in the `.adopt` file), it is then removed from `queue.list` and thus not scanned anymore.

## Core Principles

The idea is for this project to be as *simple* as possible. As such, there are a few core principles at work here:

 * I don't want to maintain a major database and web service. As such, the database is completely destroyed and recreated with each scan of the queue.
 * The project list should be simple to identify projects that are of interest to potential developers. It is not designed to provide an extensive list of all details about a project.
 * The `.adopt` file should be *really* simple to add to a project.

# Using This Code

**Requirements**: this code only requires CherryPy3 and the standard Python library.

There are two pieces to this codebase:

 * `website.py` is the front end that displays the list of unmained projects, let's you add a project etc.
 * `adopt-queue.py` processes the queue of projects and updates the database (this would be run on cron).

To get you started we include some example `.adopt` files in `\examplesadopts\` including a sample local queue.

To run the website, run:

```
python website.py
```

This will spin up a CherryPy server at `127.0.0.1:8080`.

You can now go to `127.0.0.1:8080/add/` to add a link to an `adopt` file somewhere (e.g. https://raw.githubusercontent.com/jonobacon/adopt-a-project/master/exampleadopts/example2.adopt). This will now add this to the `queue.list` queue in the same directory.

Now, to process the remote queue run:

```
python adopt-queue.py
```

This will blow away the sqllite database and update it with the new list of projects.

If you would prefer to hack on this and only load the local example data (not fetching remote files), run:

```
python adopt-queue.py -e
```

You should then see a file call `generated.html` created that lists the projects that are not maintained.
