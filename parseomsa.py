from elementtree import ElementTree
from urllib2 import urlopen, URLError, HTTPError
import re
import yaml

class ParseOmsa:
	"""Class to parse Dell's RSS feed for hardware updates"""

	def __init__(self, model):
		"""ParseOmsa

		Model is used to create the URL in which we will parse using ElementTree

		"""
		baseUrl = "http://support.dell.com/support/Downloads/rss/"
		modelUrl = "rss.aspx?c=us&cs=RC956904&l=en&s=hied&systemid=pwe_%s&deviceids=all&oscodes=RH52&osl=en" % (model)	
		self.model = model
		self.percs = {}
		self.url = baseUrl + modelUrl	
		try:
			req = urlopen(self.url)
		except URLError, e:
			print e.reason
		except HTTPError, e:
			print e.reason

		self.tree = ElementTree.parse(req)	
		self.titles = self.tree.findall("//title")
			
	def bios_version(self):
		"""Sets self.bios

		Get system bios version by searching through titles, matching against regex 'bios'.
		Once a title is found that matches BIOS, the string is split on whitespace. The string
		is then sliced, setting the last index value to self.bios. Strip() is used to clear whitespace
		
		"""
		regex = re.compile(r'bios', re.I)
		for node in self.titles:
			if regex.search(node.text):
				s = node.text.split()
				self.bios = s[-1].strip()
	
	def perc_versions(self):
		"""Sets a self.percs, a dict which contains PERC controller type and firmware version

		Get perc controllers for the systems by matching titles against the regex 'PERC'. 
		Once the titles are found, the strings are split. The key is a slice of the title 
		string, the value is the last index in the title string (firmware version).

		"""
		regex = re.compile(r'perc', re.I)
		for node in self.titles:
			if regex.search(node.text):
				key = node.text.split()
				val = key[-1].split('/')
				self.percs[' '.join(key[-4:-1])] = val[-1]
	
	def write_yaml(self):
		"""Write YAML file, containing bios version, model, and perc firmware version	
		
		Output is a YAML file, named (self.model).yaml
			
		"""
		data = {'model': self.model,
			'bios': self.bios,
			'percs': self.percs}
		
		try :
			f = open("%s.yaml" % (self.model), "w")
		except Exception, e:
			print "Oops, problem %s" % (e)
			return

		yaml_data = yaml.dump(data, default_flow_style=False)
		f.write(yaml_data)
		f.close()
