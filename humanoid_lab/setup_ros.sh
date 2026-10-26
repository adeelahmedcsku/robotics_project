#!/usr/bin/env bash
set -euo pipefail
. /etc/os-release
if [ "${ID:-}" != "ubuntu" ] || [ "${VERSION_ID:-}" != "24.04" ]; then
  echo 'This installer is for Ubuntu 24.04 only.' >&2
  exit 1
fi
sudo apt update
sudo apt install -y software-properties-common curl python3-venv
sudo add-apt-repository -y universe
python3 - <<'PY'
import json
import urllib.request
api = 'https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest'
release = json.load(urllib.request.urlopen(api))
assets = [x for x in release['assets'] if x['name'].startswith('ros2-apt-source_')
          and x['name'].endswith('.noble_all.deb')]
if len(assets) != 1:
    raise SystemExit('No unique Noble ROS 2 apt source asset; inspect official releases')
url = assets[0]['browser_download_url']
if not url.startswith('https://github.com/ros-infrastructure/ros-apt-source/releases/'):
    raise SystemExit('Unexpected download origin')
print('Official asset:', url)
urllib.request.urlretrieve(url, '/tmp/robotics-ros2-apt-source.deb')
PY
sudo dpkg -i /tmp/robotics-ros2-apt-source.deb
sudo apt update
sudo apt install -y ros-jazzy-desktop ros-dev-tools python3-colcon-common-extensions
echo 'Next: source /opt/ros/jazzy/setup.bash'
