from pathlib import Path


def add_japanese_patterns() -> None:
    path = Path('_site/index.html')
    html = path.read_text(encoding='utf-8')
    if 'data-support-patterns' in html:
        return

    anchor = '<section id="services" class="section alt">'
    if anchor not in html:
        raise SystemExit('Could not find services section on Japanese home')

    section = '''<section class="section support-patterns" data-support-patterns aria-labelledby="support-patterns-title">
      <div class="container">
        <div class="support-patterns-head">
          <div>
            <p class="eyebrow">支援パターン</p>
            <h2 class="section-title" id="support-patterns-title">実務では、こういうところから入ります。</h2>
          </div>
          <p class="section-copy">個別案件の社名や成果数値ではなく、HDNが実際に扱う支援テーマを匿名化して整理しています。</p>
        </div>
        <div class="support-pattern-list">
          <article>
            <span class="case-no">CASE 01</span>
            <div><h3>保険診療中心のクリニックで、自費診療を立ち上げる</h3><p><b>整理するもの</b> 診療メニュー、価格、患者説明、問診、予約、決済、院内オペレーション、フォロー導線。</p><p><b>確認する指標</b> 問い合わせ、問診完了、予約、決済、再診・継続。</p></div>
          </article>
          <article>
            <span class="case-no">CASE 02</span>
            <div><h3>LINE登録後の患者導線を、受付業務まで含めてつなぎ直す</h3><p><b>整理するもの</b> LINE登録、問診、予約、決済案内、患者ステータス、再来院・再購入フォロー。</p><p><b>確認する指標</b> 登録後離脱、問診完了、予約転換、対応工数、再来院。</p></div>
          </article>
          <article>
            <span class="case-no">CASE 03</span>
            <div><h3>SNS・動画を「再生数」で終わらせず、診療導線へつなげる</h3><p><b>整理するもの</b> 患者が知りたい情報、動画テーマ、プロフィール導線、HP・LINEへの接続、問い合わせ後の流れ。</p><p><b>確認する指標</b> 視聴後の遷移、LINE登録、問い合わせ、予約までの離脱。</p></div>
          </article>
        </div>
        <p class="support-pattern-note">※ 実績数値は、公開可能な一次情報が確認できたものだけを掲載します。成果を保証する表現は行いません。</p>
      </div>
    </section>\n\n'''
    html = html.replace(anchor, section + anchor, 1)

    style = '''<style id="support-pattern-style">
    .support-patterns{background:#fff!important}
    .support-patterns-head{display:grid;grid-template-columns:minmax(0,.8fr) minmax(280px,.55fr);gap:44px;align-items:start;margin-bottom:28px}
    .support-pattern-list{border-top:1px solid #d9d3cb}
    .support-pattern-list article{display:grid;grid-template-columns:94px minmax(0,1fr);gap:24px;padding:26px 0;border-bottom:1px solid #d9d3cb}
    .case-no{font-size:11px;font-weight:800;letter-spacing:.08em;color:#8f201b;padding-top:5px}
    .support-pattern-list h3{margin:0;font-size:21px;line-height:1.5}
    .support-pattern-list p{margin:8px 0 0;color:#6d6660;font-size:14px;line-height:1.8}
    .support-pattern-list b{color:#24211f}
    .support-pattern-note{margin:16px 0 0;color:#807870;font-size:11px;line-height:1.7}
    @media(max-width:760px){.support-patterns-head{grid-template-columns:1fr;gap:14px}.support-pattern-list article{grid-template-columns:1fr;gap:8px;padding:22px 0}.support-pattern-list h3{font-size:18px}}
  </style>'''
    if 'id="support-pattern-style"' not in html:
        html = html.replace('</head>', style + '\n</head>', 1)

    path.write_text(html, encoding='utf-8')


def add_english_patterns() -> None:
    path = Path('_site/en/index.html')
    html = path.read_text(encoding='utf-8')
    if 'data-support-patterns' in html:
        return

    anchor = '<section id="services" class="section">'
    if anchor not in html:
        anchor = '<section class="section">'
    if anchor not in html:
        raise SystemExit('Could not find insertion point on English home')

    section = '''<section class="section support-patterns" data-support-patterns aria-labelledby="support-patterns-title">
      <div class="container">
        <div class="support-patterns-head"><div><p class="eyebrow">Support patterns</p><h2 id="support-patterns-title">Where our work usually starts.</h2></div><p class="section-copy">These are anonymized operational patterns, not client claims or guaranteed outcomes.</p></div>
        <div class="support-pattern-list">
          <article><span>CASE 01</span><div><h3>Launching a private-care service inside an insurance-led clinic</h3><p>Service design, pricing, patient explanation, forms, booking, payment, staff workflow and follow-up.</p></div></article>
          <article><span>CASE 02</span><div><h3>Rebuilding the patient journey after LINE registration</h3><p>Questionnaires, booking, payment guidance, patient status, staff handling and repeat-visit communication.</p></div></article>
          <article><span>CASE 03</span><div><h3>Connecting social and video content to actual consultation flow</h3><p>Patient questions, content themes, profile links, website/LINE handoff and the path from inquiry to booking.</p></div></article>
        </div>
      </div>
    </section>\n\n'''
    html = html.replace(anchor, section + anchor, 1)
    path.write_text(html, encoding='utf-8')


def verify() -> None:
    jp = Path('_site/index.html').read_text(encoding='utf-8')
    en = Path('_site/en/index.html').read_text(encoding='utf-8')
    for source, label in ((jp, 'Japanese'), (en, 'English')):
        if 'data-support-patterns' not in source:
            raise SystemExit(f'{label} support patterns missing')
        if source.count('CASE 0') < 3:
            raise SystemExit(f'{label} support patterns incomplete')
    for forbidden in ('必ず売上', '必ず改善', 'Guaranteed results'):
        if forbidden in jp or forbidden in en:
            raise SystemExit(f'Unsupported outcome claim found: {forbidden}')


if __name__ == '__main__':
    add_japanese_patterns()
    add_english_patterns()
    verify()
