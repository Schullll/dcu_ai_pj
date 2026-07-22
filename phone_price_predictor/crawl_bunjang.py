import requests
import re
import time
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 노이즈 매물 제외 키워드 (매입광고/재고정리 광고/액세서리 등만 — 파손은 F등급으로 포함시킴)
EXCLUDE_KEYWORDS = [
    '매입', '정크', '계정락', '재고정리', 
    '케이스', '커버', '필름', '보호필름', '충전기', '거치대', '스트랩', '카드지갑'
]

# (표시용 모델명, [검색에 쓸 키워드 변형들])
target_models = [
    ("아이폰 13", ["아이폰 13"]),
    ("아이폰 13 프로", ["아이폰 13 프로", "아이폰 13 Pro", "아이폰13pro"]),
    ("아이폰 13 프로맥스", ["아이폰 13 프로맥스", "아이폰 13 Pro Max", "아이폰13promax"]),
    ("아이폰 14", ["아이폰 14"]),
    ("아이폰 14 프로", ["아이폰 14 프로", "아이폰 14 Pro", "아이폰14pro"]),
    ("아이폰 14 프로맥스", ["아이폰 14 프로맥스", "아이폰 14 Pro Max", "아이폰14promax"]),
    ("아이폰 15", ["아이폰 15"]),
    ("아이폰 15 프로", ["아이폰 15 프로", "아이폰 15 Pro", "아이폰15pro"]),
    ("아이폰 15 프로맥스", ["아이폰 15 프로맥스", "아이폰 15 Pro Max", "아이폰15promax"]),
    ("아이폰 16", ["아이폰 16"]),
    ("아이폰 16 프로", ["아이폰 16 프로", "아이폰 16 Pro", "아이폰16pro"]),
    ("아이폰 16 프로맥스", ["아이폰 16 프로맥스", "아이폰 16 Pro Max", "아이폰16promax"]),
    ("갤럭시 S22", ["갤럭시 S22"]),
    ("갤럭시 S22 플러스", ["갤럭시 S22 플러스", "갤럭시 S22+", "갤럭시S22플러스", "갤럭시 S22 Plus"]),
    ("갤럭시 S22 울트라", ["갤럭시 S22 울트라", "갤럭시S22울트라", "갤럭시 S22 Ultra"]),
    ("갤럭시 S23", ["갤럭시 S23"]),
    ("갤럭시 S23 플러스", ["갤럭시 S23 플러스", "갤럭시 S23+", "갤럭시S23플러스", "갤럭시 S23 Plus"]),
    ("갤럭시 S23 울트라", ["갤럭시 S23 울트라", "갤럭시S23울트라", "갤럭시 S23 Ultra"]),
    ("갤럭시 S24", ["갤럭시 S24"]),
    ("갤럭시 S24 플러스", ["갤럭시 S24 플러스", "갤럭시 S24+", "갤럭시S24플러스", "갤럭시 S24 Plus"]),
    ("갤럭시 S24 울트라", ["갤럭시 S24 울트라", "갤럭시S24울트라", "갤럭시 S24 Ultra"]),
    ("갤럭시 S25", ["갤럭시 S25"]),
    ("갤럭시 S25 플러스", ["갤럭시 S25 플러스", "갤럭시 S25+", "갤럭시S25플러스", "갤럭시 S25 Plus"]),
    ("갤럭시 S25 울트라", ["갤럭시 S25 울트라", "갤럭시S25울트라", "갤럭시 S25 Ultra"]),
    ("갤럭시 Z플립3", ["갤럭시 Z플립3", "갤럭시 Z Flip3"]),
    ("갤럭시 Z플립4", ["갤럭시 Z플립4", "갤럭시 Z Flip4"]),
    ("갤럭시 Z플립5", ["갤럭시 Z플립5", "갤럭시 Z Flip5"]),
    ("갤럭시 Z폴드3", ["갤럭시 Z폴드3", "갤럭시 Z Fold3"]),
    ("갤럭시 Z폴드4", ["갤럭시 Z폴드4", "갤럭시 Z Fold4"]),
    ("갤럭시 Z폴드5", ["갤럭시 Z폴드5", "갤럭시 Z Fold5"]),
]

all_results = []
seen_pids = set()

for model_label, keyword_variants in target_models:
    print(f"수집 중: {model_label}")

    for keyword in keyword_variants:
        url = f"https://api.bunjang.co.kr/api/1/find_v2.json?q={keyword}&page=0&n=100"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            data = res.json()
            items = data.get('list', [])

            for item in items:
                pid = item.get('pid')
                if pid in seen_pids:
                    continue
                seen_pids.add(pid)

                name = item.get('name', '')
                price = item.get('price', '0')

                if any(kw in name for kw in EXCLUDE_KEYWORDS):
                    continue

                try:
                    price = int(price)
                except:
                    continue

                if price < 30000 or price > 4000000:
                    continue

                storage_match = re.search(r'(\d{2,4})\s*(GB|gb|TB|tb|기가)', name)
                if not storage_match:
                    continue

                storage = storage_match.group(0)

                all_results.append({
                    'search_keyword': model_label,
                    'name': name,
                    'price': price,
                    'storage': storage,
                    'update_time': item.get('update_time'),
                    'used_flag': item.get('used')
                })

        except Exception as e:
            print(f"  에러 발생 ({keyword}): {e}")

        time.sleep(0.5)

df = pd.DataFrame(all_results)
print(f"\n1차 수집 완료: 총 {len(df)}개 매물")

# 모델별 IQR 기반 이상치 제거
Q1 = df.groupby('search_keyword')['price'].transform(lambda x: x.quantile(0.25))
Q3 = df.groupby('search_keyword')['price'].transform(lambda x: x.quantile(0.75))
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_cleaned = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)].copy()
print(f"IQR 필터링 후: 총 {len(df_cleaned)}개 매물")

# 저장용량 표기 통일 (256GB/256기가/256gb → 숫자 256)
def normalize_storage(s):
    if pd.isna(s):
        return None
    num = re.search(r'\d+', s)
    return int(num.group()) if num else None

df_cleaned['storage_gb'] = df_cleaned['storage'].apply(normalize_storage)

# 상태 등급 추출 (F: 파손/고장/불량, S: 미개봉/무잔상, A: S급표기, B: 일반)
def extract_condition(name):
    if any(kw in name for kw in ['파손', '고장', '불량', '부품용', '액정파손', '작동불가']):
        return 'F'
    elif any(kw in name for kw in ['미개봉', '풀박스', '무잔상', '잔상없음', '미사용', '새상품']):
        return 'S'
    elif 'S급' in name:
        return 'A'
    elif any(kw in name for kw in ['A+급', 'A급']):
        return 'B'
    else:
        return 'B'

df_cleaned['condition'] = df_cleaned['name'].apply(extract_condition)

# 브랜드 구분
def get_brand(keyword):
    return 'Apple' if '아이폰' in keyword else 'Samsung'

df_cleaned['brand'] = df_cleaned['search_keyword'].apply(get_brand)

# 완전 중복 매물 제거 (제목+가격 동일)
df_cleaned = df_cleaned.drop_duplicates(subset=['name', 'price'], keep='first')
print(f"완전 중복 제거 후: 총 {len(df_cleaned)}개 매물")

df_cleaned.to_csv('bunjang_final_data.csv', index=False, encoding='utf-8-sig')
print("\n저장 완료: bunjang_final_data.csv")
print(df_cleaned['condition'].value_counts())
print()
print(df_cleaned.groupby('condition')['price'].agg(['mean', 'count']))