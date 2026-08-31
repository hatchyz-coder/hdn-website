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
  const roles = new Set(['院長', '医師', '医療法人経営者', '事務長', 'その他医療機関関係者']);
  const selfPayStatuses = new Set(['まだ導入していない', '検討・情報収集中', '一部導入している', 'すでに複数メニューを運用している']);

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

  function validateRegistration(payload) {
    if (payload.name.length < 3) return 'お名前は3文字以上で正確に入力してください。';
    if (payload.organization_name.length < 4) return '医療機関名・法人名は4文字以上で正確に入力してください。';
    if (!roles.has(payload.role)) return '役職を選択してください。';
    if (!selfPayStatuses.has(payload.self_pay_status)) return '現在の自費診療の状況を選択してください。';
    return '';
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

    const validationMessage = validateRegistration(payload);
    if (validationMessage) {
      show(validationMessage);
      return;
    }

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
        const message = typeof body.message === 'string' ? body.message : '';
        throw new Error(message || body.error_code || `HTTP_${response.status}`);
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
      const message = String(error?.message || '');
      show(message.startsWith('VALIDATION_') || message.startsWith('HTTP_') || message === 'TURNSTILE_FAILED'
        ? '送信を完了できませんでした。通信環境をご確認のうえ、もう一度お試しください。'
        : message || '送信を完了できませんでした。通信環境をご確認のうえ、もう一度お試しください。');
    } finally {
      resetTurnstile();
      form.classList.remove('is-loading');
      if (button) button.textContent = original;
    }
  });
})();
