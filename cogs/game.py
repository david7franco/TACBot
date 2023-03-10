import asyncio
import random
from discord.ext import commands


class Game(commands.Cog):
    """ 
    game commands for a discord bot
    """

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} ready')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    async def roll(self, ctx):
        # can be used 1 time, every 2 seconds per user
        # randomly rolls between 1 and 10,000
        roll = random.randint(1, 10000)
        await ctx.send(f'{ctx.message.author.name} rolled {roll}')

    @commands.command(aliases=['roll2'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def duel(self, ctx):
        # can be used 1 time, every 5 seconds per user
        # Random number roll 1v1 game

        player1 = ctx.message.author.name
        player2 = ctx.message.mentions[0].name
        player1_roll = random.randint(1, 100)
        player2_roll = random.randint(1, 100)
        roll_diff = abs(player1_roll - player2_roll)

        await ctx.send(f'```{player1} rolled {player1_roll}\n{player2} rolled {player2_roll}```')
        if player1_roll == player2_roll:
            await ctx.send(f'```Draw, no winner```')
        elif player1_roll > player2_roll:
            await ctx.send(f'```{player1} wins with a difference of {roll_diff}```')
        else:
            await ctx.send(f'```{player2} wins with a difference of {roll_diff}```')

    @commands.command(aliases=['r'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def react(self, ctx):
        # waits for the user to react with the same emoji the Bot used
        
        await ctx.send('React using 🍆 within 5 seconds')
        # checks the author of the reaction and which reaction emoji they used
        def check(reaction, user):
            return user == ctx.message.author and reaction.emoji == '🍆'

        # wait 5 seconds to see if the user that ran the command has reacted with the correct emoji
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=5.0, check=check)
        except asyncio.TimeoutError as e:
            await ctx.channel.send(f'Too slow!')
        else:
            await ctx.channel.send('Well done')
        
async def setup(client):
    await client.add_cog(Game(client))
