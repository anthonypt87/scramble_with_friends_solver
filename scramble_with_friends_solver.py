import argparse
import bisect
from collections import namedtuple


# Configs
DEFAULT_DICTIONARY_LOCATION = '/usr/share/dict/words'
SOWPODS_DICTIONARY_LOCATION = 'sowpods.txt'


class InvalidBoardError(Exception):
	pass


class Solver(object):
	def __init__(self, board, sorted_valid_words):
		self._valid_words = sorted_valid_words
		self._board = board
		self._found_words_so_far = set([])

	def solve(self):
		initial_locations = self._board.get_all_locations()
		for location in initial_locations:
			self._update_words_found_starting_at_location(location)

		return self._found_words_so_far

	def _update_words_found_starting_at_location(self, location):
		stack = []

		initial_location = location
		initial_word_so_far = self._board[location]
		initial_locations_traveled = set([])
		state = self.SolutionState(initial_location, initial_word_so_far, initial_locations_traveled)

		stack.append(state)

		while stack:
			current_location, word_so_far, locations_traveled = stack.pop()
			
			if self._is_valid_word(word_so_far):
				self._found_words_so_far.add(word_so_far)

			if self._is_valid_prefix(word_so_far):
				for new_location in self._board.get_valid_neighboring_locations(current_location):

					if new_location in locations_traveled:
						continue

					new_word_so_far = word_so_far + self._board[new_location]
					new_locations_traveled = locations_traveled.copy()
					new_locations_traveled.add(current_location)
					new_state = self.SolutionState(new_location, new_word_so_far, new_locations_traveled)
					
					stack.append(new_state)
		
	SolutionState = namedtuple('SolutionState', ('current_location', 'word_so_far', 'locations_traveled'))

	def _is_valid_word(self, word):
		location_in_sorted_valid_words = bisect.bisect_left(
			self._valid_words,
			word
		)
		if location_in_sorted_valid_words >= len(self._valid_words):
			return False

		return self._valid_words[location_in_sorted_valid_words] == word

	def _is_valid_prefix(self, word):
		location_in_sorted_valid_words = bisect.bisect_left(
			self._valid_words,
			word
		)
		if location_in_sorted_valid_words >= len(self._valid_words):
			return False

		return self._valid_words[location_in_sorted_valid_words].startswith(word)


class Board(object):
	"""Boards are maps from (x,y) coordinate to values"""

	def __init__(self, values):
		"""Board are initialized with a list of 16 values representing the 4x4
		grid on the board (left to right, top to bottom), 0 indexed.
	  x ---> y,
					 |
					 |
					 v
		"""
		self._board_layout = self._get_board_layout_from_values(values)

	def _get_board_layout_from_values(self, values):
		if len(values) != 16:
			raise InvalidBoardError

		board_layout = {}
		current_character_index = 0
		for x in range(4):
			for y in range(4):
				board_layout[(x,y)] = values[current_character_index]
				current_character_index += 1

		return board_layout

	@classmethod
	def build_board_from_string(cls, string_values):
		values = string_values.split(' ')
		return cls(values)

	def __getitem__(self, location_pair):
		return self._board_layout[location_pair]

	def __setitem__(self, location_pair, value):
		self._board_layout[location_pair] = values

	@classmethod
	def get_valid_neighboring_locations(cls, location_pair):
		directions_matrix = [
			(-1, 1),
			(0, 1),
			(1, 1),
			(-1, 0),
			(1, 0),
			(-1, -1),
			(0, -1),
			(1, -1)
		]

		new_locations = []
		for direction_matrix in directions_matrix:
			new_location = (location_pair[0] + direction_matrix[0], location_pair[1] + direction_matrix[1])

			if 0 <= new_location[0] <= 3 and 0 <= new_location[1] <= 3:
				new_locations.append(new_location)

		return new_locations

	@classmethod
	def get_all_locations(self):
		all_locations = []
		for x in range(4):
			for y in range(4):
				all_locations.append(
					(x,y)
				)
		return all_locations


def get_valid_words_from_dictionary(dictionary_location):
	valid_words = []
	with open(dictionary_location) as entries:
		for entry in entries:
			normalized_entry = entry.strip().lower()

			if len(normalized_entry) <= 1:
				continue

			valid_words.append(
				normalized_entry
			)
	return sorted(valid_words)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Solve the board')
	parser.add_argument('board', metavar='N', nargs=16, help='board')
	args = parser.parse_args()

	board = Board(args.board)
	dictionary = get_valid_words_from_dictionary(SOWPODS_DICTIONARY_LOCATION)

	solver = Solver(board, dictionary)
	print solver.solve()


