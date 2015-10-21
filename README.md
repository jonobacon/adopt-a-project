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

**Requirements**: this code only requires the standard Python library.

To get you started we include some example `.adopt` files in `\examplesadopts\` including a sample local queue.

To process the remote queue:

```
python adopt-queue.py
```

If you run the following it will process the example local queue and local adopt files (saves in fetching remote files):

```
python adopt-queue.py -e
```

You should then see a file call `generated.html` created that lists the projects that are not maintained.
