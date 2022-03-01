. /secrets/config.env
cd /var/www/coffeeshopsite
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DBADMIN', '$DBADMIN', '$DBADMINPWD')" | python3 manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_user(pk=2, username='$DBUSER1', email='$DBUSER1EMAIL', password='$DBUSER1PWD', first_name='$DBUSER1FIRSTNAME', last_name='$DBUSER1LASTNAME')" | python3 manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_user(pk=3, username='$DBUSER2', email='$DBUSER2EMAIL', password='$DBUSER2PWD', first_name='$DBUSER2FIRSTNAME', last_name='$DBUSER2LASTNAME')" | python3 manage.py shell
echo "alter sequence auth_user_id_seq restart with 4;"
