<img src="https://cdn.upload.systems/uploads/2LW1xcE7.png">

### This discord bot is no longer getting maintained and will not be receiving any updates.

# SauceBot
A Discord bot that utilizes SauceNao API to find the source of anime image, you can invite the bot [here](https://top.gg/bot/923142964279115817).

## Getting started

You will need to have a discord bot first before cloning this repository, you can create one [here](https://discord.com/developers/applications) and copy the token. SauceBot will need the `bot` and `applications.commands` scopes selected for it to function as intended.

Although it's not really necessary, you can get a SauceNao API key in order to perform lots of queries, you can get one [here](https://saucenao.com/user.php), create an account and press the "Account" tab in the bottom, press the API button and copy the key. 

## Install

**Step 1:** Clone the repository by using `git clone https://github.com/Profility/saucebot.git`

**Step 2:** Install all the pre-requisites by using `pip install -r requirements.txt`

**Step 3:** Fill out the following inside the `config-example.ini` file and rename it to `config.ini` once done.

```ini
[discord]
token: BOT_TOKEN ; You will put your discord bot token here.

[saucenao]
api_key: SAUCENAO_APIKEY ; You will put your SauceNao API Key here, or you can leave it empty.
```

**Step 4:** Run `bot.py` file and you are good to go!

## Built with
This discord bot relies on the following:
* [pycord](https://github.com/Pycord-Development/pycord)
* [pysaucenao](pysaucenao)
