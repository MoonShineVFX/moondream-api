from marshmallow import Schema, fields


class UserBaseSechma(Schema):
    email = fields.Email()
    password = fields.String()
    uid = fields.String()
    displayName = fields.String(attribute='display_name', )
    emailVerified = fields.Bool(attribute='email_verified')
    phoneNumber = fields.String(attribute='phone_number')
    photoUrl = fields.String(attribute='photo_url')
    disabled = fields.Bool()


class UserBaseRequiredSchma(UserBaseSechma):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserUpdateSchma(UserBaseSechma):
    uid = fields.String(required=True)
    custom_claims = fields.String()


class UserResetPasswordSchma(Schema):
    email = fields.Email(required=True)


class UserDeleteSchma(Schema):
    uid = fields.String(required=True)
