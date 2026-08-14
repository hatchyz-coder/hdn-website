from pathlib import Path

ARTICLE_BASE = "https://article.hdnjapan.com"

BLOCKS = {
    "index.html": '''<section class="article-bridge" data-article-bridge aria-label="HDNの記事・コラム">
      <div class="article-bridge-inner">
        <div class="article-bridge-head"><p>HDNの記事・コラム</p><h2>支援の背景にある考え方を、実務記事で公開しています。</h2><a href="https://article.hdnjapan.com/">記事一覧を見る →</a></div>
        <div class="article-bridge-list">
          <a href="https://article.hdnjapan.com/articles/line-booking-payment-flow/"><span>患者導線設計</span><strong>LINE予約と決済が分断すると起きる問題と、患者導線を整える方法</strong><small>予約・問診・決済・フォローを別々にしないための実務整理</small></a>
          <a href="https://article.hdnjapan.com/articles/clinic-video-strategy/"><span>医療マーケティング</span><strong>無難な動画では、患者は動かない</strong><small>患者の不安、診療理解、認知の3つに分けて動画を設計する考え方</small></a>
          <a href="https://article.hdnjapan.com/articles/regenerative-medicine-improvement-orders/"><span>クリニック運営</span><strong>再生医療の改善命令から確認したい5つの実務ポイント</strong><small>制度・提供体制・記録管理を、現場運用の視点から確認</small></a>
        </div>
      </div>
    </section>''',
    "self-pay.html": '''<section class="article-bridge article-bridge-single" data-article-bridge aria-label="関連する実務記事">
      <div class="article-bridge-inner"><div class="article-bridge-head"><p>関連する実務記事</p><h2>自費診療は、メニューより先に運用を設計する。</h2></div><div class="article-bridge-list"><a href="https://article.hdnjapan.com/articles/regenerative-medicine-improvement-orders/"><span>クリニック運営</span><strong>再生医療の改善命令から確認したい5つの実務ポイント</strong><small>自費領域でも、提供体制・適格性判断・記録管理まで運用として考える必要があります。</small></a></div></div>
    </section>''',
    "lhub.html": '''<section class="article-bridge article-bridge-single" data-article-bridge aria-label="関連する実務記事">
      <div class="article-bridge-inner"><div class="article-bridge-head"><p>関連する実務記事</p><h2>LINEを入れるだけでは、患者導線はつながりません。</h2></div><div class="article-bridge-list"><a href="https://article.hdnjapan.com/articles/line-booking-payment-flow/"><span>患者導線設計</span><strong>LINE予約と決済が分断すると起きる問題と、患者導線を整える方法</strong><small>患者の離脱とスタッフ負荷がどこで生まれるかを整理しています。</small></a></div></div>
    </section>''',
    "medical-sns.html": '''<section class="article-bridge article-bridge-single" data-article-bridge aria-label="関連する実務記事">
      <div class="article-bridge-inner"><div class="article-bridge-head"><p>関連する実務記事</p><h2>再生数より、患者が次に動ける動画を考える。</h2></div><div class="article-bridge-list"><a href="https://article.hdnjapan.com/articles/clinic-video-strategy/"><span>医療マーケティング</span><strong>無難な動画では、患者は動かない</strong><small>不安を減らす動画、診療理解を深める動画、認知を取る動画の3分類を解説します。</small></a></div></div>
    </section>''',
    "en/index.html": '''<section class="article-bridge" data-article-bridge aria-label="HDN Insights">
      <div class="article-bridge-inner"><div class="article-bridge-head"><p>HDN Insights</p><h2>Read the operating logic behind our work.</h2><a href="https://article.hdnjapan.com/en/">View all articles →</a></div><div class="article-bridge-list">
        <a href="https://article.hdnjapan.com/en/articles/line-booking-payment-flow/"><span>Patient Journey</span><strong>What happens when LINE booking and payment are disconnected</strong><small>How fragmented booking, intake, payment and follow-up create patient drop-off and staff workload.</small></a>
        <a href="https://article.hdnjapan.com/en/articles/clinic-video-strategy/"><span>Healthcare Marketing</span><strong>Safe, generic videos rarely move patients</strong><small>A practical framework for reassurance, clinical understanding and reach.</small></a>
        <a href="https://article.hdnjapan.com/en/articles/regenerative-medicine-improvement-orders/"><span>Clinic Operations</span><strong>Five operational checks from Japan's regenerative medicine improvement orders</strong><small>Provider systems, eligibility decisions, reporting and record management.</small></a>
      </div></div>
    </section>''',
    "en/self-pay.html": '''<section class="article-bridge article-bridge-single" data-article-bridge aria-label="Related insight"><div class="article-bridge-inner"><div class="article-bridge-head"><p>Related insight</p><h2>Private care requires operating design, not only a menu.</h2></div><div class="article-bridge-list"><a href="https://article.hdnjapan.com/en/articles/regenerative-medicine-improvement-orders/"><span>Clinic Operations</span><strong>Five operational checks from regenerative medicine improvement orders</strong><small>A practical reminder that private-care services require systems, judgment and records.</small></a></div></div></section>''',
    "en/lhub.html": '''<section class="article-bridge article-bridge-single" data-article-bridge aria-label="Related insight"><div class="article-bridge-inner"><div class="article-bridge-head"><p>Related insight</p><h2>LINE alone does not create a connected patient journey.</h2></div><div class="article-bridge-list"><a href="https://article.hdnjapan.com/en/articles/line-booking-payment-flow/"><span>Patient Journey</span><strong>What happens when LINE booking and payment are disconnected</strong><small>Where patient drop-off and staff workload emerge when the flow is fragmented.</small></a></div></div></section>''',
}

STYLE = '''<style id="article-bridge-style">
.article-bridge{padding:64px 0;border-top:1px solid #d9d3cb;background:#f7f4ef}.article-bridge-inner{width:min(1120px,calc(100% - 40px));margin:auto;display:grid;grid-template-columns:minmax(230px,.62fr) minmax(0,1.35fr);gap:36px 54px}.article-bridge-head p{margin:0 0 10px;color:#8e211b;font-size:12px;font-weight:800}.article-bridge-head h2{margin:0;font-size:clamp(25px,3vw,36px);line-height:1.35}.article-bridge-head>a{display:inline-block;margin-top:18px;font-size:13px;font-weight:800;text-decoration:underline;text-underline-offset:4px}.article-bridge-list{border-top:1px solid #bbb3aa}.article-bridge-list>a{display:grid;grid-template-columns:150px minmax(0,1fr);gap:4px 22px;padding:18px 0;border-bottom:1px solid #bbb3aa;color:inherit;text-decoration:none}.article-bridge-list span{grid-row:1/3;color:#746c65;font-size:11px;font-weight:800;letter-spacing:.02em}.article-bridge-list strong{font-size:16px;line-height:1.5}.article-bridge-list small{color:#6f6862;font-size:12px;line-height:1.65}.article-bridge-list>a:hover strong{text-decoration:underline;text-underline-offset:4px}.article-bridge-single .article-bridge-list>a{padding-top:12px}@media(max-width:760px){.article-bridge{padding:46px 0}.article-bridge-inner{width:min(100% - 28px,1120px);grid-template-columns:1fr;gap:24px}.article-bridge-list>a{grid-template-columns:1fr;gap:6px}.article-bridge-list span{grid-row:auto}.article-bridge-head>a{margin-top:12px}}
</style>'''


def add_block(relative: str, block: str) -> None:
    path = Path("_site") / relative
    if not path.exists():
        raise SystemExit(f"Missing generated page: {relative}")
    source = path.read_text(encoding="utf-8")
    if 'data-article-bridge' in source:
        return
    if 'id="article-bridge-style"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    marker = '<section class="precontact-trust"'
    if marker in source:
        source = source.replace(marker, block + "\n" + marker, 1)
    elif "</main>" in source:
        source = source.replace("</main>", block + "\n</main>", 1)
    else:
        source = source.replace("</body>", block + "\n</body>", 1)
    path.write_text(source, encoding="utf-8")


def verify() -> None:
    for relative in BLOCKS:
        source = (Path("_site") / relative).read_text(encoding="utf-8")
        if 'data-article-bridge' not in source:
            raise SystemExit(f"Missing article bridge: {relative}")
        if ARTICLE_BASE not in source:
            raise SystemExit(f"Missing article domain: {relative}")
    checks = {"lhub.html":"line-booking-payment-flow","medical-sns.html":"clinic-video-strategy","self-pay.html":"regenerative-medicine-improvement-orders","en/lhub.html":"line-booking-payment-flow"}
    for relative, slug in checks.items():
        if slug not in (Path("_site") / relative).read_text(encoding="utf-8"):
            raise SystemExit(f"Wrong contextual article link: {relative}")


if __name__ == "__main__":
    for page, block in BLOCKS.items():
        add_block(page, block)
    verify()
