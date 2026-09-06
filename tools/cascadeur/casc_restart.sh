#!/bin/bash
# Ensure a responsive Cascadeur + in-app MCP server. Rule (user 2026-09-05): if Cascadeur is running but the
# script server does not answer (playback loop, modal dialog, hang), just kill it and start fresh — scenes are
# rebuilt by script / reloaded from the saved .casc, nothing is lost.
if ! curl -s -m 3 http://127.0.0.1:8765/health | grep -q '"ok": true'; then
  if tasklist //FI "IMAGENAME eq cascadeur.exe" 2>/dev/null | grep -qi cascadeur.exe; then
    echo "Cascadeur unresponsive -> killing"; taskkill //F //IM cascadeur.exe >/dev/null 2>&1; sleep 2
  fi
  cmd //c start "" "C:\Program Files\Cascadeur\cascadeur.exe" >/dev/null 2>&1 </dev/null; sleep 25   # detach stdio: an inherited pipe hangs any caller that pipes this script
  for i in $(seq 1 12); do "/c/Program Files/Cascadeur/cascadeur.exe" --run-script scripts.mcp.start_server >/dev/null 2>&1; sleep 5
    if curl -s -m 3 http://127.0.0.1:8765/health | grep -q '"ok": true'; then echo "MCP up (try $i)"; break; fi; done
fi
curl -s -m 3 http://127.0.0.1:8765/health; echo
# restore the window if minimized: a minimized Cascadeur never renders take_image screenshots
powershell -NoProfile -Command "Add-Type 'using System;using System.Runtime.InteropServices;public class W{[DllImport(\"user32.dll\")]public static extern bool ShowWindow(IntPtr h,int n);[DllImport(\"user32.dll\")]public static extern bool IsIconic(IntPtr h);}'; \$p=Get-Process cascadeur -ErrorAction SilentlyContinue|Select-Object -First 1; if(\$p -and [W]::IsIconic(\$p.MainWindowHandle)){[W]::ShowWindow(\$p.MainWindowHandle,9)|Out-Null; 'window restored'}" 2>/dev/null
