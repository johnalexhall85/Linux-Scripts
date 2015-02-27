import os
import sys
import sqlite3
import random
import getpass

def print_record(player):
	db = sqlite3.connect('rps.db')
	win_cursor = db.execute("SELECT * FROM games WHERE player=? AND result='win'", (player,))
	wins = len(win_cursor.fetchall())
	loss_cursor = db.execute('SELECT * FROM games WHERE player=? AND result="loss";', (player,))
	losses = len(loss_cursor.fetchall())
	tie_cursor = db.execute('SELECT * FROM games WHERE player=? AND result="tie"', (player,))
	ties = len(tie_cursor.fetchall())

	print('Your current record is', str(wins) + '-' + str(losses) + '-' + str(ties))

def get_user_choice(user_choice):
	choices = ['rock','paper','scissors','r','p','s']
	
	while user_choice not in choices:
		user_choice = input('You didn\'t choose rock, paper, or scissors. What\'s your choice? ').lower()
	
	if user_choice == 'r':
		user_choice = 'rock'
	elif user_choice == 'p':
		user_choice = 'paper'
	elif user_choice == 's':
		user_choice = 'scissors'
	
	return user_choice


def get_computer_choice():
	comp_choices = ['rock','paper','scissors']
	return comp_choices[random.randint(0,2)]


def get_result(uchoice,cpuchoice):
	if uchoice == cpuchoice:
		print('You both chose {}, it\'s a tie!'.format(uchoice))
		return 'tie'
	elif uchoice == 'rock':
		if cpuchoice == 'paper':
			print('You chose {} and the Computer chose {}, you LOSE!'.format(uchoice,cpuchoice))
			return 'loss'
		if cpuchoice == 'scissors':
			print('You chose {} and the Computer chose {}, you WIN!'.format(uchoice,cpuchoice))
			return 'win'
	elif uchoice == 'paper':
		if cpuchoice == 'rock':
			print('You chose {} and the Computer chose {}, you WIN!'.format(uchoice,cpuchoice))
			return 'win'
		if cpuchoice == 'scissors':
			print('You chose {} and the Computer chose {}, you LOSE!'.format(uchoice,cpuchoice))
			return 'loss'
	elif uchoice == 'scissors':
		if cpuchoice == 'rock':
			print('You chose {} and the Computer chose {}, you LOSE!'.format(uchoice,cpuchoice))
			return 'loss'
		if cpuchoice == 'paper':
			print('You chose {} and the Computer chose {}, you WIN!'.format(uchoice,cpuchoice))
			return 'win'


def new_game(player):
	db = sqlite3.connect('rps.db')
	usr_choice = get_user_choice(input('\nRock, paper, or scissors? ').lower())
	cpu_choice = get_computer_choice()
	result = get_result(usr_choice, cpu_choice)
	db.execute('INSERT INTO games (game_id, player, user_choice, cpu_choice, result) VALUES (?,?,?,?,?)', (1,player,usr_choice,cpu_choice,result))
	db.commit()
	db.close()
	print_record(player)
	play_again(player)


def play_again(player):
	yn = ['y','n']
	
	play_again = input('Would you like to play again [y/n]? ')
	
	while play_again not in yn:
		play_again = input('Please select y or n. Would you like to play again [y/n]? ')
	
	if play_again == 'y':
		new_game(player)
	elif play_again == 'n':
		pass


def main():
	player_name = getpass.getuser()

	db = sqlite3.connect('rps.db')
	db.execute('CREATE TABLE IF NOT EXISTS players (player_id INT, name TEXT);')
	db.execute('CREATE TABLE IF NOT EXISTS games (game_id INT, player TEXT, user_choice TEXT, cpu_choice TEXT, result TEXT);')
	db.execute('INSERT INTO players (player_id, name) VALUES (?,?);', (1, player_name))
	db.commit()
	db.close()

	print('Hi {}!'.format(player_name))
	print_record(player_name)

	new_game(player_name)


if __name__ == '__main__':
	main()