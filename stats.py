import database

db = database.DB()

def enumerate_sort(results, reverse = False):
	n = len(list(results))
	print(list(results))
	for i in range(n - 1):
		for j in range(0, n - i - 1):
			if reverse == False:
				if results[j][1] > results[j + 1][1]:
					results[j], results[j + 1] = results[j + 1], results[j]
			elif reverse == True:
				if results[j][1] < results[j + 1][1]:
					results[j], results[j + 1] = results[j + 1], results[j]
	return results



def get_top_numbers(order):
	data = db.fetch_all_winning_combo()
	results = [0] * 50
	for winning_combo in data:
		for number in winning_combo:
			results[int(number) - 1] += 1
	results = list(enumerate(results))
	print(results)
	results = enumerate_sort(results) if order == 1 else enumerate_sort(results, reverse = True)
	return results