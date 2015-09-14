# Dokku. Build your own PaaS - Sergey Parkhomenko

## Introduction
Don’t like configuring and satisfying system requirements? Your dream is to deploy applications in one click? 
PaaS is the solution! During the year 2014, we all did a great dive into the world of development automatisation and 
optimisation. Riding this curve, there are a lot of cloud PaaS providers. The most famous are Heroku,
Google Apps Engine, etc. Each of them offers great opportunities for deploying, running and scaling your application,
but the first and the biggest issue is that they don’t offer enough flexibility in environment configuration.
Every developer had a situation when he needed something more from provider, who gives you limited bunch of features.
Another issue is cost. PaaS providers, mentioned above, cost money. This is not bad, because they do their job well,
but it is possible to avoid those expenses. And now is time to say one word: “Dokku”.

## Definitions
**Platform as a service (PaaS)** is a category of cloud computing services that provides a platform allowing customers
to develop, run, and manage Web applications without the complexity of building and maintaining the infrastructure
typically associated with developing and launching an app. PaaS can be delivered in two ways: as a public cloud
service from a provider, where the consumer controls software deployment and configuration settings, and the provider
provides the networks, servers, storage and other services to host the consumer's application; or as software
installed in private data centers or public infrastructure as a service and managed by internal IT departments.

**Heroku** is a cloud platform as a service (PaaS) supporting several programming languages.

**Dokku** is a Docker-powered PaaS implementation.

## PaaS use case
Let'ts imagine that you have a small blog written in Django which you need to deploy fast an easy. Also this blog is
under development and you are going to roll out updates every day during the upcoming month. Simultaneously, lets
imagine default actions which you do when you need to match such requirements. You purchase a new virtual or
dedicated server, or buy a new EC2 instance, set up a new environment for the project, or adopt your existing
infrastructure to requirements of your new blog, what can be especially painful if you have projects with other
system level requirements which can even use different languages. If you manage with very diverse technologies
stacks, sooner or later, your server becomes a trash can. But this is still not all pain which you experience in
such kind routine. If your changes to the code base require system configuration or packages modifications, you start
spending more time on deployment than on development. This is the right time to say: "Stop! I'm not a system
administrator! I don't want to configure and maintain, I want to write code!". And right after this phrase you become
a target audience for PaaS providers.

## Installing Dokku
Let's assume that you already have configured and running server where we will install Dokku.
SSH into your host machine and run the following command:
```
server $ wget -qO- https://raw.github.com/progrium/dokku/v0.3.26/bootstrap.sh | sudo DOKKU_TAG=v0.3.26 bash
```
Please, **notice** that I use the latest version of Dokku (0.3.26) for this moment.
Also, I want to emphasize that you have to run installation using **sudo** even if you are logged in via root user. This is important as this instalaltor creates a custom dokku user for executing commands and it is important to make sure if this user has enough permissions for building packages, creating configs and required directories. Otherwise your future project builds will fail.
After script finish you need to go back to your local machine console and run the following:
```
$ cat ~/.ssh/id_rsa.pub | ssh root@<machine-address> "sudo sshcommand acl-add dokku <your-app-name>"
```
Where <machine-address> is ip or hostname of your server and <your-app-name> is the name of application we will deploy. This command may be not required if you already have configured SSH keys and you log in to your server without credentials.

## Deploying sample Django application to Dokku
This guideline shows how fast and easy you can set up your own PaaS. Some points may differ depending on your OS. In
this example we will install Dokku on the server and deploy "Hello, world" Django application.

Clone any sample django application from github, cd to tha application's directory and add dokku as remote server by:
  ```
  local $ git remote add dokku dokku@<machine-address>:<your-app-name>
  ```
Push application to Dokku:
  ```
  local $ git push dokku <branch-name>:master
  ```
Pay attantion, that dokku will deploy your application **only** if you push to the master branch!

If your application requires additional dependencies like database or cache server, application deployment is not finished yet. Take a look on "Plugins" session.

## Buildpacks or why previous section is so short
If you are curious, why application deployment described in the previous is so short and where are dependencies installation, this section is for you.

So what is exactly **buildpack** and what black magic it does?

**Buildpack** is a bunch of scripts for building container image.

So what Dokku does is exactly determining what buildpack is required for your application and building a new contanier for your project. As the result you have a very high level of isolation for your applications and an awesome orchestration solution. Notice, that Dokku is compatible with Heroku buildpacks.

But what if Dokku doesn't determine a buildpack for your application correctly?

You can create a `.env` file in your application root directory and specify a buildpack by yourself:
  ```
  export BUILDPACK_URL=https://github.com/OShalakhin/heroku-buildpack-geodjango
  ```
  
  You can also just put a Dockerfile inside the project root and Dokku will pick it up and build an environment from it by default!

## Plugins
As was mentioned above, Dokku provides a very high level of isolation for your projects. Here you may ask, what if my application requires a database or a cache server. You can either use a simple database or cache server installed and configured on your server (recommended for stable production purposes), or use Dokku plugins. Dokku provides quite good set of plugins for setting up and running persistent containers for databases, caches, message queues, etc.

Let's install postgresql Dokku plugin and wire it to our application as an example.

First of all, you need to clone plugin to Dokku's plugins directory:
```
cd /var/lib/dokku/plugins
git clone https://github.com/jeffutter/dokku-postgresql-plugin postgresql
dokku plugins-install
```
Then we create a database for application:
```
server $ dokku postgresql:create <your-app-name>
```
This command automatically creates and wires a database to <your-app-name> application. It also outputs an appropriate DATABASE_URL to console which you need to put to your application's configuration.

## Debugging
If you are experiencing troubles with building your application, run `dokku trace` on your server and try to deploy your application one more time. You will get a detailed verbose output of container building process.

If you have issues with running application, run `dokku logs <your-app-name` to get logs of your app. 

You can get more info about Dokku troubleshooting from documentation. It has explanations with guidlines for lots of occasions.

## Dokku advantages over competitors
1. You pay only for the server where Dokku is installed
2. Fully customisable
3. Supports build from Dockerfile
4. Has a great plugins infrastructure
5. Easy change number of workers per application

## Dokku disadvantages
1. Doesn't scale on many machines. If you want this, explore Deis

## Conclusion
If you have a number of small applications you need to deploy, Dokku is the right choice. It will provide you high
level of isolation per application and will make you forget pain you experience during applications deployment.

## References

1. [PaaS Wiki](https://en.wikipedia.org/wiki/Platform_as_a_service)
2. [Dokku Documentation](http://progrium.viewdocs.io/dokku/)
3. [Deis](http://deis.io/)
