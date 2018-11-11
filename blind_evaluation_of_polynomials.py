
"""
	https://z.cash/blog/snark-explain2
	Given Alice has a Polynomial of degree d
	Given Bob has a point, s, on the polynomial
		We want Bob to find out E(P(s))
		Without Alice telling Bob P and without Bob telling Alice about s

	Solution:
		Bob sends Alice: E(1), E(s), E(s^2), ... , E(s^d)
		Alice computs E(P(s)) from that because:
			E(ax + by) = E(x)^a * E(y)^b
			So: E(P(x)) = E(x^0)^a_0 + E(x^1)^a_1 + ... + E(x^d)^a_d
"""


class Finite_Integer_HH:
	def __init__(self, g, p):
		self.p = p
		self.g = g

	def hh(self, a, b):
		return (a * b) % self.p

	def linear_combination(self, hidings, alphas):
		""" E(ax + by), given E_x, E_y, a, b """
		result = 1
		for hiding, alpha in zip(hidings, alphas):
			result = (result * hiding ** alpha) % self.p
		return result

	def __call__(self, x):
		return (self.g ** x) % self.p

class Bob:
	def __init__(self, E, s, d):
		self.E = E
		self.s = s
		self.d = d

	def create_hidings(self):
		return [self.E(s**i) for i in range(self.d+1)]

class Alice:
	def __init__(self, E, alphas):
		self.E = E
		self.alphas = alphas
		self.d = len(alphas) - 1

	def compute_E_P_s_zk(self, hidings):
		return self.E.linear_combination(hidings, self.alphas)

	def compute_E_P_s(self, s):
		P_s = sum(self.alphas[i] * (s ** i) for i in range(self.d + 1))
		return self.E(P_s)

def test_generate_true_proof()
	E = Finite_Integer_HH(19, 191) # random cyclic group 
	A = Alice(E, [1, 2]) # 1 + 2 * x
	s = 1
	B = Bob(E, s, A.d)
	hidings = B.create_hidings()

	E_P_s_zk = A.compute_E_P_s_zk(hidings)
	E_P_s_full_knowledge = A.compute_E_P_s(s)
	print(E_P_s_zk == E_P_s_full_knowledge)

if __name__ == '__main__':
	test_generate_true_proof()

