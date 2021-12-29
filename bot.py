import typing
import discord
import logging
from utils import embeds
from utils.config import config
from pysaucenao import SauceNao
from discord.ext import commands
from urllib.request import getproxies
from pysaucenao.errors import SauceNaoException

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
    
try:
    sauce = SauceNao(
        api_key=config['saucenao']['api_key'],
        results_limit=config['saucenao']['results_limit'],
        min_similarity=config['saucenao']['min_similarity'],
        proxy=getproxies()
    )
except Exception as e:
    log.error(f"Failed to initialize SauceNao object: {e}")

@bot.command(name="help")
async def help(ctx):
    await ctx.reply(
        embed = embeds.help_embed()
    )

@bot.command(name='saucenao', aliases=config['saucenao']['aliases'])
async def saucenao(ctx, url: typing.Optional[str]):
    leftButton = "\u2B05"
    rightButton = "\u27A1"
    buttons = (leftButton, rightButton)
    
    currentPage = 1
    resultsPages = []
    results = None
    try:
        if url:
            results = await sauce.from_url(url)
        else:
            if ctx.message.attachments:
                results = await sauce.from_url(ctx.message.attachments[0].url)
            else:
                await ctx.reply(
                    embed=embeds.help_embed()
                )
                return

    except SauceNaoException as e:
        await ctx.reply(
            embed=embeds.error_embed(
                title = "API Error!",
                description = f"""
                Failed to get results from the image, gif, or video.\n\n**Error:** {e}
                """
            ), delete_after=30.0
        )
        return
    
    try:
        if results == None: raise IndexError
        def checks(reaction, user):
            if user != ctx.message.author:
                return False
            if str(reaction.emoji) not in buttons:
                return False
            return True
        
        for result in results:
            resultsPages.append(
                embeds.results_embed(
                    database=f"[{result.index}]({result.url})",
                    similarity=f"{result.similarity}%",
                    author=f"[{result.author_name}]({result.author_url})",
                    title=result.title,
                    thumbnail=result.thumbnail,
                )
            )
            
        resultsEmbed = await ctx.reply(embed=resultsPages[currentPage - 1].set_footer(text=f"Page {currentPage} of {len(resultsPages)}"), delete_after=config['saucenao']['timeout'])
        
        if len(results) > 1:
            for button in buttons:
                await resultsEmbed.add_reaction(button)
            
            while True:
                reaction, user = await ctx.bot.wait_for("reaction_add", check=checks, timeout=config['saucenao']['timeout'])
                
                if reaction.emoji == leftButton:   
                    await resultsEmbed.remove_reaction(leftButton, user)
                    if currentPage != 1:
                        currentPage = currentPage - 1
                        await resultsEmbed.edit(embed=resultsPages[currentPage - 1].set_footer(text=f"Page {currentPage} of {len(resultsPages)}"))
                if reaction.emoji == rightButton:    
                    await resultsEmbed.remove_reaction(rightButton, user)
                    if currentPage != len(resultsPages):
                        currentPage = currentPage + 1
                        await resultsEmbed.edit(embed=resultsPages[currentPage - 1].set_footer(text=f"Page {currentPage} of {len(resultsPages)}"))
    except IndexError:
        await ctx.reply(
            embed=embeds.error_embed(
                title = "No Results!",
                description = f"""
                I can't find the source of the image, gif, or video. Maybe the results had low similarity percentage?\n\nPlease use other ways of finding the source either by reverse image searching or using source locators like [SauceNao](https://saucenao.com/) and [trace.moe](https://trace.moe) or by creating a post in [r/SauceSharingCommunity](https://www.reddit.com/r/SauceSharingCommunity/).
                """
            ), delete_after=30.0
        )

bot.run(config['discord']['token'])