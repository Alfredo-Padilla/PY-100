import re

INSTRUCTION = [
	# Memoria
	'MOV <ORG> <DST>',
	'SWP',
	'SAV',
	# Operaciones
	'ADD <ORG>',
	'SUB <ORG>',
	'NEG',
	# Control de flujo
	'JMP <ETI>',
	'JEZ <ETI>',
	'JNZ <ETI>',
	'JGZ <ETI>',
	'JLZ <ETI>'
]

# Posibles valores de <ORG> y <DST>
DIRECTIONS = [
	'ACC',
	'UP',
	'RIGHT',
	'DOWN',
	'LEFT'
	#'ANY',
	#'NIL'
]

PORTS = [
	'UP',
	'RIGHT',
	'DOWN',
	'LEFT'
]

# Aquí se almacenan las etiquetas personalizadas
TAGS = []

# Un origen puede ser:
	#	Un int
	#	El ACC
	# 	Un puerto
	# Un destino puede ser:
	#	El ACC
	# 	Un puerto

def inst_launcher(node, inst):
	print('- Lanzando inst_launcher()')
	ret = False
	
	# MOV
	if re.search('\AMOV', inst):
		ret = mov(node, inst)
	# SWP
	elif inst == 'SWP':
		ret = swp(node)	
	# SAV
	elif inst == 'SAV':
		ret = sav(node)

	# ADD
	elif re.search('\AADD', inst):
		ret = add(node, inst)
	# SUB
	elif re.search('\ASUB', inst):
		ret = sub(node, inst)
	# NEG
	elif inst == 'NEG':
		ret = neg(node)

	# JMP
	elif re.search('\AJMP', inst):
		ret = jmp(node, inst)
	# JEZ
	elif re.search('\AJEZ', inst):
		ret = jez(node, inst)
	# JNZ
	elif re.search('\AJNZ', inst):
		ret = jnz(node, inst)
	# JGZ
	elif re.search('\AJGZ', inst):
		ret = jgz(node, inst)
	# JLZ
	elif re.search('\AJLZ', inst):
		ret = jlz(node, inst)
		

	return ret

# ======= #
# MEMORIA #
# ======= #
# MOV 
def mov(node, inst):
	print('- - Lanzando mov()')
	ret = True
	org, dst, t_org, t_dst = '', '', '', ''
	
	aux = inst.split(' ')
	# Origen y tipo de origen
	try:
		org, t_org = int(aux[1]), 'int'
	except:
		if aux[1] in PORTS:
			org, t_org = aux[1], 'port'
		elif aux[1] == 'ACC':
			print('Origen acc')
			org, t_org = aux[1], 'acc'
		else:
			print('falso')
			ret = False
	
	# Destino y tipo de destino
	if aux[2] in PORTS:
		print('Destino puerto')
		dst, t_dst = aux[2], 'port'
	elif aux[2] == 'ACC':
		dst, t_dst = aux[2], 'acc'
	else:
		ret = False

	if ret:
		print('- - - Moviendo {} de {} a {}'.format(org, aux[1], dst))
		ret = node.MOV(org, dst, t_org, t_dst)

	return ret

# SWP
def swp(node):
	print('- - Lanzando swp()')
	node.SWP()
	print('- - - Intercambiado ACC por BAK')
	return True

# SAV
def sav(node):
	print('- - Lanzando sav()')
	node.SAV()
	print('- - - Escrito el ACC en BAK')
	return True

# =========== #
# OPERACIONES #
# =========== #
# ADD
def add(node, inst):
	print('- - Lanzando add()')
	ret = True
	org, t_org = '', ''
	
	aux = inst.split(' ')
	# Tipo de origen
	try:
		org, t_org = int(aux[1]), 'int'
	except:
		if aux[1] in PORTS:
			org, t_org = aux[1], 'port'
		elif aux[1] == 'ACC':
			print('Origen acc')
			org, t_org = aux[1], 'acc'
		else:
			print('falso')
			ret = False


	if ret:
		print('- - - Sumando {} de {} al ACC'.format(org, aux [1]))
		node.ADD(org, t_org)

	return ret

# SUB
def sub(node, inst):
	print('- - Lanzando sub()')
	ret = True
	org, t_org = '', ''
	
	aux = inst.split(' ')
	# Tipo de origen
	try:
		org, t_org = int(aux[1]), 'int'
	except:
		if aux[1] in PORTS:
			org, t_org = aux[1], 'port'
		elif aux[1] == 'ACC':
			print('Origen acc')
			org, t_org = aux[1], 'acc'
		else:
			print('falso')
			ret = False


	if ret:
		print('- - - Rwestando {} de {} al ACC'.format(org, aux [1]))
		node.SUB(org, t_org)

	return ret

# NEG
def neg(node):
	print('- - Lanzando neg()')
	node.NEG()
	print('- - - Valor del ACC negado')
	return True

# ====== #
# SALTOS #
# ====== #
def find_tag(node, inst):
	ret = False
	n = 0
	
	aux = inst.split(' ')[-1]+':'
	txt = node.get_text()
	if aux in node.TAGS:
		for line in range(len(txt)):
			if txt[line].endswith(aux):
				print('- - Etiqueta {} en la linea {}'.format(txt[line], line))
				n = line
				ret = True
	
	return n, ret

# JMP
def jmp(node, inst):
	print('- - Lanzando jmp()')
	ret = False

	n, ret = find_tag(node, inst)

	if ret:
		print('- - - Saltando a la instruccion {}'.format(n))
		node.JMP(n)

	return ret

# JEZ
def jez(node, inst):
	print('- - Lanzando jez()')
	ret = False

	n, ret = find_tag(node, inst)

	if ret:
		print('- - - Saltando a la instruccion {}'.format(n))
		node.JEZ(n)

	return ret

# JNZ
def jnz(node, inst):
	print('- - Lanzando jnz()')
	ret = False

	n, ret = find_tag(node, inst)

	if ret:
		print('- - - Saltando a la instruccion {}'.format(n))
		node.JNZ(n)

	return ret

# JGZ
def jgz(node, inst):
	print('- - Lanzando jgz()')
	ret = False

	n, ret = find_tag(node, inst)

	if ret:
		print('- - - Saltando a la instruccion {}'.format(n))
		node.JGZ(n)

	return ret

# JLZ
def jlz(node, inst):
	print('- - Lanzando jlz()')
	ret = False

	n, ret = find_tag(node, inst)

	if ret:
		print('- - - Saltando a la instruccion {}'.format(n))
		node.JLZ(n)

	return ret