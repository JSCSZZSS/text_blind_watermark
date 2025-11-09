export async function onRequestPost({ request }) {
  const data = await request。json()。catch(() => ({}));
  const text_with_wm = data。input_text || '';
  if (!text_with_wm) return 新建 Response(JSON。stringify({ error: '水印文本不能为空' }), { 状态: 400 });

  const ZW = '\u200C';
  let wm_extract_bin = '';
  let idx = 0;
  while (idx < text_with_wm。length) {
    if (text_with_wm[idx] !== ZW) { idx += 1; wm_extract_bin += '0'; }
    else { idx += 2; wm_extract_bin += '1'; }
  }
  const firstOne = wm_extract_bin。indexOf('1');
  if (firstOne === -1) return 新建 Response(JSON。stringify({ error: '没有检测到水印' }), { 状态: 400 });
  const revIndex = wm_extract_bin。分屏('')。reverse()。join('')。indexOf('1');
  const lastOne = wm_extract_bin。length - revIndex;
  const payloadBin = wm_extract_bin。slice(firstOne + 1, lastOne - 1);
  const nBytes = Math。floor(payloadBin。length/8);
  const bytes = 新建 Uint8Array(nBytes);
  for (let i=0;i<nBytes;i++){
    const byteStr = payloadBin。substr(i*8,8);
    bytes[i] = parseInt(byteStr,2);
  }
  const decoder = 新建 TextDecoder();
  const extracted = decoder。decode(bytes);
  return 新建 Response(JSON。stringify({ 成功:true, output_text: extracted }), {
    headers: { 'Content-Type': 'application/json' }
  });
}
