# Alpaca MCP Server Setup Guide

이 문서는 Portfolio Manager 스킬에서 사용할 Alpaca MCP (Model Context Protocol) Server를 설정/구성하는 방법을 설명합니다.

## Alpaca MCP Server란?

Alpaca MCP Server는 표준 인터페이스를 통해 Claude가 Alpaca 브로커리지 계정 데이터에 접근할 수 있게 해주는 Model Context Protocol 서버입니다. 이를 통해 Portfolio Manager 스킬은 Alpaca 계정에서 실시간 포지션, 계정 정보, 거래 이력을 직접 조회할 수 있습니다.

## Prerequisites

### 1. Alpaca Account

Alpaca 브로커리지 계정이 필요합니다 (paper trading 또는 live):

- **가입:** https://alpaca.markets/
- **Paper Trading:** 무료, 가상 자금 사용 (테스트 권장)
- **Live Trading:** 실제 자금 계정 (입금 필요)

### 2. Alpaca API Keys

Alpaca 대시보드에서 API 키를 발급합니다.

**Paper Trading용:**
1. Alpaca dashboard 로그인: https://app.alpaca.markets/
2. "Paper Trading" 계정으로 이동
3. "Your API Keys" 섹션 이동
4. "Generate New Key" 클릭
5. 다음 정보를 저장:
   - **API Key ID** (public key)
   - **Secret Key** (private key - 1회만 표시)

**Live Trading용:**
1. Alpaca dashboard 로그인
2. "Live Trading" 계정으로 이동
3. "Your API Keys" 섹션 이동
4. "Generate New Key" 클릭
5. API credentials 저장

⚠️ **보안 주의:** Secret Key는 절대 공유하거나 버전관리 시스템에 커밋하지 마세요. 비밀번호처럼 취급해야 합니다.

## Installation

### Option 1: MCP Server 사용 (Claude Desktop/Web 권장)

**Step 1: Alpaca MCP Server 설치**

Alpaca MCP server는 Claude MCP marketplace 또는 standalone 패키지로 제공될 수 있습니다.

Claude 환경에서 사용 가능 여부 확인:
```bash
# 사용 가능한 MCP 서버 목록
claude mcp list
```

설치되어 있지 않다면 Anthropic MCP server 설치 가이드를 플랫폼에 맞게 따르세요.

**Step 2: API Keys 구성**

Alpaca credentials를 환경 변수로 설정합니다.

**macOS/Linux:**
```bash
# Paper Trading
export ALPACA_API_KEY="your_api_key_id"
export ALPACA_SECRET_KEY="your_secret_key"
export ALPACA_PAPER=true

# Live Trading
export ALPACA_API_KEY="your_api_key_id"
export ALPACA_SECRET_KEY="your_secret_key"
export ALPACA_PAPER=false
```

세션 재시작 후에도 유지하려면 `~/.bashrc` 또는 `~/.zshrc`에 추가:
```bash
echo 'export ALPACA_API_KEY="your_api_key_id"' >> ~/.bashrc
echo 'export ALPACA_SECRET_KEY="your_secret_key"' >> ~/.bashrc
echo 'export ALPACA_PAPER=true' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
# Paper Trading
$env:ALPACA_API_KEY="your_api_key_id"
$env:ALPACA_SECRET_KEY="your_secret_key"
$env:ALPACA_PAPER="true"

# Live Trading
$env:ALPACA_API_KEY="your_api_key_id"
$env:ALPACA_SECRET_KEY="your_secret_key"
$env:ALPACA_PAPER="false"
```

Windows에서 환경 변수 영구 저장:
```powershell
[System.Environment]::SetEnvironmentVariable('ALPACA_API_KEY', 'your_api_key_id', 'User')
[System.Environment]::SetEnvironmentVariable('ALPACA_SECRET_KEY', 'your_secret_key', 'User')
[System.Environment]::SetEnvironmentVariable('ALPACA_PAPER', 'true', 'User')
```

**Step 3: MCP Server 시작**

Claude 실행 시 MCP server가 자동 시작되어야 합니다. 연결 확인:
```bash
# MCP 서버 상태 확인 (CLI 제공 시)
claude mcp status
```

### Option 2: Direct API Integration (대안)

MCP server를 사용할 수 없으면 Python 기반 Alpaca API 직접 연동으로 대체할 수 있습니다.

**Step 1: Alpaca Python SDK 설치**
```bash
pip install alpaca-trade-api
```

**Step 2: 구성 파일 생성**

`~/.alpaca/config.ini` 생성:
```ini
[alpaca]
api_key_id = your_api_key_id
secret_key = your_secret_key
base_url = https://paper-api.alpaca.markets  # Paper trading
# base_url = https://api.alpaca.markets     # Live trading
```

권한 설정:
```bash
chmod 600 ~/.alpaca/config.ini
```

**Step 3: 연결 테스트**

제공된 테스트 스크립트 실행:
```bash
python3 portfolio-manager/scripts/test_alpaca_connection.py
```

예상 출력:
```
✓ Successfully connected to Alpaca API
Account Status: ACTIVE
Equity: $100,000.00
Cash: $50,000.00
Buying Power: $200,000.00
Positions: 5
```

## Available MCP Tools

구성이 완료되면 Portfolio Manager는 다음 Alpaca MCP 도구를 사용할 수 있습니다.

### `mcp__alpaca__get_account_info`
계정 요약 조회:
- Total equity (portfolio value)
- Cash balance
- Buying power
- Account status
- Day trading buying power (해당 시)

### `mcp__alpaca__get_positions`
모든 오픈 포지션 조회:
- Symbol ticker
- Quantity (shares)
- Average entry price (cost basis)
- Current market price
- Current market value
- Unrealized P&L ($ and %)
- Today's P&L

### `mcp__alpaca__get_portfolio_history`
포트폴리오 과거 성과 조회:
- Equity time series
- Profit/loss time series
- Timeframes: 1D, 1W, 1M, 3M, 1Y, All

### `mcp__alpaca__get_orders`
주문 목록 조회(open/filled/cancelled):
- Order ID
- Symbol
- Quantity
- Order type (market, limit, stop 등)
- Status
- Fill price (체결 시)
- Timestamps

### `mcp__alpaca__get_activities`
계정 활동 조회:
- Trades (fills)
- Dividend payments
- Stock splits
- Journal entries

## Verification and Testing

### Test 1: Account Connection

Claude에게 계정 정보 조회 요청:
```
"Can you get my Alpaca account information?"
```

예상 응답에는 equity, cash, buying power가 포함되어야 합니다.

### Test 2: Portfolio Positions

현재 포지션 요청:
```
"What positions do I have in my portfolio?"
```

예상 응답에는 모든 보유 종목의 수량/가치가 포함되어야 합니다.

### Test 3: Portfolio Analysis

Portfolio Manager 스킬 실행:
```
"Analyze my portfolio"
```

스킬은 다음을 수행해야 합니다:
1. MCP로 포지션 조회
2. 추가 시장 데이터 수집
3. 종합 분석 수행
4. 상세 보고서 생성

## Troubleshooting

### Error: "Alpaca MCP Server not connected"

**원인 가능성:**
1. MCP server 미실행
2. API keys 미구성
3. API keys 만료/오류

**해결 방법:**
1. Claude를 재시작해 MCP server 재초기화
2. 환경 변수 확인: `echo $ALPACA_API_KEY`
3. Alpaca dashboard에서 API keys 점검(필요 시 재발급)
4. 계정 상태 확인(정지 여부)

### Error: "Invalid API credentials"

**원인 가능성:**
1. 잘못된 API keys
2. live keys를 paper mode와 혼용 (또는 반대)
3. API keys 철회됨

**해결 방법:**
1. API Key ID/Secret Key 재확인(공백/오타 포함)
2. `ALPACA_PAPER` 설정과 API key 종류 일치 확인
3. Alpaca dashboard에서 키 재발급
4. 올바른 계정(paper/live) 사용 확인

### Error: "Forbidden - insufficient permissions"

**원인 가능성:**
1. API keys 권한 제한
2. 계정 거래 승인 미완료

**해결 방법:**
1. 전체 권한으로 API keys 재발급
2. Alpaca dashboard에서 계정 상태 확인
3. Live 계정은 승인 절차 완료 여부 확인

### Error: "No positions found"

**원인 가능성:**
1. 실제로 빈 포트폴리오
2. 잘못된 계정 선택(paper/live)
3. API stale 데이터

**해결 방법:**
1. Alpaca dashboard에서 포지션 존재 확인
2. `ALPACA_PAPER` 설정이 의도 계정과 일치하는지 확인
3. Claude에 포지션 재조회 요청
4. Alpaca API status 확인: https://status.alpaca.markets/

### MCP Server Not Responding

**해결 방법:**
1. Claude 애플리케이션 재시작
2. MCP server 로그 확인(가능한 경우)
3. 네트워크 연결 확인
4. Direct API integration(Option 2)로 우회

## Security Best Practices

### 1. 테스트는 Paper Trading부터
반드시 paper 계정에서 충분히 검증 후 live로 전환하세요.

### 2. API Keys 보호
- API keys를 GitHub/버전관리 시스템에 커밋 금지
- 하드코딩 대신 환경 변수 사용
- config 파일 권한: `chmod 600`
- 정기적 키 교체(예: 90일)

### 3. Read-Only Keys 사용 (지원 시)
포트폴리오 분석만 필요하면 read-only API key 사용을 권장합니다. 오주문 리스크를 줄일 수 있습니다.

### 4. API Usage 모니터링
- Alpaca dashboard API 호출 로그 확인
- 계정 활동 정기 점검
- 이상 활동 알림 설정

### 5. Paper/Live 환경 분리
- 서로 다른 환경 변수 prefix 사용
- paper/live credentials 혼용 금지
- 키 용도 문서화

## API Rate Limits

Alpaca API에는 호출 제한이 있습니다.

**Free Tier:**
- 분당 200 requests
- 무료 시장 데이터는 15분 지연

**Paid Tier (Alpaca Markets Data subscription):**
- 더 높은 rate limit
- 실시간 데이터

**Best Practices:**
- Portfolio Manager 스킬은 내장 rate limiting 포함
- 분석은 1분에 1회 이상 실행하지 않기
- 빈번 모니터링 시 캐싱 고려

## Alternative: Manual Data Entry

Alpaca 통합이 불가할 때 수동 포트폴리오 데이터를 사용할 수 있습니다.

**CSV Format:**
```csv
symbol,quantity,cost_basis,current_price
AAPL,100,150.00,175.50
MSFT,50,280.00,310.25
GOOGL,25,2500.00,2750.00
```

**사용 방법:**
1. 브로커에서 CSV로 포지션 내보내기
2. Claude에 파일 제공: "Analyze my portfolio using this CSV file"
3. 스킬이 데이터를 파싱해 분석 수행

**제한 사항:**
- 실시간 업데이트 없음
- 과거 성과 데이터 없음
- 수동 업데이트 필요

## Additional Resources

**Alpaca Documentation:**
- API docs: https://alpaca.markets/docs/
- Python SDK: https://github.com/alpacahq/alpaca-trade-api-python
- API reference: https://alpaca.markets/docs/api-references/trading-api/

**MCP Protocol:**
- Anthropic MCP docs: https://docs.anthropic.com/claude/docs/model-context-protocol
- MCP specification: https://github.com/anthropics/mcp

**Support:**
- Alpaca support: support@alpaca.markets
- Alpaca community: https://forum.alpaca.markets/
- API status: https://status.alpaca.markets/
