from marshmallow import Schema, fields, post_load

from ..models.user import FirebaseUser

class UserBaseSechma(Schema):
    email = fields.Email()
    password = fields.String()
    uid = fields.String()
    displayName = fields.String(attribute="display_name", )
    emailVerified = fields.Bool(attribute="email_verified")
    phoneNumber = fields.String(attribute="phone_number")
    photoUrl = fields.String(attribute="photo_url")
    disabled = fields.Bool()
    customClaims = fields.Dict(attribute="custom_claims")
    
    @post_load
    def load_user(self, data, **kwargs):
        return FirebaseUser(**data)

class CreateUserSechma(UserBaseSechma):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    
class UidRequiredSechma(UserBaseSechma):
    uid = fields.String(required=True)
    
