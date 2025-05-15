''' downloads and tags the musics from a given input txt file list
    and gives the given TAG to the music '''


from downloader import music_downloader
from music_sorter import main


WD_PATH = r'C:/Users/const/OneDrive/Documents/Code/Python/Apollo'
MUSIC_PATH = r'C:/Users/const/Music/Apollo/'
FILES_TO_DL_PATH = WD_PATH + '/dl_list.txt'



def get_files():
    ''' returns the files to dl '''

    files_to_dl = open(FILES_TO_DL_PATH).read()
    return files_to_dl.split('\n')





if __name__ == '__main__':
    files_to_process = get_files()
    for i in files_to_process:
        music_downloader(i, MUSIC_PATH)
    main(MUSIC_PATH)
