"""
20개 모델의 스펙 및 신품가 매핑표

신품가(normalized_new_price)는 삼성/LG/애플 공식 발표 자료 및 언론보도의
실제 국내(또는 미국) 출고가를 확인하여 반영했으며,
데이터셋의 정규화 스케일(2.90~7.85)에 맞춰 자연로그 변환(ln(USD 환산가))을 적용함.
- 환율은 2016~2020년 평균치(약 1,130원/달러)를 가정하여 KRW→USD 환산
- Apple은 미국 공식 출시가(USD)를 그대로 사용
"""

phone_models = {
    # ===== Samsung =====
    "갤럭시 S7 (2016)": {
        "device_brand": "Samsung", "os": "Android", "screen_size": 12.9,
        "rear_camera_mp": 12.0, "front_camera_mp": 5.0,
        "ram": 4.0, "battery": 3000, "weight": 152, "release_year": 2016,
        "storage_options": {32: 6.606, 64: 6.658},  # 확인: 836,000 / 880,000원
        "is_4g": True, "is_5g": False
    },
    "갤럭시 S8 (2017)": {
        "device_brand": "Samsung", "os": "Android", "screen_size": 14.7,
        "rear_camera_mp": 12.0, "front_camera_mp": 8.0,
        "ram": 4.0, "battery": 3000, "weight": 155, "release_year": 2017,
        "storage_options": {64: 6.718, 128: 6.930},  # 확인: 935,000 / 1,155,000원
        "is_4g": True, "is_5g": False
    },
    "갤럭시 노트8 (2017)": {
        "device_brand": "Samsung", "os": "Android", "screen_size": 16.0,
        "rear_camera_mp": 12.0, "front_camera_mp": 8.0,
        "ram": 6.0, "battery": 3300, "weight": 195, "release_year": 2017,
        "storage_options": {64: 6.876, 256: 7.012},  # 확인: 1,094,500 / 1,254,000원
        "is_4g": True, "is_5g": False
    },
    "갤럭시 S9 (2018)": {
        "device_brand": "Samsung", "os": "Android", "screen_size": 14.7,
        "rear_camera_mp": 12.0, "front_camera_mp": 8.0,
        "ram": 4.0, "battery": 3000, "weight": 163, "release_year": 2018,
        "storage_options": {64: 6.741, 256: 6.930},  # 확인: 957,000 / 1,155,000원
        "is_4g": True, "is_5g": False
    },
    "갤럭시 노트9 (2018)": {
        "device_brand": "Samsung", "os": "Android", "screen_size": 16.2,
        "rear_camera_mp": 12.0, "front_camera_mp": 8.0,
        "ram": 6.0, "battery": 4000, "weight": 201, "release_year": 2018,
        "storage_options": {128: 6.876, 512: 7.088},  # 확인: 1,094,500 / 1,353,000원
        "is_4g": True, "is_5g": False
    },
    "갤럭시 S10 (2019)": {
        "device_brand": "Samsung", "os": "Android", "screen_size": 15.5,
        "rear_camera_mp": 12.0, "front_camera_mp": 10.0,
        "ram": 8.0, "battery": 3400, "weight": 157, "release_year": 2019,
        "storage_options": {128: 6.840, 512: 7.046},  # 확인: 1,056,000 / 1,298,000원
        "is_4g": True, "is_5g": False
    },
    "갤럭시 A50 (2019)": {
        "device_brand": "Samsung", "os": "Android", "screen_size": 16.5,
        "rear_camera_mp": 25.0, "front_camera_mp": 25.0,
        "ram": 4.0, "battery": 4000, "weight": 174, "release_year": 2019,
        "storage_options": {64: 6.037},  # 확인: 473,000원 (단일 모델)
        "is_4g": True, "is_5g": False
    },
    "갤럭시 S20 (2020)": {
        "device_brand": "Samsung", "os": "Android", "screen_size": 15.8,
        "rear_camera_mp": 12.0, "front_camera_mp": 10.0,
        "ram": 8.0, "battery": 4000, "weight": 163, "release_year": 2020,
        "storage_options": {128: 7.008, 256: 7.088},  # 확인: 1,248,500 / 1,353,000원
        "is_4g": True, "is_5g": True
    },

    # ===== Apple =====
    "아이폰 6s (2015)": {
        "device_brand": "Apple", "os": "iOS", "screen_size": 11.9,
        "rear_camera_mp": 12.0, "front_camera_mp": 5.0,
        "ram": 2.0, "battery": 1715, "weight": 143, "release_year": 2015,
        "storage_options": {16: 6.475, 64: 6.619, 128: 6.744},  # 확인: $649/$749/$849
        "is_4g": True, "is_5g": False
    },
    "아이폰 7 (2016)": {
        "device_brand": "Apple", "os": "iOS", "screen_size": 11.9,
        "rear_camera_mp": 12.0, "front_camera_mp": 7.0,
        "ram": 2.0, "battery": 1960, "weight": 138, "release_year": 2016,
        "storage_options": {32: 6.475, 128: 6.619, 256: 6.744},  # 확인: $649/$749/$849
        "is_4g": True, "is_5g": False
    },
    "아이폰 8 (2017)": {
        "device_brand": "Apple", "os": "iOS", "screen_size": 11.9,
        "rear_camera_mp": 12.0, "front_camera_mp": 7.0,
        "ram": 2.0, "battery": 1821, "weight": 148, "release_year": 2017,
        "storage_options": {64: 6.550, 256: 6.744},  # 확인: $699/$849
        "is_4g": True, "is_5g": False
    },
    "아이폰 X (2017)": {
        "device_brand": "Apple", "os": "iOS", "screen_size": 14.7,
        "rear_camera_mp": 12.0, "front_camera_mp": 7.0,
        "ram": 3.0, "battery": 2716, "weight": 174, "release_year": 2017,
        "storage_options": {64: 6.907, 256: 7.046},  # 확인: $999/$1,149
        "is_4g": True, "is_5g": False
    },
    "아이폰 XR (2018)": {
        "device_brand": "Apple", "os": "iOS", "screen_size": 15.5,
        "rear_camera_mp": 12.0, "front_camera_mp": 7.0,
        "ram": 3.0, "battery": 2942, "weight": 194, "release_year": 2018,
        "storage_options": {64: 6.619, 128: 6.684, 256: 6.801},  # 확인: $749/$799/$899
        "is_4g": True, "is_5g": False
    },
    "아이폰 11 (2019)": {
        "device_brand": "Apple", "os": "iOS", "screen_size": 15.5,
        "rear_camera_mp": 12.0, "front_camera_mp": 12.0,
        "ram": 4.0, "battery": 3110, "weight": 194, "release_year": 2019,
        "storage_options": {64: 6.550, 128: 6.619, 256: 6.744},  # 확인: $699/$749/$849
        "is_4g": True, "is_5g": False
    },
    "아이폰 SE 2세대 (2020)": {
        "device_brand": "Apple", "os": "iOS", "screen_size": 11.9,
        "rear_camera_mp": 12.0, "front_camera_mp": 7.0,
        "ram": 3.0, "battery": 1821, "weight": 148, "release_year": 2020,
        "storage_options": {64: 5.989, 128: 6.107, 256: 6.213},  # 확인: $399/$449/$499
        "is_4g": True, "is_5g": False
    },

    # ===== LG =====
    "LG G5 (2016)": {
        "device_brand": "LG", "os": "Android", "screen_size": 13.7,
        "rear_camera_mp": 16.0, "front_camera_mp": 8.0,
        "ram": 4.0, "battery": 2800, "weight": 159, "release_year": 2016,
        "storage_options": {32: 6.606},  # 확인: 836,000원 (단일 모델)
        "is_4g": True, "is_5g": False
    },
    "LG G6 (2017)": {
        "device_brand": "LG", "os": "Android", "screen_size": 14.5,
        "rear_camera_mp": 13.0, "front_camera_mp": 5.0,
        "ram": 4.0, "battery": 3300, "weight": 163, "release_year": 2017,
        "storage_options": {32: 6.586, 64: 6.680},  # 확인: 819,500 / 899,800원
        "is_4g": True, "is_5g": False
    },
    "LG V30 (2017)": {
        "device_brand": "LG", "os": "Android", "screen_size": 15.7,
        "rear_camera_mp": 13.0, "front_camera_mp": 5.0,
        "ram": 4.0, "battery": 3300, "weight": 158, "release_year": 2017,
        "storage_options": {64: 6.733, 128: 6.784},  # 확인: 949,300 / 998,800원
        "is_4g": True, "is_5g": False
    },
    "LG G7 씽큐 (2018)": {
        "device_brand": "LG", "os": "Android", "screen_size": 15.7,
        "rear_camera_mp": 16.0, "front_camera_mp": 8.0,
        "ram": 4.0, "battery": 3000, "weight": 162, "release_year": 2018,
        "storage_options": {64: 6.678, 256: 6.762},  # 확인: 898,700 / 976,800원
        "is_4g": True, "is_5g": False
    },
    "LG V50 씽큐 (2019)": {
        "device_brand": "LG", "os": "Android", "screen_size": 15.9,
        "rear_camera_mp": 12.0, "front_camera_mp": 8.0,
        "ram": 6.0, "battery": 4000, "weight": 183, "release_year": 2019,
        "storage_options": {128: 6.967},  # 확인: 1,199,000원 (단일 모델)
        "is_4g": True, "is_5g": True
    },
}