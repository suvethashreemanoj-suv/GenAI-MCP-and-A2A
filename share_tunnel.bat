@echo off
REM Share CV Agent without opening Windows Firewall (uses outbound tunnel)
echo.
echo === CV Agent Tunnel Setup (no firewall change needed) ===
echo.
echo STEP 1: Keep this running in another terminal:
echo        python main.py
echo.
echo STEP 2: Pick ONE option below:
echo.

where cloudflared >nul 2>&1
if %errorlevel%==0 (
    echo [A] cloudflared ^(recommended^)
    echo     cloudflared tunnel --url http://127.0.0.1:8003
    echo.
)

where ngrok >nul 2>&1
if %errorlevel%==0 (
    echo [B] ngrok
    echo     ngrok http 8003
    echo.
)

echo [C] localtunnel ^(needs Node.js^)
echo     npx localtunnel --port 8003
echo.

echo STEP 3: Copy the HTTPS URL you get, e.g. https://abc-xyz.trycloudflare.com
echo.
echo STEP 4: Add to your .env:
echo        CV_AGENT_PUBLIC_URL=https://YOUR-TUNNEL-URL
echo.
echo STEP 5: Share with your friend for their ML agent .env:
echo        CV_AGENT_URL=https://YOUR-TUNNEL-URL/process
echo.
echo STEP 6: Friend tests in browser:
echo        https://YOUR-TUNNEL-URL/
echo.
pause
