export async function onRequestPost({ request }) {
  const data = await request。json()。catch(() => ({}));
  const wm = data。watermark || '';
  const text = data。input_text || '';
  if (!text) return 新建 Response(JSON。stringify({ error: '输入文本不能为空' }), { 状态: 400 });
  if (wm === undefined) return 新建 Response(JSON。stringify({ error: 'watermark 字段缺失' }), { 状态: 400 });

  const encoder = 新建 TextEncoder();
  const bytes = encoder。encode(wm);
  const bits = Array。from(bytes)。map(b => b。toString(2)。padStart(8,'0'))。join('');
  const wm_bin = '1' + bits + '1';

  const textChars = Array。from(text);
  if (textChars。length <= wm_bin。length) {
    return 新建 Response(JSON。stringify({ error: `文本太短，至少需要 ${wm_bin。length + 1} 个字符` }), { 状态: 400 });
  }
  const ZW = '\u200C';
  let out = '';
  for (let i=0;i<textChars。length;i++){
    out += textChars[i];
    if (i < wm_bin。length && wm_bin[i] === '1') out += ZW;
  }
  return 新建 Response(JSON。stringify({ 成功:true, output_text: out }), {
    headers: { 'Content-Type': 'application/json' }
  });
}
