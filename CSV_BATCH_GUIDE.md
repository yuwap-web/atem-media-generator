# CSV 一括処理ガイド

**Batch Export (CSV) 機能の完全な使い方**

---

## 📋 概要

CSV（カンマ区切り値）ファイルから複数のテキストパラメータを読み込み、一度に複数の画像を自動生成できます。

**使用例**:
- 複数のニュース速報を一括生成
- イベント参加者の名前で複数のロワーサード画像を作成
- テンプレートを使った大量画像生成

---

## 🚀 基本的な使い方

### ステップ 1: CSV ファイルを準備

テンプレートのパラメータに対応したCSVファイルを作成します。

**テンプレート「Simple Title」の場合:**

```csv
title,subtitle
Welcome to ATEM,Professional Graphics
Session Start,Live Event
Scene Transition,Smooth Change
Breaking News,Latest Updates
```

**テンプレート「Lower Third - Name Only」の場合:**

```csv
name,title
山田太郎,ニュースキャスター
鈴木花子,天気予報士
佐藤次郎,スポーツキャスター
田中美咲,アナウンサー
```

**重要な注意:**
- **第1行（ヘッダー）**: テンプレートのパラメータ名と完全に一致する必要があります
- **パラメータ順序**: 任意の順序で問題ありません
- **必須パラメータ**: 各行に必須パラメータが入っていなければスキップされます
- **オプションパラメータ**: 空欄で問題ありません

---

## 📝 テンプレートごとの CSV 例

### 1. Simple Title テンプレート

```csv
title,subtitle
Welcome,Graphics
Start,Event
Transition,Change
```

**テンプレートの要件:**
- 必須: `title`
- オプション: `subtitle`

---

### 2. Lower Third - Name Only テンプレート

```csv
name,title
Taroh Yamada,News Anchor
Hanako Suzuki,Weather Forecaster
Jiro Sato,Sports Commentator
```

**テンプレートの要件:**
- 必須: `name`
- オプション: `title`

---

### 3. Lower Third - Japanese テンプレート

```csv
name,title
山田太郎,ニュースキャスター
鈴木花子,天気予報士
佐藤次郎,スポーツキャスター
田中美咲,アナウンサー
```

---

### 4. カスタムテンプレート例

独自テンプレート「title_japanese.json」の場合:

```json
{
  "required_parameters": ["title"],
  "optional_parameters": ["subtitle"]
}
```

対応するCSV:

```csv
title,subtitle
プレゼンテーション,2026年3月
ニュース速報,緊急情報
イベント案内,ご参加ください
```

---

## 🔧 Batch Export の実行手順

### ステップ 1: テンプレートを選択

左パネルで「Batch Export」に使用するテンプレートをクリックして選択します。

**例**:「Lower Third - Name Only」を選択

### ステップ 2: ツールバーで「Batch Export (CSV)」をクリック

メニューバーの「Batch Export (CSV)」ボタンをクリック

### ステップ 3: CSV ファイルを選択

ダイアログボックスで準備したCSVファイルを選択

```
~/Desktop/names.csv  ← このファイルを選択
```

### ステップ 4: 確認して実行

表示される確認ダイアログで:
- テンプレート名: "Lower Third - Name Only"
- CSVファイル名: "names.csv"
- 出力フォルダ: "~/mediafile/output"

を確認して「Yes」をクリック

### ステップ 5: 処理完了

進捗が表示され、完了すると成功メッセージが表示されます

```
Batch processing complete!
Generated 4 images.

Output directory: ~/mediafile/output
```

---

## 📂 出力ファイル

生成されたファイルは `output/` ディレクトリに保存されます。

```
output/
├── lower_third_name_only_20260301_120000.png
├── lower_third_name_only_20260301_120001.png
├── lower_third_name_only_20260301_120002.png
└── lower_third_name_only_20260301_120003.png
```

**ファイル名形式:**
```
{template_type}_{template_name}_{YYYYMMDD}_{HHMMSS}.png
```

---

## ⚠️ トラブルシューティング

### 問題 1: CSV ファイルが読み込めない

**症状**: ファイル選択後、エラーメッセージが出る

**原因と対策**:
1. **文字コード**: UTF-8 で保存されているか確認
   - Excel で保存する場合:「CSV (UTF-8)」形式を選択
2. **ファイル拡張子**: `.csv` であることを確認
3. **ヘッダー**: 第1行がテンプレートパラメータと一致しているか確認

### 問題 2: いくつかの行がスキップされた

**症状**: CSV に 5 行あるが、3 個の画像だけ生成された

**原因**: 必須パラメータが不足している

**対策**: CSV ファイルを確認
```csv
name,title
山田太郎,ニュースキャスター  ✅ OK
鈴木花子,               ✅ OK (title は オプション)
,佐藤次郎               ❌ NG (name が空)
```

3 行目の `name` が空なため、この行はスキップされます

### 問題 3: 文字化けが発生

**症状**: 生成された画像に日本語が表示されない

**原因**:
1. フォントが選択されていない
2. CSV が UTF-8 で保存されていない

**対策**:
1. テンプレートが日本語フォント（ヒラギノ等）を使用しているか確認
2. CSV を UTF-8 で保存し直す

---

## 💡 実践的な例

### シナリオ: ニュース番組の複数キャスターのロワーサード生成

**1. CSV ファイルを作成** (`news_casters.csv`):

```csv
name,title
田中花子,メインキャスター
山田太郎,ニュースコメンテーター
鈴木次郎,気象予報士
佐藤美咲,スポーツキャスター
```

**2. テンプレートを選択**:
- 「Lower Third - Japanese」を選択

**3. Batch Export を実行**:
- `news_casters.csv` を選択
- 「Yes」で確認

**4. 結果**:
```
Generated 4 images.
- lower_third_japanese_20260301_120000.png (田中花子)
- lower_third_japanese_20260301_120001.png (山田太郎)
- lower_third_japanese_20260301_120002.png (鈴木次郎)
- lower_third_japanese_20260301_120003.png (佐藤美咲)
```

すべての画像が `output/` フォルダに保存されます！

---

## 🎯 CSV 作成のベストプラクティス

### ✅ 推奨:
```csv
title,subtitle
Welcome,Professional
Start,Event
```
- シンプルで読みやすい
- UTF-8 で保存
- ダブルクォートなし

### ❌ 避けるべき:
```csv
"title","subtitle"
"Welcome","Professional"
```
- 不要なダブルクォート
- テンプレートとの一致が難しい

---

## 🔄 パフォーマンス

| 項目 | 時間 |
|------|------|
| 1 画像生成 | ~500ms |
| 10 画像一括 | ~5秒 |
| 100 画像一括 | ~50秒 |

大量の画像を生成する場合は、背景で処理されるため、その間アプリは応答します。

---

## 📊 CSV ファイル検証

Batch Export 前に CSV を検証するには:

```bash
# ターミナルで確認
head -5 your_file.csv
```

出力例:
```
name,title
山田太郎,ニュースキャスター
鈴木花子,天気予報士
佐藤次郎,スポーツキャスター
```

---

## 🚀 応用例

### 1. イベント参加者リスト
```csv
name,affiliation
Alice,Company A
Bob,Company B
Carol,Company C
```

### 2. 売上ランキング
```csv
rank,company,amount
1位,Company A,1000万円
2位,Company B,900万円
3位,Company C,850万円
```

### 3. スケジュール案内
```csv
date,event,location
2026-03-01,Meeting A,Room 101
2026-03-02,Meeting B,Room 102
2026-03-03,Meeting C,Room 103
```

---

**CSV 一括処理で効率的に複数の画像を生成しましょう！** 🚀

[← テンプレートガイド](TEMPLATE_GUIDE.md) | [クイックスタート →](QUICK_START_CUSTOMIZER.md)
