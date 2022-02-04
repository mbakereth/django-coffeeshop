from oauth2_provider.oauth2_validators import OAuth2Validator

# The default validator will work on the primary key of the User table.
# This is an integer not usually presented to the user.  We change the default
# to use username instead.
# We also add email, first and last name for informational purposes
class CoffeeShopOAuth2Validator(OAuth2Validator):

    def get_additional_claims(self, request):
        return {
            "sub": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
