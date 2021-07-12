from os import system
import data_collection
import result
import stats

class Menu:

	def __init__(self):
		self.PURPLE = '\033[95m'
		self.LIGHT_BLUE = '\033[94m'
		self.CYAN = '\033[96m'
		self.GREEN = '\033[92m'
		self.ORANGE = '\033[93m'
		self.RED = '\033[91m'
		self.ENDC = '\033[0m'
		self.BOLD = '\033[1m'
		self.UNDERLINE = '\033[4m'

	def clear(self):
		system("clear")

	def print_error(self, error):
		self.clear()
		print(self.BOLD + self.RED + "ERROR: " + self.ENDC + error)

	def print_menu(self, txt, choice_list=["\n"]):
		self.clear()
		print(self.CYAN + txt + "\n\n")
		i = 1
		for choice in choice_list:
			print(self.CYAN + str(i) + " - " + self.GREEN + choice)
			i += 1
		print("\n\n")
		choice = self.get_input("int", end=len(choice_list))
		return choice

	def get_input(self, rule , end=0):
		uinput = input(" : ")
		if rule == "int":
			if self.verif_nmbr(uinput, rule, end):
				return int(uinput)
			else:
				self.print_error("Wrong input!")
				return False

	def verif_nmbr(self, uinput, rule, end):
		if rule == "int":
			if uinput.isdigit():
				if int(uinput) <= end:
					return True
		else:
			self.print_error("Wrong input!")
			return False

	def print_result(self, result_title, result_list):
		self.clear()
		print(self.CYAN + "Results for" + self.BOLD + result_title + "\n")
		i = 1
		for result in result_list:
			print(self.CYAN + str(i) + " - " + self.GREEN + str(result))
			i += 1
		input("Press enter to continue...")

menu = Menu()

choices = ['Print all data', 'Print top numbers', 'Scan for results']#, 'Scan for new results', ''
while 1:
	user_choice = menu.print_menu("Type the row # to choose: " ,choices)

	if user_choice == 1:
		menu.print_result("Winning combo list: ", stats.db.fetch_all_winning_combo())

	if user_choice == 2:
		order_choice = menu.print_menu("Choose an order: ", ['Ascending order', 'Descending order'])
		print_list = []
		for result in stats.get_top_numbers(order_choice):
			print_list.append('Number ' + str(result[0] + 1) + ' - ' + str(result[1]) + ' times.')
		menu.print_result("Top numbers: ", print_list)

	if user_choice == 3:
		
		data_collection.scan()
