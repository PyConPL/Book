# Expert system in Python in 5 minutes by Hubert Piotrowski

Python is known for many of its features, no doubts abopt that for sure. What is actually the most powerful feature or better though - the main key feature of any language itself to me is the fact that we can write 3rd party modules which talk to another languages or to some 3rd party frameworks.

The example of such a extension which I am going to briefly describe here is going to be pyCLIPS, which is a wrapper for CLIPS (C Language Integrated Production System) "language". It is framework written in such a way that its user interface closely resembles that of the programming language **Lisp**

It uses rules and facts which are being processed to get rules fired based on facts which in the end call for instance call assigned python functions.

![alt text](http://clipsrules.sourceforge.net/clips.gif "CLIPS Logo")

Example syntax of CLIPS

    (deftemplate car_problem
     (slot name)
     (slot status)
    )
    (deffacts trouble_shooting
     (car_problem (name ignition_key) (status on))
     (car_problem (name engine) (status wont_start))
     (car_problem (name headlights) (status work))
    )
    (defrule rule1
     (car_problem (name ignition_key) (status on))
     (car_problem (name engine) (status wont_start))
      =>
     (assert (car_problem (name starter) (status faulty)))
    )


# Installtion and first steps

The easiest way to install pyclips package is going to be by using pip

    pip install pyclips

Once you install it now we can start writing our first simple rules engine. The module fully embeds the CLIPS engine, with COOL (Clips Object Oriented Language) and environments support. This allows you to use very clear and easy to read syntax to write very complex expert systems.

# Basics




## Final note

Of course I am fully aware of the fact that pyCLIPS project is not being updated since 2008. This is not the main point in that article. I just wanted to show how to use C module for Python with external laguage and its semi-engine (something like LISP) which allows you to write much simpler and cleaner code for expert systems.

## Sources

http://pyclips.sourceforge.net/web/ - official web site for pyCLIPS project

http://clipsrules.sourceforge.net/ - A Tool for Building Expert Systems
