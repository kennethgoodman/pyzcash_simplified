# https://z.cash/blog/snark-explain3/

"""

	We need a way to enforce that Alice does in fact send E(P(s)) and not a random value
	
"""
import random
from functools import reduce

def get_factors(n):   
	""" https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python#6800214 """ 
	return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def randomly_pick_a_point_in_fp(p):
	return random.randint(1, p)

class Integer_Finite_Field:
	def __init__(self, p):
		self.p = p
		self.generators = self.get_generators()

	def get_generators(self):
		def test_for_gen(gen):
			n = (self.p - 1) // 2
			n = int(n)
			return gen**2 != 1 and gen**n != 1
		possible_generators = get_factors(self.p - 1)
		return list(filter(test_for_gen, possible_generators))

	def pick_random_gen(self):
		return random.choice(self.generators)

	def __eq__(self, other):
		return self.p == other.p

class Integer_Finite_Field_Element:
	def __init__(self, value, field):
		self.value = value
		self.field = field

	def __mul__(self, other):
		if not isinstance(other, int):
			other = other.value
		return Integer_Finite_Field_Element((other ** self.value) % self.field.p, self.field)

	def __repr__(self):
		return "Integer_Finite_Field_Element(" + str(self.value) + ")"

	def __eq__(self, other):
		return self.value == other.value and self.field == other.field

class Bob:
	def __init__(self, field):
		self.field = field
		self.alpha = self.a = None

	def randomly_pick_a_point_in_fp(self):
		alpha = randomly_pick_a_point_in_fp(self.field.p)
		self.alpha = Integer_Finite_Field_Element(alpha, self.field)
		return self.alpha

	def randomly_pick_a_generator(self):
		self.a = Integer_Finite_Field_Element(self.field.pick_random_gen(), self.field)
		return self.a

	def get_b(self):
		return self.alpha * self.a

class Alice:
	def __init__(self, field):
		self.field = field

	def get_a_b_prime(self, a, b):
		""" b_prime = gamma * b = gamma * alpha * a = alpha * (gamma * a) = alpha * a_prime """
		gamma = randomly_pick_a_point_in_fp(self.field.p)
		gamma = Integer_Finite_Field_Element(gamma, self.field)
		return gamma * a, gamma * b


def KC_test(Bob, Alice):
	alpha = Bob.randomly_pick_a_point_in_fp()
	a = Bob.randomly_pick_a_generator()
	b = Bob.get_b() # alpha * a
	a_prime, b_prime = Alice.get_a_b_prime(a, b)
	return b_prime == alpha * a_prime


def test_generate_true_proof():
	p = 191
	field = Integer_Finite_Field(p)
	B = Bob(field)
	A = Alice(field)
	print(KC_test(B, A))

if __name__ == '__main__':
	test_generate_true_proof()

