# IMDBCrawler
Crawler to pull all reviews on IMDB for specified contents. Made using selenium.

### Required Libaries:
- selenium

```
pip install -U selenium
```
### How to Use:

The files 'kmovieIMDB.csv' and 'kdramaIMDB.csv' are used to store the list of contents you want to pull reviews for. The only column that is absolutely required is 'url' and the link should be for the user review page such as 'https://www.imdb.com/title/tt26160190/reviews?ref_=tt_urv'

These csv files will be read, and then all of its reviews and details about the review itself will be pulled and stored as a new csv file. 

```
def scrape_reviews(url, days_threshold=31):
```
You can change the days_threshold variable here. It will grab reviews that was written within the specified days. Ex: If you want reviews written within the last month, you can set it as 31. If you want all reviews, input 9999999 - the number is so high it will just grab everything.

### Using ChromeDriver: 
Make sure you have downloaded the latest ChromeDriver file, which you can find [here](https://chromedriver.chromium.org/getting-started), make sure to get the correct one for your OS and Chrome version. It may be necessary to update your Chrome as well.

```
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
```

This is to create a driver instance in **Linux**. You will have to change this line if your OS is NOT linux. 

For example, this would be what you would change it to in **Windows**:
```
# Specify the path to the ChromeDriver executable if not added to PATH
chrome_driver_path = 'path/to/chromedriver.exe'

# Create ChromeDriver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path)
```

# IMDB 크롤러
지정된 콘텐츠에 대한 IMDB의 모든 리뷰를 수집하는 크롤러입니다. Selenium을 사용하여 만들었습니다.

### 필요한 라이브러리:
- selenium
  
### 사용법:

'kmovieIMDB.csv' 및 'kdramaIMDB.csv' 파일은 리뷰를 가져올 콘텐츠 목록을 저장하는 데 사용됩니다. 반드시 필요한 열은 'url'뿐이며 링크는 'https://www.imdb.com/title/tt26160190/reviews?ref_=tt_urv'와 같은 사용자 리뷰 페이지를 가리킵니다.

이 csv 파일들은 읽혀지고, 그 후에 모든 리뷰와 리뷰 자체에 대한 세부 정보가 새로운 csv 파일로 추출되어 저장됩니다.

```
def scrape_reviews(url, days_threshold=31):
```
여기서 days_threshold 변수를 변경할 수 있습니다. 이 변수는 지정된 일수 내에 작성된 리뷰를 가져옵니다. 예를 들어, 지난 한 달간 작성된 리뷰를 원하는 경우 31로 설정할 수 있습니다. 모든 리뷰를 원하는 경우 9999999를 입력하면 됩니다. 숫자가 매우 크기 때문에 모든 것을 가져올 것입니다.

### ChromeDriver 사용전: 
최신 ChromeDriver 파일을 다운로드했는지 확인하세요. 여기에서 찾을 수 있습니다. 사용 중인 OS 및 Chrome 버전에 맞는 것을 가져오세요. Chrome을 업데이트해야 할 수도 있습니다.

리눅스로 드라이버 인스턴스 만들기: 
```
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
```

이것은 **리눅스**에서 드라이버 인스턴스를 만드는 것입니다. 사용 중인 OS가 리눅스가 아닌 경우 이 줄을 변경해야 합니다.

예를 들어, **윈도우**에서는 다음과 같이 변경해야 합니다:
```
# Specify the path to the ChromeDriver executable if not added to PATH
chrome_driver_path = 'path/to/chromedriver.exe'

# Create ChromeDriver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path)
```
