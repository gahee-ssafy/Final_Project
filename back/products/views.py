from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DepositProducts, SpotPrice
from .serializers import DepositProductsSerializer, SpotPriceSerializer

import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity # 유사도 계산 도구
from .models import DepositProducts
from django.conf import settings
from django.http import JsonResponse


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



# [F09] 추천 기능 

def cosine_similarity(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


@api_view(['POST'])
def recommend(request):
    # 1. 프론트엔드에서 보낸 사용자 입력 받기
    # 하드코딩
    user_input = request.data.get('message')
    
    # 2. 사용자 입력 임베딩 (GMS API)
    GMS_API_KEY="S14P02EB04-212fb62d-0aaf-410d-a2ab-27f5f8993de2"
    
    url = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {GMS_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "text-embedding-3-large", "input": user_input}
    
    response = requests.post(url, headers=headers, json=payload)
    user_vector = response.json()['data'][0]['embedding']

    # 3. DB 상품들과 유사도 비교
    products = DepositProducts.objects.exclude(embedding_vector__isnull=True)
    results = []
    for p in products:
        score = cosine_similarity(user_vector, p.embedding_vector)
        results.append({
            'name': p.fin_prdt_nm,
            'bank': p.kor_co_nm,
            'similarity': round(float(score), 4)
        })

    # 4. 정렬 후 TOP 3 반환
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return JsonResponse({'recommendations': results[:3]})