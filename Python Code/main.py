import requests 
import json
import pyttsx3
import speech_recognition as sr
import re


API_KEY = "tmV7duCfiGeD"

PROJECT_TOKEN = "tvWjTQiviORF"

RUN_TOKEN = "tTHYRt2imQKT"


# print(data)

class Data:
	"""docstring for Data """
	def __init__(self,api_key, project_token):
		self.api_key = API_KEY
		self.project_token = PROJECT_TOKEN
		self.params = {
			"api_key": self.api_key
		}
		self.get_data()

	def print_all_data(self):
		all_data = self.get_data()
		print(all_data)

	def get_data(self):
		response = requests.get(f"https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data", params = {"api_key": API_KEY})
		self.data = json.loads(response.text)
		# return self.data

	def get_total_cases(self):
		total = self.data["total"]

		for content in total:
			if content["name"] == "Coronavirus Cases:":
				return content['value']
		return "0"


	def get_total_deaths(self):
		total = self.data["total"]  

		for content in total:
			if content["name"] == "Deaths:":
				return content['value']
		return "0"


	def get_country_data(self,country):
		data_country = self.data["country"]

		for content in data_country:
			if content['name'].lower() == country.lower():
				return content
		return "0"
	def get_all_countries(self):
		countries = []
		for country in self.data["country"]:
			countries.append(country['name'].lower())
		return countries


# print(data.get_all_countries())

def speak(text):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()

def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
		except Exception as e:
			print("Exception:", str(e))
	return said.lower()

def main():
	data = Data(API_KEY,PROJECT_TOKEN)
	print("Program starting")
	END_PHRASE = "stop"
	country_list = data.get_all_countries()

	TOTAL_PATTERNS = {
					re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
					re.compile("[\w\s]+ total cases"): data.get_total_cases,
					re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
					re.compile("[\w\s]+ total deaths"): data.get_total_deaths,
					re.compile("total deaths"): data.get_total_deaths

					}


	COUNTRY_PATTERNS = {
					re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
					re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths']



					}
	

	while True:
		print("Listening...")
		text = get_audio()
		result = None
		print(text)

		for pattern, func in COUNTRY_PATTERNS.items():
			if pattern.match(text):
				words = set(text.split(" "))
				for country in country_list:
					if country in words:
						result = func(country)
						break


		for pattern, func in TOTAL_PATTERNS.items():
			if pattern.match(text):
				result = func()
				break

		if result:
			print(result)
			speak(result)


		if text.find(END_PHRASE) != -1:
			print("Exiting")
			break

main()


