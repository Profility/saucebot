import discord
import typing
from datetime import datetime
from utils.config import config
from discord.colour import Color

def results_embed(database: typing.Optional[str], similarity: typing.Optional[float], author: typing.Optional[str], title: typing.Optional[str], thumbnail: typing.Optional[str]):
    resultsmessage = discord.Embed(
        color=Color.green(),
        title="✅ Sauce Found!"
    )
    
    resultsmessage.timestamp = datetime.now()
    if database:
        resultsmessage.add_field(
            name="Database:",
            value=database,
            inline=False
        )

    if similarity:
        resultsmessage.add_field(
            name="Similarity:",
            value=similarity,
            inline=False
        )

    if author:
        resultsmessage.add_field(
            name="Author:",
            value=author,
            inline=False
        )

    if title:
        resultsmessage.add_field(
            name="Title:",
            value=title,
            inline=False
        )

    if thumbnail:
        resultsmessage.set_thumbnail(url=thumbnail)
        
    return resultsmessage

def error_embed(title: str, description: str):
    errormessage = discord.Embed(
        color = Color.red(),
        title = f"❌   {title}",
        description = description
    )
    
    errormessage.timestamp = datetime.now()
    
    return errormessage

def help_embed():
    helpmessage = discord.Embed(
        color = Color.lighter_gray(),
        title="Instructions on how to use SauceBot!",
        description=f"""
        Using SauceBot is very easy and straightforward, you only need to say `{config['discord']['prefix']}saucenao` along with the URL or the file of the anime image, gif, video.\n\nThere are aliases to this command, like **{', '.join(config['discord']['aliases'])}**\n\nPlease do keep in mind that results are not always accurate. To check their accuracy, please refer to the similarity percentage.\n\n**Video Demonstration:**
        """
    ).set_image(
        url = "https://cdn.upload.systems/uploads/kXz4TvKf.gif"
    )
    
    helpmessage.timestamp = datetime.now()
    
    return helpmessage