import hashlib
import binascii
from ecdsa import SigningKey, NIST384p

class Transaction:
	def __init__(self):
		self.id = None
		self.input = None
		self.input = None
		self.output = None

class Output:
	def __init__(self, address, amount):
		self.address = address
		self.amount = amount

class Input:
	def __init__(self):
		self.outputId = None
		self.outputIndex = None
		self.signature = None

class UnspentOutput:
	def __init__(self, outputId, outputIndex, address, amount):
		self.outputId = outputId
		self.outputIndex = outputIndex
		self.address = address
		self.amount = amount

class UnspentOutputs:
	def __init__(self):
		self.__listUtxo = []

	def updateListUtxo(self,list):
		self.__listUtxo = list

	def newUnspentOutputs (self, transactions):
		list = []
		for transaction in transactions:
			for inpt in transaction.input:
				utxo = UnspentOutput(transaction.id, inpt.outputId, inpt.outputIndex, inpt.address, inpt.amount)
				list.append(utxo)
		self.updateListUtxo(list)

def findUnspendOutput(outputId, outputIndex, listUnspentOutputs):
	for utxo in listUnspentOutputs:
		if utxo.outputId == outputId and utxo.outputIndex == outputIndex:
			return True

def idTransaction(transaction):
	inputContents = ""
	outputContents = ""
	for inpt in transaction.inputs:
		inputContents += (inpt.outputId+inpt.outputIndex)
	for output in transaction.outputs:
		outputContents += (output.address + output.amount)
	return hashlib.sha256((str(inputContents) + str(outputContents)).encode('utf-8')).hexdigest()

def createSigningKey():
	return SigningKey.generate(curve=NIST384p)

def singningInput(transaction, inputIndex, listUnspentOutputs, key):
	inpt = transaction.inputs[inputIndex]
	data = transaction.id
	verifyingtxo = findUnspendOutput(inpt.outputId, inpt.outputIndex, listUnspentOutputs)
	return key.sing(data)

def validatingInput(input, transaction, listUnspentOutputs):
	for utxo in listUnspentOutputs:
		if input.outputIndex == utxo.outputIndex and input.outputId == utxo.outputId:
			address = utxo.address
			key = address.get_verifying_key()
			return key.verify(input.signature, transaction.id)
	return False

def validatingTransactionId(id, transaction):
	if idTransaction(transaction) == id:
		return True
	else:
		return False

