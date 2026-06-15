# Share CV Agent Without Firewall Changes

Your firewall blocks **incoming** connections from WiFi. Tunnels fix this by making an **outbound** connection from your laptop to a relay server. Your friend connects to that relay — no firewall rule needed.

## Quick start (Cloudflare — free, no account)

**Terminal 1** — run your agent:

```powershell
cd "d:\cv agent"
python main.py
```

**Terminal 2** — install cloudflared once:

```powershell
winget install Cloudflare.cloudflared
```

Then start the tunnel:

```powershell
cloudflared tunnel --url http://127.0.0.1:8003
```

You will get a URL like:

```
https://random-words-1234.trycloudflare.com
```

**Your `.env`** — add:

```env
CV_AGENT_PUBLIC_URL=https://random-words-1234.trycloudflare.com
```

Restart `python main.py` after saving.

**Friend's ML agent `.env`:**

```env
CV_AGENT_URL=https://random-words-1234.trycloudflare.com/process
```

**Friend tests in browser:**

```
https://random-words-1234.trycloudflare.com/
```

---

## Option 2: ngrok

1. Sign up at https://ngrok.com (free)
2. `ngrok http 8003`
3. Use the `https://xxxx.ngrok-free.app` URL the same way as above

---

## Option 3: localtunnel (Node.js)

```powershell
npx localtunnel --port 8003
```

Use the printed `https://xxxx.loca.lt` URL.

---

## Option 4: No network at all (demo fallback)

If tunnels are also blocked, for the assignment demo:

1. **Screen share** while you run queries on your machine
2. **Record a video** of `python test_client.py` working
3. **Merge repos** — friend clones your CV agent code and runs both agents on one laptop:
   - CV on `8003`, ML on `8002`

---

## Why this works

```
Friend's laptop  -->  tunnel server (internet)  <--  your laptop (outbound)
                      (no inbound firewall needed)
```

Normal WiFi sharing needs:

```
Friend's laptop  -->  your laptop:8003  (BLOCKED by firewall)
```

---

## Run helper script

```powershell
.\share_tunnel.bat
```
