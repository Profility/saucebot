import json
import typing
import discord
import logging
from utils import embeds
from utils.config import config
from pysaucenao import SauceNao
from discord.errors import NotFound
from urllib.request import getproxies
from discord.ext import commands, pages
from pysaucenao.errors import SauceNaoException

log = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

bot = commands.Bot(
    command_prefix=json.loads(config.get("discord", "prefix")),
    help_command=None,
    case_insensitive=True
)

try:
    sauce = SauceNao(
        api_key=config.get("saucenao", "api_key"),
        results_limit=config.getint("saucenao", "results_limit"),
        min_similarity=config.getfloat("saucenao", "min_similarity"),
        proxy=getproxies()
    )
except Exception as e:
    log.error(f"Failed to initialize SauceNao object: {e}")
    
@bot.event
async def on_ready():
    log.info(f'Logged in: {bot.user} ({bot.user.id})')
    await bot.change_presence(activity=discord.Game(config.get("discord", "status")))

@bot.command(name="help")
async def help(ctx):
    await ctx.send(
        embed = embeds.help_embed()
    )
    
@bot.command(name='saucenao', aliases=json.loads(config.get("saucenao", "aliases")))
async def saucenao(ctx, src: typing.Optional[str]):
    resultsPages = []
    results = None
    try:
        if src:
            if src.startswith("<@"):
                try:
                    member = await bot.fetch_user(src.strip("<@!>"))
                except NotFound:
                    await ctx.send(
                        embed=embeds.error_embed(
                            title = "Not Found!",
                            description = "The user mentioned does not exist."
                        )
                    )
                    return
                results = await sauce.from_url(member.avatar.url)
            elif src.startswith("https://") or src.startswith("http://"):
                results = await sauce.from_url(src)
            else:
                await ctx.send(
                    embed=embeds.error_embed(
                        title = "Not a URL!",
                        description = "The argument given is not a URL, please make sure that it starts with either **https://** or **https://** for it to work."
                    )
                )
                return
        else:
            if ctx.message.attachments:
                results = await sauce.from_url(ctx.message.attachments[0].url)
            else:
                await ctx.send(
                    embed=embeds.help_embed()
                )
                return
        try:
            if results == None: raise IndexError
            for result in results:
                resultsPages.append(
                    embeds.results_embed(
                        database=f"[{result.index}]({result.url})",
                        similarity=f"{result.similarity}%",
                        author=f"[{result.author_name}]({result.author_url})",
                        title=result.title,
                        thumbnail=result.thumbnail,
                    ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
                )
            if len(results) > 1:
                paginator = pages.Paginator(
                    pages=resultsPages,
                    show_disabled=False,
                    show_indicator=True,
                    author_check=True
                )
                paginator.customize_button(
                    button_name="prev",
                    button_emoji="⬅️",
                )
                paginator.customize_button(
                    button_name="next",
                    button_emoji="➡️",
                )
                paginator.customize_button(
                    button_name="first",
                    button_emoji="⏪",
                )
                paginator.customize_button(
                    button_name="last",
                    button_emoji="⏩",
                )
                await paginator.send(ctx)
            else:
                await ctx.send(
                    embed=resultsPages[0]
                )
        except IndexError:
            await ctx.send(
                embed=embeds.error_embed(
                    title = "No Results!",
                    description = f"""
                    I can't find the source of the image or gif. Maybe the results had low similarity percentage?\n\nPlease use other ways of finding the source either by reverse image searching or using source locator websites like [SauceNao](https://saucenao.com/) and [trace.moe](https://trace.moe) or by creating a post in [r/SauceSharingCommunity](https://www.reddit.com/r/SauceSharingCommunity/).
                    """
                ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
            )
    except SauceNaoException as e:
        await ctx.send(
            embed=embeds.error_embed(
                title = "API Error!",
                description = f"""
                Failed to get results from the image or gif.\n\n**Error:** {e}
                """
            ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
        )

bot.run(config.get("discord", "token"))