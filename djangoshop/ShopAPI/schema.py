import graphene
from graphene_django import DjangoObjectType
from shopapp.models import OrderModel, Products
from django.contrib.auth.models import User

class OrderType(DjangoObjectType):
    class Meta:
        model = OrderModel
        fields = '__all__'

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class ProductType(DjangoObjectType):
    class Meta:
        model = Products
        fields = '__all__'

class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    user = graphene.Field(UserType)

    def resolve_all_orders(root, info):
        # We can easily optimize query count in the resolve method
        return OrderModel.objects.select_related('user').prefetch_related('products')

    def resolve_user(root, info, name):
        try:
            return User.objects.get(name=name)
        except User.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)


# query {
#   allOrders {
#     id
#     orderId
#     user {
#       username
#     }
  
# }
# }

# {
#   "data": {
#     "allOrders": [
#       {
#         "id": "126",
#         "orderId": 126,
#         "user": {
#           "username": "admin"
#         }
#       },
#       {
#         "id": "127",
#         "orderId": 127,
#         "user": {
#           "username": "admin"
#         }
#       },
#       {
#         "id": "128",
#         "orderId": 128,
#         "user": {
#           "username": "admin"
#         }
#       }




# query {
#   allOrders {
#     id
#     orderId
#     user {
#       username
#     }
#     products{
#       name
#       productCode
#     }
  
# }
# }

# {
#   "data": {
#     "allOrders": [
#       {
#         "id": "126",
#         "orderId": 126,
#         "user": {
#           "username": "admin"
#         },
#         "products": [
#           {
#             "name": "XBOX",
#             "productCode": 3214
#           },
#           {
#             "name": "asd",
#             "productCode": 213123
#           }
#         ]
#       },