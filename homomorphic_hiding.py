# https://z.cash/blog/snark-explain

"""
	Looking for E(x) Such That:
		if x != y:
			E(x) != E(y)
		
		if a == E(x) and b == E(y):
			there exists f, such that:
				f(E(x), E(y)) = E(x + y)
"""

class Finite_Integer_HH:
	def __init__(self, g, p):
		self.p = p
		self.g = g

	def hh(self, a, b):
		return (a * b) % self.p

	def __call__(self, x):
		return (self.g ** x) % self.p

class Simple_Zero_Knowledge_Proof:
	""" 
		proving that you know x,y such that x + y = c 
	
		Not really zero knowledge because an attack can iterate through Z to find E(i) = x

	"""
	def __init__(self, E, c):
		self.E = E
		self.c = c

	def generate_proof(self, x, y):
		return self.E(x), self.E(y)

	def validate_proof(self, E_x, E_y):
		return self.E.hh(E_x, E_y) == self.E(self.c)


def test_generate_true_proof():
	x = 3
	y = 5
	c = 8

	E = Finite_Integer_HH(19, 191) # random cyclic group 
	ZK = Simple_Zero_Knowledge_Proof(E, c)
	proof = ZK.generate_proof(x, y)
	print("true proof is", ZK.validate_proof(*proof))

def test_generate_false_proof():
	x = 3
	y = 5
	c = 9

	E = Finite_Integer_HH(19, 191) # random cyclic group 
	ZK = Simple_Zero_Knowledge_Proof(E, c)
	proof = ZK.generate_proof(x, y)
	print("false proof is", ZK.validate_proof(*proof))

if __name__ == '__main__':
	test_generate_true_proof()
	test_generate_false_proof()

