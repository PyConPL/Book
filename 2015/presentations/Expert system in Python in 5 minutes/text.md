# Expert system in Python in 5 minutes by Hubert Piotrowski

Python is known for many of its features, no doubts about that for sure. What is actually the most powerful feature or better though - the main key feature of any language itself to me - is the fact that we can write 3rd party modules which talk to another languages or to some 3rd party frameworks.

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

# Dive into..

## Registering Python function

We can register Python function which we later on can call from CLIPS engine whenever any of the facts match any of rules. Example:

    import clips
    
    class RulesEngine:
        def __init__(self):
            clips.Conserve = True
            clips.RegisterPythonFunction(self.myDebug, 'myDebug')
            
        def myDebug(self, msg):
            print "my debug message with content: {0}" .format(msg)

Now how to load rules into rules engine. Let's assume that our system has all the rules stores in one folder and rules files are named with extension .clp

## Loading rules

Loading such a rules files can be done like this


    import clips
    
    class RulesEngine:
        def __init__(self):
            # registering python/clips functions hooks
            # of course also we can have here some log objects initialized etc
            
        def loadClipsRules(self):
            # rules_folder variable can be taken from ini file, etc
            clips.BatchStar(os.path.join(rules_folder, 'Constants.clp')) # as a single file
            
            # or batch loading
            for f in filter(lambda s: s.endswith('.clp'), os.listdir(rules_folder)):
                clips.BatchStar(os.path.join(rules_folder, f))
                # now lets check if engine did not have any errors
                e = clips.ErrorStream.Read()
                if e:
                    self.log.warning('Engine ini process has errors!\n%s' % e)
                    raise Exception()

## Debug


Now if we want to debug any of the rules that Clipe Enigne is firing or what kind of state is being updated you can dump them by adding dumping method, example:

    def dumpOutput(self):
        result = clips.TraceStream.Read()
        if result:
            self.log.info('CLIPS traceback:\n%s' % result)

        result = clips.StdoutStream.Read()
        if result:
            self.log.info('CLIPS stdout:\n%s' % result)

        result = clips.ErrorStream.Read()
        if result:
            self.log.warning('Errors:\n%s' % result)


## Facts

Before we are going to dive into details how to process facts and take some actions what first comes first - loading facts. To simplify this article let's assume that fact is a very simple state which is going to be checked by rules engine. If some states of an entity are going to match any of the rules then that particular rule(s) is going to be fired. Fired means that engine can modify any of its internal objects (another facts) or for example call one of the registered before Python functions.

How to load fact into rules engine from Python, example:

    instance = clips.FindInstance(some_object_hash)
    
Now modify facts

    instance.Slots['some_attribute'] = serializable_python_variable
    
We can also assign a fact which is a reference to another instance

    instance.Slots['some_attribute'] = clips.FindInstance(another_object_hash)
    
We can also send singnal to the engine about some changes of facts, so engine is going to be aware of our assigning process.

    clips.Eval('(modify-instance %s (some_fact (create$)))' % instance.Name)
    
    
## Let the fire burn

Once you know how to register Python functions and assign facts it is time to see how exactly you are going to use rules engine. Again to simplify the description I will assume that you alredy assigned facts, loaded rules and python functions so let's focus only on the execution of the rules.

Below function can be started as a dedicated thread which has to go into ininity loop so we are going to keep processing rules over and over again (based on changeable facts)

    def reactor():
        self.log.info('Start processing')
        rules_fired = clips.Run(5000)
        self.log.info('CLIPS fired %s rules' % (rules_fired))
        # here you can dump output to debug what was happening

Now as for debug. It is very important to notice that if debug is actually enabled the whole engine is going to be few times slowe, which of course is not recommended in production use. Another thing...it leaks realy badly with debug being on.


## Final note

Of course I am fully aware of the fact that pyCLIPS project is not being updated since 2008. This is not the main point in that article. I just wanted to show how to use C module for Python with external laguage and its semi-engine (something like LISP) which allows you to write much simpler and cleaner code for expert systems.

## Sources

http://pyclips.sourceforge.net/web/ - official web site for pyCLIPS project

http://clipsrules.sourceforge.net/ - A Tool for Building Expert Systems
