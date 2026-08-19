(() => {
  const TURNSTILE_SITE_KEY = '0x4AAAAAAESziEFBo263ZEbw';
  const TURNSTILE_ACTION = 'hdn_consultation';
  const endpoint = 'https://tnooknfyshieujolwtem.supabase.co/functions/v1/register-consultation';

  const form = document.getElementById('consultation-form');
  if (!form) return;

  const status = document.getElementById('form-status');
  const button = form.querySelector('button[type="submit"]');
  const qs = new URLSearchParams(location.search);
  let turnstileWidgetId = null;
  let turnstileToken = '';

  const ctaContext = {
    cta_source: qs.get('cta_source') || 'direct',
    cta_intent: qs.get('cta_intent') || 'general',
    cta_position: qs.get('cta_position') || 'unknown',
  };

  const attribution = {
    utm_source: qs.get('utm_source') || '',
    utm_medium: qs.get('utm_medium') || '',
    utm_campaign: qs.get('utm_campaign') || '',
    utm_content: qs.get('utm_content') || '',
    utm_term: qs.get('utm_term') || '',
    landing_page: location.href,
    referrer: document.referrer || ''
  };

  const intentTopicMap = {
    lhub: 'LINE・LHub・予約・問診・決済導線',
    sns: '集患・広告・SNS・動画',
    self_pay: '自費診療・オンライン診療',
    journey_review: '既存業務・患者導線の改善',
  };

  const preferredTopic = intentTopicMap[ctaContext.cta_intent];
  if (preferredTopic) {
    const topic = Array.from(form.querySelectorAll('input[name="consultation_topics"]')).find(
      (input) => input.value === preferredTopic
    );
    if (topic) topic.checked = true;
  }

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
    if (turnstileWidgetId !== null && window.turnstile) window.turnstile.reset(turnstileWidgetId);
  }

  const turnstileMount = document.createElement('div');
  turnstileMount.id = 'consultation-turnstile';
  turnstileMount.style.margin = '4px 0 0';
  button?.parentNode?.insertBefore(turnstileMount, button);

  window.hdnConsultationTurnstileReady = () => {
    if (!window.turnstile || turnstileWidgetId !== null) return;
    turnstileWidgetId = window.turnstile.render('#consultation-turnstile', {
      sitekey: TURNSTILE_SITE_KEY,
      action: TURNSTILE_ACTION,
      theme: 'auto',
      callback: (token) => { turnstileToken = token; clearStatus(); },
      'expired-callback': () => { turnstileToken = ''; },
      'error-callback': () => {
        turnstileToken = '';
        show('本人確認の読み込みに失敗しました。ページを再読み込みしてお試しください。');
      }
    });
  };

  const turnstileScript = document.createElement('script');
  turnstileScript.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?onload=hdnConsultationTurnstileReady&render=explicit';
  turnstileScript.async = true;
  turnstileScript.defer = true;
  document.head.appendChild(turnstileScript);

  try {
    window.gtag?.('event', 'consultation_form_view', {
      form_name: 'hdn_consultation',
      ...ctaContext,
    });
  } catch (_) {}

  let started = false;
  form.addEventListener('input', () => {
    if (started) return;
    started = true;
    try {
      window.gtag?.('event', 'consultation_form_start', {
        form_name: 'hdn_consultation',
        ...ctaContext,
      });
    } catch (_) {}
  }, { once: true });

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

    const topics = data.getAll('consultation_topics').map((value) => String(value).trim()).filter(Boolean);
    if (topics.length === 0) {
      show('相談したい内容を1つ以上選択してください。');
      return;
    }
    if (!turnstileToken) {
      show('本人確認が完了していません。確認欄が表示されるまで少し待ってから、もう一度お試しください。');
      return;
    }

    const submissionKey = form.dataset.submissionKey || createSubmissionKey();
    form.dataset.submissionKey = submissionKey;
    const payload = {
      name: String(data.get('name') || '').trim(),
      organization_name: String(data.get('organization_name') || '').trim(),
      email: String(data.get('email') || '').trim(),
      phone: String(data.get('phone') || '').trim(),
      consultation_topics: topics,
      consideration_stage: String(data.get('consideration_stage') || '').trim(),
      message: String(data.get('message') || '').trim(),
      privacy_consent: data.get('privacy_consent') === 'yes',
      submission_key: submissionKey,
      company_website: '',
      turnstile_token: turnstileToken,
      ...attribution
    };

    const original = button?.textContent || '';
    if (button) { button.disabled = true; button.textContent = '送信しています…'; }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload),
        credentials: 'omit'
      });
      let body = {};
      try { body = await response.json(); } catch (_) {}
      if (!response.ok || body.ok !== true) throw new Error(body.error_code || `HTTP_${response.status}`);

      delete form.dataset.submissionKey;
      form.reset();
      show('ご相談を受け付けました。内容を確認のうえ、HDNよりご連絡します。', 'success');
      try {
        window.gtag?.('event', 'consultation_form_submit', {
          form_name: 'hdn_consultation',
          ...ctaContext,
        });
        window.gtag?.('event', 'generate_lead', {
          event_category: 'consultation',
          event_label: 'hdn_corporate',
          ...ctaContext,
        });
      } catch (_) {}
    } catch (error) {
      const code = String(error?.message || 'UNKNOWN').replace(/[^A-Z0-9_-]/gi, '').slice(0, 40) || 'UNKNOWN';
      console.warn('Consultation submission failed:', code);
      show(`送信を完了できませんでした。エラーコード：${code}`);
    } finally {
      resetTurnstile();
      if (button) { button.disabled = false; button.textContent = original; }
    }
  });
})();
