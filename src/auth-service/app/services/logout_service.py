from flask_jwt_extended import unset_jwt_cookies



def logout_user(response):
    logout_res = unset_jwt_cookies(response)

    return logout_res 