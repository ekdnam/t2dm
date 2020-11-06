if __name__ == '__main__':
	fileobj = open('data/params.txt', 'r')
	rawData = []
	for line in fileobj:
		rawData.append(line)
	print(rawData)
	modified_data = []
	for data in rawData:
		data = data.replace("\n", "")
		data = data.split("+")
		print(data)
		modified_data.append(data)
		# print(type(data))
	print("new list is")
	# print(rawData)
	for data in modified_data:
		print(data)

	# for data_list in modified_data:
	# 	for info in data_list:
	result = []
	result = sum(modified_data, [])
	for data in result:
		print(data)

	modified_data = []
	[modified_data.append(x) for x in result if x not in modified_data]
	print(modified_data)

	with open("data/fields.txt", "w") as writefileobj:
		for item in modified_data:
			writefileobj.write("{}\n".format(item))

	print("process completed!!!")


