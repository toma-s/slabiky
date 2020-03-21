# Linguistics analysis: Syllabification

## About

Application allows you to syllabify texts written in Slavic languages and analyze lengths and frequencies of occuring syllables as well as frequencies of their lengths. 

Input: 
* a text file (.txt) in Slavic language
* special case – diphtongs in Slovak language need to be replaced respectively: $(ia), &(ie), #(io), %(iu), §(ou), ě(au)

Output: 
* syllable_text.txt – a text (.txt) file containing syllabified text (all letters changed to lowercase, all special characters removed);
* syllable_lengths_text.txt – a text file (.txt) containing legths of syllables corresponding to words from syllable_text.txt file;
* syllables_multiplicity.xls – an excel table containing frequencies and lengths of all syllables occuring in the input text;
* number_of_length_of_syllables_with_repetition.xls – an excel table containing frequencies of all occuring lengths of syllables, with all syllables taken into account (tokens – i.e., if the syllable “ma” with length 2 occurs 500-times in the text, it contributes to the frequency of length two 500-times);
* number_of_length_of_syllables_without_repetition.xls – an excel table containing frequencies of all occuring lengths of syllables, only with different syllables taken into account (types – i.e., if the syllable “ma” with length 2 occurs 500-times in the text, it contributes to the frequency of length 2 only once).

Note: Texts have to be written correctly in order to get the best possible results (i.e. punctuation etc.). 
Possible known bugs: Application may not be able to distinguish all abbreviations correcly, which may cause them to appear in the results, although all abbreviations should be removed.


## Instructions for local use of the console application:

#### Before running syllabification application, you need to: 
* install Python 3.7 (compatibility with other versions of Python is possible but not guaranteed, installation instructions can be found here);
* install xlwt library for Python using pip (you can do that by entering command “python -m pip install xlwt” to your command line; pip instructions can be found here);
* download application ZIP from github by clicking „Clone or download“ and then „Download ZIP“;
* unzip/extract downloaded ZIP file (you may need a special application for that purpose, e.g. WinRAR or 7zip). 

#### To analyze chosen file using syllabification application you need to enter the following command to your command line:  

`<python_path> <init_path> <file_name> <file_path> <encoding> <language_path>`

Where:
* `<python_path>`	 - represents path to python.exe file on your computer
* `<init_path` - represents path to init_terminate_module.py located in downloaded and unzipped syllabification application folder
* `<file_name>` - name of an input file ( file you want to analyze) 
* `<file_path>` - path to the folder containing input file
* `<encoding>` - coding of the input file (in case of using one of the UTF-8 codings, it is required to add  “-sig” at the end of coding type, e.g. UTF-8-sig instead of UTF-8) 
* `<language_path>` - path to a language file corresponding to language of input file located in downloaded and unzipped syllabification application folder

After the execution of given command, output files will be located in the <file_path> directory (the one containing input file).
 
#### Examples (these command parts shoule be separated by blank space in command line):
* `<python_path>`:
C:/Users/Michal/AppData/Local/Programs/Python/Python37-32/python.exe
* `<init_path>`:
C:/Users/Michal/Documents/slabiky-master/application/py_scripts2.0/init_terminate_module.py
* `<file_name>`:
test.txt 
* `<file_path>` (this could be any folder where you put your input file):
C:/Users/Michal/Documents/slabiky/application/py_scripts2.0/  
* `<encoding>`:
UTF-8-sig 
* `<language_path>`:
C:/Users/Michal/Documents/slabiky/application/py_scripts2.0/configs/conf_cs_lat.json 

#### Note that: 
* type of slash (frontslash “/” or backslash “\”) depends on your operating system
* application folder of syllable application contains two versions of py_scripts folder; use py_scripts1.0 for Basic syllabification (using only vowels, sonorants and obstruents) and py_scripts2.0 for Advanced syllabification (vowels, glides, liquids, nasals, obstruents)
