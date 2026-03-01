# テンプレート作成ガイド

ATEM Media File Generator では、JSON ベースのテンプレートシステムを使用して、カスタマイズ可能な画像レイアウトを定義できます。

---

## 📋 テンプレートの基本構造

```json
{
  "name": "My Template",
  "template_type": "title",
  "background_color": [0, 0, 0, 255],
  "layers": [
    {
      "name": "Text Layer",
      "x": 100,
      "y": 400,
      "width": 1720,
      "height": 200,
      "font_name": "Helvetica",
      "font_size": 80,
      "color": [255, 255, 255, 255],
      "alignment": "center",
      "parameter_key": "title"
    }
  ],
  "required_parameters": ["title"],
  "optional_parameters": ["subtitle"]
}
```

---

## 🎨 テンプレート属性詳細

### トップレベル属性

| 属性 | 型 | 説明 | 例 |
|------|-----|------|-----|
| **name** | string | テンプレート名（ユーザーに表示） | "Simple Title" |
| **template_type** | string | テンプレートタイプ（title/lower_third/other） | "title" |
| **background_color** | [R,G,B,A] | 背景色（RGBA 0-255） | [0, 0, 0, 255] |
| **layers** | array | テキストレイヤーの配列 | [...] |
| **required_parameters** | array | 必須パラメータ | ["title"] |
| **optional_parameters** | array | オプションパラメータ | ["subtitle"] |

### background_color について

- **形式**: [Red, Green, Blue, Alpha]
- **範囲**: 0-255
- **例**:
  - 黒: `[0, 0, 0, 255]`
  - 白: `[255, 255, 255, 255]`
  - 透明背景: `[0, 0, 0, 0]`
  - 赤: `[255, 0, 0, 255]`
  - 青: `[0, 0, 255, 255]`
  - 緑: `[0, 255, 0, 255]`

### Text Layer 属性

| 属性 | 型 | 説明 | 例 |
|------|-----|------|-----|
| **name** | string | レイヤー名 | "Title Text" |
| **x** | int | X 座標（左上を起点） | 100 |
| **y** | int | Y 座標（左上を起点） | 400 |
| **width** | int | テキスト領域の幅 | 1720 |
| **height** | int | テキスト領域の高さ | 200 |
| **font_name** | string | フォント名 | "Helvetica" |
| **font_size** | int | フォントサイズ（ピクセル） | 80 |
| **color** | [R,G,B,A] | テキスト色（RGBA） | [255, 255, 255, 255] |
| **alignment** | string | テキスト配置（left/center/right） | "center" |
| **parameter_key** | string | CSV に対応するパラメータキー | "title" |

---

## 🖋️ 利用可能なフォント

### macOS システムフォント

以下のフォントは macOS に標準インストールされています：

| フォント名 | 説明 | 用途 |
|-----------|------|------|
| **Helvetica** | クラシックサンセリフ | 標準テンプレート |
| **Arial** | 汎用サンセリフ | 代替フォント |
| **Menlo** | モノスペース | タイムコード等 |
| **Courier New** | 古典的モノスペース | レトロスタイル |
| **Times New Roman** | セリフ体 | フォーマル文書 |
| **Georgia** | セリフ体（画面向け） | 読みやすい |
| **Monaco** | プログラマー向けモノスペース | テクニカル |

### 推奨フォント

```
テンプレート用途別推奨：
  • タイトル → Helvetica, Arial
  • ロウアーサード → Helvetica, Arial
  • テロップ → Helvetica, Arial
  • テクニカル → Menlo, Monaco
  • レトログ → Courier New
```

### カスタムフォント追加

1. TTF ファイルを `fonts/` ディレクトリに配置
2. テンプレートの `font_name` にファイル名を指定（拡張子なし）

```bash
# 例: フォントを追加
cp /path/to/MyFont.ttf fonts/MyFont.ttf

# テンプレートで使用
"font_name": "MyFont"
```

---

## 🎯 実践的な例

### 例 1: シンプルなロウアーサード

```json
{
  "name": "Lower Third Blue",
  "template_type": "lower_third",
  "background_color": [0, 50, 100, 200],
  "layers": [
    {
      "name": "Name",
      "x": 80,
      "y": 930,
      "width": 800,
      "height": 60,
      "font_name": "Helvetica",
      "font_size": 48,
      "color": [255, 255, 255, 255],
      "alignment": "left",
      "parameter_key": "name"
    },
    {
      "name": "Title",
      "x": 80,
      "y": 1000,
      "width": 800,
      "height": 50,
      "font_name": "Helvetica",
      "font_size": 32,
      "color": [200, 200, 255, 255],
      "alignment": "left",
      "parameter_key": "title"
    }
  ],
  "required_parameters": ["name"],
  "optional_parameters": ["title"]
}
```

### 例 2: マルチカラーテンプレート

```json
{
  "name": "Colorful Layers",
  "template_type": "other",
  "background_color": [40, 40, 40, 255],
  "layers": [
    {
      "name": "Header - Gold",
      "x": 100,
      "y": 100,
      "width": 1720,
      "height": 80,
      "font_name": "Helvetica",
      "font_size": 64,
      "color": [255, 200, 0, 255],
      "alignment": "center",
      "parameter_key": "header"
    },
    {
      "name": "Content - White",
      "x": 150,
      "y": 250,
      "width": 1620,
      "height": 300,
      "font_name": "Arial",
      "font_size": 48,
      "color": [255, 255, 255, 255],
      "alignment": "left",
      "parameter_key": "content"
    },
    {
      "name": "Footer - Gray",
      "x": 100,
      "y": 950,
      "width": 1720,
      "height": 50,
      "font_name": "Menlo",
      "font_size": 24,
      "color": [150, 150, 150, 255],
      "alignment": "right",
      "parameter_key": "footer"
    }
  ],
  "required_parameters": ["header", "content"],
  "optional_parameters": ["footer"]
}
```

---

## 📐 画面座標について

```
1920×1080 ピクセル（横×縦）

  (0,0) ──────── (1920,0)
    ↓            ↓
    │  IMAGE    │
    │           │
  (0,1080) ─ (1920,1080)
```

### よく使う座標

| 用途 | 座標 | 幅 | 高さ |
|------|------|-----|------|
| フルスクリーンタイトル | x:100, y:400 | 1720 | 200 |
| ロウアーサード（下部） | x:80, y:930 | 800 | 60 |
| 左パネル | x:50, y:100 | 400 | 900 |
| 右パネル | x:1470, y:100 | 400 | 900 |
| 上部バー | x:0, y:0 | 1920 | 100 |
| 下部バー | x:0, y:980 | 1920 | 100 |

---

## 🛠️ テンプレート作成のステップ

### 1. テンプレートファイル作成

```bash
# JSON ファイルを作成
nano templates/my_template.json
```

### 2. JSON 構造を記述

基本的なテンプレートから開始

### 3. アプリで確認

```bash
# アプリを再起動
python main.py
# または
open "dist/ATEM Media Generator.app"
```

### 4. パラメータをテスト

- テンプレートを選択
- パラメータを入力
- プレビューを確認

### 5. 微調整

- x, y 座標を微調整
- フォント名・サイズを変更
- 色を修正

---

## 🎨 色選択ガイド

### RGBA カラー値

RGB + Alpha チャンネルで色を指定：

```
[Red, Green, Blue, Alpha]
各値: 0-255

完全不透明: Alpha = 255
半透明: Alpha = 128
透明: Alpha = 0
```

### よく使う色

```json
{
  "白": [255, 255, 255, 255],
  "黒": [0, 0, 0, 255],
  "赤": [255, 0, 0, 255],
  "青": [0, 0, 255, 255],
  "緑": [0, 255, 0, 255],
  "黄": [255, 255, 0, 255],
  "シアン": [0, 255, 255, 255],
  "マゼンタ": [255, 0, 255, 255],
  "グレー": [128, 128, 128, 255],
  "濃いグレー": [64, 64, 64, 255],
  "薄いグレー": [200, 200, 200, 255]
}
```

---

## ✅ テンプレート検証

テンプレートが正しいか確認：

```bash
# Python スクリプトから検証
python -c "
from template_manager import TemplateManager
manager = TemplateManager()
success, error = manager.validate_template_file('templates/my_template.json')
print(f'Valid: {success}')
if not success:
    print(f'Error: {error}')
"
```

---

## 💡 トラブルシューティング

### フォントが見つからない

**症状**: デフォルトフォントで表示される

**解決**:
- フォント名がシステムに存在するか確認
- macOS: `Font Book.app` で確認可能
- フォント名は正確に記入（大文字小文字区別）

### テキストが表示されない

**症状**: テンプレートは読み込まれるが、テキストが表示されない

**解決**:
- `parameter_key` が CSV パラメータと一致するか確認
- テキスト色が背景色と同じでないか確認
- x, y 座標が画面内にあるか確認

### テキストが重なる

**症状**: 複数のテキストレイヤーが重複

**解決**:
- y 座標と height を調整して、間隔を作る
- layer の順序を確認

---

## 📦 テンプレート配布

独自テンプレートを他者と共有：

1. テンプレート JSON をアップロード
2. ドキュメントに使用方法を記載
3. サンプル CSV を用意

---

## 参考リンク

- [メインガイド](README.md)
- [リリースガイド](RELEASE_GUIDE.md)

---

**Happy Template Creating! 🎨**
