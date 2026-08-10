# SNS・動画戦略 共通ナビ反映メモ

## 反映済み
- medical-sns.html: PC/スマホの共通ナビにSNS・動画戦略を追加し、当該ページをcurrent表示
- tsuyoshi-hadano.html: PC/スマホの共通ナビを追加し、SNS・動画戦略への導線を維持

## 次の反映対象
- index.html
- self-pay.html
- lhub.html
- lhub-lp.html（ヘッダーがある場合）

## 方針
- PC: SNS・動画戦略を主要サービスとして直接リンク
- スマホ: 2列または既存レイアウト内で文字被り・横スクロールを起こさない
- medical-sns.html では aria-current="page"
- 既存の自費診療、LHub、記事、代表、無料相談導線を削除しない
