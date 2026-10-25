---
title: PPG와 맥박산소측정
aliases: [PPG, photoplethysmography, pulse oximetry, SpO2]
tags: [생체신호, 광학센서, PPG]
date: 2026-10-20
description: 조직을 통과하거나 반사된 빛에서 맥동 혈액량과 산소포화도를 추정하는 원리와 한계.
---

> [!abstract] 한눈에
> PPG는 박동에 따라 달라지는 빛의 흡수를 측정한다. 맥박산소측정기는 적색광과 적외선에서 산소화·탈산소화 헤모글로빈의 흡수 차이를 이용해 SpO₂를 추정한다. 둘 다 혈액을 채취하지 않고 광학 신호와 보정모형으로 값을 추정한다.

## 광원, 조직, 광검출기

LED가 조직에 빛을 보내면 일부는 흡수되고 일부는 산란된 뒤 photodiode에 도달한다. 심장 박동에 따라 동맥 혈액량이 변하므로 검출되는 빛도 주기적으로 변한다.

PPG 신호는 보통 두 성분으로 나눈다.

- **DC 성분**: 조직, 정맥혈, 비맥동 동맥혈과 평균 광경로가 만드는 느린 기준값
- **AC 성분**: 심장 박동에 따른 동맥 혈액량 변화

AC/DC 정규화는 광원 세기나 손가락 두께 같은 전체 크기 차이를 어느 정도 줄인다. 하지만 센서 압력과 움직임까지 자동으로 제거하지는 않는다.

## 두 파장을 이용한 SpO₂ 추정

산소화 헤모글로빈과 탈산소화 헤모글로빈은 적색광과 적외선을 다르게 흡수한다. 장치는 두 파장에서 맥동 성분과 기준 성분을 비교한 비율

$$
R=\frac{AC_{red}/DC_{red}}{AC_{IR}/DC_{IR}}
$$

을 만들고, 기기별 보정곡선을 통해 말초 산소포화도 SpO₂를 추정한다. 조직의 산란, 광경로, 센서 구조가 복잡해서 Beer-Lambert 법칙만으로는 값을 바로 계산할 수 없다.

## 파형 분석

PPG의 peak 간격으로 맥박수를 추정할 수 있고, 파형의 상승·하강과 맥파 도달 시간을 분석할 수도 있다. 그러나 ECG의 R peak와 PPG peak는 같은 사건이 아니다. ECG는 전기 활성, PPG는 말초 혈액량 변화를 보므로 둘 사이에는 전기-기계 지연과 맥파 전달 시간이 포함된다.

## 흔한 실패 원인

- 손가락 움직임과 센서 미끄러짐
- 낮은 말초 관류와 차가운 피부
- 주변광 유입
- 매니큐어·센서 위치·과도한 압력
- 피부 특성에 따른 체계적 편향

따라서 단일 SpO₂ 숫자만 저장하지 말고 원시 PPG, 신호 품질, 측정 부위와 상황을 함께 기록하는 편이 좋다.

> [!warning] 범위
> 맥박산소측정 값은 추정치이며 조건에 따라 부정확할 수 있다. 증상과 의료진의 판단을 대신하지 않는다.

## 출처

- 개인 학습 기록, Notion `Studies / 2024 Spring / BiS200 / Final`, Optical Sensors and Pulse Oximetry
- U.S. FDA, [Pulse Oximeter Basics](https://www.fda.gov/consumers/consumer-updates/pulse-oximeter-basics)
- U.S. FDA, [Pulse Oximetry Technology](https://www.fda.gov/media/162709/download)
