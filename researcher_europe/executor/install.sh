#!/usr/bin/env bash
# Install stage EU's executor on an always-on Ubuntu server (Oracle Cloud Always Free
# ARM, or any x86 VPS): IB Gateway kept logged in by IBC, a checkout of this repo, and
# two weekday timers that run eu_executor.py. See researcher_europe/executor/README.md.
#
# Run as the normal login user (ubuntu on Oracle), not as root:
#   bash install.sh
# It asks for what it needs; or set these beforehand to run without questions:
#   IB_USER IB_PASSWORD IBKR_ACCOUNT_ID IBKR_ENVIRONMENT(paper|live) GITHUB_TOKEN
#   EXECUTOR_PUSH_LOG(1|0)
# Re-running is safe: every step checks what is already there.
set -euo pipefail

REPO_URL="https://github.com/robertsben333-cmyk/claude_research.git"
HOME_DIR="$HOME/eu-executor"
REPO_DIR="$HOME_DIR/claude_research"
VENV="$HOME_DIR/venv"
IBC_DIR="/opt/ibc"
JTS="$HOME/Jts"
IBC_HOME="$HOME/ibc"
ARCH="$(uname -m)"

say() { printf '\n== %s\n' "$*"; }
ask() { local var="$1" prompt="$2" secret="${3:-}"; if [ -z "${!var:-}" ]; then
          if [ -n "$secret" ]; then read -rsp "$prompt: " "$var"; echo; else read -rp "$prompt: " "$var"; fi; fi; }

[ "$(id -u)" -ne 0 ] || { echo "run this as your normal user (it uses sudo where needed), not as root"; exit 1; }

say "Questions (nothing is sent anywhere except IBKR and GitHub)"
ask IB_USER "IBKR username of the DEDICATED EU account (its own login)"
ask IB_PASSWORD "IBKR password for that username" secret
ask IBKR_ENVIRONMENT "paper or live (start with paper)"
case "$IBKR_ENVIRONMENT" in paper|live) ;; *) echo "must be paper or live"; exit 1;; esac
ask IBKR_ACCOUNT_ID "Account number (DU... for paper, U... for live)"
ask GITHUB_TOKEN "GitHub fine-grained token for robertsben333-cmyk/claude_research (Contents: read, or read+write to push logs)" secret
ask EXECUTOR_PUSH_LOG "Push daily logs to the eu-ibkr-log branch? 1 = yes (token needs write), 0 = no"

say "System packages"
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git python3-venv python3-pip xvfb unzip curl jq \
  libxtst6 libxrender1 libxi6 libgtk-3-0 libasound2t64 2>/dev/null || \
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git python3-venv python3-pip xvfb unzip curl jq \
  libxtst6 libxrender1 libxi6 libgtk-3-0 libasound2

say "Swap (IB Gateway wants about 1 GB of memory)"
if ! swapon --show | grep -q /swapfile; then
  sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile >/dev/null && sudo swapon /swapfile
  grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
fi

JAVA_DIR=""
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
  say "Java 17 with JavaFX for ARM (Azul Zulu), because IBKR's installer bundles an x86 Java"
  if [ ! -x /opt/zulu17/bin/java ]; then
    URL=$(curl -fsSL "https://api.azul.com/metadata/v1/zulu/packages/?java_version=17&os=linux&arch=aarch64&archive_type=tar.gz&java_package_type=jre&javafx_bundled=true&latest=true&release_status=ga&availability_types=CA&page_size=1" | jq -r '.[0].download_url')
    [ -n "$URL" ] && [ "$URL" != "null" ] || { echo "could not find an Azul Zulu 17 FX JRE for aarch64"; exit 1; }
    curl -fsSL "$URL" -o /tmp/zulu17.tar.gz
    sudo mkdir -p /opt/zulu17 && sudo tar -xzf /tmp/zulu17.tar.gz -C /opt/zulu17 --strip-components=1
  fi
  JAVA_DIR=/opt/zulu17
  /opt/zulu17/bin/java -version 2>&1 | head -1
fi

say "IB Gateway (stable)"
if ! ls -d "$JTS"/ibgateway/[0-9]* >/dev/null 2>&1; then
  curl -fsSL https://download2.interactivebrokers.com/installers/ibgateway/stable-standalone/ibgateway-stable-standalone-linux-x64.sh -o /tmp/ibgw.sh
  if [ -n "$JAVA_DIR" ]; then
    INSTALL4J_JAVA_HOME_OVERRIDE="$JAVA_DIR" sh /tmp/ibgw.sh -q
  else
    sh /tmp/ibgw.sh -q
  fi
fi
GW_VER=$(ls -d "$JTS"/ibgateway/[0-9]* | sort -V | tail -1 | xargs basename)
echo "IB Gateway version $GW_VER in $JTS/ibgateway/$GW_VER"

say "IBC (logs the gateway in and restarts it nightly)"
if [ ! -x "$IBC_DIR/gatewaystart.sh" ]; then
  IBC_URL=$(curl -fsSL https://api.github.com/repos/IbcAlpha/IBC/releases/latest | jq -r '.assets[] | select(.name | test("IBCLinux.*zip")) | .browser_download_url' | head -1)
  curl -fsSL "$IBC_URL" -o /tmp/ibc.zip
  sudo mkdir -p "$IBC_DIR" && sudo unzip -oq /tmp/ibc.zip -d "$IBC_DIR"
  sudo chmod +x "$IBC_DIR"/*.sh "$IBC_DIR"/scripts/*.sh
  sudo chown -R "$USER" "$IBC_DIR"
fi
mkdir -p "$IBC_HOME/logs"
umask 077
cat > "$IBC_HOME/config.ini" <<EOF
IbLoginId=$IB_USER
IbPassword=$IB_PASSWORD
TradingMode=$IBKR_ENVIRONMENT
FIX=no
ReadOnlyApi=no
AcceptIncomingConnectionAction=accept
AcceptNonBrokerageAccountWarning=yes
AllowBlindTrading=yes
ExistingSessionDetectedAction=primary
ReloginAfterSecondFactorAuthenticationTimeout=yes
SecondFactorAuthenticationTimeout=180
AutoRestartTime=11:45 PM
ColdRestartTime=07:05
TrustedTwsApiClientIPs=127.0.0.1
CommandServerPort=0
EOF
umask 022
chmod 600 "$IBC_HOME/config.ini"
# point IBC's start script at what we installed
sed -i \
  -e "s|^TWS_MAJOR_VRSN=.*|TWS_MAJOR_VRSN=$GW_VER|" \
  -e "s|^IBC_INI=.*|IBC_INI=$IBC_HOME/config.ini|" \
  -e "s|^TRADING_MODE=.*|TRADING_MODE=$IBKR_ENVIRONMENT|" \
  -e "s|^TWOFA_TIMEOUT_ACTION=.*|TWOFA_TIMEOUT_ACTION=restart|" \
  -e "s|^IBC_PATH=.*|IBC_PATH=$IBC_DIR|" \
  -e "s|^TWS_PATH=.*|TWS_PATH=$JTS|" \
  -e "s|^LOG_PATH=.*|LOG_PATH=$IBC_HOME/logs|" \
  -e "s|^JAVA_PATH=.*|JAVA_PATH=${JAVA_DIR:+$JAVA_DIR/bin}|" \
  "$IBC_DIR/gatewaystart.sh"

say "This repository and the Python environment"
mkdir -p "$HOME_DIR"
git config --global credential.helper store
umask 077
printf 'https://x-access-token:%s@github.com\n' "$GITHUB_TOKEN" > "$HOME/.git-credentials"
umask 022
if [ ! -d "$REPO_DIR/.git" ]; then
  git clone -q --depth 50 "$REPO_URL" "$REPO_DIR"
else
  git -C "$REPO_DIR" fetch -q origin main && git -C "$REPO_DIR" checkout -q -B main origin/main
fi
[ -d "$VENV" ] || python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q ib_async requests pyyaml

say "Settings file for the executor (readable by you only)"
sudo tee /etc/eu-executor.env >/dev/null <<EOF
IBKR_ACCOUNT_ID=$IBKR_ACCOUNT_ID
IBKR_ENVIRONMENT=$IBKR_ENVIRONMENT
EXECUTOR_PUSH_LOG=$EXECUTOR_PUSH_LOG
EXECUTOR_HOME=$HOME_DIR
EXECUTOR_REPO=$REPO_DIR
EOF
sudo chown "$USER" /etc/eu-executor.env && sudo chmod 600 /etc/eu-executor.env

say "systemd: the gateway, and two weekday timers in Amsterdam time"
sudo tee /etc/systemd/system/ibgateway.service >/dev/null <<EOF
[Unit]
Description=IB Gateway under IBC (stage EU executor)
After=network-online.target
Wants=network-online.target

[Service]
User=$USER
ExecStart=/usr/bin/xvfb-run -a $IBC_DIR/gatewaystart.sh -inline
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF
for job in flatten open; do
  sudo tee /etc/systemd/system/eu-$job.service >/dev/null <<EOF
[Unit]
Description=Stage EU executor: $job
After=ibgateway.service

[Service]
Type=oneshot
User=$USER
EnvironmentFile=/etc/eu-executor.env
ExecStart=$VENV/bin/python $REPO_DIR/researcher_europe/executor/eu_executor.py $job
TimeoutStartSec=7200
EOF
done
sudo tee /etc/systemd/system/eu-flatten.timer >/dev/null <<'EOF'
[Unit]
Description=Stage EU: sell yesterday's book, weekdays 15:35 Amsterdam

[Timer]
OnCalendar=Mon..Fri 15:35 Europe/Amsterdam
AccuracySec=30s

[Install]
WantedBy=timers.target
EOF
sudo tee /etc/systemd/system/eu-open.timer >/dev/null <<'EOF'
[Unit]
Description=Stage EU: buy today's book once the Routine hands it over, from 16:00 Amsterdam

[Timer]
OnCalendar=Mon..Fri 16:00 Europe/Amsterdam
AccuracySec=30s

[Install]
WantedBy=timers.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now ibgateway.service
sudo systemctl enable --now eu-flatten.timer eu-open.timer

say "Done. Approve the IBKR login on your phone now (IBKR Mobile push)."
echo "Then, after a minute:"
echo "  $VENV/bin/python $REPO_DIR/researcher_europe/executor/eu_executor.py check"
echo "should print 'connected (tws), account $IBKR_ACCOUNT_ID ...'."
echo "Gateway log: journalctl -u ibgateway -f    IBC log: ls $IBC_HOME/logs"
echo "Timers:      systemctl list-timers 'eu-*'"
