# GitHub 実装・公開手順

このサイトは、GitHubでソース管理し、GitHub Pagesでプレビュー公開できる構成にしています。

## 現在できていること

- ローカルGitリポジトリ化済み
- `main` ブランチ作成済み
- 初回コミット作成済み
- GitHub Pages用ワークフロー作成済み
- 公開用ビルドスクリプト作成済み
- サイト検証スクリプト作成済み

## 推奨リポジトリ名

```text
hdn-website
```

または、公開前の試作であることを明確にするなら、

```text
hdn-site-prototype
```

## GitHub側で先に行うこと

1. GitHubで新規リポジトリを作成する
2. Repository name は `hdn-website` などにする
3. README、.gitignore、License は追加しない
4. 作成後に表示される remote URL を控える

例:

```text
https://github.com/<owner>/hdn-website.git
```

## ローカルからGitHubへ接続する

GitHub上の空リポジトリを作成した後、下記を実行します。

```bash
cd hdn-site-prototype
./scripts/connect-github.sh https://github.com/<owner>/hdn-website.git
```

このスクリプトは、次を行います。

- サイト検証
- GitHub Pages用ビルド
- `origin` リモート追加または更新
- `main` ブランチをGitHubへpush

## GitHub Pages設定

GitHubへpushした後、GitHubの管理画面で下記を設定します。

```text
Settings > Pages > Build and deployment > Source > GitHub Actions
```

その後、`main` ブランチへpushされるたびに、`.github/workflows/deploy-pages.yml` が動き、GitHub Pagesへ公開されます。

## 本番反映前の考え方

最初はGitHub Pagesを「確認用URL」として使うのが安全です。

本番の `hdnjapan.com` へ反映する方法は、次のいずれかです。

1. WordPressへ移植する
2. 静的HTMLサイトとしてホスティングする
3. GitHub Pagesまたは別ホスティングを本番・サブドメインに接続する

現時点では、まずGitHub Pagesで確認URLを作り、内容・画像・スマホ表示・問い合わせ導線を確認してから本番反映するのが現実的です。

## 更新運用

日常的な更新は次の流れです。

1. チャッピーで修正意図、訴求、文面を整理する
2. CodexでHTML/CSS、画像、リンク、CTAを修正する
3. `./scripts/verify-site.sh` を実行する
4. 問題なければcommitする
5. `git push origin main` でGitHubへ反映する
6. GitHub Pagesの確認URLで表示を確認する
