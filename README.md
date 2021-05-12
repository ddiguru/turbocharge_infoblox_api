# turbocharge_infoblox_api

This repository contains the scripts useed in the multi-part series of articles entitled **Turbocharge your Infoblox
RESTful calls**.

## The scripts

* wapi-grid.py - A simple script which creates an infinite loop to fetch the WAPI grid object.
* wapi-network.py - A simple synchronous WAPI script which inserts 1024 24-bit network objects into the grid
* wapi-request.py - A WAPI script which inserts 1024 24-bit networks in a single WAPI call using the request object
* wapi-threaded.py - A WAPI script which leverages concurrency to insert 1024 24-bit networks using threads
