# Claude Trading Skills

このリポジトリは、株式投資やトレードに役立つClaudeスキルをまとめたものです。各スキルには、プロンプト設計、参照資料、補助スクリプトが含まれており、システマティックなバックテスト、マーケット環境分析、バブル判定、米国株リサーチをClaudeに任せることができます。ClaudeのウェブアプリとClaude Codeの両方で活用できます。

English README is available at [`README.md`](README.md).

## リポジトリ構成
- `<skill-name>/` – 各スキルのソースフォルダ。`SKILL.md`、参照資料、補助スクリプトが含まれます。
- `zip-packages/` – Claudeウェブアプリの**Skills**タブへそのままアップロードできるZIPパッケージ置き場。

## はじめに
### Claudeウェブアプリで使う場合
1. 利用したいスキルに対応するZIPを`zip-packages/`からダウンロードします。
2. ブラウザでClaudeを開き、**Settings → Skills**に進んでZIPをアップロードします（詳しくはAnthropicの[Skillsローンチ記事](https://www.anthropic.com/news/skills)を参照）。
3. 必要な会話内でスキルを有効化します。

### Claude Code（デスクトップ/CLI）で使う場合
1. このリポジトリをクローン、もしくはダウンロードします。
2. 使いたいスキルのフォルダ（例: `backtest-expert`）をClaude Codeの**Skills**ディレクトリにコピーします（Claude Code → **Settings → Skills → Open Skills Folder**。詳細は[Claude Code Skillsドキュメント](https://docs.claude.com/en/docs/claude-code/skills)を参照）。
3. Claude Codeを再起動、またはリロードすると新しいスキルが認識されます。

> ヒント: ソースフォルダとZIPの内容は同一です。スキルをカスタマイズする場合はソースフォルダを編集し、ウェブアプリ向けに配布するときは再度ZIP化してください。

## スキル一覧
- **Backtest Expert** (`backtest-expert`)
  - 戦略仮説の定義、パラメータ堅牢性検証、スリッページモデル、ウォークフォワード検証など、プロ仕様のバックテスト手法を網羅。
  - `references/methodology.md`（テスト手法）と`references/failed_tests.md`（失敗事例集）が付属。
- **Market Environment Analysis** (`market-environment-analysis`)
  - 株式指数、為替、コモディティ、金利、センチメントを含むグローバル市場分析とレポート作成をガイド。
  - インジケータ解説（`references/indicators.md`）、分析パターン集に加え、レポート整形用スクリプト`scripts/market_utils.py`を同梱。
- **Stanley Druckenmiller Investment Advisor** (`stanley-druckenmiller-investment`)
  - ドラッケンミラーの投資哲学をもとに、マクロポジショニング、流動性分析、リスク管理を日英両言語で支援。
  - 投資哲学の詳細、分析手順、ケーススタディを含むリファレンス一式を収録。
- **US Market Bubble Detector** (`us-market-bubble-detector`)
  - ミンスキー/キンドルバーガーフレームワークに基づく8指標バブルスコアリングと、フェーズ診断、利確・ヘッジ戦術を提供。
  - 歴史的事例、日英版クイックリファレンス、対話型スコアラー`scripts/bubble_scorer.py`を利用可能。
- **US Stock Analysis** (`us-stock-analysis`)
  - ファンダメンタル/テクニカル分析、同業比較、投資レポート生成を一体化した米国株リサーチ用スキル。
  - `fundamental-analysis.md`、`technical-analysis.md`、`financial-metrics.md`、`report-template.md`による分析フレームワークを収録。

## カスタマイズと貢献
- トリガー説明や機能メモを調整する場合は、各フォルダ内の`SKILL.md`を更新してください。ZIP化する際はフロントマター`name`がフォルダ名と一致しているか確認してください。
- 参照資料の追記や新規スクリプト追加でワークフローを拡張できます。
- 変更を配布する場合は、最新の内容を反映したZIPを`zip-packages/`に再生成してください。

## 参考リンク
- Claude Skillsローンチ概要: https://www.anthropic.com/news/skills
- Claude Code Skillsガイド: https://docs.claude.com/en/docs/claude-code/skills

質問や改善案があればissueを作成するか、各スキルフォルダにメモを残しておくと、後から利用するユーザーにもわかりやすくなります。
