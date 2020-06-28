# -*- coding: utf-8 -*- 
# -*- coding: cp1251 -*-
import random
import time
import re
import discord
import os, sys
import get
from discord.ext import commands
from random import randint


game_channel_text = 679307689184198696
game_channel_voice = 676748711203831808


#Check
'''def in_channel(channel_id):
	def predicate(ctx):
		return ctx.message.channel.id == channel_id
	return commands.check(predicate)'''

def for_game_channel_text(ctx):
	return ctx.message.channel.id == game_channel_text
def for_game_channel_voice(ctx):
	return ctx.message.channel.id == game_channel_voice


#prefix
PREFIX = "!"
client= commands.Bot(command_prefix = PREFIX)
#words
message_random = ['вероятность, что','вероятность того, что','какова вероятность']

#auto_role
@client.event
async def on_member_join(member):
	channel = client.get_channel( id = 691640681248063502 )
	role= discord.utils.get(member.guild.roles, id = 691642962664226867)
	await member.add_roles(role)
	x = random.randint(1,2)
	if x == 1:
		await channel.send(embed= discord.Embed(description=f"Приветствуем{member.mention} в нашей ебанутой семье."))
	elif x == 2:
		await channel.send(embed= discord.Embed(description=f"О еще один зелёный. Ну привет,{member.mention}."))


#remove_help
@client.remove_command('help')

# On_ERROR
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.CommandNotFound):
		await ctx.send(f'Команды \"{ctx.message.content}\" не существует. Произошел CommandNotFound')
	elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
		await ctx.send('Вы не обладаете достаточным уровнем доступа для использования этой команды')
	raise error
#on_ready_bot

@client.event
async def on_ready():
	print('bot connected')
	game = discord.Game(r"Еблю с кодом")
	await client.change_presence(status=discord.Status.online, activity=game);

#talk

#mb
@client.event
async def on_message(message):
	msg = message.content.lower()
	r = 0
	while r <= (len(message_random))-1:
		#result = discord.utils.get(message_random,str= msg)
		word= message_random[r]
		message_all = re.findall(word, msg)
		r+=1
		if ((set(message_all)) & (set(message_random))):
			rand = randint(1, 100)
			await message.channel.send('Вероятность этого ' + str(rand) + ' %')
		else:
			continue
	await client.process_commands(message)














##Games


@client.command()
@commands.has_permissions()
@commands.check(for_game_channel_text)
async def start_game_mafia(ctx):
	def start_game(ctx):
		if len(gamers) < 8:
			ctx.send("Слишком мало человек")
		elif len(gamers) > 14:
			ctx.send("Слишком много человек")
		else:
			f=1
	gif_timer = discord.File('timer.gif')
	emb = discord.Embed(title="Game", color=0x309bf3)
	emb.add_field(name= "__________",value="Начата игра в Мафию! Она начнется через 2 минуты. Для участия напишите команду !user_play_mafia")
	emb.add_field(name= "__________",value="2:00")
	await ctx.send(embed=emb)
	gamers= []
	timer = 200
	while(timer >= 0):
		timer -= 1
		time.sleep(1)
		if timer == 150:
			emb = discord.Embed(title="Game", color=0x309bf3)
			emb.add_field(name= "__________",value="1:50")
			await ctx.send(embed=emb)
		elif timer == 0:
			start_game()

@client.command()
@commands.has_permissions()
@commands.check(for_game_channel_text)
async def user_play_mafia(ctx):
	await ctx.send("Команда сработала")
	if ctx.message.author.id in gamers:
		await ctx.send("Вы уже назодитесь в команде. Подождите, пока все не присоединятся")
	else:
		gamers.append(ctx.message.author.id)
		await ctx.send(f"Вы в игре и вместе с вами {len(gamers)}")
	
	

	

	
	

	


#Cmmands_help
@client.command()
@commands.has_permissions()
async def help(ctx):
	emb = discord.Embed(title = "Подходи, пообщаемся", color= 0x1cff01)
	emb.add_field(name = '{}help'.format( PREFIX ), value= 'Если тебе разъяснить что-то надо, то ты не боись. Подходи- пообщаесмся' )
	emb.add_field(name = '{}help_admin'.format( PREFIX ), value= 'То какими методами пахан те пиздов дать может')
	emb.add_field(name = '{}help_social'.format( PREFIX ), value= 'Узнаешь, что я умею' )
	emb.add_field(name = '{}hello'.format( PREFIX ), value= 'Ну здравствуй' )
	await ctx.send(embed= emb)
#!help_admin
@client.command()
@commands.has_permissions(administrator=True)
async def help_admin(ctx):
	emb = discord.Embed(title= "Навигация по командам админов", color= 0xffff01)
	emb.add_field(name = '{}user_mute'.format( PREFIX ), value= 'Мут пользователя. Синтаксис: {}user_mute @id'.format(PREFIX) )
	emb.add_field(name = '{}user_ban'.format( PREFIX ), value= 'Бан пользователя. Синтаксис: {}user_ban @id'.format(PREFIX) )
	emb.add_field(name = '{}user_kick'.format( PREFIX ), value= 'Кик пользователя. Синтаксис: {}user_kick @id'.format(PREFIX) )
	await ctx.send(embed= emb)

@client.command()
@commands.has_permissions()
async def help_social(ctx):
	emb = discord.Embed(title= "Навигация по командам админов", color= 0xfffa)
	emb.add_field(name = 'Вероятность', value= 'Узнать вероятнось, чего либо.\nНапишите: Какова вероятность... , Вероятность, что... , Вероятность того, что...' )

	await ctx.send(embed= emb)
#Command
#Command_!user_kick
@client.command()
@commands.has_permissions(administrator=True)
async def user_kick(ctx, member: discord.Member, *, reason= None):
	await ctx.channel.purge(limit = 1)
	await member.kick(reason= reason)
	await ctx.send(f'Кик игрока {member.name})')
#Command_!user_ban
@client.command()
@commands.has_permissions(administrator=True)
async def user_ban(ctx, member: discord.Member, *, reason= None):
	await ctx.channel.purge(limit = 1)
	await member.ban(reason= reason)
	await ctx.send(f'Бан игрока {member.name})')

#Command_!user_unban
@client.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(administrator=True)
async def user_unban(ctx, member: discord.Member, *, reason= None):
	await ctx.channel.purge(limit = 1)
	await member.unban(reason= reason)
	await ctx.send(f'Игрок {member.name} был разбанен')

#Command_!hello
@client.command()
@commands.has_permissions()
async def hello(ctx):
	await ctx.send(f'ДаДова {ctx.message.author.mention}')

#Command_!user_mute
@client.command()
@commands.has_permissions(administrator=True)
async def user_mute(ctx, member:discord.Member):
	roles= str(member.roles)
	await member.edit(roles=[])

	mute_role = discord.utils.get( ctx.message.guild.roles, name="mute")				#Установка роли- Мут
	await member.add_roles(mute_role)
	await ctx.send(f'У { member.mention }, ограничение чата, за нарушение прав! Все предыдущие роли были сняты.')

#Read_token.txt
'''token = os.environ.get('token-bot')'''
token = open("token.txt", 'r').readline()
client.run(token)


'''i = 0
	while i <= len(found):
		role= discord.utils.get(member.guild.roles, id=found[i])
		await member.remove_roles(role)
		await client.send("The role has been deleted!")
		i+=1
found= re.findall(r"'([^']*)'", msg)'''


#found= re.findall(r"'([^']*)'", roles)
#found = re.findall(r'id=([^id= name]*)', roles)
'''i = 1
	while i <= len(found):
		role= discord.utils.get(member.guild.roles, id=found[i])
		await member.remove_roles(role)
		await client.send("The role has been deleted!")
		i+=1'''