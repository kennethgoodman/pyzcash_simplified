


"""

E(x) = g^x (mod p)
E(x + y) = g^(x+y) = g^x + g^y  = E(x) + E(y)

Alice has a P(x) of order d
Bob chooses alpha in F_p and s on P
	computes:
		V = <g, g^s, ..., g^s^d> = [ E(s**i) for i in range(d+1) ]
		V2 =<g^alpha, g^(alpha * s), ..., g^(alpha * s^d)> = [E(alpha * s^i)]
Alice computes:
	a = g^P(s) <- linear combinations of V
	b = g^(alpha * P(s)) <- linear combination of V2

Bob checks that: 
	b = a^alpha = g^P(s)^alpha = g^(P(s) * alpha) = b

"""
import random
def randomly_pick_a_point_in_fp(p):
	return random.randint(1, p)

class Finite_Integer_HH:
	def __init__(self, g, p):
		self.p = p
		self.g = g

	def linear_combination(self, hidings, alphas):
		""" E(ax + by), given E_x, E_y, a, b """
		result = 1
		for hiding, alpha in zip(hidings, alphas):
			result = (result * hiding ** alpha) % self.p
		return result

	def __call__(self, x):
		return (self.g ** x) % self.p

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

class Bob:
	def __init__(self, E, s, d):
		self.E = E
		self.s = s
		self.d = d
		self.alpha = None

	def check_verifiability(self, a, b):
		return b == (a**self.alpha) % self.E.p

	def create_hidings(self):
		V, V2 = [], []
		self.alpha = randomly_pick_a_point_in_fp(self.E.p)
		for i in range(self.d + 1):
			V.append(self.E(self.s**i))
			V2.append(self.E(self.alpha * self.s**i))
		return V, V2

def test_generate_true_proof():
	E = Finite_Integer_HH(19, 191) # random cyclic group 
	A = Alice(E, [1, 2, 3, 5]) # 1 + 2 * x + 3 * x ^2 + 5 * x^5
	s = 1
	B = Bob(E, s, A.d)
	hidings_one, hidings_two = B.create_hidings()

	E_P_s_zk_a = A.compute_E_P_s_zk(hidings_one)
	E_P_s_zk_b = A.compute_E_P_s_zk(hidings_two)
	E_P_s_full_knowledge = A.compute_E_P_s(s)
	print(E_P_s_zk_a == E_P_s_full_knowledge)
	print(B.check_verifiability(E_P_s_zk_a, E_P_s_zk_b))

if __name__ == '__main__':
	test_generate_true_proof()