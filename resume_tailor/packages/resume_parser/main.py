#!/usr/bin/python3
import os
import joblib
import random
import json
import nltk
import warnings

import pandas as pd

from datetime import datetime, time
from time import sleep
from django.conf import settings
from pathlib import Path
from pdfminer.high_level import extract_text
from striprtf.striprtf import rtf_to_text
from nltk.parse.corenlp import CoreNLPServer, CoreNLPParser

warnings.simplefilter(action='ignore', category=FutureWarning)

from .cleaner import create_features
from .messages import messages

class ResumeParser(object):
	"""docstring for ResumeParser."""

	def __init__(self, name):
		super(ResumeParser, self).__init__()

		self.birth = datetime.now()
		self.name = str(name)
		self.server = CoreNLPServer()
		self.server.corenlp_options = ['-preload', 'ner']
		self.server.java_options = ['-mx5g']
		self.server.url = 'http://localhost:9000'

		self.bullet_feature_headings = [
			'stopword_%',
			'word_count',
			'proper_noun_%',
			'verb_%'
		]

		self.name_feature_headings = [
			'line_length',
			'word_count',
			'verb_%',
			'adj_%',
			'stopword_%',
			'punctuation_%',
			'number_%',
			'proper_noun_%',
			'symbol_count',
			'list_markers_count',
			'determiners_count',
			'name_count',
			'line_length_trans',
			'word_count_trans',
			'verb_%_trans',
			'adj_%_trans',
			'stopword_%_trans',
			'punctuation_%_trans',
			'number_%_trans',
			'proper_noun_%_trans'
		]

		self.org_feature_headings = [
			'line_length',
			 'word_count',
			 'verb_%',
			 'adj_%',
			 'stopword_%',
			 'punctuation_%',
			 'number_%',
			 'proper_noun_%',
			 'symbol_count',
			 'list_markers_count',
			 'determiners_count',
			 'name_count',
			 'company_count',
			 'line_length_trans',
			 'word_count_trans',
			 'verb_%_trans',
			 'adj_%_trans',
			 'stopword_%_trans',
			 'punctuation_%_trans',
			 'number_%_trans',
			 'proper_noun_%_trans'
		]

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

		bullet_features = numeric_only[self.bullet_feature_headings]

		# Get set of name features
		name_features = numeric_only[self.name_feature_headings]

		# Get set of company features
		org_features = numeric_only[self.org_feature_headings]

		# Classify each line of the text as either bullet or not
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

	def labeler(self, row):
		# Give final labels using Stanford's NLP Named Entity tagger to
		# supplement fill in the non-bullet items, giving the "None"
		# label to anything remaining unidentified.
		if row['is_bullet'] == 1:
			return 'Bullet'
		elif row['is_name'] == 1:
			return 'Name'
		else:
			if len(row['line']) == 1:
				return 'None'
			else:
				ents = self.ner_tagger.tag(row['line'].split())
				return ents

	def count_named_ents(self, label: str):
		skips = ['Name', 'Bullet', 'None']
		if label not in skips:
			count = sum([1 for pair in label if pair[1] != 'O'])
			return count
		else:
			return 0

	def relabeler(self, row):
	    if row['ents'] == 0 and row['label'] == 'Bullet'\
		 or row['label'] == 'Name':
	        return row['label']
	    elif row['ents'] == 1:
	        label = [ent[1].capitalize() for ent in row['label'] if ent[1] != 'O']
	        if label[0] != '':
	            return label[0]

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
		labeled_data = self.resume_out_path + self.name + '_labeled_data.csv'
		labeled.to_csv(labeled_data)

		partial = pd.read_csv(self.resume_out_path + self.name + '_labeled_data.csv', sep=',')
		# Start Stanford NLP Server
		print('Starting server...\n')
		self.server.start()
		print('Server started')


		# Instantiate a tagger
		print('Instantiating a ner tagger...')
		self.ner_tagger = CoreNLPParser(url = 'http://localhost:9000',\
		 tagtype='ner')
		print('Tagger ready.')

		print('Labeling data...')
		partial.rename({'Unnamed: 0': 'doc_line'}, axis=1, inplace=True)
		partial['label'] = partial.apply(lambda x: self.labeler(x), axis=1)
		print('Data has been labeled.\nShutting down server...')
		self.server.stop()
		print('Server shut down.')

		partial['ents'] = partial['label'].apply(lambda x: self.count_named_ents(x))
		partial['label'] = partial.apply(lambda x: self.relabeler(x), axis =1)
		# Write out labeled data
		final_labeled_data = self.resume_out_path + self.name + '_final_labeled_data.csv'
		partial.to_csv(final_labeled_data)
		print('La Machina has printed your results.')
		self.death = datetime.now()
		lifespan = self.death - self.birth
		sleep(2)
		print('La Machina read your resume in {} seconds.'\
		.format(lifespan))
		sleep(2)
		print('You\'re welcome for my service.')
		sleep(0.5)
	    # Print success message
	    # print('Success! {}'.format(random.choice(messages)))

	def say_status(self):
		status = settings.DEBUG
		return status
