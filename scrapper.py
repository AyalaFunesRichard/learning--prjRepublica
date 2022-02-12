import requests
import lxml.html as html
import os
import datetime

HOME_URL = "https://www.larepublica.co/"

XPATH_LINK_TO_ARTICLE = '//div[contains(@class, "V_Title_Img")]/a/@href'
# XPATH_LINK_TO_ARTICLE = '//h2/a[contains(@href, "larepublica.co")]/@href'
XPATH_TITLE = '//h2[@class=""]/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/text()'


def parse_notice(link, today):
    print(link)
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            print(parsed)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                print(title)
                # title = title.replace('\"', '')  # borrar las "
                # print(title)

                summary = parsed.xpath(XPATH_SUMMARY)[0]

                body = parsed.xpath(XPATH_BODY)

            except IndexError as ve:
                print(ve)
                return
            except Exception as e:
                print(e)

            # manejador contextual : si el archivo llega a cerrar. manteniene todo de manera segura
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

            print("\n\n\n")

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if(response.status_code == 200):
            # convertir caracteres especiales para q python pueda leer
            home = response.content.decode('utf-8')
            # Convertir home (q es la pg) en un archivo para aplicar XPath
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')  # StringFormatTime
            if not os.path.isdir(today):
                os.mkdir(today)  # crea una carpeta en caso no exista

            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
