from product.models import *
from product.serializer import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from product.helper import authenticate_user


class AddCategory(APIView):
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        user_id = authenticate_user(request)
        if not user_id:
            return Response({'msg': 'Unauthorized'}, status=401)

        # Create the category and return the response
        name = request.data.get('name')
        category = Category.objects.create(user_id=user_id, name=name)
        serializer = CategorySerializer(category)
        return Response({'msg': 'Category created successfully', 'data': serializer.data})



class GetAllCategory(GenericAPIView):
  """
  :return: Get all the category from the category table.
  """
  serializer_class = CategorySerializer
  authentication_classes = [TokenAuthentication]
  def get(self, request):
    user = self.request.user.id
    items = Category.objects.all()
    serializer = CategorySerializer(items, many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class AddSubCategory(GenericAPIView):
  serializer_class = SubCategorySeriaizer
  authentication_classes = (TokenAuthentication,)
  def post(self,request):
    user_id = authenticate_user(request)
    if not user_id:
      return Response({'msg': 'Unauthorized'}, status=401)
    name = request.data.get('name')
    category = Category.objects.get(id=request.data['category'])
    sub_category = SubCategory.objects.create(user_id=user_id,name=name,category=category)    
    sub_category.save()
    serializer = SubCategorySeriaizer(sub_category)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class GetSubCategory(GenericAPIView):
  serializer_class = SubCategorySeriaizer
  authentication_classes = [TokenAuthentication]
  def get(self,request):
    items = SubCategory.objects.all()
    serializer = SubCategorySeriaizer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class AddProduct(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    def post(self,request):
      user_id = authenticate_user(request)
      if not user_id:
        return Response({'msg': 'Unauthorized'}, status=401)
      try:  
        name = request.data.get('name')
        description = request.data.get('description')
        quantity = request.data.get('quantity')
        price = request.data.get('price')
        category = Category.objects.get(id=request.data['category'])
        sub_category = SubCategory.objects.filter(category=category,id=request.data['sub_category']).first()
        product = Product.objects.create(user_id=user_id,name=name,description=description,quantity=quantity,price=price,category=category,subcategory=sub_category)
        product.save()
        serializer = ProductSerializer(product)
        return Response({"status": "success", "data": serializer.data}, status = 200)
      except:
        return Response({"status": "Not found "}, status = 400)


class GetAllProduct(GenericAPIView):
  serializer_class = ProductSerializer
  authentication_classes = [TokenAuthentication]
  def get(self,request):
    if not self.request.user.is_authenticated:
      return Response({'msg':'user not found'})
    items = Product.objects.all()
    serializer = ProductSerializer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class GetProductByCategory(GenericAPIView):
  """
  :return: All the product shown by the category.
  """
  serializer_class = ProductSerializer
  authentication_classes = [TokenAuthentication]
  def get(self,request,id):
    try:
      res = Product.objects.filter(category=id)
      serializer =  ProductSerializer(res, many=True)
      return Response({"status": "success", "data": serializer.data}, status = 200)
    except:
      return Response({"status": "Not Found"}, status = 400)


class GetProductBySubcategory(GenericAPIView):
  serializer_class = ProductSerializer
  authentication_classes = [TokenAuthentication]
  def get(self,request,id):
    if not self.request.user.is_authenticated:
      return Response({'msg':'User Not Found'})
    items = Product.objects.filter(subcategory=id)
    serializer = ProductSerializer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class GetCatSubPro(GenericAPIView):
  serializer_class = AllModelSerializer
  authentication_classes = [TokenAuthentication]
  def post(self,request,id):
    user_id = authenticate_user(request)
    if not user_id:
      return Response({'msg': 'Unauthorized'}, status=401)
    category = Category.objects.get(id=id)
    quantity = int(request.data['quantity'])
    sub_category = SubCategory.objects.filter(category=category,id=request.data['sub_category']).first()
    product = Product.objects.filter(category=category,subcategory=sub_category,id=request.data['product']).first()
    try:
      res = AllModels.objects.get(user_id=user_id,category=category,subcategory=sub_category,product=product)
      res.quantity += quantity
    except:
      res = AllModels.objects.create(user_id=user_id,category=category,subcategory=sub_category,product=product,quantity=quantity)
    res.save()
    serializer = AllModelSerializer(res)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class GetAllModel(GenericAPIView):
  serializer_class = AllModelSerializer
  authentication_classes = [TokenAuthentication]
  def get(self,request):
    if not self.request.user.is_authenticated:
      return Response({'msg':'User Not Found'})
    order = AllModels.objects.filter(user=self.request.user)
    serializer = AllModelSerializer(order,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class CreateCustomGamingPc(GenericAPIView):
    serializer_class = CustomGaminPcSerializer
    authentication_classes = [TokenAuthentication]
    def post(self, request, id):
      user_id = authenticate_user(request)
      if not user_id:
        return Response({'msg': 'Unauthorized'}, status=401)
      id = [id] if not isinstance(id, list) else id
      category = Category.objects.get(id=id[0])
      products = Product.objects.filter(category=category, id__in=request.data['product'])
      price = request.data.get('price')
      if len(products)> 3:
        return Response({'msg':'Only Select Three'})
      else:
        res = CustomGamingPc.objects.filter(user_id=user_id,category=category)
        if res.exists():
            res = res.first()
            res.product.add(*products)
        else:
            res = CustomGamingPc.objects.create(user_id=user_id,category=category,price=price)
            res.product.set(products)
        res.save()
        serializer = CustomGaminPcSerializer(res)
        return Response({'msg':'Success','data':serializer.data},status=200)


class GetCustomGamingPc(GenericAPIView):
  authentication_classes = [TokenAuthentication]
  def get(self, request):
    user_id = authenticate_user(request)
    if not user_id:
      return Response({'msg': 'Unauthorized'}, status=401)
    custom_game = CustomGamingPc.objects.filter(user_id=user_id).first()
    if custom_game is None:
        return Response({'msg': 'Custom gaming PC not found'})
    products = Product.objects.filter(category=custom_game.category)
    diff = 0
    closest_match = None
    min_diff = float('inf')
    for product in products:
        diff += abs(custom_game.price - product.price)
        if diff <= min_diff:
            closest_match = product
            min_diff = diff
    if closest_match.price == custom_game.price:
        return Response({'msg': 'Success', 'data': closest_match.to_dict()}, status=200)
    else:
        return Response({'msg': 'error', 'data': closest_match.to_dict()}, status=400)