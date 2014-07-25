# DC-FOIA-SERVO

The District of Columbia Government announced the roll out of [a new FOIA portal](https://foia-dc.gov). This is to be commended. 

But, the portal has no API, has a funky search tool, no permalinks, and no syndication method. What's a dcdotgov watcher to do?!

Look! @DC-FOIA-SERVO to the Rescue.

## Usage
```
sudo apt-get install -y firefox
sudo apt-get install -y python-pip
sudo pip install virtual env
git clone https://github.com/vzvenyach/dc-foia-servo.git && cd dc-foia-servo
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python err.py
```

## License 
MIT