(() => {
  const furutaPortrait = document.querySelector('.speaker-photo-furuta');
  if (furutaPortrait) {
    furutaPortrait.src = 'data:image/jpeg;base64,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';
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
