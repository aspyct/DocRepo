DocRepo
===

A small webapp that lets you store, preview and download documents.

It is designed to be very easy to run and backup.
For example, you could store the documents on a folder that's backed up on dropbox or any other cloud solution.

Also features an invoice counter for those of us who need it.

How to run
---
You need python3.
Run the `run.sh` script, and open http://localhost:8080

By default, access is restricted to localhost only.
If you want to change that, update the `conf.ini`.
If you intend to store sensitive documents, you should somehow secure access to it.

Customizing
---
This is a cherrypy / angularjs app, so go ahead and have fun with it. Pull requests are welcome!
