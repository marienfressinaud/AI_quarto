# -*- coding: utf-8 -*-

class Piece:
	'''
	A piece is represented by:
	* a color (blue or red)
	* a size (small or large)
	* a shape (round or square)
	* a consistency (hole or full)
	'''

	def __init__(self, properties):
		'''
		Initalizes a Piece
		'''
		self.color = properties['color']
		self.size = properties['size']
		self.shape = properties['shape']
		self.consistency = properties['consistency']