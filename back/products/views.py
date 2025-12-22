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