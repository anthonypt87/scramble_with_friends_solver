import unittest

from scramble_with_friends_solver import Board
from scramble_with_friends_solver import InvalidBoardError
from scramble_with_friends_solver import Solver


class SolverUnitTest(unittest.TestCase):

	default_valid_words = ['a', 'ape', 'cape', 'mop', 'opp', 'pea']

	def test_gets_solution(self):
		board = Board(['a'] * 16)
		solutions = self._solve_board(board)
		self.assertIn('a', solutions)

	def _solve_board(self, board, valid_words=None):
		solver = self._get_solver(board, valid_words)
		return solver.solve()

	def _get_solver(self, board, valid_words=None):
		if valid_words is None:
			valid_words = self.default_valid_words
		return Solver(board, valid_words)

	def test_gets_multiple_solutions(self):
		initial_layout = 'c a p e ' * 4
		initial_layout = initial_layout.strip()
		board = Board.build_board_from_string(
			initial_layout
		)
		solutions = self._solve_board(board)
		self.assertGreater(len(solutions), 1)
		self.assertIn('cape', solutions)
		self.assertIn('ape', solutions)

		self.assertNotIn('pea', solutions)

	def test_can_not_go_back_and_forwards_on_same_letter(self):
		board = Board([
			'z','z','z','z',	
			'z','z','z','z',	
			'z','z','z','z',	
			'p','o','z','z',	
		])
		solutions = self._solve_board(board)
		self.assertNotIn('pop', solutions)


class BoardTest(unittest.TestCase):
	def test_board_can_be_initialized_with_only_16_values(self):
		board = Board(['a'] * 16)
		self.assertRaises(InvalidBoardError, lambda: Board(['a'] * 15))
		self.assertRaises(InvalidBoardError, lambda: Board(['a'] * 17))

	def test_board_can_be_built_from_space_separated_strings(self):
		bunch_of_as = 'a ' * 16
		bunch_of_as = bunch_of_as.strip()
		board = Board.build_board_from_string(bunch_of_as)

	def test_board_can_be_get_and_set(self):
		board = Board([
			'a', 'b', 'c', 'd', 
			'e', 'f', 'g', 'h',
			'i', 'j', 'k', 'l',
			'm', 'n', 'o', 'p'
		])
		self.assertEqual(board[1,1], 'f')

	def test_board_can_get_valid_neighboring_locations(self):
		valid_locations = Board.get_valid_neighboring_locations((1, 1))
		self.assertIn((0,1), valid_locations)
		self.assertEqual(len(valid_locations), 8)

		valid_locations = Board.get_valid_neighboring_locations((0, 1))
		self.assertIn((0,0), valid_locations)
		self.assertEqual(len(valid_locations), 5)

