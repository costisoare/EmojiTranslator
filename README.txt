1. PREREQUISITES

You need to have python3.7 running on your machine.

The following packages need to be installed in order for the app to be able to run:

Package           Version  
----------------- ---------
boto              2.49.0   
boto3             1.9.118  
botocore          1.12.118 
bz2file           0.98     
certifi           2019.3.9 
chardet           3.0.4    
docutils          0.14     
emoji             0.5.1    
entrypoints       0.3      
gensim            3.7.1    
idna              2.8      
jmespath          0.9.4    
keyring           18.0.0   
nltk              3.4      
numpy             1.16.2   
Pillow            5.4.1    
pip               19.0.2   
pocketsphinx      0.1.15   
PyAudio           0.2.11   
python-dateutil   2.8.0    
pyttsx3           2.7      
pywin32           224      
pywin32-ctypes    0.2.0    
regex             2019.3.12
requests          2.21.0   
s3transfer        0.2.0    
scikit-learn      0.20.3   
scipy             1.2.1    
setuptools        39.0.1   
singledispatch    3.4.0.3  
six               1.12.0   
sklearn           0.0      
smart-open        1.8.0    
SpeechRecognition 3.8.1    
urllib3           1.24.1   
wxPython          4.0.4    

You can install them by running: "pip install (--user) package_name". Some of those packages are automatically installed along others, so you might
not need to install all of them manually.

You also need to install the files in the wheels directory, by running "pip install (--user) file_name.whl".

2. RUNNING THE APP

The entry point to the app is main_app.py located under EmojiTranslator/emoji_translator. Run "python main_app.py" in that directory.

Please do NOT move any of the data files, such as text files or image files, as they are all referenced relative to 
the main project directory - EmojiTranslator - and contain necessary data for the app to fully run.

3. TESTED ENVIRONMENTS

- Windows 10

4. CONTACT

For any isssues/additional information, please contact me by e-mail: constantin.soare@student.manchester.ac.uk
 