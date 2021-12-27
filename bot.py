import typing
import discord
import logging
from utils import embeds
from utils.config import config
from pysaucenao import SauceNao
from discord.ext import commands
from urllib.request import getproxies

log = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

bot = commands.Bot(
    command_prefix=config['discord']['prefix'],
    help_command=None
)

@bot.event
async def on_ready():
    log.info(f'Logged in: {bot.user} ({bot.user.id})')
    await bot.change_presence(activity=discord.Game(config['discord']['status']))

saucenao = SauceNao(
    api_key=config['saucenao']['api_key'],
    results_limit=config['saucenao']['results_limit'],
    min_similarity=config['saucenao']['min_similarity'],
    proxy=getproxies()
)

@bot.command(name="help")
async def help(ctx):
    await ctx.reply(
        embed = embeds.help_embed()
    )

@bot.command(name='sauce', aliases=config['discord']['aliases'])
async def sauce(ctx, url: typing.Optional[str]):
    try:
        if url:
            results = await saucenao.from_url(url)
        elif not url:
            if ctx.message.attachments:
                results = await saucenao.from_url(ctx.message.attachments[0].url)
            else:
                await ctx.reply(
                    embed=embeds.help_embed()
                )
                return
    except Exception as e:
        await ctx.reply(
            embed=embeds.error_embed(
                title = "API Error!",
                description = f"""
                Failed to get results from the image, gif, or video.\n\n**Error:** {e}
                """
            )
        )
    try:
        await ctx.reply(
            embed=embeds.results_embed(
                database=f"[{results[0].index}]({results[0].url})",
                similarity=f"{results[0].similarity}%",
                author=f"[{results[0].author_name}]({results[0].author_url})",
                title=results[0].title,
                thumbnail=results[0].thumbnail
            )
        )
    except IndexError:
        await ctx.reply(
            embed=embeds.error_embed(
                title = "No Results!",
                description = f"""
                I can't find the source of the image, gif, or video. Maybe the results had low similarity percentage?\n\nPlease use other ways of finding the source either by reverse image searching or using source locators like [SauceNao](https://saucenao.com/) and [trace.moe](https://trace.moe) or by creating a post in [r/SauceSharingCommunity](https://www.reddit.com/r/SauceSharingCommunity/).
                """
            )
        )
            
bot.run(config['discord']['token'])