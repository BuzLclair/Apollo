import requests
import edgedriver_autoinstaller


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
edgedriver_autoinstaller.install()



DOWNLOAD_URL = 'https://myfreemp3juices.cc/'

EDGE_OPTIONS = Options()
EDGE_OPTIONS.add_argument("--headless")


def ini_driver():
    ''' start driver with the download website url '''

    driver = webdriver.Edge(options=EDGE_OPTIONS)
    driver.get(DOWNLOAD_URL)
    return driver


def search_music(driver, music_name):
    ''' search the music name on the website and return a list of results
        (first 3 results) '''

    search_bar = driver.find_element(by=By.ID, value='query')
    search_bar.send_keys(music_name)
    search_btn = driver.find_element(by=By.TAG_NAME, value='button')
    # search_btn.click()
    driver.execute_script("arguments[0].click();", search_btn)

    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, 'list-group')))
    results_list = driver.find_elements(by=By.CLASS_NAME, value='list-group-item')
    max_index = min(len(results_list),3)
    return results_list[:max_index]



class MusicCandidate:
    ''' for a given WebElement (in the list of found musics on the website)
        return info such as bitrate, download link... '''

    def __init__(self, web_elem):
        self.element = web_elem
        self.get_html()
        self.info_link = None
        self.download_link = None
        self.bitrate_value = 0

    def get_html(self):
        ''' return html element of the potential music file '''

        self.html_content = self.element.get_attribute('outerHTML')

    def get_info_link(self):
        ''' return link to informations of the potential music file '''

        self.info_link = self.html_content.split('<a onclick="window.open(\'')[1].split('\',\'')[0]
        return self.info_link

    def get_download_link(self):
        ''' return the direct download link of the potential music file '''

        self.download_link = self.html_content.split('<a class="name" title="Download" ')[1]
        self.download_link = self.download_link.split('href="')[1].split('">')[0]
        return self.download_link

    def get_bitrate(self):
        ''' return the bitrate value (quality) of the potential music file '''

        html_txt = requests.get(self.get_info_link(), timeout=10).text
        meta = html_txt.split('<meta name="description" content="')[1].split('>')[0]
        bitrate_line = meta.split(' - ')
        bitrate = list(filter(lambda x: 'KBPS' in x, bitrate_line))
        self.bitrate_value = bitrate[0].split(' KBPS')[0]
        return int(self.bitrate_value)



def best_link_picker(results_list):
    ''' among a list of WebElements (representing music file candidates), picks
        the one with the best bitrate and returns its download link '''

    results_web_elements = [MusicCandidate(x) for x in results_list]
    results_bitrate = [x.get_bitrate() for x in results_web_elements]
    optimal_music_index = results_bitrate.index(max(results_bitrate))
    optimal_music_file = results_web_elements[optimal_music_index]
    return optimal_music_file.get_download_link()


def download_from_link(link, name, path):
    ''' download file with given download link and place it in the correct folder '''

    response = requests.get(link, timeout=10).content
    with open(path + '/' + name + '.mp3', 'wb') as music_file:
        music_file.write(response)
        music_file.close()


def music_downloader(music_name, path):
    ''' handle download process from music names to downloaded file '''

    driver = ini_driver()
    results_list = search_music(driver, music_name)
    optimal_link = best_link_picker(results_list)
    driver.quit()
    download_from_link(optimal_link, music_name, path)


