---
title: MIT 18.05 확률과 통계
description: MIT 18.05 Introduction to Probability and Statistics (Spring 2022)를 따라가며 정리한 개념.
---

확률의 기초부터 빈도주의 검정, 베이지안 추론, 부트스트랩, 회귀까지 데이터를 다루는 데 필요한 통계를 한 학기에 훑는 과목이다. 공개 강의 자료는 [MIT OpenCourseWare 18.05 (Spring 2022)](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/)에 있다.

## 단원

| 단원                        | 다루는 것                          | 글                                                                                                              |
| --------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 확률의 기초와 베이즈        | 경우의 수, 조건부확률, 베이즈 정리 | [[bayes-update\|베이즈 갱신]]                                                                                   |
| 확률변수와 분포             | 이산·연속 분포, 기댓값, 분산       | [[probability-random-variables\|확률공간과 확률변수]] · [[expectation-variance-covariance\|기댓값·분산·공분산]] |
| 큰 수의 법칙과 중심극한정리 | 표본평균의 분포, 표준오차          | [[bootstrap\|부트스트랩과 표준오차]]                                                                            |
| 결합분포와 공분산           | 독립, 공분산, 상관                 | [[expectation-variance-covariance\|기댓값·분산·공분산]] · [[pearson-spearman\|피어슨과 스피어먼 상관]]          |
| 최대가능도와 베이지안 추론  | MLE, 사전·사후분포                 |                                                                                                                 |
| 가설검정                    | 귀무가설, 유의수준, t-검정         | [[confidence-interval-hypothesis-test\| 신뢰구간과 가설검정]] · [[p-value\|p-value]]                            |
| 신뢰구간과 부트스트랩       | 신뢰구간, 재표본추출               | [[confidence-interval-hypothesis-test\| 신뢰구간과 가설검정]] · [[bootstrap\|부트스트랩과 표준오차]]            |
| 선형 회귀                   | 최소제곱, 적합도                   | [[linear-regression\|단순 선형 회귀]]                                                                           |

## 강의 범위 밖

연구에 필요해 덧붙인 글이다. 18.05 강의 목록에는 없다.

- [[multiple-comparisons-fdr|다중비교와 FDR]]
