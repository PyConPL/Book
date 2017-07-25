# Rapidly Prototyping Robotics with ROS and IPython



TLDR:

We will guide you through basics of robotics and ROS.  You will control robots using Python through Jupyter Notebooks.


Learn Python in a different way and move real things.

Or use this knowledge in a crazy startup project to prototype cool robotic application.



## Workshop agenda (3h):


 - Introduction to robotics and ROS ecosystem

 - Setting up and running your first ROS Node

 - ROS concepts explained: Topic, Service, Parameter

 - Using IPython Interactive Widgets to control a robot

 - Visualizing robot senses using ROS and Bokeh library

 - Tour of ROS tools with examples: Rviz, Rosbag, TF (transforms)

 - Wrapup: how to continue learning ROS, Q&A session


## Is this for me?


This workshop is intended for people familiar with basics of Python (loops, conditionals). You don’t have to know anything about robotics we will introduce you from fundamentals and give an opportunity to control robots from IPython environment. Knowledge of GNU Linux basics (we will be using Ubuntu) is welcome, however not necessary. 


Whether you are warming up with Python and want to try something more, or you are a pro and plan to do some robotic project but never did anything with ROS - we invite you to our workshop!









## Introduction and invitation



Robotics is growing and interesting field for both work and fun.


Robots -- moving, * intelligent * devices have hundreds of interacting components that enable them to do what they are supposed to do



- [play and teach children](https://www.youtube.com/watch?v=sF0tRCqvyT0)


- explore [underwater](https://www.youtube.com/watch?v=EgtZAUDqxHE) or [space](https://vimeo.com/146183080)


- be a [companion](https://www.youtube.com/watch?v=dx0zxr3D_zU) or a [teleoperation](https://www.youtube.com/watch?v=p92415PxgCw) tool


- and so much more. Did you see a robot that can [jump and paraglide](https://www.youtube.com/watch?v=_luhn7TLfWU)? Or the [creepy one](https://www.youtube.com/watch?v=rVlhMGQgDkY) that can walk on its own and open doors? [Or the one that hitchhiked through Canada](http://mir1.hitchbot.me/)?



One can say that this is possible because the hardware is getting better or that we have access to cheap components. While this is the case, software rules the world and this software is based on ROS.



ROS -- Robot Operating System, is a set of different tools that simplify robot prototyping and more and more production.


Like in most activities, in designing robots there is a huge potential to bootstrap. That is, while one robot is different than the other they all have similar needs: there is need to connect hardware (motor drivers, cameras, other sensors), multiple computers and programs, need to control it from one place, visualize how it is going and finally do some robot stuff (plan to go somewhere or do something, talk and be social or just [be cute](https://www.youtube.com/watch?v=3g-yrjh58ms).



ROS is a tool for such bootstrapping and in this workshop, you will learn how you can start interacting with such a system or maybe build your own.




We will be doing this workshop using IPython and especially, running most of the code from Jupyter Notebooks. This is because it is a perfect prototyping tool for ROS! ROS programs, called Nodes, can be written in many languages Python, C++, Java ... What IPython offers is ease of modifying a running program and understanding what is going on. This greatly speeds up prototyping -- you can see what is wrong and repair it, while still running the program!



We invite everybody interested in robotics and ROS to our workshop but actually, there is more. Making robots move using IPython is a great way to learn some interesting programming and Python concepts such as Asynchronous Events, Objects. We will try to explain these concepts as we go and you will have a nice motivation to become a Python master -- if you are not one yet ;)


In short, this workshop will be Python beginner friendly, as much as possible.



## Plan for the workshop



### Installing software and checking if everything is working



We will be using a VirtualBox machine with Ubuntu 14.04 and ROS Indigo installed. ROS is mainly Linux based as it uses built-in Linux tools and you can not run the main ROS program -- roscore from Windows. Also, it is kind of hard, to use multiple ROS versions in the same systems, so while you can have your own computer with Linux and some other version of ROS, we will not have time to debug it if something does not work.



We will connect the virtual machine to a roscore server so that you will be able to read a secret message that our Ono (social robot) prepared for you :)



### Introduction to ROS and to the state-of-the art for robotics



We will go through some interesting parts of ROS and we will give you some examples of how ROS is used in our work and in some cool work around the world.



Robotics has its own language that you may or may not be familiar with, we will say what a sensor or a servo is and what is a difference between a normal Linux box an embedded computer and a microcontroller / Arduino. This all is so that you will have easier time figuring out the practical part of the workshop -- ask questions ;)




### Making robots move



You will be introduced to an ESP bot which is a small robot with a servo- controlled head and a light sensitive sensor. To make it move you will create an ROS *publisher* that will control the servo via an IPython Interactive widget. That is, where you will move a slider robot will move. All the needed hardware will be provided by us, excluding PC computer which you have to bring on your own.  



We will also build a function that will *subscribe* to message stream (a topic) with data from robot's light sensor.



We will real time visualize this data in IPython using a Bokeh plot.



Your challenge will be to make a program that does something with this data and sends it back to the robot.



But wait, there's more :) Try to read Ono's sensors or change Ono's emotions using a different Interactive element -- a list.



We will ask Ono about his emotions using a different way to communicate -- ROS service. You will ask a Robot sending him necessary data and he will respond to you.



### ROS tools tour



ROS has a lots of tools that could be helpful for robot prototyping. There is no chance to show them all but we will show you some common use cases and tools that could fit.



There is also a great visualization tool in ROS, called Rviz. Visualization is something super necessary when building and debugging robots.While tools such as Bokeh plots are great for couple of sensors readouts, in Rviz you can see camera images or 3d point clouds and you can also see how your robot is moving on a robot model.



You will build your own visualization of a real robot that is moving. We will also show how can you calculate relative positions of two robots using TF tool -- that simplifies another super important robot issue -- calculations using transform frames (rotations, translations, and operations on quaternions).



Finally, you will see how you can start multiple *nodes* using roslaunch and how you can record what is happening using Rosbag.



## Some references and helpful links



For a nice introduction to most of the tools used here, official [ROS tutorials](http://wiki.ros.org/ROS/Tutorials) are a very good start.




There is a [Patrick Goebel book](http://wiki.ros.org/Books/ROSbyExampleVol2) which shows how you can use and combine these tools (and couple more) to create a mobile robot with arms that can make map of its own environment to plan his movement and not bump into things



For an introduction to robotics, I recommend watching some on-line videos or participating in free MOOCs. Actually one of the first MOOCs -- [AI for robotics](https://www.udacity.com/course/artificial-intelligence-for-robotics--cs373) on Udacity is a way that Igor started using Python seriously. https://www.udacity.com/course/robotics-nanodegree--nd209

