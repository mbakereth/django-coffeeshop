. /secrets/config.env
cd /var/www/coffeeshopsite
python3 manage.py loaddata coffeeshop/fixtures/product.json
python3 manage.py loaddata coffeeshop/fixtures/address.json
python3 manage.py loaddata coffeeshop/fixtures/card.json
python3 manage.py loaddata coffeeshop/fixtures/stocklevel.json

