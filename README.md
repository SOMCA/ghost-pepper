# ghost-pepper
**Ghost Pepper** is a tool to get automatically Monkey-based scenarios,
ranked based code smells counting

Requirements
------------

**Ghost Pepper** uses Python3.5 and [Simiasque](https://github.com/k0pernicus/simiasque) to work.  
You have to install Simiasque on your phone for using **Ghost-Pepper**.

**Ghost Pepper** works on a verbose application, which can save in a log
message each time a code smell is called.  
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
3.  Launch the program, sip a cocktail and get the list of
monkey seeds that run a lot of code smells!

Arguments
---------

```
usage: ghost_pepper.py [-h] [-e EVENTS] [-i ITERATIONS] [-o] -p PACKAGE
                       [-t THROTTLE] [-v]

Tool to create automatically Monkey-based scenarios, ranked based code smells
counting

optional arguments:
  -h, --help            show this help message and exit
  -e EVENTS, --events EVENTS
                        Number of events to process
  -i ITERATIONS, --iterations ITERATIONS
                        Number of iterations
  -o, --only_one        Return only one seed - the greatest number of code
                        smells called
  -p PACKAGE, --package PACKAGE
                        The Android package to run
  -t THROTTLE, --throttle THROTTLE
                        Delay between each event
  -v, --verbose         Verbose mod for top seeds
```

Credits
-------

[SOMCA](http://sofa.uqam.ca/somca.php) -
Associate research team between [Inria](http://www.inria.fr)
and [UQÀM](http://www.uqam.ca).

License
-------

GNU AFFERO GENERAL PUBLIC LICENSE (Version 3)
