# Lemmy Response Bot
I'm really sorry for making this.

## About
This bot will reply to a "trigger word" with a list of user-defined responses. 

## Customisation
If you've downloaded the code and are running the python file directly, you can copy the blank ".env.example" file and rename to just ".env", then edit the internal lines with whatever you want.

If you're using docker, you can set the environment variables via docker when running the bot, i.e. `-e TRIGGER='BOT' -e RESPONSE='I AM A BOT'`, or in the compose file. The trigger word is not case sensitive.

Responses can be set via a `;` seperated list, i.e. `response 1;response 2` and so on. You can set this in the .env file if running from the code, or you use `-e RESPONSES: 'response 1;response 2 etc`. Honestly, I'm open to all better docker-suitable ideas here.

You can run this bot in "exclude" mode or in "include" mode. In Exclude mode, the bot will scan all of the instance's new comments for the matching trigger word, and community moderators can choose to opt-out by sending the bot a message in the format `#exclude community@instance.tld`. In Include mode, the bot can be locked down to a single community. While it will still scan all the new comments, it will only repsond if the comments are in the matching community. The default is Exclude mode, but you can set the environment variable INCLUDE='community@instance.tld' in the env file or add `-e INCLUDE='community@instance.tld'` in the docker command.

The bot will, by default, scan the newest 25 posts every 5 seconds. This should be enough to capture all the newest comments being generated across Lemmy at this point in time, however you can increase or decrease this as you see fit. If putting in Include mode, then set to a more realistic amount to cover that community, i.e. 10 comments every 60 seconds etc. This will depend on how busy that community is!

| Environment Variable    | Info | Docker env variable |
| -------- | ------- | ------- |
| USERNAME  | Your bot's username    |  -e USERNAME='username' |
| PASSWORD | Your bot's password     |  -e PASSWORD='password' |
| INSTANCE    | Your Lemmy instance's url without the https:// bit, i.e. `lemmy.zip`    |   -e INSTANCE='instance.tld' |
| TRIGGER   | The trigger word this bot will look for   | -e TRIGGER='trigger_word' |
| RESPONSES | The responses in a `;` seperated list your bot will randomly choose from. | -e RESPONSES='Response 1;Response 2;Response 3' |
| INCLUDE   | Leave blank for your bot to work over all communities. Set to `community@instance.tld` if you want to lock the bot down to a single community. | -e INCLUDE='community@instance.tld' |
| POLL_AMOUNT   | How many posts the bot will look at for the trigger word. | -e POLL_AMOUNT=25 |
| POLL_FREQ | How often (in seconds) the bot will scan the newest comments. | -e POLL_FREQ=5 |



## Install

**Clone Repository**

1. `git https://github.com/Demigodrick/lemmy_response_bot.git`

**Setup python virtual environment**

2. `pip install virtualenv`

**Move into community_bot folder**

3. `cd lemmy_respsonse_bot`

**Create the virtual environment**

4. `virtualenv venv`

**Active the virtual environment**

5. `source venv/bin/activate`

### Install requirements

6. `pip install -r requirements.txt`

### Configure `.env`
**Copy `env.example` to `.env`**

7. `cp .env.example .env`

**Update the .env with your details**

8. `nano .env`

# Running on a server

### Docker



### Via Screen

`sudo apt-get install screen`

`screen `

Go to where you've saved the script on the server

`python3 main.py`

Ctrl-A then D to get out of your screen

You can also build and run via docker.
