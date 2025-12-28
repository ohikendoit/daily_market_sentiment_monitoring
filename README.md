# Daily Market Sentiment Monitoring


### Purpose
This project produces a **daily, structured monitoring report** of U.S. equity market conditions,  
focusing on **market momentum, volatility, valuation, real yield risk, and technical signals**.

All outputs must be **data-driven, reproducible, and free of fabricated values**.

## (A) Core Market Metrics

### 1. Equity Market Level
- **S&P 500 Index**
  - Latest index level
  - **Daily / Weekly / Monthly % change**
  - Directional symbols: ↑ (increase), ↓ (decrease)

### 2. Volatility
- **VIX Index**
  - Latest index level
  - **Daily / Weekly / Monthly % change**
  - Directional symbols: ↑ / ↓

### 3. Market Sentiment
- **CNN Fear & Greed Index**
  - Latest index value
  - **Point change** (daily / weekly / monthly)
  - If no reliable public API is available, mark as **“N/A”**

### 4. Valuation
- **S&P 500 Forward P/E** (latest available)
  - Provide qualitative interpretation  
    (e.g. valuation pressure, neutral, attractive)
- **Earnings Yield**
  - Defined as: `1 / Forward P/E`
- **Real Earnings Yield**
  - Defined as: `Earnings Yield – U.S. CPI YoY`

### 5. Inflation
- **U.S. CPI YoY**
  - Latest available **monthly** value only

> **Data Integrity Rule**  
> If a metric cannot be sourced reliably from public or licensed data,  
> it must be explicitly marked as **“N/A”**.  
> No estimation, proxy, or inferred values are allowed.

## (B) Technical Indicators  
**All technical indicators must be computed using U.S. equity benchmarks  
(S&P 500 or SPY).**

### 1. Momentum
- **RSI (14-day)**
  - Current RSI value
  - Classification:
    - Overbought (≥ 70)
    - Neutral (30–69)
    - Oversold (≤ 30)

### 2. Price Distribution
- **Bollinger Bands (20-day, ±2σ)**
  - Indicate whether the current price is near:
    - Upper band
    - Middle band
    - Lower band

### 3. Participation
- **SPY Volume Trend**
  - Compare latest volume vs. 20-day average
  - Output as: ↑ (above average), ↓ (below average), or N/A

## (C) Output Requirements

### 1. Summary Table
A **single consolidated table** containing:
- Metric name
- Current value
- Daily / Weekly / Monthly change (with ↑ / ↓ symbols)
- Short **interpretation in Korean**

### 2. Commentary (2–3 sentences)
A concise narrative summary addressing:
- Overall market sentiment
- Volatility regime
- Valuation pressure
- Real earnings yield risk
- Technical momentum
- Whether interest-rate expectations  
  **support or constrain** risk appetite

## (D) Guiding Principles

- All outputs must be **deterministic and reproducible**
- Do **not** fabricate, infer, or approximate unavailable data
- Accuracy and clarity take precedence over completeness
- Missing data must always be labeled as **“N/A”**


---

### 목적
본 프로젝트는 **미국 주식 시장의 일일 상태를 구조적으로 모니터링**하기 위한 시스템이다.  
시장 **모멘텀, 변동성, 밸류에이션, 실질 수익률 리스크, 기술적 신호**를 중심으로  
**객관적·재현 가능·비조작적 데이터 리포트**를 생성하는 것을 목표로 한다.

## (A) 핵심 시장 지표

### 1. 주식 시장 수준
- **S&P 500 지수**
  - 최신 지수 수준
  - **일간 / 주간 / 월간 변동률(%)**
  - 방향 표기: ↑ (상승), ↓ (하락)

### 2. 변동성
- **VIX 지수**
  - 최신 지수 수준
  - **일간 / 주간 / 월간 변동률(%)**
  - 방향 표기: ↑ / ↓

### 3. 투자 심리
- **CNN Fear & Greed Index**
  - 최신 지수 값
  - **포인트 변화** (일 / 주 / 월)
  - 신뢰 가능한 공개 데이터 소스가 없을 경우 **“N/A”로 명시**

### 4. 밸류에이션
- **S&P 500 Forward P/E**
  - 최신 가용 값
  - 정성적 해석 제공  
    (예: 밸류에이션 부담, 중립, 매력적 수준)
- **Earnings Yield**
  - 정의: `1 / Forward P/E`
- **Real Earnings Yield**
  - 정의: `Earnings Yield – 미국 CPI YoY`

### 5. 인플레이션
- **미국 CPI YoY**
  - 최신 **월간 수치**만 사용

> **데이터 무결성 원칙**  
> 신뢰 가능한 공개 또는 라이선스 데이터가 존재하지 않는 지표는  
> 반드시 **“N/A”로 명시**하며,  
> 추정·대체·보간값은 사용하지 않는다.

## (B) 기술적 지표  
**모든 기술적 지표는 미국 주식 벤치마크  
(S&P 500 또는 SPY)를 기반으로 계산한다.**

### 1. 모멘텀
- **RSI (14일)**
  - 현재 RSI 값
  - 구분:
    - 과매수 (≥ 70)
    - 중립 (30–69)
    - 과매도 (≤ 30)

### 2. 가격 분포
- **볼린저 밴드 (20일, ±2σ)**
  - 현재 가격 위치:
    - 상단
    - 중앙
    - 하단

### 3. 거래 참여도
- **SPY 거래량 추세**
  - 최근 거래량 vs 20일 평균 비교
  - 결과: ↑ (상회), ↓ (하회), N/A

## (C) 출력 형식

### 1. 요약 테이블
**단일 요약 테이블**에 다음 항목 포함:
- 지표명
- 현재 값
- 일 / 주 / 월 변화(↑ / ↓ 포함)
- **한국어 해석(짧은 문구)**

### 2. 코멘터리 (2–3문장)
다음 요소를 종합 요약:
- 전반적 시장 심리
- 변동성 국면
- 밸류에이션 부담
- 실질 수익률 리스크
- 기술적 모멘텀
- 금리 기대가 위험자산 선호를  
  **지지하는지 또는 제약하는지**

## (D) 설계 원칙

- 모든 결과는 **결정론적이며 재현 가능**해야 한다
- 데이터 조작, 추정, 임의 보완 금지
- 완성도보다 **정확성과 명확성**을 우선
- 누락 데이터는 반드시 **“N/A”로 명시**


## Environment
- Python: 3.11
- Conda env: dmsm
- Run: `conda activate dmsm && PYTHONPATH=src python -m mm.ingest.fear_greed`