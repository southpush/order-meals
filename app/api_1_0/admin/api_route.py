# -*- coding: utf-8 -*-
from flask_restful import Api
from .api_admin import AdminEditPassword, GetCode, AdminRegister, AdminGet, AdminEdit, AdminLogin, AdminLogout, AllAdminGet
from .api_user import UserGet, GetByKeyWord, DeleteUser
from .api_shop import ShopInfoGet, ShopPass, ShopNotPass, ShopInPass, ShopGet
from .api_business import BusinessGet
from .api_license import ShopLicenseGet, LicensePass, LicenseNotPass
from .api_order import CountGet, OrderGet, OrderUserGet, OrderShopGet, ChargeBackGet, ChargeBackPass, ChargeBackNotPass, OrderBackGet
from app.api_1_0.admin import api_1_0_admin as api


api_order = Api(api)
api_order.add_resource(CountGet, '/CountGet')
api_order.add_resource(OrderGet, '/OrderGet')
api_order.add_resource(OrderUserGet, '/OrderUserGet')
api_order.add_resource(OrderShopGet, '/OrderShopGet')
api_order.add_resource(ChargeBackGet, '/ChargeBackGet')
api_order.add_resource(ChargeBackPass, '/ChargeBackPass')
api_order.add_resource(ChargeBackNotPass, '/ChargeBackNotPass')
api_order.add_resource(OrderBackGet, '/OrderBackGet')

api_admin = Api(api)
api_admin.add_resource(AdminEditPassword, '/adminEditpassword')
api_admin.add_resource(GetCode, '/getCode')
api_admin.add_resource(AdminLogin, '/adminLogin')
api_admin.add_resource(AdminRegister, '/adminRegister')
api_admin.add_resource(AdminGet, '/adminGet')
api_admin.add_resource(AdminEdit, '/adminEdit')
api_admin.add_resource(AdminLogout, '/adminLogout')
api_admin.add_resource(AllAdminGet, '/AllAdminGet')

api_user = Api(api)
api_user.add_resource(UserGet, '/userGet')
api_user.add_resource(GetByKeyWord, '/GetByKeyWord')
api_user.add_resource(DeleteUser, '/DeleteUser')


api_shop = Api(api)
api_shop.add_resource(ShopInfoGet, '/ShopInfoGet')
api_shop.add_resource(ShopPass, '/ShopPass')
api_shop.add_resource(ShopNotPass, '/ShopNotPass')
api_shop.add_resource(ShopInPass, '/ShopInPass')
api_shop.add_resource(ShopGet, '/ShopGet')

api_business = Api(api)
api_business.add_resource(BusinessGet, '/BusinessGet')

api_license = Api(api)
api_license.add_resource(ShopLicenseGet, '/ShopLicenseGet')
api_license.add_resource(LicensePass, '/LicensePass')
api_license.add_resource(LicenseNotPass, '/LicenseNotPass')




