#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

. /secrets/config.env

echo ". /secrets/config.env" >> /home/vagrant/.bashrc

# Install packages
apt-get update -y
apt-get install -y apache2 
apt-get install -y python3-pip python3.8-venv
apt-get install -y libapache2-mod-wsgi-py3
apt-get install -y postgresql postgresql-contrib 
apt-get install -y ssh telnet lsof
apt-get install -y python3-testresources
apt install -y net-tools iputils-ifconfig git
apt install -y nmap ufw
apt install -y pwgen
apt install -y libpq-dev

# Install mailcatcher
# Mailcatcher is an implementation of SMTP that stores email locally rather than
# forwarding it.  You can view and delete the emails via a web local interface.
apt install -y build-essential libsqlite3-dev ruby-dev
gem install mailcatcher --no-document 
cp /vagrant/mailcatcher/mailcatcher.service /etc/systemd/system/mailcatcher.service
chmod 755 /etc/systemd/system/mailcatcher.service
systemctl enable mailcatcher
service mailcatcher start

# Simple mail sending client.  Django has a much better and safer one, but we will use
# this to demonstrate command injection
apt-get install -y ssmtp
cp /vagrant/ssmtp/ssmtp.conf /etc/ssmtp/ssmtp.conf

# Install python packages
pip3 install -r /vagrant/coffeeshopsite/requirements.txt
pip3 install slowloris

# set hostname
hostnamectl set-hostname coffeeshop

# Install coffeeshop web app
ln -fs /vagrant/coffeeshopsite /var/www/

# Install apache config
rm /etc/apache2/apache2.conf
rm /etc/apache2/envvars
cp /vagrant/apache2/apache2.conf /etc/apache2/
cp /vagrant/apache2/envvars /etc/apache2/
a2enmod ssl

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

# Install web site
a2dissite 000-default.conf
cp /vagrant/apache2/000-default.conf /etc/apache2/sites-available/000-default.conf
a2ensite 000-default.conf
a2enmod rewrite
apachectl restart

# Set up database
cd /vagrant/coffeeshopsite
sudo -u postgres psql -c "CREATE DATABASE coffeeshop"
sudo -u postgres psql -c "CREATE USER $DBOWNER WITH PASSWORD '$DBOWNERPWD';"
sudo -u postgres psql -c "ALTER ROLE $DBOWNER SET client_encoding TO 'utf8'; ALTER ROLE $DBOWNER SET timezone TO 'UTC';"
sudo -u postgres psql -c "ALTER DATABASE coffeeshop OWNER TO $DBOWNER;"
python3 manage.py migrate
sudo -u vagrant bash -c "/var/www/coffeeshopsite/create_users.sh"
sudo -u vagrant bash -c "/var/www/coffeeshopsite/loaddata.sh"
sudo -u vagrant bash -c "/var/www/coffeeshopsite/collectstatic.sh"
systemctl restart apache2

# Create other users
adduser --disabled-password --gecos "" dbuser
usermod -a -G www-data vagrant
