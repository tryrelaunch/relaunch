// Maps plan tier names to Stripe Price IDs (test mode)
const PRICE_IDS = {
  starter: 'price_1TTqNlP1XFF6NaBoEakSDPe3',
  growth: 'price_1TTqO6P1XFF6NaBo6qMV0Xfa',
  full_service: 'price_1TTqOhP1XFF6NaBoNfjleuHK'
};

// Lightweight rate limit (resets on cold start, fine at our scale)
const hits = new Map();
const WINDOW_MS = 60 * 1000;
const MAX_PER_WINDOW = 10;

exports.handler = async function (event) {

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }

  // Rate limit by IP
  const ip = (event.headers['x-nf-client-connection-ip']
    || (event.headers['x-forwarded-for'] || '').split(',')[0].trim()
    || 'unknown');

  const now = Date.now();
  const record = hits.get(ip) || { count: 0, resetAt: now + WINDOW_MS };
  if (now > record.resetAt) {
    record.count = 0;
    record.resetAt = now + WINDOW_MS;
  }
  record.count++;
  hits.set(ip, record);

  if (record.count > MAX_PER_WINDOW) {
    return {
      statusCode: 429,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Too many requests. Try again in a minute.' })
    };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  const { plan, email, businessName, slackEmail, firstName, lastName, phone, domainChoice, currentDomain, registrar, newDomain } = body;

  if (!plan || !email) {
    return { statusCode: 400, body: 'Missing plan or email' };
  }

  const priceId = PRICE_IDS[plan];
  if (!priceId) {
    return { statusCode: 400, body: 'Invalid plan' };
  }

  const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
  if (!STRIPE_SECRET_KEY) {
    console.error('STRIPE_SECRET_KEY not configured');
    return { statusCode: 500, body: 'Payment system not configured' };
  }

  // Determine origin so we redirect back to the right place
  const origin = event.headers.origin
    || (event.headers.referer ? new URL(event.headers.referer).origin : null)
    || 'https://tryrelaunch.com';

  // Build form-encoded body for Stripe API
  const params = new URLSearchParams();
  params.append('mode', 'subscription');
  params.append('line_items[0][price]', priceId);
  params.append('line_items[0][quantity]', '1');
  params.append('customer_email', email);
  params.append('success_url', `${origin}/onboard.html?paid=true&session_id={CHECKOUT_SESSION_ID}`);
  params.append('cancel_url', `${origin}/onboard.html?cancelled=true`);
  params.append('allow_promotion_codes', 'true');
  params.append('billing_address_collection', 'auto');

  // Stash all the prospect details as metadata so we can retrieve them after payment
  if (businessName) params.append('metadata[business_name]', String(businessName).slice(0, 500));
  if (firstName) params.append('metadata[first_name]', String(firstName).slice(0, 100));
  if (lastName) params.append('metadata[last_name]', String(lastName).slice(0, 100));
  if (phone) params.append('metadata[phone]', String(phone).slice(0, 50));
  if (slackEmail) params.append('metadata[slack_email]', String(slackEmail).slice(0, 200));
  if (domainChoice) params.append('metadata[domain_choice]', String(domainChoice).slice(0, 50));
  if (currentDomain) params.append('metadata[current_domain]', String(currentDomain).slice(0, 200));
  if (registrar) params.append('metadata[registrar]', String(registrar).slice(0, 100));
  if (newDomain) params.append('metadata[new_domain_request]', String(newDomain).slice(0, 200));
  params.append('metadata[plan]', plan);

  // Subscription metadata so it shows up on the subscription record too
  if (businessName) params.append('subscription_data[metadata][business_name]', String(businessName).slice(0, 500));
  params.append('subscription_data[metadata][plan]', plan);

  try {
    const response = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: params.toString()
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Stripe API error:', response.status, err);
      return { statusCode: 502, body: 'Stripe error' };
    }

    const session = await response.json();

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ url: session.url })
    };

  } catch (err) {
    console.error('create-checkout-session error:', err.message);
    return { statusCode: 500, body: `Internal error: ${err.message}` };
  }
};
