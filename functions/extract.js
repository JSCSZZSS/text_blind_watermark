export async function onRequest(context) {
  const { request } = context;
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders() });
  }
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: corsHeaders() });
  }
  return onRequestPost(context);
}

export async function onRequestPost({ request }) {
  const data = await request.json().catch(() => ({}));
  const text_with_wm = data.input_text || '';
  if (!text_with_wm) {
    return new Response(JSON.stringify({ error: '水印文本不能为空' }), { status: 400, headers: corsHeaders() });
  }

  const ZW = '\u200C';
  let wm_extract_bin = '';
  let idx = 0;
  while (idx < text_with_wm.length) {
    if (text_with_wm[idx] !== ZW) { idx += 1; wm_extract_bin += '0'; }
    else { idx += 2; wm_extract_bin += '1'; }
  }

  const firstOne = wm_extract_bin.indexOf('1');
  if (firstOne === -1) {
    return new Response(JSON.stringify({ error: '没有检测到水印' }), { status: 400, headers: corsHeaders() });
  }

  const revIndex = wm_extract_bin.split('').reverse().join('').indexOf('1');
  const lastOne = wm_extract_bin.length - revIndex;
  const payloadBin = wm_extract_bin.slice(firstOne + 1, lastOne - 1);
  const nBytes = Math.floor(payloadBin.length / 8);
  const bytes = new Uint8Array(nBytes);
  for (let i = 0; i < nBytes; i++) {
    const byteStr = payloadBin.substr(i * 8, 8);
    bytes[i] = parseInt(byteStr, 2);
  }
  const decoder = new TextDecoder();
  const extracted = decoder.decode(bytes);

  return new Response(JSON.stringify({ success: true, output_text: extracted }), {
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