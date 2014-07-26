# Install elasticsearch
wget -qO - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
deb http://packages.elasticsearch.org/elasticsearch/1.3/debian stable main
sudo apt-get update
sudo apt-get -y install elasticsearch