# Auto Tag AWS Resource

This framework can be used to automatically tag AWS resources. It uses Boto3 Python SDK library to fetch the AWS.

It tags basis on the Owner's ID who has initially created the resource and then sets the tag accordingly. 


## Configuration

Clone the repository from [aws-resource-tagging](aws-resource-tagging) and then follow the next section. 

```bash
git clone git@github.com:vijayg92/python-devops-projects.git
cd python-devops-projects/aws-resource-tagging
```

## Usage
To run this script, AWS KEY & Secret needs to be explicitly passed at run time. 
```
python3 ec2_autotag.py -h
usage: PROG [options]

Python Boto3 AWS Framework

optional arguments:
  -h, --help       show this help message and exit
  --key KEY        AWS Key
  --secret SECRET  AWS Secret

python3 ec2_autotag.py --key "XXXXXXX" --secret "XXXXXXXX"
```

## Note
This script will only support EC2 instance tagging, for now, but later I will add a couple of more options to auto tags other AWS resources too. 

## Contributing
Pull requests are welcome. 


Please make sure to update tests as appropriate.

## License
[GPLv3](https://en.wikipedia.org/wiki/GNU_General_Public_License)
