# Theme Detector 테스트

## Unit 테스트 (Phase 1)
- test_industry_ranker.py
- test_theme_classifier.py
- test_heat_calculator.py
- test_lifecycle_calculator.py
- test_scorer.py
- test_report_generator.py
- test_uptrend_client.py

## Unit 테스트 (Phase 2)
- test_representative_stock_selector.py (동적 종목 선택, FINVIZ/FMP fallback, circuit breaker)

## Integration 테스트
- test_theme_detector_e2e.py (전체 파이프라인, mocked I/O, 네트워크 불필요)

## Network Integration 테스트 (Phase 2 TODO)
- test_finviz_performance_client.py (네트워크 필요)
- test_etf_scanner.py (네트워크 필요)
- test_uptrend_client_integration.py (네트워크 필요)
