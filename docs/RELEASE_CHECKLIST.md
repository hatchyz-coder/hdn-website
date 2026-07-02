# リリース前チェックリスト

GitHub Pagesまたは本番HPへ反映する前に確認する項目です。

## 表示確認

- トップページが表示される
- 自費診療導入支援ページが表示される
- LHub専用ページが表示される
- 無料相談ページが表示される
- ロゴが表示される
- ハッチのプロフィール写真が表示される
- イメージイラストが表示される
- スマホ幅で文字やカードが崩れない

## 文面確認

- HDN主語になっている
- ROOTSが公開文面の主語になっていない
- 制作側メモが混ざっていない
- 「実名掲載が難しい」「仮で」「とりあえず」などの内部表現がない
- 医療広告、薬機法、景表法に配慮が必要な断定表現がない
- CTAが無料相談または患者導線診断へ向いている

## 導線確認

- ナビゲーションのリンクが動く
- トップから自費導入ページへ移動できる
- トップからLHubページへ移動できる
- 各ページから無料相談ページへ移動できる
- 外部問い合わせリンクが意図したURLになっている

## GitHub反映前

```bash
./scripts/verify-site.sh
./scripts/build-pages.sh
git status --short
```

## コミット時の目安

コミットメッセージ例:

```text
Update HDN website copy and pages
Add LHub dedicated page
Add self-pay care support page
Improve pricing section
```
