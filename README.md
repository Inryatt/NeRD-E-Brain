How to get this up and running:

# Step 1

### Step 1.1
In the "server" machine, install docker
`sudo apt install docker, docker-compose-plugin`


### Step 1.2
Download/copy the 'docker-compose.yml' in this repo into a nice place on the machine.


### Step 1.3
Open terminal, cd into wherever you downloaded it, and run
`sudo docker-compose up`
TA-DA you have the backend running :)



# Step 2

Go into the machine where you have the microphone plugged into.
Clone this repository there (You may erase the docker composefiles there)
open the requirements.txt and run the apt command there


CREATE A VENV  (or not, im not your mother)
  - `python3 -m venv venv`
  - `source venv/bin/activate`
  - 
Run 
`pip install -r requirements.txt`

and then finally
`python3 stt.py`

should work
