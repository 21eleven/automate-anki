import sys
import requests
from bs4 import BeautifulSoup

def get_color_desc(color):
    colorhexa_url = "https://www.colorhexa.com/color.php"
    res = requests.post(colorhexa_url, data={'color-picker': '', 'c': color, 'h': 'h'})
    soup = BeautifulSoup(res.text, 'html.parser')
    desc = soup.find_all("div", {"class" :"color-description"})
    print(desc)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        color = sys.argv[1]
        print(color)
        get_color_desc(color)
    else:
        print(sys.argv)
