IndependentStudy
================

This independent study is to design and implement a website with the following functionality:
* [x]Users can sign up for the website.
 * [x]Users can are by default designated as a Rider
 * [x]Users can, when they navigate to the Driver page, and are not a driver, will sign up to be a driver.
* [x]Drivers can create a schedule of days, times, and locations they are available to drive.
* [ ]Riders can request a ride.
 * [ ]The system will find them routes and schedules of drivers that closesly match the rider's request.
 * [ ]The rider can select their preferred route.
 * [ ]The driver is notified of this choice.

Implementation Details
======================

The website will be built ontop of Flask and a MySql database. Flask is a framework for building websites easily in Python.
It provides the mechanisms required to handle HTTP requests and the semantics that surround that system. There are additions
to the Flask framework that are included in the `requirements.txt` file.

How to install and run?
=======================

In order to run the webserver the following needs to happen.

I recommend using a _virtualenv_ in order to run this project as there will/are a lot of dependencies that will need to be
installed.

One note is that this project is targetting Python 3.3.0+

So, to create the virtualenv the following command is run:

    virtualenv localenv

To enter into the virtualenv the following is done:

    source localenv/bin/activate

Then to install the dependencies (after activating the environment):

    pip install -r requirements.txt


This will install all the dependencies and requirements to run the project. 

Now that all of the dependencies are installed one more thing needs to happen before the site can be run. This includes creating a configuration file that 
will setup the Flask object to run on your local machine.

    [app]
    debug = True
    database_uri = sqlite:////tmp/independent_study.db
    secret_key = secret

The above example needs to be put into a file that is at `~/.independentStudy`.

After this is done the database needs to be created and prepopulated with some data so to do this the following needs to be run:

    python run.py create_db

Once the database is created run the server:

    python run.py

Then visit the website locally by going to http://127.0.0.1:5000
