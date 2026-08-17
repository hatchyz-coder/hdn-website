(() => {
  const TURNSTILE_SITE_KEY = '0x4AAAAAAESziEFBo263ZEbw';
  const TURNSTILE_ACTION = 'furuta_seminar';
  const endpoint = 'https://tnooknfyshieujolwtem.supabase.co/functions/v1/register-seminar';

  const furutaPortrait = document.querySelector('.speaker-photo-furuta');
  if (furutaPortrait) {
    furutaPortrait.src = '../assets/furuta-kazunori.svg?v=20260817-1905';
  }

  const form = document.getElementById('seminar-form');
  if (!form) return;

  const status = document.getElementById('form-status');
  const button = form.querySelector('button[type="submit"]');
  const qs = new URLSearchParams(location.search);

  let turnstileWidgetId = null;
  let turnstileToken = '';

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

  function resetTurnstile() {
    turnstileToken = '';
    if (turnstileWidgetId !== null && window.turnstile) {
      window.turnstile.reset(turnstileWidgetId);
    }
  }

  const turnstileMount = document.createElement('div');
  turnstileMount.id = 'seminar-turnstile';
  turnstileMount.style.margin = '8px 0 18px';
  if (button) button.parentNode.insertBefore(turnstileMount, button);
  else form.appendChild(turnstileMount);

  window.hdnTurnstileReady = () => {
    if (!window.turnstile || turnstileWidgetId !== null) return;
    turnstileWidgetId = window.turnstile.render('#seminar-turnstile', {
      sitekey: TURNSTILE_SITE_KEY,
      action: TURNSTILE_ACTION,
      theme: 'auto',
      callback: (token) => {
        turnstileToken = token;
        clearStatus();
      },
      'expired-callback': () => {
        turnstileToken = '';
      },
      'error-callback': () => {
        turnstileToken = '';
        show('本人確認の読み込みに失敗しました。ページを再読み込みしてお試しください。');
      }
    });
  };

  const turnstileScript = document.createElement('script');
  turnstileScript.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?onload=hdnTurnstileReady&render=explicit';
  turnstileScript.async = true;
  turnstileScript.defer = true;
  document.head.appendChild(turnstileScript);

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

    if (!turnstileToken) {
      show('本人確認が完了していません。確認欄が表示されるまで少し待ってから、もう一度お試しください。');
      return;
    }

    const submissionKey = form.dataset.submissionKey || createSubmissionKey();
    form.dataset.submissionKey = submissionKey;

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
      submission_key: submissionKey,
      company_website: '',
      turnstile_token: turnstileToken,
      ...attribution
    };

    form.classList.add('is-loading');
    const original = button?.textContent || '';
    if (button) button.textContent = '送信しています…';

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

      delete form.dataset.submissionKey;
      form.reset();
      show('お申し込みを受け付けました。参加方法は、ご登録のメールアドレスへ改めてご案内します。', 'success');
    } catch (error) {
      console.warn('Seminar submission failed:', error?.message || 'UNKNOWN');
      show('送信を完了できませんでした。通信環境をご確認のうえ、もう一度お試しください。');
    } finally {
      resetTurnstile();
      form.classList.remove('is-loading');
      if (button) button.textContent = original;
    }
  });
})();
