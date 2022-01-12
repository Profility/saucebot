<img src="https://cdn.upload.systems/uploads/yOU6zY2U.png">

# SauceBot
A Discord bot that utilizes SauceNao API to find the source of anime image.

## Getting started

You will need to have a discord bot first before cloning this repository, you can create one [here](https://discord.com/developers/applications) and copy the token. SauceBot will need the `bot` and `applications.commands` scopes selected for it to function as intended.

You will also need to have an SauceNao API Key, you can get one [here](https://saucenao.com/user.php), create an account and press the "Account" tab in the bottom,
press the API button and copy the key.

## Install

**Step 1:** Clone the repository by using `git clone https://github.com/Profility/saucebot.git`

**Step 2:** Install all the pre-requisites by using `pip install -r requirements.txt`

**Step 3:** Fill out the following inside the `config.ini` file.

```ini
[discord]
token: BOT_TOKEN

[saucenao]
api_key: SAUCENAO_APIKEY
```

**Step 4:** Run `bot.py` file and you are good to go!

## Built with
This discord bot relies on the following:
* [Python 3.10](https://www.python.org/)
* [pycord](https://github.com/Pycord-Development/pycord)
* [pysaucenao](pysaucenao)
