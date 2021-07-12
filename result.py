import database

class Result:

	def __init__(self, date):
		self.date = date
		self.winning_combo = None
		self.bonus = None
		self.extra = None
		self.prize = None
		self.maxi_combos = []
		self.db = database.DB()

	def __str__(self):
		text = (f"Date: {self.date}\n"
				f"Winning Combo: {self.winning_combo}\n"
				f"Bonus: {self.bonus}\n"
				f"Extra: {self.extra}\n"
				f"Prize: {self.prize}\n"
				f"Maxi-Millions Combos: {self.maxi_combos}")
		return text

	def set_date(self, date):
		self.date = date

	def set_winning_combo(self, winning_combo):
		self.winning_combo = winning_combo

	def set_maxi_combos(self, maxi_combos):
		self.maxi_combos = maxi_combos

	def set_bonus(self, bonus):
		self.bonus = bonus

	def set_extra(self, extra):
		self.extra = extra

	def set_prize(self, prize):
		self.prize = prize

	def print_data(self):
		if self.db:
			self.db.data_to_results()
		else:
			return "ERROR"

	def save_result_to_db(self):
		if self.db:
			self.db.add_result(self)
		else:
			return "ERROR"

