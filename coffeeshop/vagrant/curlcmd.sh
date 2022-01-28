curl -X POST \
    -H "Cache-Control: no-cache" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    "http://10.50.0.2/o/token/" \
           -d "client_id=6CokkDdu21z8cAqCT6VeNdPyxyUUcr1tCe3yZUlv" \
           -d "client_secret=qabz30iUFDeC68hacxLcIf10Jkgx31JSMnTfMFomPxZguzkLdiu56veRWsA1whABuXeUQ43GEwVTg85Zq3BSFKAOpZMJoFd8DNIQsmPwmOI0GvhQ7qS6gwYr690SCTJ2" \
           -d "code=gUf1K5UJus02PR9N9KLFJguJw5LvPu" \
           -d "redirect_uri=http://10.50.0.3/nonexistant/callback" \
           -d "grant_type=authorization_code"

