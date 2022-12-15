from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BROADCAST_CHANNEL = int(os.getenv('BROADCAST_CHANNEL'))

class DiscordAgent(object):
    def __init__(self):
        intents = discord.Intents(
            guilds=True,
            members=True,
            messages=True,
            message_content=True,
        )

        self._bot = commands.Bot(
            command_prefix="$",
            description="An example to showcase how to extract info about users",
            intents=intents
        )


@bot.command()
async def test(ctx, *args):
    print('slash_command', ctx, args)
    view = View()  # Views are managers for components
    b1, b2 = Button(emoji="🔥"), Button(emoji="💀")
    b1.callback = on_button_click
    b2.callback = on_button_click
    view.add_item(b1)
    view.add_item(b2)
    await ctx.reply('Hi !', view=view)

    @bot.command()
    async def email(self, ctx, *args):
        await ctx.reply('That functionality is not complete yet!')

    @bot.event
    async def on_button_click(interaction):
        print('button clicked!')
        await interaction.response.send_message(content='Response!')

        
    @bot.event
    async def on_ready(self):
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
        print("------")
        for guild in self.bot.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        members = '\n - '.join([member.name + ';' + str(member.id) for member in guild.members])
        print(f'Guild Members:\n - {members}')
