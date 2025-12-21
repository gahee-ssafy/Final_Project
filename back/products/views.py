from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DepositProducts, SpotPrice
from .serializers import DepositProductsSerializer, SpotPriceSerializer

# [F03] 예적금 상품 목록 조회
@api_view(['GET'])
def deposit_products(request):
    products = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data)

# [F04] 금/은 시세 데이터 조회
@api_view(['GET'])
def spot_price(request):
    # 예: URL 쿼리로 ?item=Gold 요청이 오면 금만 필터링
    item_name = request.GET.get('item') # Gold 또는 Silver
    
    if item_name:
        prices = SpotPrice.objects.filter(item_name=item_name).order_by('base_date')
    else:
        prices = SpotPrice.objects.all().order_by('base_date')
        
    serializer = SpotPriceSerializer(prices, many=True)
    return Response(serializer.data)