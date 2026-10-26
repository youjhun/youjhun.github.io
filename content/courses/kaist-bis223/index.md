---
title: BiS223 생명공학의 물리적 원리
description: 가정·단위·유도·계산 예제로 확산, 엔트로피, 평형과 전기적 상호작용을 복원하는 노트.
aliases: [BiS223]
---

## 계산과 유도

| 필요한 작업 | 바로 볼 부분 | 계산 후 확인 |
| --- | --- | --- |
| 농도차로 이동량 계산 | [[diffusion-ficks-law#수송량-계산-예\|Fick 제1법칙과 면적]] | flux와 총이동률의 단위 |
| 농도의 시간 변화 | [[diffusion-ficks-law#작은-구획의-보존식\|연속방정식에서 제2법칙]] | 초기·경계조건, 총량 |
| 확산 거리·시간 추정 | [[diffusion-ficks-law#확산-시간과-gaussian-해\|RMS 변위와 차원]] | 1D의 2와 3D의 6 |
| 확산과 마찰 연결 | [[diffusion-ficks-law#외력과-einstein-관계의-유도\|Drift와 평형 분포]] | 이동도·마찰의 단위 |
| 등식 제약 최적화 | [[lagrange-multipliers#조건식의-구성\|라그랑지안과 후보 검증]] | 경계·특이점·오목성 |
| 확률에서 엔트로피 유도 | [[entropy-boltzmann#미시상태-수에서-엔트로피\|상태 수와 Stirling 근사]] | 로그 밑, kB |
| Boltzmann 확률 계산 | [[entropy-boltzmann#두-준위-계산-예\|가중치·정규화·평균]] | 미시상태와 축퇴도 |
| 온도의 통계적 정의 | [[entropy-boltzmann#두-준위-계의-온도\|점유율에서 1/T]] | 에너지 상한과 음의 온도 |
| 두 물체의 열평형 | [[thermodynamic-driving-forces#열평형-계산-예\|에너지 보존과 엔트로피]] | 최종 온도 범위, ΔS |
| 어떤 자유에너지를 쓸지 선택 | [[thermodynamic-driving-forces#자연변수와-퍼텐셜\|U·F·H·G의 미분]] | 무엇을 고정했는지 |
| 반응·이온 이동 방향 | [[thermodynamic-driving-forces#반응-자유에너지\|반응지수와 자유에너지]] · [[thermodynamic-driving-forces#전기화학퍼텐셜\|막 양쪽의 평형]] | J와 J/mol, 전압 부호 |
| 전기적 상호작용 크기 | [[electrostatics-screening#열운동과의-비교\|Coulomb 에너지와 kBT]] | 전위와 에너지 |
| 염 농도에서 차폐 길이 | [[electrostatics-screening#농도와-debye-길이-계산\|이온강도와 Debye 길이]] | mol/L와 mol/m³ |

## 단원

| 단원 | 본문 |
| --- | --- |
| 확률적 기초 | [[probability-random-variables\|이항·Poisson·Gaussian·중심극한정리]] |
| 확산 | [[diffusion-ficks-law\|확산과 Fick 법칙]] |
| 제약 최적화 | [[lagrange-multipliers\|라그랑주 승수법]] |
| 엔트로피·앙상블 | [[entropy-boltzmann\|엔트로피·앙상블·Boltzmann 분포]] |
| 열역학 | [[thermodynamic-driving-forces\|열역학적 구동력]] |
| 전기적 상호작용 | [[electrostatics-screening\|유전분극과 전기이중층]] |

## 단위와 기호

$k_B$와 에너지 J는 입자당 기술에서 사용하고, $R$과 J/mol은 몰당 기술에서 사용한다. 온도는 K, 로그와 지수의 인수는 무차원으로 맞춘다. 같은 μ라도 화학퍼텐셜과 이동도를 동시에 가리키지 않도록 이 노트에서는 기계적 이동도를 b로 표기한다. 계산 예의 값은 과제·시험에서 가져오지 않고 별도로 정했다.

## 범위 대조

| 확인한 기록 | 연결한 개념 | 확인 경계 |
| --- | --- | --- |
| 확산·제약 최적화의 텍스트 기록 | Fick·Einstein·Lagrange | 가정과 경계조건, 새 계산 예 포함 |
| 통계·열역학의 개념 목록 | 분포·CLT·최대엔트로피·앙상블·분배함수·두 준위 온도 | 목록에서 확인한 개념을 재설명 |
| 열·부피·입자 교환 | 에너지 보존·피스톤·화학퍼텐셜·Legendre 변환 | 계산 예와 부호 유도 포함 |
| 후반의 유전·분극·이중층·다극자 기록 | Coulomb·쌍극자·Poisson–Boltzmann·Debye 길이 | 선형 평면 모형까지 보충 |
| 이미지로만 남은 유도와 첨부 강의 | 세부 항목 전체 대조 미완료 | 전체 학기 범위가 모두 채워졌다고 판정하지 않음 |

## 보충 범위

혼합·반응·막 평형, 구형 입자의 Stokes 마찰과 평면 Poisson–Boltzmann 선형화는 기록에 있는 개념을 계산에 연결하기 위한 보충 유도다. Notion의 첨부 강의·시험 원본 전체를 재현하거나 단원별 수강 이력을 새로 판정하지 않는다.

## 관련 개념

- [[courses/mit-1805/index|MIT 18.05]]
- [[first-order-linear-exact|미분방정식]]
- [[physiology-mass-balance|생리학의 물질수지]]

## 참고 자료

- Notion Studies / 2024 Spring / BiS223의 개념 기록과 유도 주제 목록. 평가 문항은 게시하지 않았다.
- Dill and Bromberg, Molecular Driving Forces, 2판.
- 각 본문의 공개 강의와 보충 자료.
