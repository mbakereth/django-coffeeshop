VMs for Web Application Security Book and Course
================================

This repo contains four VMs for performing hands-on exercises in the Web Application Security Course.  It is not a real coffee shop and is not intended for any purpose other than using during this course.

**Warning**: These VMs contain deliberate security vulnerabilities.  Do not use in a productive environment.

Prerequisites
-------------

You will need a laptop which can run Virtualbox and Vagrant.  Windows, Mac and Linux should all be able to run these.  Please install tools as per the following instructions and bring your laptop to the course.

Install software on your laptop
-------------------------------

### VirtualBox

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

The `djangi-coffeeshop` directory contains two subdirectories: `coffeeshop` and `csthirdparty`.  

Go to the `vagrant` directory of the `coffeeshop` directory and build the VM using Vagrant:

`cd django-coffeeshop/coffeeshop/vagrant`

then

`vagrant up`

This should build a VM called `coffeeshop`.  It will create the VM in VirtualBox, install Ubuntu, all the necessary packages and start an Apache web server running the toy application.

For the Spring version, you may see some errors connecting to port 8180.  You can ignore these.

Now build the second VM:

`cd ../../csthirdparty/vagrant`

`vagrant up`

This will build the second web application as a separate VM: `csthirdparty` or `csthirdpartyj`.

Test SSH to the VMs
-------------------

From the vagrant directory (`coffeeshop/django/coffeeshop/vagrant`), try ssh'ing to the VM to confirm it is running:

`cd ../../coffeeshop/vagrant`

`vagrant ssh`

`ctrl-d` to disconnect.

`cd ../../csthirdparty/vagrant`

`vagrant ssh`

`ctrl-d` to disconnect.

Test the VMs' web servers
-------------------------

The VMs are started on IP address `10.50.0.2` and `10.50.0.3`.  Visit the web servers on each of these to verify they are running:

- [http://10.50.0.2/](http://10.50.0.2/)
- [http://10.50.0.3/](http://10.50.0.3/)

The first link should show the Coffee Shop Application.  The second link will show a very simple page to confirm the server is running.

Test Mailcatcher is running
---------------------------

As for real applications, the toy coffee shop occasionally needs to send email.  This is simulated with Mailcatcher which is running on each of the four VMs.  

Mailcatcher is an SMTP implementation that saves emails locally and displays them via a simple web server.  It does not actually send the email.  The From and To addresses can be anything as no external connection is made.

The SMTP server is running on port 25 and the web server on port 1080.  Confirm Mailcatcher is running by visiting

- [http://10.50.0.2:1080/](http://10.50.0.2:1080/)
- [http://10.50.0.3:1080/](http://10.50.0.3:1080/)

To use the mail server to send email in your code, connect to port 25 as normal.

### Web Servers

The Django applications are served by wsgi running as an Apache module.  It is started automatically on boot and logs to Apache's log files in `/var/log/apache2`.


