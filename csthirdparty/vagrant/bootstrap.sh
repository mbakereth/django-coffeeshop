#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

. /secrets/config.env

echo ". /secrets/config.env" >> /home/vagrant/.profile
echo ". /secrets/config.env" >> /home/vagrant/.bashrc

# Install packages
apt-get update -y
apt-get install -y apache2 
apt-get install -y python3-pip
apt-get install -y libapache2-mod-wsgi-py3
apt-get install -y postgresql postgresql-contrib 
apt-get install -y ssh
apt install -y net-tools
apt install -y nmap

# set hostname
hostnamectl set-hostname csthirdparty

# Install mailcatcher
# Mailcatcher is an implementation of SMTP that stores email locally rather than
# forwarding it.  You can view and delete the emails via a web local interface.
apt install -y build-essential libsqlite3-dev ruby-dev
gem install mailcatcher --no-document
cp /vagrant/mailcatcher/mailcatcher.service /etc/systemd/system/mailcatcher.service
chmod 755 /etc/systemd/system/mailcatcher.service
systemctl enable mailcatcher
service mailcatcher start

# Install python packages
# Django web framework and optional packages for it
# Psycopg2 is the Python library to connect to Postgres
# Sqlalchemy is not normally needed for Django apps but we use it to demonstrate
# SQL Injection vulnerabilities
# Jupyerlab is a handy way of experimenting with Python, and supported by Django,
# but not used directly in these demos.
pip3 install django==3.2.7
pip3 install django-extensions
pip3 install django-templatetags
pip3 install django-countries
pip3 install djangorestframework
pip3 install psycopg2-binary
pip3 install sqlalchemy
pip3 install --no-dependencies django-bootstrap4==2.2.0
pip3 install django-loginas
pip3 install jupyterlab
pip3 install django-cors-headers
pip3 install django-csp

# Install apache config
rm /etc/apache2/apache2.conf
rm /etc/apache2/envvars
cp /vagrant/apache2/apache2.conf /etc/apache2/
cp /vagrant/apache2/envvars /etc/apache2/

# Set up Postgres
pgvers=12
mv /etc/postgresql/${pgvers}/main/postgresql.conf /etc/postgresql/${pgvers}/main/postgresql.conf.orig
mv /etc/postgresql/${pgvers}/main/pg_hba.conf /etc/postgresql/${pgvers}/main/pg_hba.conf.orig
cp /vagrant/postgres/postgresql.conf /etc/postgresql/${pgvers}/main/postgresql.conf
cp /vagrant/postgres/pg_hba.conf /etc/postgresql/${pgvers}/main/pg_hba.conf
chown postgres.postgres /etc/postgresql/${pgvers}/main/postgresql.conf /etc/postgresql/${pgvers}/main/pg_hba.conf
chown postgres.postgres /etc/postgresql/${pgvers}/main/pg_hba.conf
chmod 640 /etc/postgresql/${pgvers}/main/pg_hba.conf
service postgresql restart

# Install csthirdparty web app
ln -fs /vagrant/csthirdpartysite /var/www/

# Install web site
a2dissite 000-default.conf
cp /vagrant/apache2/000-default.conf /etc/apache2/sites-available/000-default.conf
a2ensite 000-default.conf
a2enmod rewrite
a2enmod headers
apachectl restart

# Set up database
cd /vagrant/csthirdpartysite
sudo -u postgres psql -c "CREATE DATABASE csthirdparty"
sudo -u postgres psql -c "CREATE USER $DBOWNER WITH PASSWORD '$DBOWNERPWD';"
sudo -u postgres psql -c "ALTER ROLE $DBOWNER SET client_encoding TO 'utf8'; ALTER ROLE $DBOWNER SET timezone TO 'UTC';"
sudo -u postgres psql -c "ALTER DATABASE csthirdparty OWNER TO $DBOWNER;"
python3 manage.py migrate
sudo -u vagrant bash -c "/var/www/csthirdpartysite/create_users.sh"
sudo -u vagrant bash -c "/var/www/csthirdpartysite/loaddata.sh"
sudo -u vagrant bash -c "/var/www/csthirdpartysite/collectstatic.sh"
systemctl restart apache2

# Add other users
adduser --disabled-password --gecos "" dbuser
