from marshmallow import Schema, fields


class UserBaseSechma(Schema):
    email = fields.Email()
    password = fields.String(load_only=True)
    uid = fields.String()
    disabled = fields.Bool()
    customClaims = fields.Dict(attribute="custom_claims")
    # displayName = fields.String(attribute="display_name" )
    # emailVerified = fields.Bool(attribute="email_verified")
    # phoneNumber = fields.String(attribute="phone_number")
    # photoUrl = fields.String(attribute="photo_url")
    

class CreateUserSechma(UserBaseSechma):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    
class UidRequiredSechma(UserBaseSechma):
    uid = fields.String(required=True)
    
