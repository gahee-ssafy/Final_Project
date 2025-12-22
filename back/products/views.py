from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DepositProducts, SpotPrice
from .serializers import DepositProductsSerializer, SpotPriceSerializer

import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity # 유사도 계산 도구
from .models import DepositProducts
from django.conf import settings


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


# [F09] : 사용자 입력 -> 벡터 
def get_recommendations(user_input_text):
    # 1. GMS API를 통해 사용자 입력을 벡터로 변환
    url = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/embeddings"
    gms_key = settings.GMS_API_KEY
    headers = {"Authorization": f"Bearer {gms_key}", "Content-Type": "application/json"}
    
    payload = {
        "model": "text-embedding-3-large",
        "input": user_input_text
    }
    
    response = requests.post(url, headers=headers, json=payload)
    user_vector = response.json()['data'][0]['embedding']

    # 2. DB에서 저장된 모든 상품과 벡터 가져오기
    products = DepositProducts.objects.exclude(embedding_vector__isnull=True)
    
    recommendations = []
    
    # 3. 코사인 유사도 계산 루프
    # 교육 자료 4권: 의미적 유사성을 수치화하는 과정
    for product in products:
        # DB에 저장된 리스트를 numpy 배열로 변환
        prod_vector = np.array(product.embedding_vector).reshape(1, -1)
        user_vec_arr = np.array(user_vector).reshape(1, -1)
        
        # 유사도 계산 (0~1 사이 값, 1에 가까울수록 닮음)
        sim_score = cosine_similarity(user_vec_arr, prod_vector)[0][0]
        
        recommendations.append({
            'product': product,
            'similarity': sim_score
        })

    # 4. 유사도 순으로 정렬하여 상위 3개 반환
    recommendations.sort(key=lambda x: x['similarity'], reverse=True)
    return recommendations[:3]

# F08 가입하기 버튼
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 로그인한 사람만 가능
def join_deposit(request, fin_prdt_cd):
    # 1. 가입하려는 상품을 찾습니다.
    product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
    user = request.user

    # 2. 이미 가입되어 있는지 확인합니다.
    # user.joined_deposits.filter(...) 방식도 가능하지만, 역참조를 쓰면 더 직관적일 때가 있습니다.
    if user.joined_deposits.filter(pk=product.pk).exists():
        # 이미 가입했으면 -> 해지 (remove)
        user.joined_deposits.remove(product)
        is_joined = False
        message = '상품 가입이 해지되었습니다.'
    else:
        # 가입 안 했으면 -> 추가 (add)
        user.joined_deposits.add(product)
        is_joined = True
        message = '상품에 가입되었습니다.'

    # 3. 변경된 상태를 프론트엔드에 알려줍니다.
    return Response({
        'is_joined': is_joined,
        'message': message
    })