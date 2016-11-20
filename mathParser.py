from cStringIO import StringIO

def next_token(inputstream):
	token_type, token_value = _next_token(inputstream)
	print token_type, token_value
	return token_type, token_value

def look_ahead(inputstream):
	token_type, token_value = _next_token(inputstream)
	if token_value != None:
		inputstream.seek(-len(str(token_value)),1)
	return token_type, token_value

def _next_token(inputstream):
	c = inputstream.read(1)
	if c == "":
		return None, None
	if c == "+":
		return "PLUS", "+"
	if c == "-":
		return "MINUS", "-"
	if c == "*":
		return "MULT", "*"
	if c == "/":
		return "DIV", "/"
	if c == "(":
		return "LPAREN", "("
	if c == ")":
		return "RPAREN", ")"
	if c >= '0' and c <= '9':
		chars = [c]
		while True:
			c = inputstream.read(1)
			if c == "." or (c >= '0' and c <= '9'):
				chars.append(c)
			else:
				if c != "":
					inputstream.seek(-1,1)
				s = ''.join(chars)
				try:
					number = int(s)
					return "INT", number
				except:
					try:
						number = float(s)
						return "FLOAT", number
					except:
						pass
				raise Exception("Unsupported number format")


def left(io):
	return io.getvalue()[io.tell():]

def expression(inputstream):
	print ("expr: inputstream = ", left(inputstream))
	result = term(inputstream)
	token_type, token_value = look_ahead(inputstream)
	while token_type == "PLUS" or token_type == "MINUS":
		token_type, token_value = next_token(inputstream)
		if token_type == "PLUS":
			result = result + term(inputstream)
		elif token_type == "MINUS":
			result = result - term(inputstream)
		token_type, token_value = look_ahead(inputstream)
	return result

def term(inputstream):
	print ("term: inputstream = ", left(inputstream))
	result = factor(inputstream)
	token_type, token_value = look_ahead(inputstream)
	while token_type == "MULT" or token_type == "DIV":
		token_type, token_value = next_token(inputstream)
		if token_type == "MULT":
			result = result * factor(inputstream)
		elif token_type == "DIV":
			result = float(result) / factor(inputstream)
		token_type, token_value = look_ahead(inputstream)
	return result

def factor(inputstream):
	print ("factor: inputstream = ", left(inputstream))
	neg = 1
	token_type, token_value = look_ahead(inputstream)
	if token_type == "MINUS":
		next_token(inputstream)
		neg = -1
	token_type, token_value = next_token(inputstream)
	if token_type == "INT" or token_type == "FLOAT":
		return token_value * neg
	if token_type == "LPAREN":
		result = expression(inputstream)
		token_type, token_value = next_token(inputstream)
		if token_type == "RPAREN":
			return result * neg
		raise Exception("Expected closing parenthesis but got: %s" %(token_value))
	raise Exception("Syntax error in factor: %s, %s" %(token_type, token_value))

def evaluate(string):
	s = StringIO(string.replace(" ",""))
	return expression(s)