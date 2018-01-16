## Note:

Canella CMS is my attempt to develop a content management system from the ground up. My goal is two fold: first, to understand how CMSs work, and second, to experiment with different ways to structure a large python project.

I can say that my goals have been achieved. Now I have a comprehensive understanding of the inner workings of the major python CMSs, beside gaining invaluable insights on structuring  python code.

### End of life notice:

This repository at its current state is not useful. In my local setup I have cleaned the code, ported the project to python 3, and reorganized the code to be more testable.

So this repository will not be updated further. If time permits, I will re-upload the different modules included in this repository as separate Flask extensions, each with its test suite and documentation.


## Introduction

Canella is a Content Management System (CMS) built for simplicity and customizability, it contains all the features you expect from a CMS; including but not limited to:

* Creating, editing, and managing pages
* Pages, along with their metadata, can be managed in an intuitive,  user-friendly WYSIWYG interface by an authorized user
* Multiple Page types.
* Seamless and arbitrary page nesting
* Comprehensive page metadata and slugging support
* An interface to manage static content (such as images, documents, and audio files ...etc)
* Versioning and revision history support for page content using SQLAlchemy-Continuum 
* A fully functional blogging system, including categories and post tags.
* A Reusable user-comments system (currently implemented for blog posts)
* A Powerful inline-editing system for pages and blog posts
* A Custom WYSIWYG interface  for creating dynamic HTML forms and publishing them as pages and exporting them as a CSV file.
* User accounts and user profile using flask security
* A Powerful editable settings system, for users to edit several types of settings in a friendly manor within their browsers
* Beautifully designed administrative interface based on Flask-Admin, with a custom layout using Material Design and bootstrap in the frontend.
* A Simple, Material Design inspired user-facing web site design.

Canella CMS is built with Flask and Python. Simplicity and customizability are the overriding principles of 'Canella CMS' design, it tries to provide the absolute set of features that make up a CMS, while leveraging the Micro-ish nature of Flask to leave out many optional features for the end-user to implement. 

## Initial Setup

The following steps will help you to get started with Canella CMS as quickly as possible. Please note that to facilitate rapid prototyping the setup of this version is less than straightforward.

* Change your working directory to the repo directory

```shell
cd canella
```

* (Optionally) Create a new virtual environment to host your project dependencies
* Install all dependencies by running:

```shell
pip install requirements.txt
```

* (Windows only) Run the ./.ignore.local/setup.cmd to prepare your environment
* If you are not using windows, then set 'Canella' as your FLASK_APP environment variable
* Run the following command:

```shell
python -m flask createdb
```

* Then run the local web server:

```shell
python -m flask run
```

* Open (http://localhost:5000) in your browser and you should be welcomed by Canella's homepage
* Navigate to (http://localhost:5000/admin/) and use username (admin) and password (admin) to login to the administrative dashboard

## Copyright

COPYRIGHT (2017) MUSHARRAF OMER AND THE CANELLA CMS CONTRIBUTERS. LICENSED UNDER THE MIT LICENSE.
