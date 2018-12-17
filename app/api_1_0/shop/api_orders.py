# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse

from app.api_1_0.response import general_response
from app.main.auth import login_required_shop
from app.models.order import orders


class shop_order(Resource):
    @login_required_shop()
    def get(self, user):
        data = reqparse.RequestParser()
        data.add_argument("page", type=int)
        page = data.parse_args()["page"]
        pagination = user.order.order_by(orders.create_time.decs()).paginate(
            page, per_page=15, error_out=False
        )
        info = pagination.items
        return general_response(info={"message": info})


