import discord
import typing
from discord.colour import Color

def results_embed(database: typing.Optional[str], similarity: typing.Optional[float], author: typing.Optional[str], title: typing.Optional[str], thumbnail: typing.Optional[str]):
    resultsmessage = discord.Embed(
        color=Color.green(),
        title="✅ Sauce Found!"
    )
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
    return discord.Embed(
        color = Color.red(),
        title = f"❌   {title}",
        description = description
    )