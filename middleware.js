export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};

export default function middleware(req) {
  const raw = process.env.ALLOWED_IPS || '';
  const list = raw.split(',').map(s => s.trim()).filter(Boolean);
  if (list.length === 0) return;

  const ip =
    req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ||
    req.headers.get('x-real-ip') ||
    '';

  if (ip && list.includes(ip)) return;

  return new Response(
    `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Access Restricted</title><style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Segoe UI',sans-serif;background:#1a1d4e;min-height:100vh;display:flex;align-items:center;justify-content:center}.card{background:#fff;border-radius:20px;padding:52px 48px;max-width:460px;width:90%;text-align:center;box-shadow:0 32px 80px rgba(0,0,0,.45)}.icon{font-size:3rem;margin-bottom:20px}.title{font-size:1.45rem;font-weight:800;color:#1a1d4e;margin-bottom:10px}.sub{font-size:.87rem;color:#8589b0;line-height:1.68;margin-bottom:28px}.ip{color:#cc2929;font-weight:700}.badge{display:inline-block;font-size:.66rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;background:#eef0f8;color:#8589b0;border-radius:6px;padding:6px 16px}</style></head><body><div class="card"><div class="icon">🔒</div><div class="title">Access Restricted</div><div class="sub">Your IP address <span class="ip">${ip || 'unknown'}</span> is not authorised to view this portal.<br/><br/>Please contact your Jaro Education administrator to get access.</div><div class="badge">Jaro Education Analytics Portal · Internal Use Only</div></div></body></html>`,
    { status: 403, headers: { 'Content-Type': 'text/html' } }
  );
}
