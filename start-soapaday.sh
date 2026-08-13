#!/bin/bash
# SOAPaDay OpenClaw gateway helper
# Preferred: systemd service (openclaw-soapaday-gateway.service)

export OPENCLAW_CONFIG_PATH=/home/openclaw/.openclaw/openclaw-soapaday.json
export OPENCLAW_WORKSPACE=/home/openclaw/.openclaw/workspace-soapaday
export OPENCLAW_GATEWAY_PORT=18790

CMD="${1:-status}"

case "$CMD" in
  start)
    echo "Starting SOAPaDay gateway via systemd..."
    systemctl --user enable --now openclaw-soapaday-gateway.service
    systemctl --user status openclaw-soapaday-gateway.service --no-pager
    ;;
  stop)
    echo "Stopping SOAPaDay gateway..."
    systemctl --user stop openclaw-soapaday-gateway.service
    ;;
  restart)
    echo "Restarting SOAPaDay gateway..."
    systemctl --user restart openclaw-soapaday-gateway.service
    systemctl --user status openclaw-soapaday-gateway.service --no-pager
    ;;
  status)
    echo "SOAPaDay OpenClaw Instance"
    echo "  Config:    $OPENCLAW_CONFIG"
    echo "  Workspace: $OPENCLAW_WORKSPACE"
    echo "  Port:      $OPENCLAW_GATEWAY_PORT"
    echo "  Bot:       @soapaday_bot"
    echo ""
    systemctl --user status openclaw-soapaday-gateway.service --no-pager 2>/dev/null || echo "Service not running. Use: $0 start"
    ;;
  logs)
    journalctl --user -u openclaw-soapaday-gateway.service -f
    ;;
  foreground)
    echo "Starting SOAPaDay gateway in foreground (port 18790)..."
    echo "Config: $OPENCLAW_CONFIG"
    echo "Workspace: $OPENCLAW_WORKSPACE"
    echo "Bot: @soapaday_bot"
    echo ""
    exec openclaw gateway --port 18790
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|logs|foreground}"
    exit 1
    ;;
esac
