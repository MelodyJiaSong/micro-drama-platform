/**
 * The Origin the Vite dev proxy forwards to the backend (follow-up 239).
 *
 * The backend admits a write only from its own origin (`libs/common/origin.py`).
 * The dev page is served from the Vite port, so the proxy rewrites the Origin of
 * the page's OWN requests to the backend's; every other Origin — another site the
 * browser has open, `null` from a sandboxed frame — is forwarded unchanged and the
 * backend refuses it. The hook used to rewrite unconditionally, which made the dev
 * server an open relay: any page could POST to 127.0.0.1:5174/api/… and arrive at
 * the backend looking same-origin.
 *
 * `devPort` is the port the request arrived on (`req.socket.localPort`), so a dev
 * server started with `--port` keeps working. A request without an Origin stays
 * without one, and the backend refuses it if it is a write (SEC-ORIGIN-HOST-01).
 */
export function forwardedOrigin(
  origin: string | undefined,
  devPort: number | undefined,
  backendOrigin: string,
): string | undefined {
  if (origin === undefined || devPort === undefined) return origin;
  const own = [`http://127.0.0.1:${devPort}`, `http://localhost:${devPort}`];
  return own.includes(origin) ? backendOrigin : origin;
}
