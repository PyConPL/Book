# Expert system in Python in 5 minutes by Hubert Piotrowski

As all we know Python is known for many of its features, flexibility, scalability and simplicity for sure. What is actually the most powerful feature of Python language to me? We can write Python extension modules which communicate with other languages.

The example of such an extension which I am going to briefly describe here is pyCLIPS, which is a wrapper for CLIPS (C Language Integrated Production System) "language". It is framework written in such a way that its user interface closely resembles that of the programming language **Lisp**.

Before we will continue, please threat this article as an example of how to build expert system by using Python. It is not any kind of a try to convince you to use expert systems for building complex software. It is more like showing you the other way of solving some design problems.

## CLIPS

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

Once you install it we can start writing our first simple rules engine. The module fully embeds the CLIPS engine, with COOL (Clips Object Oriented Language). This allows you to use very clear and easy to read syntax to write very complex expert systems.

# Dive into..

## Registering Python function

We can register Python function as a callback that will be called by CLIPS engine whenever any of the facts match any of the rules. Example:

    import clips
    
    class RulesEngine:
        def __init__(self):
            clips.Conserve = True # important to be True to be able to start catching output from CLIPS
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


If we want to debug any of the rules that CLIPS Engine is firing or get to know what kind of state is being updated we can dump them by adding dumping method, eg.:

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

Before we are going to dive into details how to process facts and take some actions what first comes first - loading facts. To simplify this article let's assume that fact is a very simple state which is going to be checked by rules engine. If some states of an entity are going to match any of the rules then that particular rule(s) is going to be fired. Fired means that engine can modify any of its internal objects (another facts) or call one of the previously registered Python functions.

Example class definition which describes an object can look like this

    (defclass MY_BASE_CLASS (role concrete)
       (slot row-source (type STRING))
       (slot row-time (type INTEGER))
    )

Naturally also we can use inheritance:

    (defclass MY_OBJECT (is-a MY_BASE_CLASS) (role concrete)
       (slot some_hash_field (type STRING))
       (slot param_1 (type STRING))
       (slot param_2 (type STRING))
    )

How to load fact into rules engine from Python, example:

    instance = clips.FindInstance(some_object_hash)
    
Now modify facts

    instance.Slots['param_1'] = serializable_python_variable
    
We can also assign a fact which is a reference to another instance

    instance.Slots['some_hash_field'] = clips.FindInstance(another_object_hash)
    
We can also send singnal to the engine about some changes of facts, so engine is going to be aware of our assigning process.

    clips.Eval('(modify-instance %s (some_fact (create$)))' % instance.Name)
    
    
## Let the fire burn

Once you know how to register Python functions and assign facts it is time to see how exactly you are going to use rules engine. Again to simplify the description I will assume that you alredy assigned facts, loaded rules and python functions so let's focus only on the execution of the rules.

Below function can be started as a dedicated thread which has to go into infinite loop so we are going to keep processing rules over and over again (based on changeable facts)

    def reactor():
        self.log.info('Start processing')
        rules_fired = clips.Run(5000) # max rules to fire for that loop
        self.log.info('CLIPS fired %s rules' % (rules_fired))
        # here you can dump output to debug what was happening
        self.myDebug()
        
## Warning

Now as for debug. From my prsonal experience. It is very important to remember that if debug is actually enabled the whole engine is going to be few times slower (in some cases), which of course is not recommended in production use. Another thing... debug being on can make engine to leak. It does not happen always and it stronlgy depends on numbers of loaded facts (few thousands and more). But that is the story for another article.


## Final note

Of course I am fully aware of the fact that pyCLIPS project is not being updated since 2008. This is not the main point in that article. I just wanted to show how to use C module for Python with external laguage and its semi-engine (something like LISP) which allows you to write much simpler and cleaner code for expert systems.

## Sources

http://pyclips.sourceforge.net/web/ - official web site for pyCLIPS project

http://clipsrules.sourceforge.net/ - A Tool for Building Expert Systems
