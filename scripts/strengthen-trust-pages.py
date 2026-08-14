from pathlib import Path

PROFILE = Path('_site/tsuyoshi-hadano.html')
CONSULTATION = Path('_site/consultation.html')

STYLE = '''<style id="trust-pages-style">
  .trust-detail{padding:72px 0;border-top:1px solid #d9d3cb;background:#f7f5f1}
  .trust-detail-inner{width:min(1040px,calc(100% - 40px));margin:auto}
  .trust-detail-head{display:grid;grid-template-columns:minmax(220px,.58fr) minmax(0,1fr);gap:28px 54px;align-items:start;margin-bottom:28px}
  .trust-detail-head h2{margin:0;font-size:clamp(28px,4vw,40px);line-height:1.3}
  .trust-detail-head p{margin:2px 0 0;color:#6d6660;line-height:1.9;font-weight:600}
  .trust-detail-list{border-top:1px solid #cfc8bf}
  .trust-detail-row{display:grid;grid-template-columns:minmax(210px,.55fr) minmax(0,1.25fr);gap:24px 48px;padding:22px 0;border-bottom:1px solid #cfc8bf}
  .trust-detail-row strong{font-size:17px;line-height:1.55}
  .trust-detail-row p{margin:0;color:#5f5954;line-height:1.85}
  .consultation-output{background:#f1eee8}
  .consultation-output .trust-detail-row strong{color:#8f201b}
  @media(max-width:760px){.trust-detail{padding:50px 0}.trust-detail-inner{width:min(100% - 28px,1040px)}.trust-detail-head,.trust-detail-row{grid-template-columns:1fr;gap:10px}.trust-detail-row{padding:18px 0}}
</style>'''

PROFILE_BLOCK = '''<section class="trust-detail" data-founder-workstyle aria-labelledby="founder-workstyle-title">
  <div class="trust-detail-inner">
    <div class="trust-detail-head">
      <h2 id="founder-workstyle-title">支援で大切にしていること</h2>
      <p>提案書を作って終わるのではなく、院長・スタッフ・患者のそれぞれが実際に動けるところまで具体化します。</p>
    </div>
    <div class="trust-detail-list">
      <div class="trust-detail-row"><strong>現場で動く形まで落とす</strong><p>診療メニューだけでなく、LINE、予約、問診、決済、診療、発送、再診、継続フォロー、スタッフの役割まで一つの運用として整理します。</p></div>
      <div class="trust-detail-row"><strong>今ある仕組みを先に見る</strong><p>新しいツールありきでは進めません。現在の患者導線、既存システム、院内オペレーションを確認し、残せるものと変えるべきものを分けます。</p></div>
      <div class="trust-detail-row"><strong>数字と現場を同時に見る</strong><p>LINE登録、問診到達、予約・決済、継続利用などの数字だけでなく、受付負荷や運用の詰まりも見ながら改善優先順位を決めます。</p></div>
    </div>
  </div>
</section>'''

CONSULTATION_BLOCK = '''<section class="trust-detail consultation-output" data-consultation-output aria-labelledby="consultation-output-title">
  <div class="trust-detail-inner">
    <div class="trust-detail-head">
      <h2 id="consultation-output-title">相談後に整理できること</h2>
      <p>初回相談では、サービス説明より先に「どこで患者が止まり、何から直すべきか」を整理します。</p>
    </div>
    <div class="trust-detail-list">
      <div class="trust-detail-row"><strong>現在の患者導線</strong><p>広告・ホームページ・SNSからLINE、問診、予約、決済、診療、再診までを並べ、分断や離脱ポイントを確認します。</p></div>
      <div class="trust-detail-row"><strong>改善の優先順位</strong><p>売上への影響、患者の分かりにくさ、スタッフ負荷の3方向から、先に直す項目と後回しにできる項目を分けます。</p></div>
      <div class="trust-detail-row"><strong>次にやること</strong><p>ページ修正、LINE導線、問診・決済、院内ルール、計測項目など、次のアクションを実務単位で整理します。</p></div>
    </div>
  </div>
</section>'''


def ensure_style(source: str) -> str:
    if 'id="trust-pages-style"' not in source:
        source = source.replace('</head>', STYLE + '\n</head>', 1)
    return source


def insert_before_precontact(source: str, block: str, marker: str) -> str:
    if marker in source:
        return source
    anchor = '<section class="precontact-trust"'
    if anchor in source:
        return source.replace(anchor, block + '\n' + anchor, 1)
    if '</main>' in source:
        return source.replace('</main>', block + '\n</main>', 1)
    raise SystemExit('Could not find insertion point')


def process(path: Path, block: str, marker: str) -> None:
    if not path.exists():
        raise SystemExit(f'Missing page: {path}')
    source = path.read_text(encoding='utf-8')
    source = ensure_style(source)
    source = insert_before_precontact(source, block, marker)
    path.write_text(source, encoding='utf-8')


process(PROFILE, PROFILE_BLOCK, 'data-founder-workstyle')
process(CONSULTATION, CONSULTATION_BLOCK, 'data-consultation-output')

for path, marker in ((PROFILE, 'data-founder-workstyle'), (CONSULTATION, 'data-consultation-output')):
    source = path.read_text(encoding='utf-8')
    if marker not in source or 'id="trust-pages-style"' not in source:
        raise SystemExit(f'Trust-page enhancement missing: {path}')
