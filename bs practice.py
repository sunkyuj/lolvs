from bs4 import BeautifulSoup
from urllib.request import urlopen

tag = "<p class='youngone' id='junu'> Hello World! </p> <div class='youngone' id='junu'> sss World! </p>" 
soup = BeautifulSoup(tag) 

# 태그 이름만 특정 
print(soup.find('p'))

# 태그 속성만 특정 
print(soup.find(class_='youngone')) 
print(soup.find(attrs = {'class':'youngone'}) )

# 태그 이름과 속성 모두 특정 
print(soup.find('div', class_='youngone'))
print(type(soup.find('p')))

