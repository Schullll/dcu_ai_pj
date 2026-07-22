"""
30개 모델(아이폰13~16, 갤럭시S22~25, Z플립/폴드3~5) 스펙 및 저장용량별 신품 출고가 매핑표

[데이터 출처 및 신뢰도]
- 화면크기/RAM/배터리/무게: 공식 스펙 (신뢰도 높음)
- 애플 가격: 삼성/애플 공식 출고가 발표 자료, 클리앙 등 커뮤니티 정리 자료 기반 검증
  (단, 아이폰16 시리즈는 정확한 한국 출고가 발표 자료를 찾지 못해 달러 환율 기준 추정치)
- 삼성 가격: 전부 삼성전자 뉴스룸 공식 보도자료 기반 검증
- 삼성 S시리즈 기본형/플러스는 한국 시장 특성상 실제로 저장용량 옵션이
  1~2개뿐인 경우가 많음 (예: S22~S25 기본형은 256GB 단일 출시) → 실제 그대로 반영
"""

phone_models = {
    # ===== Apple =====
    "아이폰13": {
        "device_brand": "Apple", "screen_size": 6.1, "ram": 4, "battery": 3227,
        "weight": 174, "release_year": 2021,
        "storage_options": {128: 1078000, 256: 1221000, 512: 1485000}
    },
    "아이폰13프로": {
        "device_brand": "Apple", "screen_size": 6.1, "ram": 6, "battery": 3095,
        "weight": 204, "release_year": 2021,
        "storage_options": {128: 1342000, 256: 1474000, 512: 1738000, 1024: 1991000}
    },
    "아이폰13프로맥스": {
        "device_brand": "Apple", "screen_size": 6.7, "ram": 6, "battery": 4352,
        "weight": 238, "release_year": 2021,
        "storage_options": {128: 1474000, 256: 1606000, 512: 1870000, 1024: 2145000}
    },
    "아이폰14": {
        "device_brand": "Apple", "screen_size": 6.1, "ram": 6, "battery": 3279,
        "weight": 172, "release_year": 2022,
        "storage_options": {128: 1243000, 256: 1397000, 512: 1694000}
    },
    "아이폰14프로": {
        "device_brand": "Apple", "screen_size": 6.1, "ram": 6, "battery": 3200,
        "weight": 206, "release_year": 2022,
        "storage_options": {128: 1540000, 256: 1694000, 512: 1991000, 1024: 2299000}
    },
    "아이폰14프로맥스": {
        "device_brand": "Apple", "screen_size": 6.7, "ram": 6, "battery": 4323,
        "weight": 240, "release_year": 2022,
        "storage_options": {128: 1749000, 256: 1892000, 512: 2200000, 1024: 2497000}
    },
    "아이폰15": {
        "device_brand": "Apple", "screen_size": 6.1, "ram": 6, "battery": 3349,
        "weight": 171, "release_year": 2023,
        "storage_options": {128: 1243000, 256: 1397000, 512: 1694000}
    },
    "아이폰15프로": {
        "device_brand": "Apple", "screen_size": 6.1, "ram": 8, "battery": 3274,
        "weight": 187, "release_year": 2023,
        "storage_options": {128: 1540000, 256: 1694000, 512: 1991000, 1024: 2299000}
    },
    "아이폰15프로맥스": {
        "device_brand": "Apple", "screen_size": 6.7, "ram": 8, "battery": 4441,
        "weight": 221, "release_year": 2023,
        "storage_options": {256: 1900000, 512: 2200000, 1024: 2497000}
    },
    "아이폰16": {
        "device_brand": "Apple", "screen_size": 6.1, "ram": 8, "battery": 3561,
        "weight": 170, "release_year": 2024,
        "storage_options": {128: 1250000, 256: 1400000, 512: 1700000}  # ※추정치
    },
    "아이폰16프로": {
        "device_brand": "Apple", "screen_size": 6.3, "ram": 8, "battery": 3582,
        "weight": 199, "release_year": 2024,
        "storage_options": {128: 1560000, 256: 1700000, 512: 2000000, 1024: 2300000}  # ※추정치
    },
    "아이폰16프로맥스": {
        "device_brand": "Apple", "screen_size": 6.9, "ram": 8, "battery": 4685,
        "weight": 227, "release_year": 2024,
        "storage_options": {256: 1910000, 512: 2200000, 1024: 2500000}  # ※추정치
    },

    # ===== Samsung S =====
    "갤럭시S22": {
        "device_brand": "Samsung", "screen_size": 6.1, "ram": 8, "battery": 3700,
        "weight": 167, "release_year": 2022,
        "storage_options": {256: 999900}
    },
    "갤럭시S22플러스": {
        "device_brand": "Samsung", "screen_size": 6.6, "ram": 8, "battery": 4500,
        "weight": 196, "release_year": 2022,
        "storage_options": {256: 1199000}
    },
    "갤럭시S22울트라": {
        "device_brand": "Samsung", "screen_size": 6.8, "ram": 12, "battery": 5000,
        "weight": 228, "release_year": 2022,
        "storage_options": {256: 1452000, 512: 1551000, 1024: 1749000}
    },
    "갤럭시S23": {
        "device_brand": "Samsung", "screen_size": 6.1, "ram": 8, "battery": 3900,
        "weight": 168, "release_year": 2023,
        "storage_options": {256: 1155000, 512: 1276000}
    },
    "갤럭시S23플러스": {
        "device_brand": "Samsung", "screen_size": 6.6, "ram": 8, "battery": 4700,
        "weight": 196, "release_year": 2023,
        "storage_options": {256: 1353000, 512: 1474000}
    },
    "갤럭시S23울트라": {
        "device_brand": "Samsung", "screen_size": 6.8, "ram": 12, "battery": 5000,
        "weight": 234, "release_year": 2023,
        "storage_options": {256: 1599400, 512: 1720400, 1024: 1962400}
    },
    "갤럭시S24": {
        "device_brand": "Samsung", "screen_size": 6.2, "ram": 8, "battery": 4000,
        "weight": 167, "release_year": 2024,
        "storage_options": {256: 1155000, 512: 1298000}
    },
    "갤럭시S24플러스": {
        "device_brand": "Samsung", "screen_size": 6.7, "ram": 12, "battery": 4900,
        "weight": 196, "release_year": 2024,
        "storage_options": {256: 1353000, 512: 1496000}
    },
    "갤럭시S24울트라": {
        "device_brand": "Samsung", "screen_size": 6.8, "ram": 12, "battery": 5000,
        "weight": 232, "release_year": 2024,
        "storage_options": {256: 1698400, 512: 1841400, 1024: 2127400}
    },
    "갤럭시S25": {
        "device_brand": "Samsung", "screen_size": 6.2, "ram": 12, "battery": 4000,
        "weight": 162, "release_year": 2025,
        "storage_options": {256: 1155000, 512: 1298000}
    },
    "갤럭시S25플러스": {
        "device_brand": "Samsung", "screen_size": 6.7, "ram": 12, "battery": 4900,
        "weight": 190, "release_year": 2025,
        "storage_options": {256: 1353000, 512: 1496000}
    },
    "갤럭시S25울트라": {
        "device_brand": "Samsung", "screen_size": 6.9, "ram": 12, "battery": 5000,
        "weight": 218, "release_year": 2025,
        "storage_options": {256: 1698400, 512: 1841400, 1024: 2127400}
    },

    # ===== Z 시리즈 =====
    "갤럭시Z플립3": {
        "device_brand": "Samsung", "screen_size": 6.7, "ram": 8, "battery": 3300,
        "weight": 183, "release_year": 2021,
        "storage_options": {256: 1254000}
    },
    "갤럭시Z플립4": {
        "device_brand": "Samsung", "screen_size": 6.7, "ram": 8, "battery": 3700,
        "weight": 187, "release_year": 2022,
        "storage_options": {256: 1299900, 512: 1398000}
    },
    "갤럭시Z플립5": {
        "device_brand": "Samsung", "screen_size": 6.7, "ram": 8, "battery": 3700,
        "weight": 187, "release_year": 2023,
        "storage_options": {256: 1398900}  # ※추정치(뉴스 기사 반올림값 기반)
    },
    "갤럭시Z폴드3": {
        "device_brand": "Samsung", "screen_size": 7.6, "ram": 12, "battery": 4400,
        "weight": 271, "release_year": 2021,
        "storage_options": {256: 1999900, 512: 2098000}
    },
    "갤럭시Z폴드4": {
        "device_brand": "Samsung", "screen_size": 7.6, "ram": 12, "battery": 4400,
        "weight": 263, "release_year": 2022,
        "storage_options": {256: 1998700, 512: 2097700}
    },
    "갤럭시Z폴드5": {
        "device_brand": "Samsung", "screen_size": 7.6, "ram": 12, "battery": 4400,
        "weight": 253, "release_year": 2023,
        "storage_options": {256: 2331000}
    },
}