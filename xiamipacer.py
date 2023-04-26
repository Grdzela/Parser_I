import bs4
import requests
import xlsxwriter

main_url = 'https://trade59.ru/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
data = [['Named', 'Price', 'Link', 'Image']]


def get_soup(url):
    res = requests.get(url, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')


categories_page = get_soup(main_url+'catalog.html?cid=117')
categories = categories_page.findAll('a', class_='cat_item_color')
for cat in categories:
    subcategories_page = get_soup(main_url+cat['href'])
    subactegories = subcategories_page.findAll('a', class_='cat_item_color')
    for subcat in subactegories:
        xiaomi_page = get_soup(main_url+subcat['href'])
        xiaomis = xiaomi_page.findAll('div', class_='items-list')
        for xiaomi in xiaomis:
            title = xiaomi.find('a')['title'].strip()
            price = xiaomi.find('div', class_='price').find(text=True).strip()
            url = xiaomi.find('a')['href'].strip()
            img = xiaomi.find('div', class_='image')['style'].split(
                'url(')[1].split(')')[0].replace('/tn/', '/source/')
            data.append([title, price, url, img])

with xlsxwriter.Workbook('xiaomi.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, info in enumerate(data):
        worksheet.write_row(row_num, 0, info)
