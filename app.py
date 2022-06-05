from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from time import sleep,time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math,os,sys
from getpass import getpass
from tqdm import tqdm
import plyer.platforms.win.notification
from plyer import notification


print('Welcome to...')
print('Auto Reader')
print("Warning")
print('** Please consider that you are using this program at your own risk. **')
print('>> Please read the instruction below CAREFULLY so you not missing anything. <<')
print('First You Need to Open https://xreading.com/login/index.php to select the book you want me to read')
print('Then after add that book just close that window to logout from the xreading')
input('finished (if so, just press enter): ')
print('Now AutoReader will read that book for you and then will close it for you')


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

#define the driver
options = webdriver.EdgeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Edge(service = Service(resource_path('msedgedriver.exe')),options=options)

driver.get('https://xreading.com/login/index.php')

#login

username = driver.find_element(by=By.XPATH,value='//input[@type="text"]')

username.send_keys(input('Enter Your Email : '))

password = driver.find_element(by=By.XPATH,value='//input[@type="password"]')

password.send_keys(getpass('Enter Your Password : '))

password.send_keys(Keys.RETURN)

word = driver.find_element(by=By.XPATH,value='//*[@id="region-main"]/div/div[4]/div/div[1]/div[2]/div[2]/div[1]/ul[1]/li[2]').text

#function to strNum to num
convertStrToInt = lambda word : int(''.join(word.split(' ')[-1].split(',')))

totalWord = convertStrToInt(word)

print(f'total Word : {totalWord}')

#round int function
def rounder(num):
	digit = len(str(num)) -2

	return math.ceil(num/(10**digit))*(10**digit)

roundedWord = rounder(totalWord)

roundedTime = roundedWord/230 #word per minutes

#click the continue reading or read again(it wont work with read again)
try:
	continueRead = driver.find_element(by=By.XPATH,value='//*[@id="region-main"]/div/div[4]/div/div[1]/div[2]/div[2]/div[2]/a')
	continueRead.click()
except Exception as e:
	readAgain = driver.find_element(by=By.XPATH,value='/html/body/div[1]/div[3]/div/div/div/div/section[1]/div/div[4]/div/div[1]/div[2]/div[2]/div[2]/input[1]')
	readAgain.click()
	sleep(1)
	confirmButton = driver.find_element(by=By.XPATH,value='//*[@id="page-institution"]/div[4]/div/div/div[3]/button[1]')
	confirmButton.click()


print(f'Rounded word : {roundedWord} words')
hrs = int(roundedTime//60)
mins = int(roundedTime%60)
secs = round((roundedTime%1)*60)
time_text = 'Program will take '
if hrs:
	time_text += f'{hrs} hours'

if mins:
	time_text += f' {mins} minutes'

if secs:
	time_text += f' and {secs} seconds'

print(time_text+' to complete this book.')
#get the start time

finishing = ''
while finishing.lower() not in ['y','n']:
	finishing = input('Want to complete(going to the last page and close it) the book for you [Y]/n :')

startTime = time()

with tqdm(total = math.ceil(roundedTime*3)) as bar:
	while (time() - startTime  )/60 < roundedTime:
		page =driver.find_element(by=By.TAG_NAME,value='body')

		page.send_keys(Keys.END)
		sleep(10)
		page.send_keys(Keys.HOME)
		sleep(10)
		bar.update(1)





#loop clicking

#get to the last page and quit the book
notification.notify("AutoReader", "Your Book Is Now Finished")


if finishing.lower() == 'y':
	while True:
		try:
			sleep(5)
			page =driver.find_element(by=By.TAG_NAME,value='body')
			page.send_keys(Keys.END)
			nextButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next-slide')))
			nextButton.click()
		except TimeoutException:
			closeBook = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close-book')))
			closeBook.click()
			break
elif finishing.lower() == 'n':
	exit_book = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="bookreader-main"]/nav/div/ul/li[4]/a/i')))
	exit_book.click()
driver.close()
print('End Of Program')
print('THANK YOU')