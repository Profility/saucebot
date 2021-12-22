import typing
import discord
from ruamel.yaml import YAML
from pysaucenao import SauceNao
from discord.ext import commands
from embeds import error_embed, results_embed

with open('config.yml', 'r') as conf:
    try:
        config = YAML().load(conf)
    except:
        raise Exception("Failed to load configuration file.")

bot = commands.Bot(
    command_prefix=config['discord']['prefix'],
    help_command=None
)

@bot.event
async def on_ready():
    print(f'{bot.user} ({bot.user.id}) is connected to discord!')
    await bot.change_presence(activity=discord.Game(config['discord']['status']))

saucenao = SauceNao(
    api_key=config['saucenao']['api_key'],
    results_limit=config['saucenao']['results_limit'],
    min_similarity=config['saucenao']['min_similarity'],
)

@bot.command(name='sauce', aliases=['source', 'saucenao', 'get', 'search'])
async def sauce(ctx, url: typing.Optional[str]):
    try:
        if url:
            results = await saucenao.from_url(url)
        elif not url:
            if ctx.message.attachments:
                results = await saucenao.from_url(ctx.message.attachments[0].url)

        if results:
            try:
                await ctx.reply(
                    embed=results_embed(
                        database=f"[{results[0].index}]({results[0].url})",
                        similarity=f"{results[0].similarity}%",
                        author=f"[{results[0].author_name}]({results[0].author_url})",
                        title=results[0].title,
                        thumbnail=results[0].thumbnail
                    )
                )
            except Exception as e:
                await ctx.reply(
                    embed=error_embed(
                        title = "Encountered an error!",
                        description = f"""
                        Something went wrong whilst trying to reply with the results.

                        Error: {e}
                        """
                    )
                )
        else:
            await ctx.reply(
                embed=error_embed(
                    title = "No results!",
                    description = f"""
                    I can't find the source of the image, gif, or video. Maybe the results had low similarity percentage?

                    Please use other ways of finding the source either by reverse image searching or using other source locators like [trace.moe](https://trace.moe) or by creating a post in [r/SauceSharingCommunity](https://www.reddit.com/r/SauceSharingCommunity/).
                    """
                )
            )
    except Exception as e:
        await ctx.reply(
            embed=error_embed(
                title = "API Error!",
                description = f"""
                Failed to get results from the image, gif, or video.

                Error: {e}
                """
            )
        )
            
bot.run(config['discord']['token'])