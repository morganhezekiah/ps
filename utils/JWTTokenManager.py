import jwt
from users.models import User
from django.conf import settings
from datetime import datetime, timedelta



class UserTokenManager(object):
    def generateToken(self, user):
        exp = datetime.now()+timedelta(days = 1/(24*2))
        tokenPayload={
            "userId":user.id,
            "userSlug":user.slug,
            "exp":exp
            
        }

        token = jwt.encode(tokenPayload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return token

    def decodeToken(self, token):
        try:
            payload = jwt.decode(token,settings.JWT_SECRET, algorithms=(settings.JWT_ALGORITHM,))
            userSlug = payload.get("userSlug")
            userId = payload.get("userId")
            user = User.object.get(id=userId)
            return {"state":True,"user":user, "message":"Token correct"}
            
        except jwt.ExpiredSignatureError as tokenExpiredException:
            return {"state":False, "message":"Token seems to be expired"}