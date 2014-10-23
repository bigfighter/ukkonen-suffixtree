#!/usr/bin/env python3

def make_stree(t):
	'''Constructs a suffix tree in linear time, using Ukkonen's algorithm.

	This method is an implementation of algorithm 2 from
	Esko Ukkonen's paper "On-line construction of suffix trees".

	Example use:
		root = make_stree('cacao')
		print(root.get_debug_string())

	Expected output:
		0: (1,2) "ca"
		1:    (3,inf) "cao"
		2:    (5,inf) "o"
		3: (2,2) "a"
		4:    (3,inf) "cao"
		5:    (5,inf) "o"
		6: (5,inf) "o"

	For more information about Ukkonen's algorithm, see
	https://en.wikipedia.org/wiki/Ukkonen%27s_algorithm and
	http://www.cs.helsinki.fi/u/ukkonen/SuffixT1withFigs.pdf
	'''

	INF = float('inf')

	class State():

		def __init__(self):
			self.g = {}
			self.f = None

		def get_debug_string(self):
			result = []
			def impl(self, indent=0):
				for k, p, s in sorted(self.g.values()):
					substring = t[k:len(t) if p == INF else int(p)+1]
					result.append('%s(%s,%s) "%s" ' % (' '*3*indent, k, p, substring))
					impl(s, indent=indent+1)
			impl(self)
			return '\n'.join('%i: %s' % (i, v) for i, v in enumerate(result))

	def update(s, k, i):
		oldr = root
		(end_point, r) = test_and_split(s, k, i-1, t[i])
		while not end_point:
			r_prime = State()
			r.g[t[i]] = (i, INF, r_prime)
			if oldr != root:
				oldr.f = r
			oldr = r
			(s, k) = canonize(s.f, k, i-1)
			(end_point, r) = test_and_split(s, k, i-1, t[i])
		if oldr != root:
			oldr.f = s
		return (s, k)

	def test_and_split(s, k, p, char):
		if k <= p:
			k_prime, p_prime, s_prime = s.g[t[k]]
			if char == t[k_prime+p-k+1]:
				return (True, s)
			else:
				r = State()
				k_prime, p_prime, s_prime = s.g.pop(t[k_prime])
				s.g[t[k_prime]] = (k_prime, k_prime+p-k, r)
				r.g[t[k_prime+p-k+1]] = (k_prime+p-k+1, p_prime, s_prime)
				return (False, r)
		else:
			k_prime, p_prime, s_prime = s.g.get(char, (None, None, None))
			return (k_prime is not None, s)

	def canonize(s, k, p):
		if p < k:
			return (s, k)
		else:
			k_prime, p_prime, s_prime = s.g[t[k]]
			while p_prime - k_prime <= p - k:
				k += p_prime - k_prime + 1
				s = s_prime
				if k <= p:
					k_prime, p_prime, s_prime = s.g[t[k]]
		return (s, k)

	root = State()
	bot = State()
	root.f = bot
	for i, v in enumerate(set(t)):
		bot.g[v] = (-i-1, -i-1, root)
	s = root
	k = 1
	t = ' ' + t # python indexes are 0-based, but the algorithm is 1-based
	for i in range(1, len(t)):
		(s, k) = update(s, k, i)
		(s, k) = canonize(s, k, i)
	return root

def test():
	print(make_stree('cacao').get_debug_string().split() == '''0: (1,2) "ca"
1:    (3,inf) "cao"
2:    (5,inf) "o"
3: (2,2) "a"
4:    (3,inf) "cao"
5:    (5,inf) "o"
6: (5,inf) "o"'''.split())
	print(make_stree('mississippi$').get_debug_string().split() == '''0: (1,inf) "mississippi$"
1: (2,2) "i"
2:    (3,5) "ssi"
3:       (6,inf) "ssippi$"
4:       (9,inf) "ppi$"
5:    (9,inf) "ppi$"
6:    (12,inf) "$"
7: (3,3) "s"
8:    (4,5) "si"
9:       (6,inf) "ssippi$"
10:       (9,inf) "ppi$"
11:    (5,5) "i"
12:       (6,inf) "ssippi$"
13:       (9,inf) "ppi$"
14: (9,9) "p"
15:    (10,inf) "pi$"
16:    (11,inf) "i$"
17: (12,inf) "$"'''.split())

if __name__ == '__main__':
	test()
