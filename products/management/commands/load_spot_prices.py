import pandas as pd
from django.core.management.base import BaseCommand
from products.models import SpotPrice
from django.conf import settings
import os

class Command(BaseCommand):
    help = '금/은 시세 엑셀 데이터를 DB에 저장합니다.'

    def handle(self, *args, **options):
        # 파일 경로 설정 (프로젝트 루트 기준)
        base_dir = settings.BASE_DIR
        gold_file = os.path.join(base_dir, 'Gold_prices.xlsx')
        silver_file = os.path.join(base_dir, 'Silver_prices.xlsx')

        # 데이터 적재 함수
        def load_excel(file_path, item_name):
            try:
                df = pd.read_excel(file_path)
                # 엑셀 컬럼명 확인 필요! (예: '일자', '종가'라고 가정)
                # 만약 컬럼명이 영어(Date, Close)라면 그에 맞춰 수정하세요.
                
                for index, row in df.iterrows():
                    # 날짜 형식 변환 (YYYY-MM-DD)
                    date_val = pd.to_datetime(row['일자']).date() # 컬럼명이 '일자'인 경우
                    price_val = float(row['종가']) # 컬럼명이 '종가'인 경우

                    # 중복 방지 (같은 날짜, 같은 품목이 없으면 생성)
                    if not SpotPrice.objects.filter(base_date=date_val, item_name=item_name).exists():
                        SpotPrice.objects.create(
                            item_name=item_name,
                            base_date=date_val,
                            price=price_val
                        )
                self.stdout.write(self.style.SUCCESS(f'{item_name} 데이터 저장 완료!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'{item_name} 로드 실패: {str(e)}'))

        # 파일이 존재할 경우 실행
        if os.path.exists(gold_file):
            load_excel(gold_file, 'Gold')
        else:
            self.stdout.write(self.style.WARNING(f'파일 없음: {gold_file}'))

        if os.path.exists(silver_file):
            load_excel(silver_file, 'Silver')
        else:
            self.stdout.write(self.style.WARNING(f'파일 없음: {silver_file}'))