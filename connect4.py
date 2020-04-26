import pygame
import random
import copy

def print_grid(grid):
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			print(grid[i][j], end=' ')
		print()

def drop_token(grid, index, token):
	# If the top of the column is already taken, cannot drop token
	if grid[0][index] != '.':
		return grid, True
	else:
		# Test from the bottom of the array to the top
		for j in range(len(grid)-1, -1, -1):
			if grid[j][index] == '.':
				break

		grid[j][index] = token
		return grid, False
		
# Tests to hceck if somebody won the game
def check_lines(grid, token):
	len_x = len(grid)
	len_y = len(grid[0])
	
	for i in range(0, len_x):
		for j in range(0, len_y-3):
			# x x x x
			#if grid[i][j:j+4] == [token]*4:
			if grid[i][j] == token and grid[i][j+1] == token and grid[i][j+2] == token and grid[i][j+3] == token:
				print("line won on : i "+str(i)+" j "+str(j))
				return True
	
	return False

def check_cols(grid, token):
	len_x = len(grid)
	len_y = len(grid[0])
	
	for i in range(len_x-1, 2, -1):
		for j in range(0, len_y):
			# x
			# x
			# x
			# x
			if grid[i][j] == token and grid[i-1][j] == token and grid[i-2][j] == token and grid[i-3][j] == token:
				print("column won on : i "+str(i)+" j "+str(j))
				return True

	return False
	
def check_diags(grid, token):
	len_x = len(grid)
	len_y = len(grid[0])
	
	for i in range(1, len_x-2):
		for j in range(1, len_y-1):
			# x
			#  x
			#   x
			#    x
			if j+2 <= len_y-1:
				if grid[i-1][j-1] == token and grid[i][j] == token and grid[i+1][j+1] == token and grid[i+2][j+2] == token:
					print("normal diag won on : i "+str(i)+" j "+str(j))
					return True
			#    x
			#   x
			#  x
			# x
			if j-2 >= 0:
				if grid[i-1][j+1] == token and grid[i][j] == token and grid[i+1][j-1] == token and grid[i+2][j-2] == token:
					print("inverse diag won on : i "+str(i)+" j "+str(j))
					return True
	
	return False

def check_win(grid, token):
	len_x = len(grid)
	len_y = len(grid[0])
	
	if check_diags(grid, token) or check_lines(grid, token) or check_cols(grid, token):
		return True
		
	return False

# Tests for the AI
def check_weight_immediate_win(grid, weight_list, token):
	# Make a copy of the grid to prevent the function from 
	# adding tokens for real
	test_grid = copy.deepcopy(grid)

	# If adding a token somewhere result in a win,
	# add it as the highest weight
	for index in range(len(grid[0])):
		test_grid, error = drop_token(test_grid, index, token)
		if check_win(test_grid, token):
			weight_list.append( (index, 10) )
	
	del test_grid
	
	return weight_list

def check_weight_lines(grid, x, y, weight_list, token):
	len_x = len(grid)
	len_y = len(grid[0])

	# Check for a line of two tokens
	# x [x]
	if y+1 < len_y:
		if grid[x][y+1] == token:
			# Check that there is space to add two other tokens
			if y+3 < len_y:
				# Check that the space for the other tokens are free
				# and that there are enough tokens below
				if grid[x][y+2] == '.' and grid[x][y+3] == '.':
					if (x+1 < len_x and grid[x+1][y+2] != '.') or x == len_x-1:
						weight_list.append( (y+2, 5) )
			if y-2 >= 0:
				if grid[x][y-1] == '.' and grid[x][y-2] == '.':
					if (x+1 < len_x and grid[x+1][y-1] != '.') or x == len_x-1:
						weight_list.append( (y-1, 5) )
	
	# Check for a line of three tokens
	# x [x x]
	if y+2 < len_y:
		if grid[x][y+1] == token and grid[x][y+2] == token:
			# Check that there is space to add another token
			if y+3 < len_y:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if grid[x][y+3] == '.':
					if (x+1 < len_x and grid[x+1][y+3] != '.') or x == len_x-1:
						weight_list.append( (y+3, 9) )
			if y-1 >= 0:
				if grid[x][y-1] == '.':
					if (x+1 < len_x and grid[x+1][y-1] != '.') or x == len_x-1:
						weight_list.append( (y-1, 9) )
						
	return weight_list

def check_weight_cols(grid, x, y, weight_list, token):
	len_x = len(grid)
	len_y = len(grid[0])

	# Check for a column of two tokens
	# [x]
	#  x
	if x-1 < len_x:
		if grid[x-1][y] == token:
			# Check that there is space to add two other tokens
			if x-3 >= 0:
				# Check that the space for the other tokens are free
				if grid[x-2][y] == '.' and grid[x-3][y] == '.':
					weight_list.append( (y, 5) )	

	# Check for a column of three tokens
	# [x]
	# [x]
	#  x
	if x-2 < len_x:
		if grid[x-1][y] == token and grid[x-2][y] == token:
			# Check that there is space to add another tokens
			if x-3 >= 0:
				# Check that the space for the other tokens are free
				if grid[x-3][y] == '.':
					weight_list.append( (y, 9) )

	return weight_list

def check_weight_diags(grid, x, y, weight_list, token):
	len_x = len(grid)
	len_y = len(grid[0])

	# Check for a diag of two tokens
	#   [x]
	#  x
	if x-1 >= 0 and y+1 < len_y:
		if grid[x-1][y+1] == token:
			# Check that there is space to add either two token above or three token below
			if x-3 >= 0 and y+3 < len_y:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if grid[x-2][y+2] == '.' and grid[x-3][y+3] == '.':
					if grid[x-2][y+2] != '.':
						weight_list.append( (y+2, 5) )

			if x+2 < len_x and y-2 >= 0:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if grid[x-1][y-1] == '.' and grid[x-2][y-2] == '.':
					if grid[x+2][y-1] != '.':
						weight_list.append( (y-1, 5) )
				
	#   x
	# [x]
	if x+1 < len_x and y-1 >= 0:
		if grid[x+1][y-1] == token:
			# Check that there is space to add either two token below or three token above
			if x-2 >= 0 and y+2 < len_y:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if grid[x-1][y+1] == '.' and grid[x-2][y+2] == '.':
					if grid[x-1][y+2] != '.':
						weight_list.append( (y+1, 5) )
			
			if x+3 < len_x and y-3 >= 0:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if grid[x+2][y-2] == '.' and grid[x+3][y-3] == '.':
					if grid[x+2][y-1] != '.':
						weight_list.append( (y-2, 9) )

	# Check for a diag of three tokens	
	#    [x]
	#   [x]
	#  x
	if x-2 >= 0 and y+2 < len_y:
		if grid[x-1][y+1] == token and grid[x-2][y+2] == token:
			# Check that there is space to add either one token above or one token below
			if x-3 >= 0 and y+3 < len_y:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if grid[x-2][y+3] != '.' and grid[x-3][y+3] == '.':
					weight_list.append( (y+3, 9) )
			
			if x+1 < len_x and y-1 >= 0:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if (x+2 < len_x and grid[x+2][y-1] != '.') or x == len_x-1:
					weight_list.append( (y-1, 9) )
				
	#   x
	#  [x]
	# [x]
	if x+2 < len_x and y-2 >= 0:
		if grid[x+1][y-1] == token and grid[x+2][y-2] == token:
			# Check that there is space to add either one token above or one token below
			if x-1 >= 0 and y+1 < len_y:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if grid[x][y+1] != '.' and grid[x-1][y+1] == '.':
					weight_list.append( (y+1, 9) )
			
			if x+3 < len_x and y-3 >= 0:
				# Check that the space for another token is free
				# and that there are enough tokens below
				if (x+4 < len_x and grid[x+4][y-3] != '.') or x == len_x-1:
					weight_list.append( (y-3, 9) )	

	return weight_list
	
def check_weight(grid, x, y, weight_list, token):
	weight_list = check_weight_lines(grid, x, y, weight_list, token)
	weight_list = check_weight_cols(grid, x, y, weight_list, token)
	weight_list = check_weight_diags(grid, x, y, weight_list, token)
	return weight_list

def bot(grid):
	# Array of pairs (column index, weight)
	weight_list = []
	
	# First check if there is a way to win the game with the token
	#weight_list = check_weight_immediate_win(grid, weight_list, 'x')
	
	# If there isnt, check the other cases
	if not weight_list:
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				if grid[i][j] == 'x' or grid[i][j] == 'o':
					weight_list = check_weight(grid, i, j, weight_list, grid[i][j])
	
	# If no weight, choose a random column, either next to an existing token
	# Or totally randomly
	if not weight_list:
		index_list = []
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				if grid[i][j] == 'x' or grid[i][j] == 'o':
					index_list.append(j);
		
		error = False
		while True:
			column = random.choice(index_list)
			column += random.randrange(-1, 1, 1)
			if column < 0:
				colum = 0
			if column >= len(grid[0]):
				column = len(grid[0])-1
			
			grid, error = drop_token(grid, column, 'x')
			if not error:
				break
	else:
		# Sort by first entry in the pairs inside the weight list
		sorter = lambda x: (x[1], x[0])
		weight_list_sorted = sorted(weight_list, key=sorter)
		# Get dupes of heaviest weight
		weight_list_max = []
		weight_list_max.append(weight_list_sorted[0])
		for i in range(len(weight_list_sorted)):
			if weight_list_sorted[0][1] == weight_list_sorted[i][1]:
				weight_list_max.append(weight_list_sorted[i])
			else:
				break
				
		pair = random.choice(weight_list_max)
		column = pair[0]
		grid, error = drop_token(grid, column, 'x')
	
	return grid

def main():
	# Init pygame
	pygame.init()
	pygame.display.set_mode((100, 100))
	
	# Prepare grid  
	grid = [['.' for x in range(7)] for y in range(6)]

	print("Please enter a column number: ")
	
	while True:
		try:
			for ev in pygame.event.get():
				# Window X button
				# TODO: debug
				if ev.type == pygame.QUIT:
					break
				if ev.type == pygame.KEYDOWN:
					if ev.key == pygame.K_ESCAPE:
						break
					else:
						# Check ASCII code for numbers only (1-7)
						if ev.unicode and ord(ev.unicode) in range(49,56):
							column = int(ev.unicode)-1
							print("column : "+str(column))
							grid, error = drop_token(grid, column, 'o')

							if error:
								print("Column is full, choose another\n");
							else:
								print("Player has played :")
								print()
							
								print_grid(grid)
								# Check if someone won
								if check_win(grid, 'o'):
									print("Player won")
									break
								
								print("\n\n")
								
								print("Bot has played :")
								print()
								grid = bot(grid)
								print_grid(grid)
								if check_win(grid, 'x'):
									print("AI won")
									break

		except KeyboardInterrupt:
			break

	# Exit
	pygame.quit()
	
main()