from pathlib import Path
import re


def replace_home_fv() -> None:
    index = Path('_site/index.html')
    html = index.read_text(encoding='utf-8')

    if 'data-fv-journey' not in html:
        pattern = re.compile(
            r'<figure class="visual-card" aria-label="医療機関の患者基盤活用イメージ">.*?</figure>',
            re.DOTALL,
        )
        journey = '''<aside class="hero-panel" data-fv-journey aria-label="患者導線の確認ポイント">
          <div class="panel-top">
            <div>
              <strong>患者導線を、分解して確認する。</strong>
              <span>集客だけでなく、来院前後の離脱と継続まで見ます。</span>
            </div>
            <span class="status">PATIENT JOURNEY</span>
          </div>
          <div class="workflow">
            <div class="flow-row">
              <div class="icon">01</div>
              <div><h3>広告・HP・SNS</h3><p>どこから来て、どこで迷っているか</p></div>
              <span class="metric">入口</span>
            </div>
            <div class="flow-row">
              <div class="icon">02</div>
              <div><h3>LINE・問診</h3><p>登録後に患者との接点が切れていないか</p></div>
              <span class="metric">接点</span>
            </div>
            <div class="flow-row">
              <div class="icon">03</div>
              <div><h3>予約・決済</h3><p>手続きの負担やスタッフ対応が離脱を生んでいないか</p></div>
              <span class="metric">転換</span>
            </div>
            <div class="flow-row">
              <div class="icon">04</div>
              <div><h3>再診・自費・物販・紹介</h3><p>診療後の関係を継続できる仕組みがあるか</p></div>
              <span class="metric">継続</span>
            </div>
          </div>
        </aside>'''
        html, count = pattern.subn(journey, html, count=1)
        if count != 1:
            raise SystemExit('Could not replace the home FV visual with the patient-journey panel.')

    html = html.replace('assets/illustration-consulting-board.png', 'assets/lhub-line-commerce.png', 1)
    html = html.replace('alt="LHubで患者CRMを運用する画面イメージ"', 'alt="LHubのLINE患者導線・運用画面"', 1)
    index.write_text(html, encoding='utf-8')


def preserve_consultation_real_photo() -> None:
    consultation = Path('_site/consultation.html')
    html = consultation.read_text(encoding='utf-8')
    html = html.replace('assets/illustration-consulting-board.png', 'assets/hadano-profile.jpg', 1)
    html = html.replace('alt="医療機関の患者導線を診断する相談イメージ"', 'alt="株式会社HDN代表 羽田野剛士"', 1)
    consultation.write_text(html, encoding='utf-8')


def verify_home_fv() -> None:
    html = Path('_site/index.html').read_text(encoding='utf-8')
    hero = re.search(r'<section class="hero">(.*?)</section>', html, re.DOTALL)
    if not hero:
        raise SystemExit('Home hero not found')
    if 'hadano-profile.jpg' in hero.group(1):
        raise SystemExit('Representative portrait must not appear in the home first view')
    if 'data-fv-journey' not in hero.group(1):
        raise SystemExit('Patient journey panel is missing from the home first view')


if __name__ == '__main__':
    replace_home_fv()
    preserve_consultation_real_photo()
    verify_home_fv()
