Articles App
============


.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


Setting Up Development Environment
----------------------------------

Using Docker
^^^^^^^^^^^^

* Docker; if you don’t have it yet, follow the installation_instructions_.
.. _installation_instructions: https://docs.docker.com/install/#supported-platforms

* Docker Compose; refer to the official documentation for the installation_guilde_.
.. _installation_guilde: https://docs.docker.com/compose/install/


Then you can build the environment, this can take a while especially the first time you run this particular command on your development system:

    $ make build

That's it!

To run server normally at anytime, just run this command:

    $ make up

To open bash to create super user or excute any manage.py commands:

    $ make bash

To make fast migration instead of opening bash:

    $ make makemigrations

    $ make migrate

To allow debugging in development with ipdb, run server with this command:

    $ make debug django


I used make instead of docker-compose because Makefile is a simple way to organize code compilation also it make it more easier than docker-compose.


Running Locally
^^^^^^^^^^^^^^^

1- create a virtualenv.

2- Activate the virtualenv you have just created.

3- Install development requirements:

    $ pip install -r requirements/local.txt

4- Configure your DB, to make it easily you can change the DB to be sqlite3 instead of postgresql django_doc_.
.. _django_doc_: https://docs.djangoproject.com/en/2.0/ref/settings/#s-databases

5- Apply Migrations

    $ ./manage.py migrate

6- Run server

    $ ./manage.py runserver



Full Scenario in this project
-----------------------------

* Once DB is created, you will find in admin page two groups with it's custom permission **Writer** and **Editor**.

* You can create any user from admin page and add him to any group to get the permissions for this user.

* Any user can login in the project and depends on his permission the blog links will appear to him.

* You will find in the admin page 'Blog' which you can add the title and description of the blog to let writers start writing the content of the blog.

* Any blog doesn't relate with writer, will be shown in **Open Blogs** page, which writers can assign any article from this page to themself to start writing the content.

* Writer can see all his blogs in **My Blogs** page, which he can update the blog with the content and add the link for Google doc to draft this blog. Then this blog will change it's status from Draft to be In-Review.

* Editor can see all blogs with In-Review status in **Need Approved** page, which he can review the blog and take an action either accept or reject the blog. If the blog is rejected, the writer can update it again and submit for review. If the blog is accpeted, the writer can't update it again and it will be published.

* Editor can also reassign blogs from one writer to another one in **Reassign Blogs** page, which he will see all (Draft or Reject) blogs that already related by writer.

* **Blogs** page, will list all accepted blogs and this page visible to all users whether they are authorized or not.
