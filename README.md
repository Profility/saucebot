<img width="150" height="150" src="https://cdn.upload.systems/uploads/tlCIatyN.jpg">

# SauceBot
A Discord bot that utilizes SauceNao API to find the source of anime image, gif, or video.

## Getting started

You will need to have a discord bot first before cloning this repository, you can create one [here](https://discord.com/developers/applications) and copy the token. SauceBot will need the bot and applications.commands scopes selected for it to function as intended.

You will also need to have an SauceNao API Key, you can get one [here](https://saucenao.com/user.php), create an account and press the "Account" tab in the bottom,
press the API button and copy the key.

## Install

**Step 1:** Clone the repository by using git.

**Step 2:** Install all the pre-requisites by using `pip install -r requirements.txt`

**Step 3:** Fill out the following inside the `config.yml` file

```yml
discord:
  token: ""

saucenao:
  api_key: ""
```

**Step 4:** Run the `bot.py` file and you are good to go!

## Built with
This discord bot relies on the following:

* [Python 3.10](https://www.python.org/)
* [PyCord](https://github.com/Pycord-Development/pycord)
* [ruamel.yaml](https://pypi.org/project/ruamel.yaml/)
* [PySauceNao](pysaucenao)
