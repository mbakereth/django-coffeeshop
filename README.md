Web Application Security Practice VMs
=====================================

This repo is intended to accompany:

- My upcoming Web Application Security book
- My web application security courses. 

The repo contains two VMs for performing hands-on exercises.  It is not a real coffee shop and is not intended for any purpose other than using with the book or courses.

**Warning**: These VMs contain deliberate security vulnerabilities.  Do not use as-is in a productive environment.

Prerequisites
-------------

You will need a laptop which can run Virtualbox and Vagrant.  Windows, Mac and Linux should all be able to run these.  On M1 Macs, at the time of writing, Virtualbox does not work, but you can use Docker instead.  Please install tools as per the following instructions.

Install software on your laptop
-------------------------------

### Docker (Mac M1 Only)

Visit [https://www.docker.com/get-started/](https://www.docker.com/get-started/) and follow the link to install Docker Desktop for your architecture.

Launch Docker Desktop and click on the preferences button (top of the window, to the right of the window title). Click on *Resources*, slide *Memory* up to 4GB and click *Apply & Restart* (the unit on ElasticSearch in particular needs this much memory).

### Xcode and Docker Mac Connect (Mac M1 Only)

We need Docker Mac Connect to provide IP addresses to our Docker containers so we can access them from web browsers.  

Go to the Apple App Store and search for Xcode.  Click the *Get* button on the search result to install it.

If you haven't already, install the Homebrew package manager by visiting [https://brew.sh](https://brew.sh) and following the instructions there.

Install Docker Mac Connect with

```
brew install chipmk/tap/docker-mac-net-connect
sudo brew services start chipmk/tap/docker-mac-net-connect
```

### VirtualBox (Not Mac M1)

VirtualBox provides the virtualisation for the VMs needed for the course.

Go to [virtualbox.org](https://virtualbox.org) and follow the directions to download and install VirtualBox for your OS.

Also install the VirtualBox extension pack.  Follow the Downloads link on the VirtualBox page and click on *All supported platforms* under **VirtualBox 6.x.x Oracle VM VirtualBox Extension**.

### Vagrant

Vagrant lets you script and repeat the creation and provisioning of VMs.  We will use Vagrant to automatically build our web application VMs.  Vagrant uses VirtualBox for the actual virtualisation.

Visit [vagrantup.com/downloads](https://www.vagrantup.com/downloads).  Download Vagrant for your OS.  

### Web browsers

Ensure you have recent versions of **Firefox** and **Chrome** installed on your laptop.

### HTTP Toolkit

HTTP Toolkit allows you to intercept and view requests and responses between your web browser and pages you visit.

Visit [httptoolkit.tech](https://httptoolkit.tech) and download and install HTTP Toolkit.

Download the VMs
----------------

The exercises are based on a toy online coffee store.  It consists of two VMs, both in the same Git repo.  Download it with

`git clone git@github.com:mbakereth/django-coffeeshop.git`

or

`git clone https://github.com/mbakereth/django-coffeeshop.git`

Build the two VMs
-----------------

The `django-coffeeshop` directory contains two subdirectories: `coffeeshop` and `csthirdparty`.  

Go to the `vagrant` directory of the `coffeeshop` directory and build the VM using Vagrant:

`cd django-coffeeshop/coffeeshop/vagrant`

If you don't have an M1 Mac, build the machine with 

`vagrant up`

If you do have an M1 Mac, use the following command instead:

`vagrant up --provider docker`

This should build a VM called `coffeeshop`.  It will create the VM in VirtualBox (or a Docker container on Mac M1, configured to look and feel like a VM), install Ubuntu, all the necessary packages and start an Apache web server running the toy application.

Now build the second VM:

`cd ../../csthirdparty/vagrant`

`vagrant up`

or, on Mac M1, 

`vagrant up --provider docker`

This will build the second web application as a separate VM: `csthirdparty`.

Test SSH to the VMs
-------------------

From the vagrant directory (`coffeeshop/django/coffeeshop/vagrant`), try ssh'ing to the VM to confirm it is running:

`cd ../../coffeeshop/vagrant`

`vagrant ssh`

`Ctrl-d` to disconnect.

`cd ../../csthirdparty/vagrant`

`vagrant ssh`

`Ctrl-d` to disconnect.

Test the VMs' web servers
-------------------------

The VMs are started on IP address `10.50.0.2` and `10.50.0.3`.  Visit the web servers on each of these to verify they are running:

- [http://10.50.0.2/](http://10.50.0.2/)
- [http://10.50.0.3/](http://10.50.0.3/)

The first link should show the Coffee Shop Application.  The second link will show a very simple page to confirm the server is running.

Test MailCatcher is running
---------------------------

As for real applications, the toy coffee shop occasionally needs to send email.  This is simulated with MailCatcher which is running on each of the two VMs.  

MailCatcher is an SMTP implementation that saves emails locally and displays them via a simple web server.  It does not actually send the email.  The From and To addresses can be anything as no external connection is made.

The SMTP server is running on port 25 and the web server on port 1080.  Confirm MailCatcher is running by visiting

- [http://10.50.0.2:1080/](http://10.50.0.2:1080/)
- [http://10.50.0.3:1080/](http://10.50.0.3:1080/)

To use the mail server to send email in your code, connect to port 25 as normal.

### Web Servers

The Django applications are served by Wsgi running as an Apache module.  It is started automatically on boot and logs to Apache's log files in `/var/log/apache2`.

Restarting the Web Server
-------------------------

If you make changes to the code, you will need to restart Apache from within the VM.  First ssh to it with

```
cd django-coffeeshop/coffeeshop/vagrant
vagrant ssh
```
or

```
cd django-coffeeshop/csthirdparty/vagrant
vagrant ssh
```
Then restart Apache with

```
sudo apachectl restart
```

Shutting Down the VM
--------------------

From within the VM's vagrant directory (on your host, not inside the VM), run

```
vagrant down
```
To destroy the VM and deallocate the disk it consumes, run

```
vagrant destroy
```

To bring the VM up again, run

```
vagrant up
```
If the VM was not destroyed, it will simply boot again.  If you previously destroyed, it, Vagrant will recreate the VM and boot it.

You're Ready!
-------------

If you're doing one of the web app security courses, you now have eveything you need to start the course.

If you're following the book, you are now ready to start the hands-on exercises.
