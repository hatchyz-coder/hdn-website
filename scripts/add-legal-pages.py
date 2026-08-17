from __future__ import annotations

import re
from pathlib import Path

SITE = Path("_site")
COMPANY = "株式会社HDN"
REPRESENTATIVE = "代表取締役 羽田野 剛士"
ADDRESS = "〒103-0027 東京都中央区日本橋3丁目2番14号 日本橋KNビル4F"
CONTACT_URL = "https://forms.gle/148jgfSnDgDZ2HsEA"
UPDATED = "2026年8月17日"

JP_PAGES = {
    "privacy.html": (
        "プライバシーポリシー・個人情報保護方針",
        "privacy",
        """
<section id="privacy"><h2>個人情報保護方針</h2>
<p>株式会社HDN（以下「当社」といいます。）は、医療機関向けコンサルティング、自由診療導入支援、LHub導入・運用支援、患者CRM・予約・問診・決済導線設計、広告表現確認その他の事業を行うにあたり、個人情報および個人データの重要性を認識し、個人情報の保護に関する法律その他の関係法令・ガイドラインを遵守し、適切な取得、利用、管理および保護に努めます。</p>
<ul>
<li>利用目的をできる限り特定し、その目的の達成に必要な範囲で個人情報を取り扱います。</li>
<li>不正な手段による取得を行わず、法令上必要な場合には利用目的の通知・公表または同意取得を行います。</li>
<li>個人データへの不正アクセス、漏えい、滅失、毀損等を防止するため、必要かつ適切な安全管理措置を講じます。</li>
<li>委託先に個人データの取扱いを委託する場合、必要かつ適切な監督を行います。</li>
<li>本人からの開示、訂正、利用停止等の請求に、法令に従い適切に対応します。</li>
<li>個人情報保護に関する管理体制を継続的に見直し、改善します。</li>
</ul></section>
<section><h2>1. 事業者情報</h2><dl><dt>名称</dt><dd>株式会社HDN</dd><dt>住所</dt><dd>〒103-0027 東京都中央区日本橋3丁目2番14号 日本橋KNビル4F</dd><dt>代表者</dt><dd>代表取締役 羽田野 剛士</dd></dl></section>
<section><h2>2. 取得する情報</h2><p>当社は、事業および本サイトの運営に必要な範囲で、氏名、会社・医療機関名、所属・役職、住所、電話番号、メールアドレス、相談・問い合わせ内容、契約・取引情報、請求・支払に関する情報、セミナー等への申込情報、本サイトの閲覧・利用情報その他本人から提供された情報を取得することがあります。</p><p>また、医療機関その他の取引先から委託を受け、患者情報等の個人データを取り扱う場合があります。その場合、当社は委託された業務の範囲および委託元の指示・契約に従って取り扱います。要配慮個人情報を取り扱う場合には、個人情報保護法その他の関係法令に従います。</p></section>
<section><h2>3. 利用目的</h2><ul><li>問い合わせ、相談、資料請求等への対応</li><li>サービスの提案、契約手続、本人・担当者確認、連絡、提供、保守、運用支援およびアフターサポート</li><li>医療機関向けコンサルティング、自由診療導入支援、LHubその他の業務設計・システム導入支援の実施</li><li>請求、決済、入金確認、会計・税務その他の取引管理</li><li>セミナー、イベント、記事、サービス情報等の案内（法令上必要な同意・手続を含む）</li><li>サービス・ウェブサイトの利用状況の把握、品質改善、新サービスの企画・開発</li><li>不正利用、セキュリティ事故、トラブル等の防止・調査・対応</li><li>法令、行政機関・裁判所等の命令その他の法的義務への対応</li><li>上記目的に付随する業務</li></ul></section>
<section><h2>4. 第三者提供</h2><p>当社は、本人の同意がある場合、法令に基づく場合その他個人情報保護法で認められる場合を除き、個人データを第三者に提供しません。共同利用を行う場合には、法令に従い必要事項をあらかじめ公表または本人が容易に知り得る状態に置きます。</p></section>
<section><h2>5. 委託・外部サービスの利用</h2><p>当社は、システム運用、クラウド、フォーム、アクセス解析、メール、決済、会計その他の業務の全部または一部を外部事業者に委託することがあります。委託に伴い必要な範囲で個人データを提供する場合、委託先の選定、契約、アクセス制御その他必要かつ適切な監督を行います。国外に所在する事業者のサービスを利用する場合には、適用法令を踏まえて必要な対応を行います。</p></section>
<section><h2>6. 安全管理措置</h2><p>当社は、個人データの取扱いに関する責任体制・規程等の整備、取扱状況の確認、従業者への教育、アクセス権限の管理、認証・ログ管理、機器・媒体の管理、漏えい等の防止、委託先管理等の安全管理措置を、事業規模・取扱情報・リスクに応じて実施します。安全管理措置の具体的内容については、法令上開示が必要な範囲で、本人からの求めに応じて回答します。</p></section>
<section><h2>7. 保有個人データの開示等</h2><p>本人は、法令に定める範囲で、利用目的の通知、保有個人データまたは第三者提供記録の開示、訂正・追加・削除、利用停止・消去、第三者提供の停止等を請求できます。請求を希望する場合は、下記窓口からご連絡ください。本人確認および請求内容の確認後、法令に従って対応します。法令上、請求に応じないことが認められる場合には、その旨を説明します。</p></section>
<section><h2>8. Cookie・アクセス解析</h2><p>本サイトでは、利便性向上、利用状況の把握、品質改善等のためCookieその他の類似技術およびアクセス解析サービスを利用することがあります。詳細は<a href="cookie-policy.html">Cookie・アクセス解析方針</a>をご確認ください。</p></section>
<section><h2>9. お問い合わせ窓口</h2><p>個人情報の取扱い、開示等の請求その他本方針に関するお問い合わせは、<a href="https://forms.gle/148jgfSnDgDZ2HsEA" target="_blank" rel="noopener noreferrer">HDNお問い合わせフォーム</a>からご連絡ください。</p></section>
<section><h2>10. 改定</h2><p>当社は、法令、サービス内容、個人情報の取扱状況等の変更に応じ、本方針を改定することがあります。重要な変更がある場合は、本サイト上で分かりやすい方法により告知します。</p></section>
""",
    ),
    "terms.html": (
        "サイト利用規約",
        "terms",
        """
<section><h2>1. 適用</h2><p>本規約は、株式会社HDN（以下「当社」といいます。）が運営するウェブサイト「hdnjapan.com」および当社が本サイト上で提供する情報・コンテンツの利用条件を定めるものです。本サイトを利用した場合、本規約に同意したものとみなされます。</p></section>
<section><h2>2. 個別契約との関係</h2><p>当社のコンサルティング、LHubその他の有料サービスについて個別契約、申込書、利用規約等が別途存在する場合、その内容が本規約に優先します。本サイトの閲覧のみをもって有料サービスの契約が成立するものではありません。</p></section>
<section><h2>3. 掲載情報の位置付け</h2><p>本サイトおよびHDNの記事・コラムに掲載する情報は、一般的な情報提供を目的とするものです。医療上の診断・治療、法律上の助言、税務・会計上の助言、個別案件についての適法性保証その他の専門家による個別判断を提供するものではありません。必要に応じて医師、弁護士、税理士その他の専門家へご確認ください。</p></section>
<section><h2>4. 知的財産権</h2><p>本サイトに掲載する文章、画像、ロゴ、デザイン、資料、プログラムその他のコンテンツに関する著作権、商標権その他の知的財産権は、当社または正当な権利者に帰属します。法令で認められる場合を除き、権利者の許可なく複製、転載、改変、販売、再配布等を行うことはできません。</p></section>
<section><h2>5. 禁止事項</h2><ul><li>法令または公序良俗に反する行為</li><li>当社または第三者の権利・利益・信用を侵害する行為</li><li>不正アクセス、脆弱性探索、過度な負荷その他本サイトの運営を妨害する行為</li><li>本サイトのコンテンツを、事実と異なる形で当社の推奨・保証・提携等を示すために利用する行為</li><li>その他当社が不適切と合理的に判断する行為</li></ul></section>
<section><h2>6. 外部サイト・外部サービス</h2><p>本サイトには第三者が運営するサイト、フォーム、SNSその他の外部サービスへのリンクが含まれる場合があります。外部サービスの内容、可用性、セキュリティ、個人情報の取扱い等は各提供者の規約・方針に従います。</p></section>
<section><h2>7. サイトの変更・中断</h2><p>当社は、保守、障害、セキュリティ対応、事業上の必要その他合理的な理由により、本サイトの内容を変更し、または提供を一時中断・終了することがあります。</p></section>
<section><h2>8. 免責</h2><p>当社は、掲載情報の正確性・完全性・最新性の確保に努めますが、将来にわたりこれらを保証するものではありません。本サイトの利用により生じた損害については、当社に故意または重過失がある場合その他法令上責任を免れることができない場合を除き、法令で認められる範囲で責任を負いません。詳細は<a href="disclaimer.html">免責事項</a>をご確認ください。</p></section>
<section><h2>9. 規約の変更</h2><p>当社は、法令の変更、サービス内容の変更その他合理的な必要がある場合、本規約を変更することがあります。変更後の規約は本サイトに掲載した時点または別途定める効力発生日から適用します。</p></section>
<section><h2>10. 準拠法・管轄</h2><p>本規約は日本法に準拠します。本サイトの利用に関して当社と利用者との間で紛争が生じた場合、法令に別段の定めがある場合を除き、東京地方裁判所を第一審の専属的合意管轄裁判所とします。</p></section>
""",
    ),
    "cookie-policy.html": (
        "Cookie・アクセス解析方針",
        "cookies",
        """
<section><h2>1. Cookie等の利用</h2><p>本サイトでは、サイトの安定運用、利用状況の把握、利便性・コンテンツ・導線の改善等のため、Cookie、ローカルストレージ、ピクセルその他これらに類する技術を利用することがあります。</p></section>
<section><h2>2. Google Analytics等</h2><p>本サイトでは、Google LLCが提供するGoogle Analytics 4等のアクセス解析サービスを利用することがあります。これらのサービスでは、閲覧したページ、参照元、利用日時、端末・ブラウザに関する情報、サイト上の操作イベント等が収集される場合があります。解析結果は、サイトの利用状況の把握および改善のために利用します。</p><p>アクセス解析サービスによる情報の取扱いは、各提供事業者の利用規約・プライバシーポリシー等に従います。当社は、アクセス解析のために取得する情報のみから、閲覧者の氏名等を特定することを目的としていません。</p></section>
<section><h2>3. 外部フォーム・SNS等</h2><p>本サイトからGoogle Forms、SNSその他の外部サービスへ遷移する場合、遷移先でCookie等が利用されることがあります。外部サービスでの情報の取扱いは各提供者の規約・方針をご確認ください。</p></section>
<section><h2>4. Cookieの管理</h2><p>利用者は、ブラウザの設定によりCookieを削除または無効化できます。ただし、Cookie等を無効化した場合、本サイトまたは外部サービスの一部機能が正常に動作しないことがあります。Google Analyticsについては、Googleが提供するオプトアウト手段を利用できる場合があります。</p></section>
<section><h2>5. 本方針の変更</h2><p>利用する技術・サービスの変更や法令改正等に応じ、本方針を改定することがあります。</p></section>
""",
    ),
    "security.html": (
        "情報セキュリティ基本方針",
        "security",
        """
<section><h2>基本方針</h2><p>株式会社HDNは、医療・ヘルスケア領域を含む事業において取り扱う情報資産の重要性を認識し、機密性、完全性および可用性を適切に確保するため、事業規模、取扱情報およびリスクに応じた情報セキュリティ対策に取り組みます。</p></section>
<section><h2>1. 管理体制</h2><p>情報セキュリティに関する責任と権限を明確にし、必要な規程・手順を整備するとともに、定期的な見直しを行います。</p></section>
<section><h2>2. アクセス管理</h2><p>業務上必要な者にアクセス権限を限定し、認証、権限管理、ログ管理その他必要な技術的措置を行います。</p></section>
<section><h2>3. 人的・物理的安全管理</h2><p>従業者・関係者への教育・周知を行い、端末、媒体、文書等について紛失、盗難、無断持出し等のリスクに応じた管理を実施します。</p></section>
<section><h2>4. 委託先・クラウドサービス管理</h2><p>外部委託先やクラウドサービスを利用する場合、取扱情報の重要度に応じて提供者の安全管理状況、契約条件、アクセス範囲等を確認し、必要な監督を行います。</p></section>
<section><h2>5. インシデント対応</h2><p>情報セキュリティ事故またはその疑いを把握した場合、影響の確認、封じ込め、原因調査、再発防止、関係者・関係機関への連絡その他法令・契約に応じた対応を行います。</p></section>
<section><h2>6. 継続的改善</h2><p>法令、技術、脅威、事業内容の変化を踏まえ、情報セキュリティ対策を継続的に改善します。</p></section>
""",
    ),
    "disclaimer.html": (
        "免責事項",
        "disclaimer",
        """
<section><h2>1. 一般情報としての掲載</h2><p>本サイトおよびHDNの記事・コラムの内容は、公開時点で確認可能な情報および当社の実務上の知見に基づく一般的な情報提供です。個別の医療行為、法的判断、税務・会計判断、投資判断その他の専門的判断を代替するものではありません。</p></section>
<section><h2>2. 医療・広告・制度情報</h2><p>医療制度、医療広告、薬機法、景品表示法、健康増進法、個人情報保護その他の制度・ガイドラインは改正・更新されることがあります。当社は情報の更新に努めますが、掲載内容が常に最新の法令・行政解釈・個別事情に適合することを保証するものではありません。具体的な案件では、最新の一次情報および必要に応じて専門家の確認を行ってください。</p></section>
<section><h2>3. 支援例・試算・数値</h2><p>本サイトに掲載する支援例、売上・費用等の試算、シミュレーション、参考数値は、特記がない限り特定条件下の例または参考情報です。同様の成果、売上、集客数、費用対効果等を保証するものではありません。実際の結果は診療科、地域、患者層、価格、運用体制、広告条件その他多数の要因により異なります。</p></section>
<section><h2>4. 外部リンク</h2><p>本サイトからリンクする第三者サイト・サービスについて、当社はその内容、利用可能性、セキュリティ、取引条件等を保証しません。利用者自身の判断と責任でご利用ください。</p></section>
<section><h2>5. サービス提供との区別</h2><p>本サイト上の情報閲覧のみでは、当社の有料コンサルティング、LHubその他のサービス契約は成立しません。具体的な提供範囲、責任分担、料金、成果物その他の条件は、個別契約・申込内容等に従います。</p></section>
""",
    ),
}

EN_PAGES = {
    "privacy.html": ("Privacy Policy & Personal Information Protection Policy", "privacy", """
<section><h2>Personal Information Protection Policy</h2><p>HDN Inc. recognizes the importance of personal information in its healthcare consulting, private-care implementation support, LHub implementation and operations support, patient-journey design, advertising review and related businesses. We handle personal information in accordance with Japan's Act on the Protection of Personal Information and other applicable laws and guidelines.</p></section>
<section><h2>Controller information</h2><dl><dt>Company</dt><dd>HDN Inc. (株式会社HDN)</dd><dt>Address</dt><dd>Nihonbashi KN Building 4F, 3-2-14 Nihonbashi, Chuo-ku, Tokyo 103-0027, Japan</dd><dt>Representative</dt><dd>Tsuyoshi Hadano, Representative Director</dd></dl></section>
<section><h2>Information and purposes</h2><p>We may collect contact details, organization and role, inquiry and consultation content, contract and transaction information, billing/payment-related information, seminar or event registrations, website usage information and other information provided to us. We use such information to respond to inquiries; propose, contract, deliver, operate and support services; manage billing and transactions; provide permitted service or event communications; improve websites and services; protect security; comply with law; and perform related business activities.</p><p>Where we process patient or other personal data on behalf of a healthcare institution or business client, we process it within the scope of the entrusted work and applicable instructions, agreements and law.</p></section>
<section><h2>Third parties and processors</h2><p>We do not disclose personal data to third parties without consent except where permitted by applicable law. We may use cloud, forms, analytics, communications, payment, accounting and other service providers and will take appropriate measures for processor selection, contracts, access and oversight. Where overseas services are used, we address applicable legal requirements as appropriate.</p></section>
<section><h2>Security and data-subject requests</h2><p>We take organizational, personnel, physical and technical security measures appropriate to the nature and risks of the data. Subject to applicable law, individuals may request notice of purpose, access, correction, deletion, suspension of use or other rights available under Japanese law. Please contact us through the <a href="https://forms.gle/148jgfSnDgDZ2HsEA" target="_blank" rel="noopener noreferrer">HDN inquiry form</a>.</p></section>
<section><h2>Cookies and updates</h2><p>See our <a href="cookie-policy.html">Cookie & Analytics Policy</a>. We may update this policy as laws, services or data practices change.</p></section>
"""),
    "terms.html": ("Website Terms of Use", "terms", """
<section><h2>Scope</h2><p>These terms apply to hdnjapan.com and the information and content made available by HDN Inc. Separate service agreements, order forms or service-specific terms take precedence for paid consulting, LHub or other services.</p></section>
<section><h2>Information only</h2><p>Website and editorial content is provided for general information. It is not medical diagnosis or treatment advice, legal advice, tax/accounting advice or a guarantee of regulatory compliance for a specific case.</p></section>
<section><h2>Intellectual property and prohibited use</h2><p>Copyrights, trademarks and other rights in website content belong to HDN Inc. or their lawful owners. Unauthorized reproduction, redistribution, modification or use that infringes rights, interferes with site operations, misrepresents HDN endorsement, or violates law is prohibited.</p></section>
<section><h2>External services, changes and liability</h2><p>Third-party links and services are governed by their providers. We may change, suspend or discontinue this website for maintenance, security or business reasons. We seek accuracy and currency but do not guarantee that all content will remain complete or current. Liability is limited to the extent permitted by applicable law.</p></section>
<section><h2>Governing law</h2><p>These terms are governed by the laws of Japan. Except where otherwise required by law, the Tokyo District Court has exclusive jurisdiction as the court of first instance.</p></section>
"""),
    "cookie-policy.html": ("Cookie & Analytics Policy", "cookies", """
<section><h2>Use of cookies and similar technologies</h2><p>We may use cookies, local storage, pixels and similar technologies for stable operation, usage measurement and improvement of website content and user journeys.</p></section>
<section><h2>Analytics</h2><p>We may use Google Analytics 4 and similar analytics services. These services may process page views, referrers, date/time, device/browser information and interaction events. We use aggregated or analytical results to understand and improve the website and do not use analytics data alone for the purpose of identifying visitors by name.</p></section>
<section><h2>External forms and controls</h2><p>External forms, social networks and other third-party services may use their own cookies and technologies. You can generally manage or disable cookies through your browser settings, although some features may not work as intended.</p></section>
"""),
    "security.html": ("Information Security Policy", "security", """
<section><h2>Policy</h2><p>HDN Inc. recognizes the importance of information assets used in healthcare and related businesses and works to maintain appropriate confidentiality, integrity and availability according to the scale of our operations, the information involved and relevant risks.</p></section>
<section><h2>Controls</h2><p>We maintain responsibility and procedures for security, restrict access on a need-to-use basis, apply authentication and logging where appropriate, educate personnel, manage devices and media, assess service providers according to risk, and respond to suspected incidents with investigation, containment, notification and remediation as required.</p></section>
<section><h2>Continuous improvement</h2><p>We review and improve our controls as laws, technologies, threats and business operations evolve.</p></section>
"""),
    "disclaimer.html": ("Disclaimer", "disclaimer", """
<section><h2>General information</h2><p>Website and HDN editorial content is general information based on sources and practical knowledge available at the time of publication. It does not replace individual medical, legal, tax, accounting or other professional judgment.</p></section>
<section><h2>Regulatory information</h2><p>Healthcare, advertising, pharmaceutical, consumer-protection and privacy rules may change. We seek to keep information useful and current but cannot guarantee that every page reflects the latest rule or the facts of a specific case.</p></section>
<section><h2>Examples and estimates</h2><p>Case examples, simulations, revenue/cost figures and reference numbers are examples under stated or assumed conditions and do not guarantee equivalent business outcomes. Actual results vary by clinic, market, pricing, operations, advertising and other factors.</p></section>
<section><h2>External services and contracts</h2><p>We do not guarantee third-party sites or services linked from this website. Viewing this website alone does not create a paid consulting, LHub or other service agreement; individual contracts govern service scope, fees, deliverables and responsibilities.</p></section>
"""),
}


def page_template(title: str, body: str, *, lang: str, prefix: str, canonical: str) -> str:
    home = "/en/" if lang == "en" else "/"
    brand_sub = "Healthcare operations & patient journey support" if lang == "en" else "医療機関の導線設計・運用支援"
    back = "Back to HDN" if lang == "en" else "HDNトップへ戻る"
    updated_label = "Last updated" if lang == "en" else "最終更新日"
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | HDN</title>
<meta name="description" content="{title} - HDN Inc.">
<link rel="canonical" href="https://hdnjapan.com/{canonical}">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon-hdn.svg">
<style>
:root{{--ink:#24211f;--muted:#6d6660;--line:#d9d3cb;--paper:#f7f4ef;--red:#a82019;--max:920px}}*{{box-sizing:border-box}}body{{margin:0;color:var(--ink);font-family:"BIZ UDPGothic","Yu Gothic","Hiragino Kaku Gothic ProN",Meiryo,sans-serif;line-height:1.85;background:#fff}}a{{color:var(--red);text-underline-offset:3px}}header{{border-bottom:1px solid var(--line);background:#fff}}.head{{width:min(var(--max),calc(100% - 36px));margin:auto;min-height:72px;display:flex;justify-content:space-between;align-items:center;gap:20px}}.brand{{display:flex;align-items:center;gap:12px;color:var(--ink);text-decoration:none;font-weight:800}}.brand img{{width:105px}}.brand small{{display:block;color:var(--muted);font-size:11px}}main{{width:min(var(--max),calc(100% - 36px));margin:0 auto;padding:64px 0 80px}}.eyebrow{{margin:0 0 8px;color:var(--red);font-size:12px;font-weight:800;letter-spacing:.08em}}h1{{font-size:clamp(30px,5vw,46px);line-height:1.3;margin:0 0 14px}}.updated{{color:var(--muted);font-size:12px;margin-bottom:42px}}section{{padding:28px 0;border-top:1px solid var(--line)}}section:first-of-type{{border-top:2px solid #bdb5ac}}h2{{font-size:21px;line-height:1.5;margin:0 0 12px}}p,li,dd,dt{{font-size:14px}}ul{{padding-left:1.4em}}dl{{display:grid;grid-template-columns:120px 1fr;margin:0}}dt,dd{{padding:10px 0;border-bottom:1px solid #ece7e1}}dt{{font-weight:800}}dd{{margin:0}}.legal-note{{margin-top:38px;padding:18px;border:1px solid var(--line);background:var(--paper);font-size:12px;color:var(--muted)}}footer{{background:#121712;color:#ddd;padding:30px 0}}.foot{{width:min(var(--max),calc(100% - 36px));margin:auto}}.foot-links{{display:flex;flex-wrap:wrap;gap:10px 20px;margin-bottom:16px}}.foot a{{color:#fff;font-size:12px}}.foot-meta{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:11px;color:#aaa}}@media(max-width:600px){{.head{{align-items:flex-start;flex-direction:column;padding:14px 0}}dl{{grid-template-columns:1fr}}dt{{border-bottom:0;padding-bottom:0}}}}
</style>
</head><body><header><div class="head"><a class="brand" href="{home}"><img src="{prefix}assets/hdn-logo.png" alt="HDN"><span>{COMPANY}<small>{brand_sub}</small></span></a><a href="{home}">{back} →</a></div></header><main><p class="eyebrow">LEGAL / POLICY</p><h1>{title}</h1><p class="updated">{updated_label}: {UPDATED if lang == 'ja' else 'August 17, 2026'}</p>{body}<div class="legal-note">{COMPANY} / {REPRESENTATIVE} / {ADDRESS}</div></main>{footer_html(lang=lang, prefix=prefix)}</body></html>'''


def footer_html(*, lang: str, prefix: str = "") -> str:
    if lang == "en":
        links = [
            ("Privacy", f"{prefix}privacy.html"),
            ("Terms", f"{prefix}terms.html"),
            ("Cookies & Analytics", f"{prefix}cookie-policy.html"),
            ("Information Security", f"{prefix}security.html"),
            ("Disclaimer", f"{prefix}disclaimer.html"),
            ("Company", "/en/#company"),
        ]
        descriptor = "Healthcare operations & patient journey support"
    else:
        links = [
            ("プライバシー・個人情報保護", f"{prefix}privacy.html"),
            ("利用規約", f"{prefix}terms.html"),
            ("Cookie・アクセス解析", f"{prefix}cookie-policy.html"),
            ("情報セキュリティ", f"{prefix}security.html"),
            ("免責事項", f"{prefix}disclaimer.html"),
            ("会社概要", "/#profile"),
        ]
        descriptor = "医療機関の導線設計・運用支援"
    anchors = "".join(f'<a href="{href}">{label}</a>' for label, href in links)
    return f'''<footer class="footer legal-footer" data-legal-footer><div class="footer-inner foot"><div class="foot-links">{anchors}</div><div class="foot-meta"><span>{COMPANY}｜{descriptor}</span><span>© HDN Inc.</span></div></div></footer>'''


FOOTER_STYLE = '''<style id="legal-footer-style">
.legal-footer{padding:32px 0!important}.legal-footer .footer-inner{display:block!important}.legal-footer .foot-links{display:flex;flex-wrap:wrap;gap:8px 20px;margin:0 0 14px}.legal-footer .foot-links a{color:rgba(255,255,255,.88)!important;font-size:12px;text-decoration:none}.legal-footer .foot-links a:hover{text-decoration:underline;text-underline-offset:4px}.legal-footer .foot-meta{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:rgba(255,255,255,.58);font-size:11px}@media(max-width:640px){.legal-footer .foot-links{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}.legal-footer .foot-meta{display:grid;grid-template-columns:1fr}}
</style>'''


def write_legal_pages() -> None:
    for filename, (title, _, body) in JP_PAGES.items():
        (SITE / filename).write_text(page_template(title, body, lang="ja", prefix="", canonical=filename), encoding="utf-8")
    en_dir = SITE / "en"
    en_dir.mkdir(parents=True, exist_ok=True)
    for filename, (title, _, body) in EN_PAGES.items():
        (en_dir / filename).write_text(page_template(title, body, lang="en", prefix="../", canonical=f"en/{filename}"), encoding="utf-8")


def inject_footer(relative: str) -> None:
    path = SITE / relative
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    lang = "en" if relative.startswith("en/") else "ja"
    prefix = "" if lang == "ja" else ""
    footer = footer_html(lang=lang, prefix=prefix)
    html = re.sub(r'<footer class="footer(?: [^"]*)?">.*?</footer>', footer, html, count=1, flags=re.DOTALL)
    if 'data-legal-footer' not in html:
        html = html.replace("</body>", footer + "\n</body>", 1)
    if 'id="legal-footer-style"' not in html:
        html = html.replace("</head>", FOOTER_STYLE + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")


def verify() -> None:
    required = list(JP_PAGES) + [f"en/{name}" for name in EN_PAGES]
    for relative in required:
        path = SITE / relative
        if not path.exists() or path.stat().st_size < 1200:
            raise SystemExit(f"Missing or short legal page: {relative}")
    for relative in ["index.html", "self-pay.html", "lhub.html", "lhub-lp.html", "medical-sns.html", "tsuyoshi-hadano.html", "consultation.html", "en/index.html", "en/self-pay.html", "en/lhub.html"]:
        html = (SITE / relative).read_text(encoding="utf-8")
        if 'data-legal-footer' not in html:
            raise SystemExit(f"Missing legal footer: {relative}")
        for needle in ("privacy.html", "terms.html", "cookie-policy.html", "security.html", "disclaimer.html"):
            if needle not in html:
                raise SystemExit(f"Missing {needle} link in {relative}")


if __name__ == "__main__":
    write_legal_pages()
    for relative in ["index.html", "self-pay.html", "lhub.html", "lhub-lp.html", "medical-sns.html", "tsuyoshi-hadano.html", "consultation.html", "en/index.html", "en/self-pay.html", "en/lhub.html"]:
        inject_footer(relative)
    verify()
