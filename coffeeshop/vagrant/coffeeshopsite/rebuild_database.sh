#!/bin/bash
cd /vagrant/coffeeshopsite
source /secrets/config.env

sudo -u postgres psql -c "DROP DATABASE coffeeshop"
sudo -u postgres psql -c "CREATE DATABASE coffeeshop"
sudo -u postgres psql -c "ALTER DATABASE coffeeshop OWNER TO $DBOWNER;"
python3 manage.py migrate
sudo -u vagrant bash -c "/var/www/coffeeshopsite/create_users.sh"
sudo -u vagrant bash -c "/var/www/coffeeshopsite/loaddata.sh"
sudo -u vagrant bash -c "/var/www/coffeeshopsite/collectstatic.sh"
systemctl restart apache2

