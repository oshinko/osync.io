+++
date = "2018-06-19T15:00:00+09:00"
draft = false
title = "Gitbot"
tags = ["git", "gitbot", "discord", "slack"]
image = "/images/headers/gitbot.png"
+++

最新版は、 https://github.com/oshinko/gitbot をご覧ください！

## Installing on Raspbian

### Installing Python 3.6

```bash
sudo apt-get update
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
./configure
make
sudo make altinstall
```

### Installing Git

```bash
sudo apt-get install git
```

### Configuring User

```bash
sudo useradd -m -s /bin/bash git
sudo su - git
```

```bash
ssh-keygen -f $HOME/.ssh/id_rsa -C git@rasppi0w.local -q -N ""
```

```bash
python3.6 -m venv .venv
.venv/bin/python -m pip install -U -e git+https://github.com/oshinko/bot.git#egg=bot-0.0.0
.venv/bin/python -m pip install -U -e git+https://github.com/oshinko/gitbot.git#egg=gitbot-0.0.0
```

```bash
cat <<EOF> .gitbot
GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no"
GITBOT_TOKEN=YOUR_BOT_TOKEN
GITBOT_CHANNELS="#your-favorite-channel-1 #your-favorite-channel-2"
EOF
```

```bash
logout
```

### Configuring Systemd

```bash
sudo wget -O /etc/systemd/system/gitbot.service https://raw.githubusercontent.com/oshinko/gitbot/draft/gitbot.service
sudo systemctl start gitbot.service
sudo systemctl status gitbot.service
sudo systemctl enable gitbot.service
sudo service gitbot restart
```

### Cleanup (Optional)

```bash
sudo rm -r Python-3.6.5
rm Python-3.6.5.tar.xz
sudo apt-get --purge remove build-essential tk-dev
sudo apt-get --purge remove libncurses5-dev libncursesw5-dev libreadline6-dev
sudo apt-get --purge remove libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
sudo apt-get --purge remove libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
sudo apt-get autoremove
sudo apt-get clean
```
