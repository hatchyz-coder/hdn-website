# HDN Website

株式会社HDNのコーポレートサイト試作プロジェクトです。

このリポジトリは、チャッピーで訴求・構成・文面を整理し、CodexでHTML/CSS、画像差し替え、ページ追加、GitHub管理、公開準備を行う前提で運用します。

## Pages

- `index.html`：HDNトップページ
- `self-pay.html`：自費診療導入支援ページ
- `lhub.html`：LHub専用ページ
- `consultation.html`：無料相談・患者導線診断ページ

## Assets

- `assets/hdn-logo.png`：サイト表示用HDNロゴ
- `assets/hadano-profile.jpg`：代表プロフィール写真
- `assets/illustration-patient-assets.jpg`：患者基盤活用イメージ
- `assets/illustration-lhub-crm.jpg`：LHub/患者CRMイメージ
- `assets/illustration-consultation.jpg`：無料相談・患者導線診断イメージ
- `assets/pricing-reference.png`：料金表参考画像

## Local Preview

```bash
cd hdn-site-prototype
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/
```

## Build For GitHub Pages

```bash
./scripts/build-pages.sh
```

This creates `_site/` with only public files:

- HTML files
- `assets/`
- `.nojekyll`

Operational documents such as `AGENTS.md` and `HDN_SITE_EDITING_GUIDE.md` are kept in the repository but are not copied into `_site/`.

## Verify

```bash
./scripts/verify-site.sh
```

This checks:

- required HTML files exist
- referenced image assets exist
- internal-facing NG phrases are not present in public HTML

## GitHub Pages

This project includes `.github/workflows/deploy-pages.yml`.

When pushed to the `main` branch, GitHub Actions builds `_site/` and deploys it to GitHub Pages.

Before the first deployment, set the repository's Pages source to **GitHub Actions** in GitHub:

```text
Settings > Pages > Build and deployment > Source > GitHub Actions
```

For the full GitHub setup flow, see:

- `docs/GITHUB_IMPLEMENTATION.md`
- `docs/RELEASE_CHECKLIST.md`

## Editing Rule

Before changing public copy, read:

- `AGENTS.md`
- `HDN_SITE_EDITING_GUIDE.md`

Important rules:

- Public copy must be written from HDN's point of view.
- Do not expose production notes or internal draft logic.
- ROOTS may be used as a reference, but do not make ROOTS the public subject.
- HDN's value is patient journey design, LHub, self-pay care, CRM, operations, and continuous website improvement.
