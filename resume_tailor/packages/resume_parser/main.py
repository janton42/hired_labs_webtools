#!/usr/bin/python3
import os
import joblib
import random
import json

import pandas as pd

from datetime import datetime
from django.conf import settings
from pathlib import Path
from pdfminer.high_level import extract_text
from striprtf.striprtf import rtf_to_text

from .cleaner import create_features
from .messages import messages

class ResumeParser(object):
	"""docstring for ResumeParser."""

	def __init__(self, name):
		super(ResumeParser, self).__init__()

		self.birth = datetime.now()
		self.name = str(name)

	def get_resume_paths(self, resume_file: str)-> str:

		self.resume_out_path = os.path.join(settings.RESUME_OUT_PATH,\
		 self.name + '/')

		os.makedirs(self.resume_out_path, exist_ok=True)
		self.resume_in_path = os.path.join(settings.BASE_DIR, resume_file)
		self.resume_file_ext = self.resume_in_path.split('.')[-1]

	def introduce_self(self):
		print('***INFORMATION***\n\
		Hi. I\'m a parser.\n\
		My name is {}.\n\
		I was born at {}\
		Here are my paths: \n\
		\tresume_in_path = "{}"\n\
		\tresume_out_path = "{}"\n\
		My resume file type is: {}'.format(\
		self.name,\
		self.birth,\
		self.resume_in_path,\
		self.resume_out_path,\
		self.resume_file_ext))

	def text_compiler(self):
		if self.resume_file_ext == 'pdf':
			text = extract_text(self.resume_in_path)
		elif self.resume_file_ext == 'rtf':
			with open(self.resume_in_path, 'r') as file:
				content = file.read()
				text = rtf_to_text(content)
		elif self.resume_file_ext == 'txt':
			with open(self.resume_in_path, 'r') as file:
				text = file.read()
		#TODO: other file types (docx, odx, etc)
		# print(text)
		# Write resume out as a plain text doc, regardless of input type,
		# with a standardized name.
		resume_text_filename = self.resume_out_path + self.name + '_resume.txt'
		with open(resume_text_filename, 'w') as f:
			f.write(text)

		df = pd.read_table(
			resume_text_filename,
			header=None,
			on_bad_lines='skip',
			skip_blank_lines=True,
			lineterminator='\n'
			)
		raw_filename = self.resume_out_path + self.name + '_out.csv'
		df.to_csv(raw_filename, header=['line'])

	def clean_text(self):
		filename = self.resume_out_path + self.name + '_out.csv'
		df = pd.read_csv(filename)
		df.drop('Unnamed: 0',axis=1, inplace=True)
		return df

	def classify_text(self, text):
	    # Build paths to the ML models
		bullet_model_path = os.path.join(settings.ML_MODELS_PATH, 'bullets.pkl')
		name_model_path = os.path.join(settings.ML_MODELS_PATH, 'names.pkl')
		org_model_path = os.path.join(settings.ML_MODELS_PATH, 'org.pkl')

		# Import the model that has already been trained and tested
		bullet_model = joblib.load(bullet_model_path)
		name_model = joblib.load(name_model_path)
		org_model = joblib.load(org_model_path)

		# Group numerical features by removing categorical ones
		cat_feat = ['line','line_nostop','line_stemmed','tagged_line']
		numeric_only = text.drop(cat_feat, axis=1)
		numeric_path = self.resume_out_path + self.name + '_numeric_only.csv'
		numeric_only.to_csv(numeric_path)

		# Get set of rfeatures used for the bullet_model. This MUST MATCH
		# the headers passed to the model during training. If not, an error
		# will be raised

		bullet_features = numeric_only[
		['stopword_percentage',
		'word_count',
		'proper_noun_percentage',
		'verb_percentage'
		]]

		# Get set of name features
		name_features = numeric_only[
		['line_length',
		'word_count',
		'verb_percentage',
		'adj_percentage',
		'stopword_percentage',
		'punctuation_percentage',
		'number_percentage',
		'proper_noun_percentage',
		'symbol_count',
		'list_markers_count',
		'determiners_count',
		'name_count',
		'line_length_trans',
		'word_count_trans',
		'verb_percentage_trans',
		'adj_percentage_trans',
		'stopword_percentage_trans',
		'punctuation_percentage_trans',
		'number_percentage_trans',
		'proper_noun_percentage_trans'
		]]

		# Get set of company features
		org_features = numeric_only[
		['line_length',
		 'word_count',
		 'verb_percentage',
		 'adj_percentage',
		 'stopword_percentage',
		 'punctuation_percentage',
		 'number_percentage',
		 'proper_noun_percentage',
		 'symbol_count',
		 'list_markers_count',
		 'determiners_count',
		 'name_count',
		 'company_count',
		 'line_length_trans',
		 'word_count_trans',
		 'verb_percentage_trans',
		 'adj_percentage_trans',
		 'stopword_percentage_trans',
		 'punctuation_percentage_trans',
		 'number_percentage_trans',
		 'proper_noun_percentage_trans'
		]]
		# Classify each line of the text as either bullets or not
		print('Reading resume...')
		bullet_classification = bullet_model.predict(bullet_features)
		name_classification = name_model.predict(name_features)
		org_classification = org_model.predict(org_features)

		# Add classification in binary (0,1) to main DataFrame
		text['is_bullet'] = bullet_classification
		text['is_name'] = name_classification
		text['is_org'] = org_classification

		# Return only the original line and the results of the automated
		# classification
		classified = text[[
		    'line',
		    'is_bullet',
		    'is_name',
		    'is_org'
		    ]]
		return classified

	def read_resume(self):
	    # Compile text from several files of the same type in a given folder
		print('Compiling text')
		self.text_compiler()
		# Remove unecessary columns
		print('Cleaning things up a bit')
		data = self.clean_text()
		# Create features for us by the ML model
		print('Creating features for La Machina')
		data = create_features(data)

		# Write out data for debugging, or for use elsewhere
		print('Writing out clean(er) data with features')
		working_data = self.resume_out_path + self.name + '_working_data.csv'
		data.to_csv(working_data)

		# Run ML model on input text with features included
		print('La Machina is reading your resume')
		labeled = self.classify_text(data)

		# Write out labeled data
		print('La Machina has printed your results.')
		labeled_data = self.resume_out_path + self.name + '_labeled_data.csv'
		labeled.to_csv(labeled_data)

	    # Print success message
	    # print('Success! {}'.format(random.choice(messages)))
