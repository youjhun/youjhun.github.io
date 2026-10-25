---
title: MIT 18.06 선형대수
description: MIT 18.06 Linear Algebra를 따라가며 정리한 개념.
---

행렬을 '수의 표'가 아니라 공간을 바꾸는 변환으로 보는 과목이다. 열공간과 영공간, 투영과 최소제곱, 고윳값과 SVD까지 데이터 분석과 디코더 설계의 바탕이 되는 도구를 다룬다. 공개 강의 자료는 [MIT OpenCourseWare 18.06 (Spring 2010)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)에 있다.

## 단원

| 단원                    | 다루는 것                | 글                                                                                                        |
| ----------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------- |
| 행렬 곱의 열 관점       | 선형결합, 행렬 곱의 크기 | [[subspaces-rank\|열공간·영공간·랭크]]                                                                    |
| 소거와 분해 | LU·행렬식·Gram–Schmidt·QR·기저 변환 | [[elimination-lu-qr\|선형방정식의 계산]] |
| 열공간과 영공간         | 해의 존재와 유일성, rank | [[subspaces-rank\|열공간·영공간·랭크]]                                                                    |
| 부분공간과 직교         | 네 개의 기본 부분공간    | [[subspaces-rank\|열공간·영공간·랭크]]                                                                    |
| 투영과 최소제곱         | 정사영, 정규방정식       | [[least-squares\|최소제곱과 정사영]]                                                                      |
| 대칭 행렬과 양의 정부호 | 스펙트럴 분해, 이차형식  | [[quadratic-forms-positive-definite\|이차형식과 양의 정부호]] · [[covariance-matrix\|공분산 행렬]]        |
| 고윳값과 SVD            | 대각화, 특잇값 분해      | [[eigenvalues-diagonalization\|고윳값·고유벡터와 대각화]] · [[svd\|특잇값 분해]] · [[pca-svd\|PCA와 SVD]] |

## 추가 대조 범위

[강의별 목록](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/)에는 그래프·네트워크(L13), Markov(L23), 미분방정식(L26), 복소행렬·FFT(L32), 선형계획(L35), 수치선형대수(L38), 계산과학(L39)도 있다. Markov·연속계는 [[eigenvalues-diagonalization|고유모드의 계산]]에 추가했다. 복소행렬의 체계적 설명, 네트워크 incidence, 선형계획과 수치 알고리즘 전체는 아직 별도 상세 글로 다루지 않았다.
