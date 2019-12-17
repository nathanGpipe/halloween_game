#!/usr/bin/env python3
import sys
from abc import ABCMeta, abstractmethod
from watchers.observer import *
from random import random, choice


class House(Observer):
	def __init__(self):
		self.population = (int)(0+(random()*11))
		self.monsters = [choice((Vampire, Ghoul, Zombie, Werewolf))(self) for i in range(self.population)]
		
	def update(self, obj, arg):
		print(type(obj).__name__ + " cured!")
		self.i = self.monsters.index(obj)
		self.monsters.remove(obj)
		self.monsters.insert(self.i, Person(self, arg))
		
	def showMonsters(self):
		for mon in self.monsters:
			sys.stdout.write((type(mon).__name__) + " ")
		sys.stdout.write("\n")

class Neighborhood():
	def __init__(self):
		self.houses = [[House() for j in range(0,5)] for i in range(0,5)]
		
	def lookBothWays(self, player):
		for house in self.houses[player.pos[0]]:
			print("")
		
	def showNeighborhood(self):
		for street in self.houses:
			print("-------------------------------------------")
			for house in street:
				house.showMonsters()
				
	def percentCured(self):
		totalMonsters = 0
		totalCured = 0
		for street in self.houses:
			for house in street:
				for mon in house.monsters:
					totalMonsters = totalMonsters+1
					if type(mon).__name__ == "Person":
						totalCured = totalCured+1
		print("Cured: " + str(totalCured) + "\nTotal: " + str(totalMonsters))
		return int(100*(totalCured/totalMonsters))
		
class Player():
	def __init__(self):
		self.hp = (int)(200+(random()*200))
		self.weapons = [choice((NerdBomb, SourStraw, ChocolateBar))() for i in range(10)]
		#self.weapons.append(HersheyKiss())
		self.pos = [0, 0]
		
	def showWeapons(self):
		for candy in self.weapons:
			sys.stdout.write((type(candy).__name__) + " ")
		sys.stdout.write("\n")
		
	def attack(self, weapon, house):
		self.damageMod = weapon.damageMod()
		for mon in house.monsters:
			mon.defend(int((10+(random()*11))*self.damageMod), weapon, self)
		
class Weapon(object):
	def __init__(self):
		self.uses = -1
		self.att_mod = 1
	
	def damageMod(self):
		if self.uses != 0:
			self.uses = self.uses - 1
			return self.att_mod
		return 0

class HersheyKiss(Weapon):
	def __init__(self):
		super(HersheyKiss, self).__init__()

class NerdBomb(Weapon):
	def __init__(self):
		self.uses = 1;
		self.att_mod = (5+(random()*6))

class SourStraw(Weapon):
	def __init__(self):
		self.uses = 4;
		self.att_mod = (4+(random()*2))

class ChocolateBar(Weapon):
	def __init__(self):
		self.uses = 8;
		self.att_mod = (2+(random()*2))

class Monster(Observable):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def attack(self, player):
		pass
	
	def defend(self, damage, wep, player):
		vuln = 1
		for tup in self.vulnerability:
			if tup[0] == type(wep).__name__:
				vuln = tup[1]
				
		self.hp = self.hp - (damage * vuln)
		if self.hp <= 0:
			self.update(player)
		else:
			self.attack(player)

class Vampire(Monster):
	def __init__(self, observer):
		super(Vampire, self).__init__()
		self.add_observer(observer)
		self.name = "Vampire"
		self.vulnerability = [("ChocolateBar", 0)]
		self.hp = (int)(100+(random()*101))
		
	def attack(self, player):
		player.hp = player.hp - (int)(10+(random()*11))

class Ghoul(Monster):
	def __init__(self, observer):
		super(Ghoul, self).__init__()
		self.add_observer(observer)
		self.name = "Ghoul"
		self.vulnerability = [("NerdBomb", 5)]
		self.hp = (int)(40+(random()*41))
		
	def attack(self, player):
		player.hp = player.hp - (int)(15+(random()*16))

class Zombie(Monster):
	def __init__(self, observer):
		super(Zombie, self).__init__()
		self.add_observer(observer)
		self.name = "Zombie"
		self.vulnerability = [("SourStraw", 2)]
		self.hp = (int)(50+(random()*51))
		
	def attack(self, player):
		player.hp = player.hp - (int)(0+(random()*11))
		

class Werewolf(Monster):
	def __init__(self, observer):
		super(Werewolf, self).__init__()
		self.add_observer(observer)
		self.name = "Werewolf"
		self.vulnerability = [("ChocolateBar", 0), ("SourStraw", 0)]
		self.hp = 200
		
	def attack(self, player):
		player.hp = player.hp - (int)(0+(random()*41))
		

class Person(Monster):
	def __init__(self, observer, player):
		super(Person, self).__init__()
		self.add_observer(observer)
		self.name = "Person"
		self.vulnerability = [("HersheyKiss", 0), ("SourStraw", 0), ("ChocolateBar", 0), ("NerdBomb", 0)]
		self.hp = 100
		self.attack(player)
		
	def attack(self, player):
		player.hp = player.hp + (1+(random()*10))

class Game():
	
	def __init__(self):
		self.neighborhood = Neighborhood()
		self.player = Player()
		self.over = False
	
	def command(self, com):
		house = self.neighborhood.houses[self.player.pos[0]][self.player.pos[1]]
		if com == 'help':
			print('''List of commands:
look 
	- describes which directions you can move in, along with what monsters are in the house in front of you
inventory 
	- shows what candy you have avalible
status
	- shows you your current health
move <north, south, east, west> <number of spaces> 
	- moves you through the neighborhood
attack <inventory slot> 	
	- attacks the monsters in the house in front of you with the candy chosen
exit
	- close the game without saving''')
		elif com == 'exit':
			sys.exit()
			
		elif com == 'look':
			sys.stdout.write("To the west ")
			if self.player.pos[1]-1 < 0:
				sys.stdout.write("you see the edge of the forest, better not go that way.\n")
			else:
				sys.stdout.write("you see more of the neighborhood.\n")
			
			sys.stdout.write("To the east ")
			if self.player.pos[1]+1 >= 5:
				sys.stdout.write("you see the edge of the forest, better not go that way.\n")
			else:
				sys.stdout.write("you see more of the neighborhood.\n")
				
			sys.stdout.write("To the north ")
			if self.player.pos[0]+1 >= 5:
				sys.stdout.write("you see the edge of the forest, better not go that way.\n")
			else:
				sys.stdout.write("you see more of the neighborhood.\n")
				
			sys.stdout.write("To the south ")
			if self.player.pos[0]-1 < 0:
				sys.stdout.write("you see the edge of the forest, better not go that way.\n")
			else:
				sys.stdout.write("you see more of the neighborhood.\n")
				
			sys.stdout.write("The house ahead of you contains " + str(house.population) + " monsters.\n")
			sys.stdout.write("You see:\n")
			for mon in house.monsters:
				print(type(mon).__name__ + "\t\t\tHP: " + str(mon.hp));
			
		elif com[:4] == 'move':
			try:
				if com[4:] == ' north':
					if self.player.pos[0]+1 < len(self.neighborhood.houses):
						self.player.pos[0] = self.player.pos[0] + 1
			
				elif com[4:] == ' south':
					if self.player.pos[0]-1 >= 0:
						self.player.pos[0] = self.player.pos[0] - 1
			
				elif com[4:] == ' east':
					if self.player.pos[1]+1 < len(self.neighborhood.houses[0]):
						self.player.pos[1] = self.player.pos[1] + 1
			
				elif com[4:] == ' west':
					if self.player.pos[1]-1 >= 0:
						self.player.pos[1] = self.player.pos[1] - 1
			except ValueError:
				print("Whoops that wasn't quite right")
			print(self.player.pos)
		
		elif com[:6] == 'attack':
			index = -1
			try:
				index = int(com[6:]) - 1
			except ValueError:
				index = -1
				print("Whoops that wasn't quite right")
			
			try:
				if index >= 0:
					self.player.attack(self.player.weapons[index], house)
				else:
					self.player.attack(HersheyKiss(), house)
			except IndexError:
				print("Invalid inventory slot")
				
			if self.player.hp <= 0:
				self.over = True
		
		elif com == 'inventory':
			i = 1
			print("Slot 0 - an infinite stash of HersheyKisses")
			for wep in self.player.weapons:
				sys.stdout.write("Slot " + str(i) + " - ")
				sys.stdout.write((type(wep).__name__) + ": " + str(wep.uses) + " uses\n")
				i = i+1
		
		elif com == 'status':
			sys.stdout.write("Health: " + str(self.player.hp) + "\n")
			sys.stdout.write("Percent cured: " + str(self.neighborhood.percentCured()) + "\n")
		
			
game = Game()

print("Type 'help' for a list of commands")
while not game.over:
	com = input("> ")
	game.command(com)

if game.player.hp <= 0:
	print("Game over! You were slain")
else:
	print("You won!")
