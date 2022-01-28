. /secrets/config.env
cd /var/www/csthirdparty
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DBADMIN', '$DBADMIN', '$DBADMINPWD')" | python3 manage.py shell

