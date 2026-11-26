---
source: https://jungle-lms.krafton.com/learning/1326
read: 2026-11-26 16:59 KST (Aside, page text only)
---

# 과제 - 신경망을 이용한 손글씨 숫자 인식 — LMS 원문

과제 - 신경망을 이용한 손글씨 숫자 인식
과제 - 신경망을 이용한 손글씨 숫자 인식
1. 개요

본 과제는 PyTorch, TensorFlow 같은 딥러닝 프레임워크 없이 NumPy만으로 신경망의 핵심 구성 요소를 직접 구현하는 것을 목표로 합니다.

최종 산출물: MNIST 손글씨 숫자 분류기

핵심 학습 목표: Forward -> Loss -> Backward -> Update 흐름을 코드, 수식, 배열 shape으로 설명하기

필수 검증: 단위 테스트, gradient check, 학습 loss 감소 확인

참고 도서: 『밑바닥부터 시작하는 딥러닝』 1~6장

이번 과제에서 만드는 것은 손글씨 이미지를 보고 0~9 중 하나를 고르는 프로그램입니다. 이미지는 28x28 픽셀이고, 컴퓨터는 이 이미지를 784개의 숫자로 봅니다. 신경망은 이 숫자들을 여러 층에 통과시키며 각 숫자에 대한 점수(logits)를 계산합니다.

이 과제의 목표는 높은 정확도를 만들거나 팀별 모델 품질을 경쟁하는 것이 아닙니다. loss에서 시작한 gradient가 각 층을 거꾸로 지나고, optimizer가 그 gradient를 이용해 파라미터를 바꾸는 과정을 팀원 모두가 설명할 수 있어야 합니다.

2. 코드 관리

팀별 GitHub 저장소를 준비합니다.

팀의 최종 결과물은 main 또는 master 브랜치에 둡니다.

개인 작업은 각자 브랜치를 만들어 진행합니다.

매일 코어타임에 각 팀원이 구현한 코드를 함께 리뷰한 뒤 최종 브랜치에 병합합니다.

최종 브랜치에는 테스트가 통과한 코드만 남깁니다.

충돌이나 테스트 실패가 생기면 특정 개인의 문제가 아니라 팀의 문제로 보고 함께 해결합니다.

핵심 함수는 팀원이 각자 구현합니다. 파일별 분업으로 전체 역전파 흐름을 놓치지 않도록 합니다.

데이터 파일, token, 비밀번호와 개인 환경 파일은 commit하지 않습니다.

3. 개발 환경
3.1 요구 사항

Python 3.12 (로컬 Conda 환경은 3.12로 통일)

허용 라이브러리 (직접 작성하는 코드 기준): numpy, math, random, time, matplotlib, pytest

금지: tensorflow, torch, jax, sklearn, 자동미분 라이브러리

제공 코드(데이터 다운로드, 테스트, tools/selfcheck.py, 노트북 환경설정)는 os, sys, pathlib, urllib, subprocess 등 Python 표준 라이브러리를 사용합니다. 별도 설치는 필요 없습니다.

3.2 실행 환경

전체 학습을 CPU에서 빠르게 실행할 수 있으므로 로컬 환경을 권장합니다. Colab에서도 동일하게 진행할 수 있습니다.

방법 A: 로컬에서 실행 (권장)

저장소를 클론한 뒤 Conda로 Python 3.12 환경을 만들고 의존성을 설치합니다.

Bash
git clone <팀 저장소 URL>
cd mnist-lab

conda create -n mnist-nn python=3.12 -y
conda activate mnist-nn
pip install -r requirements.txt

python download_mnist.py
pytest tests/ -v

처음에는 대부분의 테스트가 실패하는 것이 정상입니다. 현재 구현 중인 일차의 테스트부터 실행하세요.

방법 B: Colab에서 실행

1

과제 템플릿을 팀 저장소에 업로드합[ok | 5935ms]
니다.

2

아래 주소에서 USERNAME, 저장소명, 브랜치명을 팀 환경에 맞게 바꿉니다.

Plain text
   https://colab.research.google.com/github/USERNAME/mnist-lab/blob/main/mnist_lab.ipynb
3

상단 메뉴 런타임 -> 런타임 유형 변경에서 Python 3을 선택합니다. GPU는 필요하지 않습니다.

4

노트북 맨 위의 환경설정 셀부터 실행합니다. 셀이 저장소를 mnist-lab 폴더로 clone하고 의존성을 설치합니다.

5

저장소 URL: 입력란에 https://github.com/krafton-jungle/mnist-lab-v2처럼 팀 저장소 주소를 입력합니다.

6

private 저장소인 경우에만 GitHub Personal Access Token을 입력합니다. 공개 저장소라면 Enter를 누릅니다.

Mac/Windows 설치 절차와 세부 명령은 저장소 README.md를 참고하세요.

4. 과제 템플릿

과제 저장소: https://github.com/krafton-jungle/mnist-lab-v2

일부 코드는 이미 구현되어 있으며 # TODO 부분만 채워 완성합니다.

제공 코드는 다시 구현하지 않아도 되지만 핵심 함수가 어디에서 호출되는지는 읽어야 합니다.

프로젝트 구조:

Plain text
mnist-lab/
├── .gitignore
├── README.md
├── REPORT.md
├── LEARNING_LOG.md
├── requirements.txt
├── download_mnist.py
├── mnist_lab.ipynb
├── data/
│   └── .gitkeep           # mnist.npz는 download_mnist.py 실행 시 생성 (commit 제외)
├── src/
│   ├── __init__.py
│   ├── data.py
│   ├── activations.py
│   ├── layers.py
│   ├── losses.py
│   ├── optimizers.py
│   ├── network.py
│   └── training.py
├── tests/
│   ├── conftest.py
│   ├── test_affine.py
│   ├── test_relu.py
│   ├── test_softmax_with_loss.py
│   ├── test_gradient_check.py
│   ├── test_sgd.py
│   └── test_training_smoke.py
└── tools/
    └── selfcheck.py
5. 데이터

MNIST 데이터는 data/mnist.npz에 저장해 사용합니다.

load_mnist() 함수는 이미 구현되어 있습니다.

파일이 없으면 다운로드 후 data/에 저장합니다.

data/mnist.npz는 .gitignore에 포함되어 있으므로 commit하지 않습니다.

미리 다운로드하려면 프로젝트 루트에서 다음 명령을 실행합니다.

Bash
python download_mnist.py

데이터 형태:

항목	shape	설명
x_train	(60000, 784)	학습 이미지
y_train	(60000,)	학습 label
x_test	(10000, 784)	테스트 이미지
y_test	(10000,)	테스트 label

이미지는 28x28 픽셀을 펼친 784차원 벡터이며, 입력값은 0~1 범위로 정규화합니다.

6. 구현 대상

이번 버전에서는 모든 구성 요소를 직접 구현하지 않습니다. 신경망 학습의 핵심 계산과 직접 연결되는 TODO만 구현합니다.

6.1 직접 구현
Day	구현 대상	파일	핵심 개념
1	Affine.forward	src/layers.py	행렬 곱과 bias broadcasting
1	ReLU.forward	src/activations.py	비선형성, backward용 mask 저장
1	SoftmaxWithLoss.forward	src/losses.py	logits, 안정적 softmax, 평균 CE loss
2	SoftmaxWithLoss.backward	src/losses.py	(probability - one-hot) / batch_size
2	ReLU.backward	src/activations.py	mask를 이용한 gradient 차단
2	Affine.backward	src/layers.py	dW, db, dx와 chain rule
3	SGD.update	src/optimizers.py	gradient 반대 방향의 제자리 갱신
3	train()의 네 단계 연결	src/training.py	Forward, Loss, Backward, Update
6.2 제공 코드
제공 항목	파일	제공하는 이유
MNIST 다운로드와 정규화	src/data.py, download_mnist.py	데이터 처리보다 신경망 계산에 집중
TwoLayerNet 조립과 가중치 초기화	src/network.py	layer 구현 후 전체 흐름 관찰
미니배치 반복	src/training.py	인덱스 처리와 반복 배선 제공
gradient check	src/training.py	backward를 수치 미분으로 검증
evaluate, plot_loss_history	src/training.py	결과 확인과 시각화
Adam	src/optimizers.py	학습 루프 Smoke용 optimizer 제공
BatchNorm, Dropout	src/layers.py	필수 범위 밖 layer의 참고 구현
단위·통합 테스트	tests/	값, shape, gradient, 학습 연결 검증
7. 개발 순서

과제는 아래 3일 일정으로 진행합니다. 각 일차의 테스트를 통과하고 개념 질문에 답할 수 있을 때 다음 단계로 이동하세요.

Day	주제	핵심 구현	검증
1	Forward, logits, loss	Affine/ReLU/SoftmaxWithLoss forward	작은 배열 값, shape, 초기 loss
2	Backward와 chain rule	출력층/ReLU/Affine backward	실제 gradient 값, gradient check
3	Update와 end-to-end 학습	SGD, train 연결	Synthetic Smoke, 전체 테스트, MNIST baseline
Day 1. Forward, logits, loss

구현:

Affine.forward

ReLU.forward

SoftmaxWithLoss.forward

확인할 shape:

Plain text
x                (B, 784)
Affine 1 output  (B, hidden_size)
ReLU output      (B, hidden_size)
Affine 2 logits  (B, 10)
probability      (B, 10)
loss             scalar

작은 배열로 x @ W + b를 직접 계산하고 코드 결과와 비교합니다. 모든 logits가 같으면 클래스 확률은 각각 1/10이고 loss는 ln(10) = 2.3026입니다. 실제 MNIST에서 학습 전 모델의 초기 loss는 logits가 조금씩 달라 ln(10)과 정확히 같지 않으며, 2.3 근처(대략 2.0~2.8)면 정상입니다. 큰 logits에서도 안전하도록 softmax 계산 전에 각 행의 최댓값을 뺍니다.

Cross Entropy에서 log(0)을 피할 때는 np.clip(확률, 1e-7, 1.0)처럼 하한을 둡니다. log(확률 + 1e-7)처럼 작은 값을 더하면 Day 1 테스트는 통과하지만, Day 2 gradient check에서 1e-5 수준의 오차로 실패할 수 있습니다.

Bash
pytest tests/test_affine.py -v -k Forward
pytest tests/test_relu.py -v -k Forward
pytest tests/test_softmax_with_loss.py -v -k Forward
python tools/selfcheck.py --day 1

Day 1에는 정확도를 확인하지 않습니다. logits와 확률을 구분하고 각 단계의 값과 shape를 설명할 수 있으면 됩니다.

Day 2. Backward와 chain rule

구현 순서:

1

SoftmaxWithLoss.backward

2

ReLU.backward

3

Affine.backward

반드시 확인할 식:

Plain text
dlogits = (probability - one_hot_target) / batch_size

dW = x.T @ dout        shape: W와 같음
db = sum(dout, axis=0) shape: b와 같음
dx = dout @ W.T        shape: x와 같음

Forward에서 저장한 입력과 mask를 Backward에서 재사용합니다. 식을 암기하기보다 실제 행렬 곱이 가능한 shape인지 확인하세요.

Bash
pytest tests/test_softmax_with_loss.py -v -k Backward
pytest tests/test_relu.py -v -k Backward
pytest tests/test_affine.py -v -k Backward
pytest tests/test_gradient_check.py -v -s
python tools/selfcheck.py --day 2

제공된 gradient_check는 파라미터를 조금 움직여 측정한 수치 미분과 여러분의 backward가 계산한 해석적 gradient를 비교합니다.

Plain text
numeric gradient
= (loss(param + eps) - loss(param - eps)) / (2 * eps)

gradient check는 Day 2의 핵심 완료 기준입니다. W2/b2에서 실패하면 출력층과 두 번째 Affine을, W1/b1에서만 실패하면 ReLU와 첫 번째 Affine을 먼저 확인하세요.

Day 3. SGD와 end-to-end 학습

구현:

SGD.update

train()의 Forward, Loss, Backward, Update 네 단계

Bash
pytest tests/test_sgd.py -v
pytest tests/test_training_smoke.py -v
pytest tests/ -v
python tools/selfcheck.py --day 3

먼저 다운로드가 필요 없는 인공 데이터 Smoke에서 loss 감소와 parameter 변화를 확인합니다. 그 다음 고정된 2층 baseline으로 MNIST를 한 번 실행하고 첫·마지막 loss와 관찰한 정확도를 기록합니다.

완료 기준:

전체 테스트와 gradient check 통과

Synthetic Smoke에서 loss 감소

MNIST baseline 1회 실행과 loss 변화 기록

팀원이 핵심 함수의 수식과 shape를 코드 없이 설명

REPORT.md와 AI·참고 기록 작성

관찰한 정확도는 실행 상태를 확인하기 위한 값이며 목표 수치로 최적화하지 않습니다.

8. 학습 루프 규칙

각 미니배치마다 반드시 다음 순서를 지킵니다.

Python
# 1. Forward
logits = model.forward(x_batch, train=True)

# 2. Loss
loss = criterion.forward(logits, y_batch)

# 3. Backward
model.backward(criterion.backward())

# 4. Update
optimizer.update(model.params, model.grads)

주의:

모델의 마지막 출력은 확률이 아니라 logits입니다.

확률과 loss는 SoftmaxWithLoss.forward가 계산합니다.

Forward에서 저장한 중간값은 Backward에서 재사용합니다.

파라미터와 해당 gradient의 shape는 항상 같아야 합니다.

Softmax는 행별 max-shift를 사용하고 Cross Entropy는 log(0)을 피해야 합니다.

SGD는 파라미터 배열을 제자리에서 갱신해야 합니다.

초심자가 자주 막히는 지점:

증상	먼저 확인할 것
Affine 출력 값이 맞지 않음	x @ W + b 순서와 bias broadcasting
backward 전에 self.x가 없음	Affine.forward에서 입력을 저장했는지
softmax 확률 합이 1이 아님	axis=1, keepdims=True
큰 logits에서 nan 또는 inf	행별 최댓값을 뺀 뒤 exp를 계산했는지
출력층 gradient 크기가 너무 큼	batch size로 나눴는지
dW.shape != W.shape	x.T @ dout 순서
db.shape != b.shape	batch 축인 axis=0으로 합산했는지
gradient check가 W2/b2에서 실패	출력층 backward와 두 번째 Affine
gradient check가 W1/b1에서 실패	ReLU backward와 첫 번째 Affine
gradient check가 모든 파라미터에서 1e-5 수준으로만 조금 실패	loss에서 log(확률 + 1e-7) 대신 np.clip으로 하한을 두었는지
loss가 줄지 않음	train 네 단계 순서와 optimizer 호출
params 값은 바뀌지만 layer 출력은 그대로	SGD가 새 배열을 대입하지 않고 제자리에서 갱신했는지 확인
9. 신경망 구조

필수 과제에서는 아래 2층 구조를 고정해서 사용합니다.

Plain text
입력 784
-> Affine(128)
-> ReLU
-> Affine(10)
-> SoftmaxWithLoss

기본 baseline 설정:

항목	값
hidden size	128
batch size	128
epochs	10
optimizer	SGD
learning rate	0.1
weight initialization	He initialization (제공)
BatchNorm / Dropout	사용하지 않음

구조를 설계하거나 여러 설정을 비교하기 전에 고정 baseline에서 구현과 loss 감소를 확인합니다. BatchNorm, Dropout, Adam은 제공 코드이며 필수 구현이나 필수 실험 대상이 아닙니다.

10. 제출물

팀별로 아래 결과물을 제출합니다.

완성한 src/ 코드

실행 가능한 mnist_lab.ipynb

전체 테스트와 gradient check 결과

REPORT.md

10.1 REPORT.md

보고서에는 다음 항목을 포함합니다.

섹션	필수 내용
0. 반·팀원	반, 팀명, 팀원 이름
1. 전체 학습 흐름	Forward, Loss, Backward, Update와 shape
2. 핵심 구현	Affine, ReLU, SoftmaxWithLoss, SGD, train 설명
3. 검증 결과	단위 테스트, gradient check, Smoke 결과
4. MNIST 실행	baseline 설정, loss 변화, 관찰 정확도, 시간
5. 오류와 해결 과정	최소 재현, 원인, 수정 후 검증
6. 참고와 AI 사용	질문, 먼저 시도한 것, 직접 검증한 방법
7. 회고	이해한 개념과 남은 질문

 

