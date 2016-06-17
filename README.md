# ghost-pepper
**Ghost Pepper** is a tool to get automatically Monkey-based scenarios,
ranked based code smells counting

Requirements
------------

**Ghost Pepper** uses Python3.5.

**Ghost Pepper** works on a verbose application, which can save in a log
message each time a code smell has been called.  
Each log has to been formatted like this: "SMELL: MY.CODE.SMELL", as a **debug
log message**.  
If you don't have this verbose application, please to use **Paprika**,
a Java application which can create a verbose APK to count each code smells
called in the app.  
You can request an access of **Paprika** sending an e-mail to
[Geoffrey Hecht](mailto:geoffrey.hecht@inria.fr).

How to use it?
--------------

1.  Connect your phone to your computer.
2.  Allow developer options in your phone.
3.  Get the application's package you want to get scenarios, and replace the field
    `APP` (in `ghost_pepper.py`) with the package name of your application.
4.  Launch the program, sip a cocktail and get the list of
monkey seeds that run a lot of code smells!

Credits
-------

[SOMCA](http://sofa.uqam.ca/somca.php) -
Associate research team between [Inria](http://www.inria.fr)
and [UQÀM](http://www.uqam.ca).

License
-------

GNU AFFERO GENERAL PUBLIC LICENSE (Version 3)
