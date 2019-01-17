import json, sys, os, requests, time, calendar
from urllib2 import urlopen, HTTPError, URLError
from optparse import OptionParser
from datetime import datetime, timedelta
from mysql import MySQL
import concurrent.futures
