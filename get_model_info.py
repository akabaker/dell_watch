#!/usr/bin/python -tt
from parseomsa import ParseOmsa

def main(models, output_dir):
	"""
	Create object for each model, writing yaml file for model

	"""
	for model in models:
		obj = ParseOmsa(model)
		obj.bios_version()
		obj.perc_versions()
		obj.write_yaml(output_dir)

if __name__ == "__main__":
	models = ['2950', 'r710', 'r900', 'r910']
	output_dir = '/var/www/html/pub/dell-yaml/'
	main(models, output_dir)
