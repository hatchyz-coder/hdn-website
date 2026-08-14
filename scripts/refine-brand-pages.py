from pathlib import Path
import re


def replace_once(html: str, old: str, new: str) -> str:
    if old in html:
        return html.replace(old, new, 1)
    return html


def refine_english_home() -> None:
    path = Path('_site/en/index.html')
    html = path.read_text(encoding='utf-8')

    html = html.replace('https://hdnjapan.com/assets/hdn-og.jpg', 'https://hdnjapan.com/assets/hdn-logo-original.jpg')
    if 'property="og:image:alt"' not in html:
        html = html.replace(
            '<meta property="og:image" content="https://hdnjapan.com/assets/hdn-logo-original.jpg">',
            '<meta property="og:image" content="https://hdnjapan.com/assets/hdn-logo-original.jpg">\n  <meta property="og:image:alt" content="HDN Inc. — patient journey and healthcare operations design">',
            1,
        )
    if 'name="twitter:image:alt"' not in html:
        html = html.replace(
            '<meta name="twitter:image" content="https://hdnjapan.com/assets/hdn-logo-original.jpg">',
            '<meta name="twitter:image" content="https://hdnjapan.com/assets/hdn-logo-original.jpg">\n  <meta name="twitter:image:alt" content="HDN Inc. — patient journey and healthcare operations design">',
            1,
        )

    if 'data-en-evidence' not in html:
        pattern = re.compile(r'<figure class="hero-card">.*?</figure>', re.DOTALL)
        evidence = '''<aside class="en-evidence" data-en-evidence aria-label="How HDN reviews a patient journey">
          <div class="en-evidence-head"><strong>We review the workflow in the order patients experience it.</strong><span>FIELD REVIEW</span></div>
          <div class="en-evidence-row"><b>01</b><div><strong>First contact</strong><p>Website, social media, ads and referrals: where does the patient enter, and where do they hesitate?</p></div></div>
          <div class="en-evidence-row"><b>02</b><div><strong>LINE and forms</strong><p>Does the next action remain clear after registration, inquiry or questionnaire completion?</p></div></div>
          <div class="en-evidence-row"><b>03</b><div><strong>Booking and payment</strong><p>Are operational steps creating unnecessary work or patient drop-off?</p></div></div>
          <div class="en-evidence-row"><b>04</b><div><strong>Follow-up and repeat care</strong><p>Is there a practical route for repeat visits, private care, products and ongoing communication?</p></div></div>
        </aside>'''
        html, count = pattern.subn(evidence, html, count=1)
        if count != 1:
            raise SystemExit('Could not replace the English home illustration card.')

    if 'id="en-evidence-style"' not in html:
        style = '''<style id="en-evidence-style">
    .en-evidence{border:1px solid #d9d3cb;background:#fff;box-shadow:none}
    .en-evidence-head{display:flex;justify-content:space-between;gap:16px;padding:17px 18px;border-bottom:1px solid #d9d3cb}
    .en-evidence-head strong{font-size:14px;line-height:1.5}.en-evidence-head span{font-size:11px;font-weight:800;color:#8f201b;letter-spacing:.08em;white-space:nowrap}
    .en-evidence-row{display:grid;grid-template-columns:38px 1fr;gap:12px;padding:15px 18px;border-bottom:1px solid #e8e2db}.en-evidence-row:last-child{border-bottom:0}
    .en-evidence-row>b{font-size:11px;color:#8f201b;padding-top:3px}.en-evidence-row strong{display:block;font-size:14px}.en-evidence-row p{margin:3px 0 0;color:#6d6660;font-size:12px;line-height:1.6}
    @media(max-width:640px){.en-evidence-head{display:grid}.en-evidence-row{grid-template-columns:32px 1fr;padding:13px 14px}}
  </style>'''
        html = html.replace('</head>', style + '\n</head>', 1)

    path.write_text(html, encoding='utf-8')


def ensure_english_lhub_social_meta() -> None:
    path = Path('_site/en/lhub.html')
    html = path.read_text(encoding='utf-8')
    if 'property="og:image"' not in html:
        marker = '<link rel="icon" href="../assets/lhub-mark-color.png">'
        meta = '''<meta property="og:type" content="website">
  <meta property="og:locale" content="en_US">
  <meta property="og:site_name" content="HDN Inc.">
  <meta property="og:title" content="LHub | LINE-Based Patient Engagement for Clinics">
  <meta property="og:description" content="Connect booking, questionnaires, payment guidance, patient status and follow-up through LINE with LHub.">
  <meta property="og:url" content="https://hdnjapan.com/en/lhub.html">
  <meta property="og:image" content="https://hdnjapan.com/assets/lhub-line-commerce.png">
  <meta property="og:image:alt" content="LHub LINE patient journey and operations screen">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="LHub | LINE-Based Patient Engagement for Clinics">
  <meta name="twitter:description" content="Connect booking, questionnaires, payment guidance, patient status and follow-up through LINE with LHub.">
  <meta name="twitter:image" content="https://hdnjapan.com/assets/lhub-line-commerce.png">
  <meta name="twitter:image:alt" content="LHub LINE patient journey and operations screen">
  '''
        if marker not in html:
            raise SystemExit('Could not find English LHub metadata insertion point.')
        html = html.replace(marker, meta + marker, 1)
    path.write_text(html, encoding='utf-8')


def improve_social_meta() -> None:
    self_pay = Path('_site/en/self-pay.html')
    html = self_pay.read_text(encoding='utf-8')
    if 'property="og:image:alt"' not in html:
        html = html.replace(
            '<meta property="og:image" content="https://hdnjapan.com/assets/self-pay-og.jpg">',
            '<meta property="og:image" content="https://hdnjapan.com/assets/self-pay-og.jpg">\n  <meta property="og:image:alt" content="HDN private medical services implementation support">',
            1,
        )
    if 'name="twitter:image:alt"' not in html:
        html = html.replace(
            '<meta name="twitter:image" content="https://hdnjapan.com/assets/self-pay-og.jpg">',
            '<meta name="twitter:image" content="https://hdnjapan.com/assets/self-pay-og.jpg">\n  <meta name="twitter:image:alt" content="HDN private medical services implementation support">',
            1,
        )
    self_pay.write_text(html, encoding='utf-8')

    sns = Path('_site/medical-sns.html')
    html = sns.read_text(encoding='utf-8')
    html = html.replace('https://hdnjapan.com/assets/hdn-logo.png', 'https://hdnjapan.com/assets/hadano-profile.jpg', 1)
    if 'property="og:image:alt"' not in html:
        html = html.replace(
            '<meta property="og:image" content="https://hdnjapan.com/assets/hadano-profile.jpg">',
            '<meta property="og:image" content="https://hdnjapan.com/assets/hadano-profile.jpg">\n  <meta property="og:image:alt" content="株式会社HDN代表 羽田野剛士">',
            1,
        )
    if 'name="twitter:title"' not in html:
        html = html.replace(
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="医療機関向けSNS・YouTube戦略支援｜株式会社HDN">\n  <meta name="twitter:description" content="患者の不安を消す情報と、診療までつながるSNS・動画導線を設計します。">\n  <meta name="twitter:image" content="https://hdnjapan.com/assets/hadano-profile.jpg">\n  <meta name="twitter:image:alt" content="株式会社HDN代表 羽田野剛士">',
            1,
        )
    sns.write_text(html, encoding='utf-8')


def localize_japanese_section_labels() -> None:
    replacements = {
        '_site/index.html': [('Working Documents', '実務成果物')],
        '_site/lhub-lp.html': [('Patient Journey', '患者導線')],
        '_site/medical-sns.html': [
            ('Medical SNS Strategy', '医療SNS・動画戦略'),
            ('3 Types of Content', 'コンテンツ設計'),
            ('What HDN Supports', 'HDNの支援'),
            ('Examples', '企画例'),
            ('From Awareness to Consultation', '認知から診療へ'),
            ('Consultation', '相談'),
        ],
    }
    for filename, pairs in replacements.items():
        path = Path(filename)
        html = path.read_text(encoding='utf-8')
        for old, new in pairs:
            html = html.replace(old, new)
        path.write_text(html, encoding='utf-8')


def verify_refinements() -> None:
    en_home = Path('_site/en/index.html').read_text(encoding='utf-8')
    if 'hdn-og.jpg' in en_home:
        raise SystemExit('English home still references missing hdn-og.jpg')
    if 'illustration-patient-assets.jpg' in en_home:
        raise SystemExit('Synthetic English home illustration remains')
    if 'data-en-evidence' not in en_home:
        raise SystemExit('English evidence panel is missing')

    en_lhub = Path('_site/en/lhub.html').read_text(encoding='utf-8')
    if 'property="og:image"' not in en_lhub or 'lhub-line-commerce.png' not in en_lhub:
        raise SystemExit('English LHub social metadata is incomplete')

    sns = Path('_site/medical-sns.html').read_text(encoding='utf-8')
    if 'property="og:image" content="https://hdnjapan.com/assets/hadano-profile.jpg"' not in sns:
        raise SystemExit('Medical SNS OGP does not use the real representative photo')
    for stale in ('Medical SNS Strategy', '3 Types of Content', 'What HDN Supports', 'From Awareness to Consultation'):
        if stale in sns:
            raise SystemExit(f'English eyebrow remains on Japanese SNS page: {stale}')


if __name__ == '__main__':
    refine_english_home()
    ensure_english_lhub_social_meta()
    improve_social_meta()
    localize_japanese_section_labels()
    verify_refinements()
