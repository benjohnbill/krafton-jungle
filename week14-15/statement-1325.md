---
source: https://jungle-lms.krafton.com/learning/1325
read: 2026-11-26 16:59 KST (Aside, page text only)
---

# 과제 - mini GPT LLM 구현 — LMS 원문

과제 - mini GPT LLM 구현
과제 - mini GPT LLM 구현
1. 개요

이 과제에서는 PyTorch 기본 모듈로 작은 GPT 계열 언어 모델을 구현하며 대규모 언어 모델(LLM)의 기본 개념과 동작 원리를 이해합니다. 텍스트가 token으로 바뀌고, causal self-attention과 TransformerBlock을 지나 다음 token 예측과 문장 분류로 이어지는 흐름을 코드와 실험으로 확인합니다.

목표는 자연스러운 문장을 만들거나 분류 정확도를 경쟁하는 것이 아닙니다. 작은 NSMC 영화 리뷰 데이터로 tokenization, next-token 학습, causal attention, Transformer, autoregressive generation, downstream classification의 관계를 연결하고 각 구성 요소가 왜 필요한지 설명하는 것이 완료 기준입니다. Tensor의 차원과 shape는 계산 흐름을 검증하고 오류를 찾기 위한 수단이며, 그 자체를 암기하거나 과제의 최종 목표로 삼지 않습니다. 생성 문장이 어색하거나 감성 분류 정확도가 높지 않아도 과제 실패가 아닙니다.

AI는 개념 이해, PyTorch API 확인, 자신이 작성한 코드의 오류 메시지 해석에 사용할 수 있습니다. TODO 함수 전체 구현이나 테스트 정답 코드를 생성해 붙여 넣는 용도로는 사용하지 않습니다. 받은 설명은 작은 tensor나 테스트로 직접 검증하고 REPORT.md의 "참고와 AI 사용"에 기록합니다.

참고 도서:

『밑바닥부터 만들면서 배우는 LLM』(길벗, 2025)

교재 소스 코드: https://github.com/rickiepark/llm-from-scratch

Day별로 먼저 읽을 교재 범위는 7장의 각 Day 절에 있습니다.

2. 코드 관리

팀별 GitHub 저장소를 준비합니다.

개인 작업은 각자 branch를 만들어 진행합니다.

main 또는 master에는 직접 push하지 않습니다.

핵심 TODO는 팀원이 각자 자기 branch에서 모두 구현합니다. 파일별로 한 명씩 나눠 맡으면 전체 흐름을 놓치므로 나누지 않습니다.

서로의 구현을 Pull Request로 리뷰한 뒤, 팀이 고른 구현 하나를 병합합니다.

병합 전에는 현재 Day의 테스트와 앞선 Day에서 통과한 테스트를 함께 확인합니다.

데이터 파일, checkpoint, token, 비밀번호, 개인 환경 파일은 commit하지 않습니다.

3. 개발 환경
3.1 요구 사항

Python 3.12

PyTorch 2.2 이상 (requirements.txt로 설치)

허용:

torch, torch.nn, torch.utils.data

numpy, matplotlib, pytest

사용하지 않음:

Hugging Face transformers, datasets, tokenizers

sentencepiece, tiktoken

spacy, nltk

lightning, accelerate

외부 pretrained model

외부 tokenizer vocabulary

교재에서 tiktoken을 사용하는 부분이 있지만, 이 과제에서는 byte-level BPE의 핵심을 직접 구현하므로 tiktoken을 사용하지 않습니다.

3.2 로컬 실행

Unit 테스트와 대부분의 Smoke 검증은 CPU에서도 실행할 수 있습니다.

Bash
git clone <팀 저장소 URL>
cd gpt-lab-v2

conda create -n gpt-lab python=3.12 -y
conda activate gpt-lab
pip install -r requirements.txt
python download_data.py

Day 1은 코드 없이 개념을 공부하는 날이며, TODO 구현과 테스트는 Day 2부터 시작합니다. 처음에는 전체 테스트가 실패하는 것이 정상입니다. 현재 Day의 테스트부터 실행하세요.

Bash
python tools/selfcheck.py --day 1     # Day 1 개념 질문
pytest tests/test_bpe.py -v           # Day 2부터 현재 Day의 테스트
python tools/selfcheck.py --day 2
3.3 Colab 실행

모델 학습에는 GPU 런타임을 권장합니다. GPU는 Unit 테스트의 필수 조건이 아닙니다.

1

브라우저에서 다음 주소로 이동합니다. USERNAME, 저장소명, branch명은 팀 환경에 맞게 바꿉니다.

Plain text
https://colab.research.google.com/github/USERNAME/gpt-lab-v2/blob/main/gpt-lab.ipynb
2

메뉴 런타임 -> 런타임 유형 변경에서 Python 3과 GPU를 선택합니다.

3

노트북의 환경설정 셀을 먼저 실행합니다.

4

Public 저장소는 token 없이 clone할 수 있습니다. Private 저장소인 경우에만 GitHub Personal Access Token을 입력합니다.

5

환경설정 -> 데이터 -> 현재 Day 테스트 -> 관찰 셀 순서로 진행합니다.

Colab 런타임이 끊기면 data/와 checkpoint 파일도 사라집니다. loss와 생성 예시는 바로 REPORT.md에 기록합니다. 노트북은 데이터가 없으면 다시 만들고, checkpoint는 제공된 save_checkpoint·load_checkpoint로 저장·복구합니다.

4. 프로젝트 소스

프로젝트 repo: https://github.com/krafton-jungle/gpt-lab-v2

일부 코드는 제공되어 있으며, 진행 중인 Day의 TODO만 직접 구현합니다.

Plain text
gpt-lab-v2/
├── README.md                         # 설치, 실행, 학습 순서 안내
├── REPORT.md                         # 팀별 최종 보고서 작성 양식
├── HINTS.md                          # 막혔을 때 단계별로 여는 힌트
├── requirements.txt                  # Python 의존성 목록
├── download_data.py                  # NSMC 다운로드와 과제 데이터 생성
├── gpt-lab.ipynb                     # 단계별 실습과 결과 관찰 노트북
├── data/
│   ├── nsmc_bpe_vocab_smoke.json     # Smoke용 사전 생성 BPE vocabulary
│   └── nsmc_bpe_vocab_light.json     # Light용 사전 생성 BPE vocabulary
├── src/                              # 직접 구현 코드와 제공 코드
│   ├── __init__.py                   # src package 초기화
│   ├── configs.py                    # 실행 규모별 설정과 일치 검사
│   ├── utils.py                      # seed, device, 진단 보조 함수
│   ├── bpe.py                        # byte-level BPE tokenizer
│   ├── dataset.py                    # 슬라이딩 윈도 Dataset과 DataLoader
│   ├── attention_practice.py         # scaled dot-product attention (Day 4 작성, Day 5 재사용)
│   ├── attention.py                  # causal multi-head self-attention
│   ├── model.py                      # LayerNorm, FeedForward, TransformerBlock, GPTModel
│   ├── train.py                      # 사전 학습·생성·checkpoint 기능
│   └── finetune.py                   # 감성 분류 미세 튜닝과 학습·평가 기능
├── tests/                            # 단계별 단위·통합 테스트
│   ├── conftest.py                   # 공통 fixture와 테스트 설정
│   ├── test_bpe.py                   # BPE 동작 검증
│   ├── test_dataset.py               # 슬라이딩 윈도 Dataset 검증
│   ├── test_attention_practice.py    # single-head attention 검증
│   ├── test_attention.py             # multi-head·causal attention 검증
│   ├── test_model.py                 # Block과 GPTModel 검증
│   ├── test_train.py                 # loss·generation·학습 기능 검증
│   └── test_finetune.py              # 감성 분류 기능 검증
└── tools/
    └── selfcheck.py                  # 단계별 테스트와 개념 자가 점검
5. 데이터와 실행 규모
5.1 [ok | 6444ms]
기본 데이터

기본 데이터는 NAVER Sentiment Movie Corpus(NSMC) 입니다.

원본 저장소: https://github.com/e9t/nsmc

라이선스: CC0 1.0

원본 컬럼: id, document, label

감성 label: 부정 0, 긍정 1

데이터 준비:

Bash
python download_data.py
파일	용도
data/nsmc_lm_train.txt	next-token 사전 학습 train 텍스트
data/nsmc_lm_val.txt	next-token 사전 학습 validation 텍스트
data/nsmc_sentiment_train.jsonl	감성 분류 train 데이터
data/nsmc_sentiment_val.jsonl	감성 분류 validation 데이터
data/nsmc_sentiment_test.jsonl	감성 분류 test 데이터
5.2 실행 규모

처음부터 전체 데이터를 반복 학습하지 않습니다. 계산 하나에서 전체 pipeline으로 단계적으로 넓힙니다.

규모	데이터·설정	목적	진행 기준
Unit	손으로 확인 가능한 수십 token	핵심 계산 하나의 동작과 원리 검증	각 Day에서 먼저 실행
Smoke	5천 자, vocab 300, context 32	전체 pipeline 연결 확인	반드시 실행
Light	10만 자, vocab 1000, context 64	데이터·vocabulary·context 확장 관찰	Smoke 통과 후 이어서 실행
Basic	사전 학습 텍스트 전체(약 140만 자), vocab 3000, context 128	더 큰 규모의 학습 경험	Light 후 여건이 허락하는 범위까지 실행

규모별 설정은 src/configs.py의 SMOKE_CONFIG, LIGHT_CONFIG, BASIC_CONFIG와 학습·데이터 설정(*_TRAIN, *_DATA)에 있습니다. tokenizer와 모델의 vocabulary 크기는 반드시 같아야 합니다.

Python
from configs import SMOKE_CONFIG, assert_vocab_match

assert_vocab_match(SMOKE_CONFIG, tokenizer)

모델 크기나 학습 횟수를 늘리기 전에 Unit과 Smoke 검증을 끝내세요. 그다음 Light를 실행하고, 진행 상황·GPU 사용 가능 여부·런타임 제한을 고려해 Basic으로 확장하세요. 각 규모에서 설정, 실행 범위, loss 변화, 중단한 위치와 이유를 기록합니다.

Python으로 pair 빈도를 매번 다시 세는 단순 BPE는 Basic 규모에서 오래 걸립니다. Apple Silicon 노트북 CPU 기준으로 Light vocabulary 학습은 약 12초였지만 Basic은 vocabulary 학습에 약 9분, encode에 약 2~5분이 걸렸고, Colab CPU에서는 더 오래 걸릴 수 있습니다. Smoke와 Light로 동작을 확인한 뒤 Basic으로 넓히고, 학습한 vocabulary는 규모별로 저장해 재사용하세요. 노트북의 Basic 셀은 vocabulary를 data/nsmc_bpe_vocab_basic.json에 저장하고 다음 실행부터 불러옵니다.

5.3 BPE 진행이 막힌 경우

Day 2에서 get_pair_counts, merge_pair, train의 병합 루프와 작은 입력 round-trip을 먼저 확인합니다. BPE 전체 학습이 느려 다음 개념 학습을 지연시킨다면 제공된 Smoke vocabulary로 Day 3를 진행하고, 이후 Light vocabulary를 사용하거나 BPE 학습을 다시 시도합니다.

Python
tokenizer = BPETokenizer(vocab_size=300)
tokenizer.load("data/nsmc_bpe_vocab_smoke.json")

이 경우에도 pair count, 겹치지 않는 병합, merge 순서 기록, byte-level round-trip의 원리는 설명할 수 있어야 합니다. 제공된 vocabulary는 train과 같은 규칙(빈도 우선, 동률이면 작은 ID 우선)으로 만들었으므로, train을 바르게 구현하면 같은 데이터에서 같은 결과가 나옵니다.

6. 구현 방법
6.1 직접 구현과 제공 코드

신경망 계산의 핵심에 직접 연결되는 TODO만 구현합니다. 데이터 반복, 학습 루프, checkpoint, sampling 같은 보조 코드는 제공합니다.

직접 구현

Day	파일	구현 대상	핵심 개념
2	src/bpe.py	get_pair_counts, merge_pair, BPETokenizer.train의 병합 루프	byte-level BPE pair 빈도, 병합, merge 학습 순서
3	src/dataset.py	GPTDatasetV1.__init__의 슬라이딩 윈도 루프	input·target 한 칸 shift, stride
4	src/attention_practice.py	scaled_dot_product_attention	score, scaling, mask, softmax
5	src/attention.py	MultiHeadAttention.forward	head 분리·결합, Day 4 함수 재사용
6	src/model.py	LayerNorm.forward	feature 차원 정규화
6	src/model.py	FeedForward.__init__의 self.layers	token별 확장·GELU·축소
6	src/model.py	TransformerBlock.forward	pre-LN과 shortcut 연결
7	src/model.py	GPTModel.forward	token·position embedding, block 연결, logits
7	src/model.py	generate_text_simple	greedy autoregressive generation
7	src/train.py	calc_loss_batch	next-token cross entropy
8	src/finetune.py	prepare_for_classification	동결, out_head 교체, 일부 층 학습
8	src/finetune.py	last_token_logits	마지막 non-pad 위치 선택

제공 코드

제공 항목	파일	제공하는 이유
BPE 특수 token, encode·decode, save·load	src/bpe.py	UTF-8 복원과 직렬화 디버깅 부담 감소
__len__·__getitem__, create_dataloader_v1	src/dataset.py	반복 배선보다 input·target 관계에 집중
MultiHeadAttention, LayerNorm, TransformerBlock, GPTModel 생성자	src/*.py	교재와 같은 레이어 선언을 두고 forward 흐름에 집중
GELU(교재 4.3의 tanh 근사식)	src/model.py	수식을 옮겨 적는 작업 축소
train_model_simple, 평가, checkpoint, sampling, plot	src/train.py	학습 boilerplate 재구현 방지
감성 데이터 준비, NSMCDataset, 정확도 계산, train_classifier_simple	src/finetune.py	분류 head 교체와 pooling 위치에 집중
Smoke·Light·Basic 설정과 vocabulary 일치 검사	src/configs.py	실행 조건 혼선 방지
seed, device, parameter·tensor 상태 확인	src/utils.py	실행 환경 보조
Smoke·Light BPE vocabulary	data/*.json	BPE에서 막혀도 다음 개념으로 진행
단위·통합 테스트	tests/	핵심 계산, mask, gradient, 모듈 연결 검증

제공 코드를 다시 구현할 필요는 없지만, 직접 구현한 함수가 어디서 호출되는지는 읽어 둡니다.

6.2 노트북과 테스트 진행 방법

gpt-lab.ipynb는 개념의 의존 관계를 따라 학습 과정을 Day 1~8로 편의상 나누어 구성했습니다. Day는 학습 순서를 구분하는 이름이며, 하루에 하나씩만 진행해야 한다는 뜻이 아닙니다.

1

환경설정과 데이터 준비 셀을 실행합니다.

2

현재 Day의 개념과 작은 입력을 먼저 확인합니다.

3

해당 src/ 파일의 TODO를 직접 구현합니다.

4

현재 Day의 테스트와 selfcheck 명령을 실행합니다.

5

구현한 계산의 원리, 결과, 핵심 불변조건을 설명할 수 있으면 날짜를 기다리지 말고 다음 Day로 이동합니다.

NotImplementedError가 나오면 현재 Day의 TODO가 남아 있는지 확인하세요. 처음부터 pytest tests/ -v만 반복하면 원인 모듈을 찾기 어려우므로 현재 Day의 테스트부터 실행합니다.

TODO의 docstring은 정답 코드가 아니라 입력·출력 shape, 지켜야 할 조건, 자주 하는 실수를 알려 줍니다. docstring, 작은 입력, 테스트 실패 메시지로 시도한 뒤에도 막히면 HINTS.md를 엽니다. 힌트는 생각할 방향, 사용할 연산, 의사 코드의 세 단계로 나뉘어 있으니 한 단계씩 열고 다시 시도하세요. 사용한 힌트 단계는 REPORT.md의 "참고와 AI 사용"에 기록합니다.

6.3 8일 진행 순서

다음 표는 권장 진행 순서입니다. Day 1은 개념 학습과 환경 준비만 하고, Day 2부터는 6.2절 순서로 진행합니다. 남은 시간은 Light·Basic 실행과 이해가 부족한 개념 복습에 사용합니다.

Day	주제	핵심 구현	학습·검증 활동
1	LLM과 GPT 기본 개념	새 구현 없음	교재 1장 정독, 참고 자료 학습, 환경 설정과 데이터 준비
2	byte-level BPE	pair count, merge, 학습 루프	BPE 원리, merge 순서 손계산, round-trip
3	Next-token Dataset과 Embedding	슬라이딩 윈도 Dataset	input·target 관계, stride, 위치 정보의 역할 확인
4	Single-head Attention	scaled dot-product attention	QKV 수식, 작은 tensor 계산, scaling·mask 검증
5	Causal Multi-Head Attention	MHA forward (Day 4 함수 재사용)	head 분리·결합, causal 불변조건, projection gradient 확인
6	TransformerBlock	LayerNorm, FFN 층 구성, shortcut	feature 정규화, pre-LN shortcut, gradient 흐름 확인
7	GPT, loss, greedy generation	GPT forward, calc_loss_batch, generation	초기 loss, tiny-batch overfit, Smoke 실행
8	분류 head와 통합 실행	out_head 교체, 마지막 non-pad logits	Light 사전 학습, 감성 분류, 여건에 따른 Basic 확장
7. 세부 구현
7.1 Day 1 - LLM과 GPT 기본 개념

핵심 질문: LLM은 무엇을 어떻게 학습하며, GPT는 어떤 구조로 한 token씩 문장을 만드는가?

먼저 읽을 교재: 1장 전체(1.1~1.8)

이 Day에는 TODO와 테스트가 없습니다. Day 2부터 만들 부품이 전체 LLM에서 어떤 역할을 하는지 먼저 그림을 잡는 날입니다. 교재 1장을 아래 표의 항목을 확인하며 읽고, 참고 자료로 그림과 실험을 보충합니다. 개발 환경 설정과 데이터 준비도 이 Day에 마칩니다.

7.1.1 교재 1장 읽기 안내
절	읽으며 확인할 것	이 과제에서 다시 만나는 곳
1.1 LLM이란 무엇인가요?	AI·머신러닝·딥러닝·LLM의 관계, "대규모"가 가리키는 것(데이터와 파라미터 수), 다음 단어 예측으로 훈련한다는 점	Day 7 next-token loss
1.2 LLM 애플리케이션	번역, 요약, 질의응답, 분류처럼 텍스트를 생성하거나 분석하는 작업	Day 8 감성 분류
1.3 LLM의 구축 단계	레이블 없는 대규모 텍스트로 사전 학습한 파운데이션 모델, 레이블이 있는 작은 데이터로 하는 미세 튜닝(지시·분류), 직접 만들어 보는 이유	Day 7~8 사전 학습, Day 8 분류 미세 튜닝
1.4 트랜스포머 구조 소개	인코더와 디코더, self-attention의 역할, BERT(인코더 기반)와 GPT(디코더 기반)의 차이	Day 4~6 attention과 TransformerBlock
1.5 대규모 데이터셋 활용하기	GPT-3 사전 학습 데이터의 구성과 token 규모, 사전 학습 비용이 큰 이유	5.2절 Smoke·Light·Basic 규모
1.6 GPT 구조 자세히 살펴보기	디코더만 쓰는 자기 회귀 모델, 다음 단어 예측이 레이블 없이 가능한 이유(자기 지도 학습), 창발적 능력	Day 7 generation
1.7 대규모 언어 모델 만들기	구현 -> 사전 학습 -> 미세 튜닝의 3단계 계획	Day 2~7 구현, Day 7~8 사전 학습, Day 8 미세 튜닝(6.3절 진행표)
1.8 요약	위 내용을 자기 말로 다시 정리	REPORT.md 1장
7.1.2 참고 자료

교재 1장과 함께 보면 좋은 자료입니다. 위에서부터 차례로 보되, 시간이 부족하면 처음 세 개와 Transformer Explainer만 봅니다. 영어 영상은 YouTube 자막(자동 번역 포함)을 사용할 수 있습니다.

자료	형식·분량	도움이 되는 내용
3Blue1Brown, Large Language Models explained briefly	영상, 약 8분	다음 단어 예측, 사전 학습과 후속 훈련, 트랜스포머를 짧게 훑어봅니다. 가장 먼저 봅니다.
3Blue1Brown, Transformers, the tech behind LLMs (Deep Learning Chapter 5)	영상, 약 27분 (글 버전)	token, embedding, 다음 token 확률 분포, softmax와 temperature를 그림으로 설명합니다. 같은 시리즈의 다음 장(attention)은 Day 4~5 복습에 좋습니다.
Andrej Karpathy, Intro to Large Language Models	강연, 약 1시간	LLM이 무엇이며 사전 학습과 미세 튜닝이 어떻게 이루어지는지 큰 그림을 잡습니다.
Transformer Explainer	브라우저 실습	브라우저에서 GPT-2 small을 실행합니다. 문장을 넣고 다음 token 후보와 확률, attention, temperature에 따른 분포 변화를 직접 관찰합니다.
Jay Alammar, The Illustrated GPT-2	글(한국어 번역 링크 있음)	디코더 전용 구조, 한 token씩 생성하는 과정, self-attention을 그림으로 설명합니다. Day 4~7 복습에도 사용합니다.
Hugging Face LLM 강좌 1장, 트랜스포머는 어떻게 동작하나요?	한국어 글	GPT·BERT·GPT-2·GPT-3로 이어지는 역사, 사전 학습과 전이 학습, 인코더·디코더 모델의 구분을 정리합니다. 라이브러리 사용 코드는 이 과제에서 쓰지 않으므로 개념 설명만 읽습니다.
위키독스, 딥 러닝을 이용한 자연어 처리 입문	한국어 온라인 책	언어 모델(3장), 워드 임베딩(9장), 트랜스포머(16장) 등 배경 지식이 부족할 때 필요한 장만 찾아 읽습니다.
Andrej Karpathy, Deep Dive into LLMs like ChatGPT	강연, 약 3시간 30분(선택)	데이터 수집, tokenization, 사전 학습, 후속 훈련까지 ChatGPT를 만드는 전체 과정을 다룹니다. 여러 번에 나누어 봅니다.

교재 1장이 인용하는 원 논문도 선택적으로 훑어볼 수 있습니다. 처음에는 그림과 초록 위주로 읽습니다.

Vaswani et al., Attention Is All You Need (2017): 트랜스포머 구조

Brown et al., Language Models are Few-Shot Learners (2020): GPT-3와 대규모 사전 학습

확인:

Bash
python tools/selfcheck.py --day 1
7.2 Day 2 - byte-level BPE

핵심 질문: 문자열을 왜 그대로 모델에 넣을 수 없으며, BPE는 무엇을 학습하는가?

먼저 읽을 교재: 2.1~2.5

교재와 다른 점: 교재는 2.5에서 GPT-2용 tiktoken BPE를 불러 사용하지만, 이 과제는 UTF-8 byte-level BPE의 pair count, merge, 학습 루프를 직접 구현합니다. 특수 token도 교재의 <|endoftext|>, <|unk|> 대신 <pad>, <unk>, <bos>, <eos>를 ID 0~3에 둡니다.

구현:

get_pair_counts

merge_pair

BPETokenizer.train의 병합 루프

손으로 먼저 확인합니다.

Python
get_pair_counts([1, 2, 1, 2, 3])
# {(1, 2): 2, (2, 1): 1, (2, 3): 1}

merge_pair([1, 2, 1, 2, 3], (1, 2), 99)
# [99, 99, 3]

merge_pair([5, 5, 5], (5, 5), 99)
# [99, 5]

특수 token, encode·decode, save·load는 제공 코드입니다. train은 1~3단계가 제공되고, 4~6단계를 반복하는 while 본문을 직접 구현합니다.

1

<pad>, <unk>, <bos>, <eos> 특수 token을 vocabulary에 둡니다.

2

byte 0~255를 기본 token으로 둡니다.

3

텍스트를 UTF-8 byte 목록으로 바꿉니다.

4

이웃한 token pair의 빈도를 셉니다.

5

가장 자주 등장한 pair를 새 token으로 등록하고, 그 순서를 merges에 기록한 뒤 병합합니다. 빈도가 같으면 ID가 작은 pair를 고릅니다.

6

목표 vocabulary 크기에 도달하거나 2번 이상 나온 pair가 없으면 멈춥니다.

encode는 merges를 학습한 순서대로 다시 적용합니다. 그래서 새 ID는 260부터 하나씩 늘어나야 하고, merges의 순서가 곧 token ID의 순서입니다.

"aaabdaaabac"로 merge 순서를 손으로 따라가 봅니다. byte token은 a=101, b=102, c=103, d=104입니다.

Plain text
1) (a, a) 4회                       -> 260 = "aa"
2) (260, a)와 (a, b)가 2회로 동률    -> ID가 작은 (a, b) -> 261 = "ab"
3) (260, 261) 2회                    -> 262 = "aaab"
4) 남은 pair가 모두 1회              -> 중단
encode("aaabdaaabac") = [262, 104, 262, 101, 103]

특수 token ID:

Plain text
0: <pad>
1: <unk>
2: <bos>
3: <eos>
4~259: byte 0~255
260 이상: BPE merge token
7.2.1 한글을 위해 꼭 알아야 할 점

한글 한 글자는 UTF-8에서 보통 byte 3개로 저장됩니다.

Python
"한".encode("utf-8")
# b'\xed\x95\x9c'
Plain text
문장: "한글"
-> UTF-8 bytes: [237, 149, 156, 234, 184, 128]
-> byte token IDs: [241, 153, 160, 238, 188, 132]  # byte 값 + 4
-> 자주 붙는 byte/token pair를 병합하며 더 큰 token 생성

byte-level BPE는 한글·영문·숫자·기호를 모두 byte 단위로 표현할 수 있어 처음 보는 단어도 <unk> 없이 처리할 수 있습니다.

decode할 때는 merge token을 원래 byte까지 모두 펼친 뒤 마지막에 한 번만 bytes(byte_values).decode("utf-8")를 호출합니다. byte를 하나씩 chr()로 바꾸면 한글의 중간 byte에서 문자가 깨질 수 있습니다.

Python
samples = [
    "이 영화는 정말 좋았다!",
    "연기, 음악, 연출 모두 좋음 ㅋㅋ",
    "한글 English 123 !?",
]
for text in samples:
    assert tokenizer.decode(tokenizer.encode(text, add_bos_eos=True)) == text

확인:

Bash
pytest tests/test_bpe.py -v
python tools/selfcheck.py --day 2
7.3 Day 3 - Next-token Dataset과 Embedding

핵심 질문: input과 target은 왜 한 칸 차이며, 같은 token의 위치는 어떻게 표현하는가?

먼저 읽을 교재: 2.6~2.8

교재와 다른 점: tokenizer만 tiktoken 대신 Day 2의 BPE를 넘깁니다. GPTDatasetV1과 create_dataloader_v1의 구조는 교재 2.6과 같고, token·position embedding은 교재처럼 Day 7의 GPTModel 안에서 더합니다.

구현:

GPTDatasetV1.__init__의 슬라이딩 윈도 루프

Plain text
token IDs: [10, 11, 12, 13, 14],  max_length = 3,  stride = 1
시작 0: input [10, 11, 12]  target [11, 12, 13]
시작 1: input [11, 12, 13]  target [12, 13, 14]

시작 위치는 0부터 stride 간격이며, target에 한 칸이 더 필요하므로 마지막 시작 위치에서도 시작 + max_length 위치의 token이 있어야 합니다. __len__, __getitem__, create_dataloader_v1은 제공됩니다.

노트북에서는 교재 2.7~2.8처럼 nn.Embedding으로 token·position embedding을 만들어 더해 봅니다.

Plain text
input IDs        (B, T)
token embedding  (B, T, C)
position index   (T)
position vector  (T, C)
output           (B, T, C)
Bash
pytest tests/test_dataset.py -v
python tools/selfcheck.py --day 3
7.4 Day 4 - Single-head scaled dot-product attention

핵심 질문: 한 token이 다른 token을 얼마나 참고할지를 어떤 계산으로 정하는가?

먼저 읽을 교재: 3.1~3.4, 3.5.1

교재와 다른 점: 교재의 SelfAttention_v2·CausalAttention은 Q·K·V projection까지 포함한 클래스입니다. 이 과제는 Day 5에서 같은 계산을 재사용하기 위해 score, mask, softmax, 가중합 부분만 scaled_dot_product_attention 함수로 분리했습니다. 변수 이름(attn_scores, attn_weights, context_vec)과 계산 순서는 교재와 같습니다.

구현:

scaled_dot_product_attention

Plain text
queries, keys, values  (B, T, D)
attn_scores            (B, T, T) = queries @ keys^T
attn_weights           (B, T, T) = softmax(mask(attn_scores) / sqrt(D))
context_vec            (B, T, D) = attn_weights @ values

scaled_dot_product_attention(queries, keys, values, mask=None, dropout=None)는 (context_vec, attn_weights)를 반환합니다. mask는 True인 칸이 가릴 위치인 bool tensor이며, 교재 3.5.1처럼 torch.triu(..., diagonal=1)로 만든 미래 위치 mask를 넘기면 해당 score를 softmax 전에 -inf로 채웁니다. dropout이 주어지면 values 가중합에 쓰는 weight에만 적용하고, 반환하는 attn_weights는 dropout 전 값입니다.

Day 4에는 multi-head reshape를 넣지 않습니다. T=3, D=2의 작은 tensor로 score와 softmax를 손으로 계산한 뒤 코드와 비교합니다.

이 함수는 Day 5의 MultiHeadAttention.forward가 그대로 호출합니다. 그때는 (B, H, T, D) 입력이 들어오므로 축 번호를 -1, -2처럼 뒤에서부터 지정해 마지막 두 축만 사용하세요. 테스트는 4차원 입력이 head별 계산과 같은지도 확인합니다.

Bash
pytest tests/test_attention_practice.py -v
python tools/selfcheck.py --day 4
7.5 Day 5 - Causal Multi-Head Attention

핵심 질문: 여러 attention head가 서로 다른 관계를 학습하도록 계산을 어떻게 나누며, causal mask는 미래 정보 사용을 어떻게 막는가?

먼저 읽을 교재: 3.5.2~3.5.3, 3.6(3.6.1~3.6.2)

교재와 다른 점: 생성자(W_query·W_key·W_value·out_proj, context_length 크기의 mask buffer)는 교재 3.6.2와 같습니다. 교재는 forward 안에서 score·mask·softmax를 다시 작성하지만, 이 과제는 Day 4의 scaled_dot_product_attention을 호출합니다. forward에는 mask를 끄고 비교할 수 있는 causal_mask와 attention weight를 확인하기 위한 return_attention_weights 인자가 추가되어 있습니다.

구현:

MultiHeadAttention.forward

Plain text
x                        (B, T, d_in)
queries, keys, values    (B, T, d_out)
head 분리                 (B, H, T, D), d_out = H * D (H = num_heads, D = head_dim)
mask                     self.mask.bool()[:T, :T]
Day 4 함수 호출           context_vec (B, H, T, D), attn_weights (B, H, T, T)
head 결합                 (B, T, d_out)
out_proj                 (B, T, d_out)

score, mask, softmax는 Day 4 함수가 이미 처리합니다. Day 5에서 새로 익힐 것은 head 분리·결합과 projection입니다. (B, T, d_out)을 곧바로 (B, H, T, D)로 view하면 shape는 맞지만 서로 다른 token의 feature가 한 head에 섞이므로, 마지막 축을 (H, D)로 나눈 뒤 head 축을 앞으로 옮깁니다. 생성자가 등록한 self.mask는 context_length 크기이므로 입력 길이 T만큼 잘라 bool로 바꿔 넘깁니다. attention dropout은 self.dropout을 Day 4 함수에 넘겨 적용합니다.

d_out % num_heads == 0이어야 하며, mask의 대각선은 현재 token 자신을 볼 수 있도록 가리지 않습니다.

return_attention_weights=False이면 context_vec을, True이면 (context_vec, attn_weights)를 반환합니다. 테스트는 각 head가 만든 attention weight, 행 합, causal mask를 이 옵션으로 확인합니다.

Bash
pytest tests/test_attention.py -v
python tools/selfcheck.py --day 5
7.6 Day 6 - LayerNorm, FeedForward, TransformerBlock

핵심 질문: attention 외에 왜 정규화, 비선형 변환, shortcut 연결이 필요한가?

먼저 읽을 교재: 4.1~4.5

교재와 다른 점: 없습니다. LayerNorm의 scale·shift, FeedForward의 layers, TransformerBlock의 att·ff·norm1·norm2·drop_shortcut이 교재 4.2~4.5와 같습니다. GELU는 교재 4.3의 tanh 근사식으로 제공됩니다.

구현:

LayerNorm.forward

FeedForward.__init__의 self.layers: Linear(emb_dim, 4 * emb_dim) -> GELU -> Linear(4 * emb_dim, emb_dim)

TransformerBlock.forward

Python
shortcut = x
x = drop_shortcut(att(norm1(x)))
x = x + shortcut
shortcut = x
x = drop_shortcut(ff(norm2(x)))
x = x + shortcut

TransformerBlock 생성자와 GELU는 제공되어 있습니다. 각 부품을 다시 선언하지 말고 forward의 데이터 흐름에 집중하세요.

Bash
pytest tests/test_model.py -v -k "LayerNorm or FeedForward or TransformerBlock"
python tools/selfcheck.py --day 6
7.7 Day 7 - GPTModel, language modeling loss, greedy generation

핵심 질문: token ID는 어떻게 vocabulary logits가 되며 next-token loss는 어떻게 계산하는가?

먼저 읽을 교재: 4.6~4.7, 5.1(5.1.1~5.1.3), 5.2, 5.4

교재와 다른 점: GPTModel(tok_emb·pos_emb·drop_emb·trf_blocks·final_norm·out_head)과 forward가 logits만 반환하고 loss는 calc_loss_batch에서 계산하는 구조는 교재와 같습니다. 제공된 train_model_simple에는 gradient clipping(grad_clip, 부록 D.3)과 checkpoint 저장(ckpt_path) 선택 인자가 추가되어 있습니다.

구현:

GPTModel.forward

generate_text_simple

train.calc_loss_batch

Plain text
in_idx (B, T) -> tok_emb + pos_emb -> drop_emb -> trf_blocks -> final_norm
              -> out_head -> logits (B, T, V)

position index는 torch.arange(T, device=in_idx.device)처럼 input과 같은 device에 만듭니다. F.cross_entropy는 (N, C)와 (N,)을 받으므로 calc_loss_batch에서 logits와 target을 각각 flatten(0, 1), flatten()으로 (B*T, V), (B*T)로 펼칩니다. logits는 softmax 전의 점수이며 확률이 아닙니다.

검증 순서:

1

학습 전 loss가 ln(vocab_size) 근처인지 확인합니다.

2

작은 batch 하나를 반복해 loss가 뚜렷하게 감소하는지 확인합니다.

3

Smoke 데이터로 짧은 학습이 끝까지 실행되는지 확인합니다.

4

greedy 생성이 context window를 넘지 않고 token을 이어 붙이는지 확인합니다.

Light·Basic 사전 학습은 Day 8에서 진행합니다.

Bash
pytest tests/test_model.py tests/test_train.py -v
python tools/selfcheck.py --day 7 --trace

tiny-batch overfit은 좋은 모델을 만드는 실험이 아닙니다. token shift에서 loss까지의 계산 graph와 gradient가 연결되었는지 확인하는 디버깅 절차입니다. 이 검증이 일반화 성능을 보장하지는 않습니다.

src/train.py의 학습·평가·checkpoint·sampling 함수는 제공 코드입니다. 다음 순서는 코드에서 찾아 설명할 수 있어야 합니다.

Plain text
optimizer.zero_grad()
loss = calc_loss_batch(...)
loss.backward()
optimizer.step()

평가에서는 model.eval()과 torch.no_grad()를 사용하고, 평가 후 학습을 계속할 때는 model.train()으로 복귀합니다.

7.8 Day 8 - 감성 분류 head와 작은 통합 실행

핵심 질문: 다음 token을 예측하는 backbone을 문장 분류에 어떻게 재사용하는가?

먼저 읽을 교재: 6.1~6.3, 6.5~6.7

교재와 다른 점: 교재는 스팸 문자 데이터와 오픈AI GPT-2 가중치를 사용하지만, 이 과제는 NSMC 영화 리뷰와 직접 사전 학습한 backbone을 사용합니다. 또 교재 6.5는 마지막 위치 출력 [:, -1, :]을 사용하지만, 이 과제는 짧은 리뷰가 padding 위치의 출력을 쓰지 않도록 마지막 non-pad 위치를 선택합니다.

구현:

prepare_for_classification: 교재 6.5처럼 모든 parameter를 동결하고 out_head를 Linear(emb_dim, num_classes)로 교체한 뒤, 새 out_head와 마지막 TransformerBlock, final_norm만 학습하도록 설정합니다.

last_token_logits: (B, T, num_classes) logits에서 샘플마다 마지막 non-pad 위치를 골라 (B, num_classes)를 반환합니다. GPT는 causal이므로 문장 전체를 본 위치는 마지막 유효 token입니다.

데이터 준비, NSMCDataset(교재의 SpamDataset에 해당), calc_accuracy_loader, calc_loss_batch, train_classifier_simple, classify_review는 제공됩니다. backbone의 position embedding은 context_length개 위치만 가지므로 리뷰의 max_length는 backbone의 context_length 이하로 둡니다.

Plain text
review IDs (B, T) -> GPTModel (out_head 교체) -> logits (B, T, 2)
                  -> 마지막 non-pad 위치 -> logits (B, 2)

사전 학습의 out_head는 각 위치의 출력을 vocab_size개 점수로 바꿔 다음 token을 예측합니다. 감성 분류는 리뷰 전체를 부정·긍정 두 class로 나누므로 out_head를 2개 점수를 내는 Linear로 교체합니다.

제공된 finetune.calc_loss_batch는 last_token_logits로 고른 (B, 2) logits와 label로 F.cross_entropy를 계산합니다. Day 7에 구현한 train.calc_loss_batch와 이름은 같지만 다른 함수입니다.

노트북 Day 8은 Smoke backbone으로 분류 loop를 먼저 확인하고, Light 사전 학습을 실행한 뒤 그 backbone으로 감성 분류를 다시 학습합니다. Basic은 여건이 허락하는 범위에서 실행합니다(5.2절).

Bash
pytest tests/test_finetune.py -v
python tools/selfcheck.py --day 8

감성 분류 정확도 임계값은 없습니다.

8. 선택 심화

필수 TODO와 가능한 범위의 Smoke·Light·Basic 실행을 마친 뒤 한 항목을 선택합니다.

temperature와 top-k가 token 분포에 미치는 영향 비교

backbone 동결과 전체 미세 튜닝의 gradient 차이 확인

weight tying 적용 전·후 parameter 수 비교

한 변수만 바꾼 Light 또는 Basic 규모 통제 실험

BPE encode·decode·save·load 코드 직접 구현

temperature·top-k는 교재 5.3 무작위성을 제어하기 위한 디코딩 전략, 훈련 루프 개선은 부록 D 훈련 루프에 부가 기능 추가하기를 참고합니다.

선택 심화 결과는 성능 순위가 아니라 조건, 관찰, 한계를 정확히 설명하는 데 의미가 있습니다.

9. 제출물

모든 Day를 마치면 python tools/selfcheck.py --all로 전체 테스트와 개념 질문을 확인하고, 실패한 테스트가 있으면 해당 Day의 핵심 계산과 불변조건부터 다시 확인합니다. 팀별로 다음을 제출합니다.

완성한 src/ 소스 코드

실행 가능한 gpt-lab.ipynb

전체 테스트 결과

REPORT.md

9.1 REPORT.md

코드를 길게 복사하지 말고 구현할 때 판단한 내용과 검증 근거를 작성합니다.

섹션	필수 내용
0. 반·팀원	반, 팀명, 팀원, 구현·리뷰 방식
1. 전체 흐름	text -> token -> Dataset -> attention -> GPT -> loss·classification의 연결 원리
2. 핵심 구현	BPE, Dataset·Embedding, Attention, Block·GPT, 분류 설명
3. 검증 결과	전체 테스트, 초기 loss, causal mask, tiny-batch overfit
4. 규모별 실행	Smoke·Light·Basic의 vocab·context·parameter·step·실행 범위, train·validation loss 변화
5. 오류와 해결	최소 입력, 원인, 수정 후 검증
6. 참고와 AI 사용	질문·참고 내용, 먼저 시도한 것, 직접 검증한 방법
7. 회고	이해한 개념, 남은 질문, 다시 구현할 때 확인할 것
