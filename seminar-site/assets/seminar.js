(() => {
  const furutaPortrait = document.querySelector('.speaker-photo-furuta');
  if (furutaPortrait) {
    furutaPortrait.src = '../assets/furuta-kazunori.svg?v=20260817-1905';
  }

  const form = document.getElementById('seminar-form');
  if (!form) return;

  const status = document.getElementById('form-status');
  const endpoint = document.querySelector('meta[name="hdn-form-endpoint"]')?.content || '';
  const qs = new URLSearchParams(location.search);

  const attribution = {
    utm_source: qs.get('utm_source') || '',
    utm_medium: qs.get('utm_medium') || '',
    utm_campaign: qs.get('utm_campaign') || '',
    utm_content: qs.get('utm_content') || '',
    utm_term: qs.get('utm_term') || '',
    landing_page: location.href,
    referrer: document.referrer || ''
  };

  function show(message, type = 'error') {
    status.className = `form-status is-${type}`;
    status.textContent = message;
    status.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function clearStatus() {
    status.className = 'form-status';
    status.textContent = '';
  }

  function createSubmissionKey() {
    if (crypto?.randomUUID) return crypto.randomUUID();
    return `${Date.now()}-${Math.random().toString(16).slice(2)}-${Math.random().toString(16).slice(2)}`;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearStatus();

    if (!form.reportValidity()) return;

    const data = new FormData(form);
    if (String(data.get('company_website') || '').trim()) {
      show('送信を受け付けました。', 'success');
      form.reset();
      return;
    }

    if (!endpoint) {
      show('現在、申込受付システムの接続準備中です。公開前に受付先を設定してください。');
      return;
    }

    const payload = {
      seminar_slug: form.dataset.seminar || 'furuta-01',
      name: String(data.get('name') || '').trim(),
      organization_name: String(data.get('organization_name') || '').trim(),
      role: String(data.get('role') || '').trim(),
      department: String(data.get('department') || '').trim(),
      email: String(data.get('email') || '').trim(),
      phone: String(data.get('phone') || '').trim(),
      self_pay_status: String(data.get('self_pay_status') || '').trim(),
      learning_topic: String(data.get('learning_topic') || '').trim(),
      advance_question: String(data.get('advance_question') || '').trim(),
      privacy_consent: data.get('privacy_consent') === 'yes',
      submission_key: createSubmissionKey(),
      ...attribution
    };

    form.classList.add('is-loading');
    const button = form.querySelector('button[type="submit"]');
    const original = button.textContent;
    button.textContent = '送信しています…';

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload),
        credentials: 'omit'
      });

      let body = {};
      try { body = await response.json(); } catch (_) { /* no-op */ }

      if (!response.ok || body.ok !== true) {
        throw new Error(body.error_code || `HTTP_${response.status}`);
      }

      try {
        if (typeof window.fbq === 'function') window.fbq('track', 'Lead');
        if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { event_category: 'seminar', event_label: 'furuta-01' });
      } catch (_) { /* analytics must never block registration */ }

      form.reset();
      show('お申し込みを受け付けました。ご登録のメールアドレスへ受付完了メールをお送りします。', 'success');
    } catch (error) {
      console.warn('Seminar submission failed:', error?.message || 'UNKNOWN');
      show('送信を完了できませんでした。通信環境をご確認のうえ、時間をおいてもう一度お試しください。');
    } finally {
      form.classList.remove('is-loading');
      button.textContent = original;
    }
  });
})();
