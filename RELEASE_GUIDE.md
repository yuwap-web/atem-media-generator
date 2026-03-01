# ATEM Media File Generator - リリースガイド

## 概要

このドキュメントは、ATEM Media File Generator の開発・ビルド・リリースプロセスの完全なガイドです。

---

## 📋 バージョン情報

| 項目 | 値 |
|------|-----|
| **現在のバージョン** | v1.0.0 |
| **リリース日** | 2026-03-01 |
| **ステータス** | ✅ 本番環境対応完備 |
| **プラットフォーム** | macOS 10.13+, Windows 7+ |
| **Python版** | 3.9+ |

---

## 🏗️ ビルドプロセス

### macOS ビルド（ローカル）

```bash
cd /Users/uts/dev_atem/mediafile

# 1. 仮想環境設定（初回のみ）
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. .app バンドルビルド
bash build-mac.sh

# 出力: dist/ATEM Media Generator.app
# サイズ: バイナリ 2.0MB、フルバンドル 28MB

# 3. GitHub Release 用 .zip 作成
ditto -c -k --sequesterRsrc dist/ATEM\ Media\ Generator.app ATEM-Media-Generator-mac.zip
```

**出力ファイル:**
- `dist/ATEM Media Generator.app/` - 本体アプリケーション
- `ATEM-Media-Generator-mac.zip` - 配布用アーカイブ (28MB)

**実行方法:**
```bash
open "ATEM Media Generator.app"
# または
"ATEM Media Generator.app/Contents/MacOS/ATEM Media Generator"
```

### Windows ビルド（Windows マシンが必要）

```powershell
cd C:\path\to\mediafile

# 1. 仮想環境設定（初回のみ）
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. EXE ビルド
.\build-windows.ps1

# 出力: dist\ATEM-Media-Generator\ATEM-Media-Generator.exe
# サイズ: ~50MB

# 3. GitHub Release 用 .zip 作成
powershell Compress-Archive -Path 'dist\ATEM-Media-Generator' -DestinationPath 'ATEM-Media-Generator-windows.zip'
```

**出力ファイル:**
- `dist\ATEM-Media-Generator\` - 本体フォルダ
- `ATEM-Media-Generator-windows.zip` - 配布用アーカイブ (50-60MB)

**実行方法:**
```
ATEM-Media-Generator.exe をダブルクリック
または: .\ATEM-Media-Generator\ATEM-Media-Generator.exe
```

---

## 🤖 GitHub Actions CI/CD

### 自動ビルドの仕組み

プロジェクトは **GitHub Actions** により自動ビルドされます：

| トリガー | macOS | Windows |
|---------|-------|---------|
| main/master ブランチ push | ✅ ビルド | ✅ ビルド |
| タグ作成 (v*.*.*)  | ✅ ビルド + Release | ✅ ビルド + Release |
| 手動トリガー | ✅ 可能 | ✅ 可能 |

### 自動ビルドファイル

```
.github/workflows/
├── build-mac.yml      - macOS ビルド設定
└── build-windows.yml  - Windows ビルド設定
```

---

## 📦 リリースプロセス

### 1. 新しいバージョンをリリース

```bash
cd /Users/uts/dev_atem/mediafile

# 1. 変更をコミット
git add -A
git commit -m "Release v1.1.0 - Add new features"

# 2. タグ作成（形式: v{major}.{minor}.{patch}）
git tag v1.1.0 -a -m "Release v1.1.0 - Description"

# 3. リモートにプッシュ
git push origin master
git push origin v1.1.0
```

### 2. GitHub Actions が自動ビルド

タグプッシュ後、GitHub Actions が自動的に：
- ✅ macOS .app バンドル生成
- ✅ Windows EXE 生成
- ✅ .zip アーカイブ作成
- ✅ GitHub Release に自動アップロード

### 3. GitHub Release 確認

ブラウザで確認：
```
https://github.com/kusurix-ux/Atem-picture-tool/releases/tag/v1.1.0
```

以下のファイルが表示されます：
- `ATEM-Media-Generator-mac.zip`
- `ATEM-Media-Generator-windows.zip`

---

## 🔄 一般的なリリース手順

### シナリオ: v1.1.0 をリリースする

```bash
# 1. 変更実装
# （main.py, feature_module.py など編集）

# 2. テスト実行（すべてパスすることを確認）
python test_integration.py

# 3. README や CHANGELOG を更新
vim README.md

# 4. コミット
git add -A
git commit -m "Feature: Add template import UI

- Add import dialog for custom templates
- Improve template validation
- Fix font loading on Windows

Version bump: v1.0.0 → v1.1.0"

# 5. タグ作成
git tag v1.1.0 -a -m "Release v1.1.0

New Features:
- Template import UI
- Improved validation
- Font loading fix

All 57 tests passing ✓"

# 6. プッシュ（自動ビルド開始）
git push origin master
git push origin v1.1.0

# 7. GitHub Release ページで確認
# https://github.com/kusurix-ux/Atem-picture-tool/releases
```

---

## 📝 ローカルテスト（リリース前）

```bash
# 1. コード品質テスト
python test_phase2.py        # 画像生成テスト
python test_gui.py           # GUI テスト
python test_csv.py           # CSV テスト
python test_integration.py   # 統合テスト

# 2. ローカルビルドテスト
bash build-mac.sh            # macOS ビルド
open "dist/ATEM Media Generator.app"  # 実行確認

# 3. すべてのテストが パス することを確認
# ✅ 57/57 tests PASSED
```

---

## 🐛 問題解決

### macOS ビルド時の問題

**問題: Qt framework symlink エラー**
```
error: symlink to Qt framework failed
```

**解決:**
- `build-mac.sh` は既に `--hidden-import` を使用して最適化されています
- `--collect-all PyQt5` は使用していません

### Windows ビルド時の問題

**問題: PyInstaller が見つからない**
```
error: command 'PyInstaller' not found
```

**解決:**
```powershell
pip install pyinstaller
```

### GitHub Actions エラー

**確認事項:**
1. `.github/workflows/` ディレクトリが存在
2. `build-mac.yml` と `build-windows.yml` が存在
3. リポジトリが public（Actions が実行可能）
4. タグ形式が `v*.*.* ` （例: v1.0.0）

---

## 📊 リリース統計

### v1.0.0 リリース

| 項目 | 数値 |
|------|------|
| 実装期間 | ~2.5 時間 |
| Python コード | 1,954 行 |
| テストスイート | 57 テスト |
| テスト成功率 | 100% ✓ |
| macOS .app サイズ | 28 MB |
| Windows EXE サイズ | 50-60 MB |
| ドキュメント | 450+ 行 |
| Git コミット数 | 7 |

---

## 🎯 次期リリース計画

### v1.1.0（計画中）
- [ ] テンプレートインポート UI
- [ ] ATEM REST API 統合（オプション）
- [ ] 画像プレビュー拡大機能
- [ ] ドラッグ&ドロップ対応

### v2.0.0（長期）
- [ ] Web UI オプション
- [ ] モーショングラフィックス対応
- [ ] テンプレートマーケットプレイス
- [ ] クラウド同期機能

---

## 📚 関連リソース

- **GitHub リポジトリ**: https://github.com/kusurix-ux/Atem-picture-tool
- **Issues**: https://github.com/kusurix-ux/Atem-picture-tool/issues
- **Releases**: https://github.com/kusurix-ux/Atem-picture-tool/releases
- **Wiki**: https://github.com/kusurix-ux/Atem-picture-tool/wiki

---

## 📞 サポート

質問や問題がある場合：
1. **GitHub Issues**: https://github.com/kusurix-ux/Atem-picture-tool/issues
2. **GitHub Discussions**: https://github.com/kusurix-ux/Atem-picture-tool/discussions
3. **ドキュメント**: README.md を参照

---

**最終更新**: 2026-03-01
**ステータス**: ✅ 本番環境対応完備
