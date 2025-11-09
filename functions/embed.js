export async function onRequest(context) {
  const { request } = context;
  // handle preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders() });
  }
  // only accept POST
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: corsHeaders() });
  }
  return onRequestPost(context);
}

export async function onRequestPost({ request }) {
  const data = await request.json().catch(() => ({}));
  const wm = data.watermark || '';
  const text = data.input_text || '';

  if (!text) {
    return new Response(JSON.stringify({ error: '输入文本不能为空' }), { status: 400, headers: corsHeaders() });
  }
  if (wm === undefined) {
    return new Response(JSON.stringify({ error: 'watermark 字段缺失' }), { status: 400, headers: corsHeaders() });
  }

  const encoder = new TextEncoder();
  const bytes = encoder.encode(wm);
  const bits = Array.from(bytes).map(b => b.toString(2).padStart(8, '0')).join('');
  const wm_bin = '1' + bits + '1';

  const textChars = Array.from(text);
  if (textChars.length <= wm_bin.length) {
    return new Response(JSON.stringify({ error: `文本太短，至少需要 ${wm_bin.length + 1} 个字符` }), { status: 400, headers: corsHeaders() });
  }

  const ZW = '\u200C';
  let out = '';
  for (let i = 0; i < textChars.length; i++) {
    out += textChars[i];
    if (i < wm_bin.length && wm_bin[i] === '1') out += ZW;
  }

  return new Response(JSON.stringify({ success: true, output_text: out }), {
    status: 200,
    headers: corsHeaders()
  });
}

function corsHeaders() {
  return {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };
}