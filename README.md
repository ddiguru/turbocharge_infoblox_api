# turbocharge_infoblox_api

This repository contains the scripts used in the multi-part series of articles entitled **Turbocharge your Infoblox
RESTful calls**. 

## Installation

To run the scripts in this repo, I strongly recommend you create a Python virtual environment or venv. This can be done
as follows:

1. Download the content of the repo to a workspace

1. unzip the file from your workspace directory

   <pre>
   unzip turbocharge_infoblox_api.zip
   </pre>

1. create a Python venv

   <pre>
   python3 -m venv turbocharge_infoblox_api
   </pre>

1. launch the virtual environment

   <pre>
   cd turbocharge_infoblox_api
   source bin/activate
   </pre>

1. use PIP to install required modules

   <pre>
   pip install -r requirements.txt
   </pre>

## The scripts

* wapi-grid.py - A simple script which creates an infinite loop to fetch the WAPI grid object.
* wapi-network.py - A simple synchronous WAPI script which inserts 1024 24-bit network objects into the grid
* wapi-request.py - A WAPI script which inserts 1024 24-bit networks in a single WAPI call using the request object
* wapi-threaded.py - A WAPI script which leverages concurrency to insert 1024 24-bit networks using threads
