# Template Customizer ガイド

## 概要

テンプレートカスタマイザーは、アプリケーション内からテンプレート属性（フォント、フォントサイズ、色、テキスト配置）をリアルタイムで変更できる機能です。JSONファイルを編集することなく、テキストレイヤーの見た目をカスタマイズできます。

**導入背景**: ユーザーは、テンプレートを固定レイアウトとして扱いつつ、実行時にテキスト属性（サイズ、色、フォント）を柔軟に変更したいという要望がありました。

---

## 主な機能

### 1. フォント選択
- **デフォルトフォント**: Helvetica、Arial、Menlo、Courier New など
- **日本語フォント**: ヒラギノ角ゴシック、ヒラギノゴシック、Arial Unicode
- プルダウンメニューから選択可能

### 2. フォントサイズ変更
- スピンボックスで 8px から 200px まで調整可能
- リアルタイムプレビューで変更内容を確認

### 3. テキスト配置
- `left` （左揃え）
- `center` （中央揃え）
- `right` （右揃え）

### 4. テキスト色
- カラーピッカーダイアログで RGBA カラーを選択
- プレビューボタンに現在の色を表示

---

## 使用方法

### ステップ 1: テンプレートを選択
左パネルから編集したいテンプレートをクリックします。

### ステップ 2: テキストレイヤーを編集
中央パネルの下部「Template Customizer」セクションに、テンプレートのすべてのテキストレイヤーが表示されます。

各レイヤーについて以下の属性を変更できます：
- **Font**: フォント名を選択
- **Size**: フォントサイズ（ピクセル）
- **Alignment**: テキスト配置（左/中央/右）
- **Color**: テキスト色をカラーピッカーで選択

### ステップ 3: 変更をプレビュー
属性を変更すると、右パネルのプレビューが自動的に更新されます。

### ステップ 4: 変更を適用またはリセット
- **Apply Changes**: 変更をテンプレートに確定
- **Reset to Original**: 変更を破棄して元の値に戻す

---

## 日本語フォント対応

### 対応フォント

#### macOS（標準搭載）
- **ヒラギノ角ゴシック** (Hiragino Sans)
  - W4～W9 の複数ウェイト対応
  - 見出しや本文に最適

- **ヒラギノゴシック** (Hiragino Sans Serif)
  - W4～W8 の複数ウェイト対応
  - 標準的な日本語フォント

#### Windows
- **メイリオ** (Meiryo)
  - 日本語フォントの標準
  - `C:\Windows\Fonts\meiryo.ttc`

- **MS 明朝** (MS Mincho)
  - 明朝体
  - `C:\Windows\Fonts\msmincho.ttc`

#### Linux
- **Noto Sans CJK**
  - オープンソース日本語フォント
  - `/usr/share/fonts/opentype/noto/`

---

## サンプルテンプレート（日本語）

### タイトルテンプレート: `title_japanese.json`
```json
{
  "name": "タイトル - 日本語",
  "template_type": "title",
  "background_color": [30, 30, 40, 255],
  "layers": [
    {
      "name": "メインタイトル",
      "x": 100,
      "y": 350,
      "width": 1720,
      "height": 250,
      "font_name": "ヒラギノ角ゴシック",
      "font_size": 72,
      "color": [255, 200, 100, 255],
      "alignment": "center",
      "parameter_key": "title"
    },
    {
      "name": "サブタイトル",
      "x": 100,
      "y": 650,
      "width": 1720,
      "height": 100,
      "font_name": "ヒラギノゴシック",
      "font_size": 40,
      "color": [180, 180, 200, 255],
      "alignment": "center",
      "parameter_key": "subtitle"
    }
  ],
  "required_parameters": ["title"],
  "optional_parameters": ["subtitle"]
}
```

### ロワーサード: `lower_third_japanese.json`
```json
{
  "name": "ロワーサード - 日本語",
  "template_type": "lower_third",
  "background_color": [0, 0, 0, 0],
  "layers": [
    {
      "name": "名前",
      "x": 80,
      "y": 930,
      "width": 800,
      "height": 60,
      "font_name": "ヒラギノ角ゴシック",
      "font_size": 48,
      "color": [255, 255, 255, 255],
      "alignment": "left",
      "parameter_key": "name"
    },
    {
      "name": "肩書き",
      "x": 80,
      "y": 1000,
      "width": 800,
      "height": 50,
      "font_name": "ヒラギノゴシック",
      "font_size": 32,
      "color": [220, 220, 220, 255],
      "alignment": "left",
      "parameter_key": "title"
    }
  ],
  "required_parameters": ["name"],
  "optional_parameters": ["title"]
}
```

---

## カスタムテンプレート作成ガイド

### ステップ 1: JSON ファイルを作成
`templates/` ディレクトリに `.json` ファイルを作成します。

### ステップ 2: テンプレート構造を定義
```json
{
  "name": "マイテンプレート",
  "template_type": "title",
  "background_color": [0, 0, 0, 255],
  "layers": [
    {
      "name": "メインテキスト",
      "x": 100,
      "y": 400,
      "width": 1720,
      "height": 200,
      "font_name": "ヒラギノ角ゴシック",
      "font_size": 72,
      "color": [255, 255, 255, 255],
      "alignment": "center",
      "parameter_key": "title"
    }
  ],
  "required_parameters": ["title"],
  "optional_parameters": []
}
```

### ステップ 3: アプリを再起動
```bash
python main.py
```

### ステップ 4: テンプレートカスタマイザーで調整
テンプレートをロードし、カスタマイザーパネルで属性を変更します。

---

## トラブルシューティング

### 日本語フォントが表示されない

**症状**: フォントを「ヒラギノ角ゴシック」に変更しても、テキストが表示されない

**解決策**:
1. **macOS**: Font Book.app を開いて、「ヒラギノ角ゴシック」がインストールされているか確認
2. **Windows**: `C:\Windows\Fonts\` に `meiryo.ttc` が存在するか確認
3. **フォント名**: テンプレートのフォント名がドロップダウンリストと完全に一致しているか確認

### テキストが重なる

**症状**: 複数のテキストレイヤーが重複して表示される

**解決策**:
1. テンプレートの JSON ファイルで、各レイヤーの `y` 座標と `height` を調整
2. レイヤー間の間隔を広げる
3. 例:
   ```json
   "y": 400,
   "height": 200
   // 次のレイヤーは y: 650 以上にする
   ```

### カスタマイザーの変更が反映されない

**症状**: テキスト色やサイズを変更しても、プレビューが更新されない

**解決策**:
1. パラメータ入力フィールドに値が入っているか確認
2. 「Apply Changes」ボタンをクリック
3. アプリを再起動して、キャッシュをクリア

---

## 高度な使用例

### 複数レイヤーの同期編集

テンプレートに複数のテキストレイヤーがある場合、各レイヤーを独立して編集できます。

例：ロワーサードの場合
- **名前レイヤー**: Hiragino Sans、48px、white
- **肩書きレイヤー**: Hiragino Sans Serif、32px、light gray

カスタマイザーで名前レイヤーのフォントサイズを 60px に変更すると、肩書きレイヤーは変わらず、プレビューでレイアウトが自動調整されます。

### テンプレート組み合わせ戦略

複数のテンプレート + カスタマイザーを活用：
1. 基本テンプレートを複数用意（日本語、英語など）
2. 必要に応じてカスタマイザーで見た目を調整
3. 一度設定したら、CSV 一括処理で複数の画像を生成

---

## 参考リンク

- [メインガイド](README.md)
- [テンプレート作成ガイド](TEMPLATE_GUIDE.md)
- [リリースガイド](RELEASE_GUIDE.md)

---

**Happy Customizing! 🎨**
