import sqlite3
import result

class DB:

	def __init__(self):
		self.connection = sqlite3.connect("LottoMax_results.db")
		self.cursor = self.connection.cursor()
		self.data = self.cursor.execute("SELECT * FROM results").fetchall()

	def add_result(self, result_object):
		if self.check_for_double(result_object.date):
			command = ("INSERT INTO results VALUES ("
						f"'{result_object.date}',"
						f"'{result_object.winning_combo}',"
						f"'{result_object.bonus}',"
						f"'{result_object.extra}',"
						f"'{result_object.prize}',"
						f"'{result_object.maxi_combos}')")
			self.cursor.execute(command)
			self.connection.commit()
			print(f"Result of {result_object.date} saved in databased!")
		else:
			print(f"Result of {result_object.date} is already in DB.")

	def check_for_double(self, new_date):
		for result in self.data:
			if result[0] == new_date:
				return False
		return True

	def fetch_all_winning_combo(self):
		self.data = self.cursor.execute("SELECT winning_combo FROM results").fetchall()
		self.arrange_win_combo_to_array()
		return self.data

	def arrange_win_combo_to_array(self):
		new_data = []
		for result in self.data:
			new_data.append(result[0].strip('[]').split(', '))
		self.data = new_data
