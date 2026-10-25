---
title: LDA (선형 판별 분석)
aliases: [선형 판별 분석, Linear discriminant analysis, 피셔 판별]
tags: [기계학습, EEG, BCI, 통계]
date: 2026-10-19
description: 두 클래스의 평균은 멀리, 각 클래스 안의 퍼짐은 작게 보이는 방향으로 투영하는 선형 분류기.
---

> [!abstract] 한눈에
> **LDA**는 자료를 한 직선 위로 투영할 때 두 클래스의 평균은 멀어지고 각 클래스 안의 퍼짐은 작아지도록 그 직선의 방향을 고른다. 답은 $\mathbf{w} \propto S_W^{-1}(\boldsymbol\mu_2 - \boldsymbol\mu_1)$이라는 닫힌 꼴로 나온다. 클래스 안의 공분산 $S_W$로 '덜 퍼진 쪽'을 보정하기 때문에 두 평균을 그냥 잇는 방향과는 달라진다. 계산이 가볍고 과적합이 적어서 뇌파 분류에서 기본 분류기로 쓰인다.

## 피셔의 기준

두 클래스의 평균을 $\boldsymbol\mu_1, \boldsymbol\mu_2$로, 클래스 안 산포 행렬(within-class scatter)을 $S_W = \Sigma_1 + \Sigma_2$로 둔다. 방향 $\mathbf{w}$로 투영했을 때 평균 차이는 $\mathbf{w}^\top(\boldsymbol\mu_2 - \boldsymbol\mu_1)$, 클래스 안 분산의 합은 $\mathbf{w}^\top S_W \mathbf{w}$다. 피셔(Fisher)는 이 둘의 비를 최대로 만드는 방향을 골랐다.

$$
J(\mathbf{w}) = \frac{\left(\mathbf{w}^\top(\boldsymbol\mu_2 - \boldsymbol\mu_1)\right)^2}{\mathbf{w}^\top S_W\, \mathbf{w}}
\qquad\Longrightarrow\qquad
\mathbf{w}^\ast \propto S_W^{-1}(\boldsymbol\mu_2 - \boldsymbol\mu_1)
$$

분자는 클래스 사이가 벌어진 정도를, 분모는 클래스 안이 퍼진 정도를 잰다.

## 평균 차이 방향과 비교

두 평균을 잇는 방향 $\boldsymbol\mu_2 - \boldsymbol\mu_1$으로 투영하는 방법이 가장 단순하다. 하지만 클래스가 길쭉하게 퍼져 있고 그 방향이 평균 차이와 비스듬하면 투영한 두 분포가 크게 겹친다. $S_W^{-1}$을 곱하면 퍼짐이 큰 방향의 성분이 줄어들어 투영 방향이 두 분포가 덜 겹치는 쪽으로 돌아간다(그림 1).

![평균 차이 방향과 피셔 방향](../../images/lda/fisher-direction.png)
_그림 1. 공분산이 같은 두 클래스. 평균 차이 방향(회색)으로 투영하면 많이 겹치지만 피셔 방향(빨강)으로 투영하면 덜 겹친다. 분리도 $J$는 약 1.3에서 4.9로 커진다._

## 분류기

두 클래스가 공분산 $\Sigma$가 같은 정규분포라고 가정하면 베이즈 최적 분류 경계는 $\mathbf{w} = \Sigma^{-1}(\boldsymbol\mu_2 - \boldsymbol\mu_1)$에 수직인 초평면이다. 이 가정 아래서 LDA는 투영 방향이자 분류기다. 분류할 때는 투영값 $\mathbf{w}^\top \mathbf{x}$를 문턱값과 비교한다. 문턱값은 두 클래스 평균을 투영한 값의 가운데에 두고, 사전확률이 다르면 그만큼 옮긴다.

뇌파 분류에서 LDA가 오래 쓰인 데에는 세 가지 이유가 있다.

- 학습이 닫힌 꼴로 끝나 빠르고 돌릴 때마다 결과가 같다.
- 자유도가 작아서 시행 수가 적어도 과적합이 덜하다.
- [[csp|CSP]] 로그 분산처럼 정규분포에 가까운 저차원 특징과 잘 맞는다.

## 유의점

- LDA는 차원 축소 기법이자 분류기다. 클래스가 둘일 때는 투영 방향과 분류 경계가 같다. 차원 축소로 쓸 때는 클래스가 $K$개면 최대 $K-1$차원까지 줄인다.
- 공분산이 같다는 가정이 맞으면 LDA는 최적이다. 가정이 조금 어긋나도 경계가 선형이어서 안정적으로 동작할 때가 많다. 공분산이 크게 다르면 이차 판별(QDA)을 고려한다.
- 특징 수가 표본 수보다 많거나 특징끼리 강하게 얽혀 있으면 $S_W$가 특이해져 역행렬을 구할 수 없다. 이때는 대각선에 작은 값을 더하는 축소 LDA(shrinkage LDA)를 쓴다.
- PCA와 LDA는 찾는 방향이 다르다. [[pca-svd|PCA]]는 라벨 없이 분산이 큰 방향을 찾는다. LDA는 라벨을 써서 클래스가 잘 갈리는 방향을 찾는다. 분산이 크다고 해서 그 방향이 클래스를 가른다는 보장은 없다.

## 관련 개념

- [[csp|CSP]]: LDA에 넣을 특징을 만드는 공간 필터
- [[covariance-matrix|공분산 행렬]]: $S_W$의 재료
- [[data-leakage|데이터 누수와 검증 단위]]: 축소 강도 같은 설정도 학습 폴드에서만 고른다

## 참고 자료

- R. A. Fisher, "The use of multiple measurements in taxonomic problems," _Annals of Eugenics_ 7(2), 179–188 (1936)
- B. Blankertz, S. Lemm, M. Treder, S. Haufe, K.-R. Müller, "Single-trial analysis and classification of ERP components — a tutorial," _NeuroImage_ 56(2), 814–825 (2011)
- T. Hastie, R. Tibshirani, J. Friedman, _The Elements of Statistical Learning_, 2nd ed., §4.3
