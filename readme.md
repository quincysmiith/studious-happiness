# Droplet maintenance

A small example of using the Digital Ocean API to manage a wobbly server.

I have a droplet on digital ocean that for reasons sometimes freezes and 
becomes unresponsive.

This project monitors the droplet via requests and restarts the droplet if 
there is no response or if the response is not a 200 response code.
