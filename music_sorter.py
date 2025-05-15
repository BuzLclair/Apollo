import os
import requests
import eyed3
import ytmusicapi



def picture_from_url(url):
    ''' returns picture (bytes format) from url '''

    return requests.get(url, timeout=10).content



class MusicFile:
    ''' define a class for a music file inside the music directory '''

    def __init__(self, name, MUSIC_PATH):
        self.file_name = name
        try:
            self.file_loaded = eyed3.load(MUSIC_PATH + '/' + name)
        except TypeError:
            self.file_loaded = eyed3.load(MUSIC_PATH + '/' + name, tag_version=(1,None,None))

    def music_name(self):
        ''' returns music name without the file type '''

        return self.file_name.split('.mp3')[0]

    def duration(self):
        ''' returns the file duration '''

        file_duration = self.file_loaded.info.time_secs
        return int(file_duration)

    def __get_artwork(self, reference):
        ''' returns artwork url for the music file '''

        artwork_url = reference['thumbnails'][-1]['url']
        artwork = picture_from_url(artwork_url)
        return artwork


    def adapt_tags(self, reference):
        ''' adjusts tags of the music files given the best pick '''

        self.file_loaded.tag.title = reference['title']
        self.file_loaded.tag.artist = reference['artists'][0]['name']
        try:
            self.file_loaded.tag.album = reference['album']['name']
        except TypeError:
            pass
        self.file_loaded.tag.release_date = reference['year']
        self.file_loaded.tag.images.set(3, self.__get_artwork(reference),'image/jpeg')
        try:
            self.file_loaded.tag.save(version=eyed3.id3.ID3_V2_3)
        except:
            self.file_loaded.tag.save(version=(1,None,None))
            # self.file_loaded.tag.save()
            # self.file_loaded.tag.save(version=(2,3,0))



def best_pick(instance):
    ''' pick best fit of file in yt music search (based on duration) picks the best
        file if the duration of the file is equal to the duration of the pick +- 5% '''

    music_instance = instance
    search_yt_raw = ytmusicapi.YTMusic().search(music_instance.music_name())
    search_yt = list(filter(lambda x: x['category'] == 'Songs', search_yt_raw))
    try:
        results_duration = [x['duration_seconds'] for x in search_yt]
        results_error = [abs((x - music_instance.duration()) / music_instance.duration()) \
                         for x in results_duration]
        candidates_pick = list(filter(lambda x: x<0.05, results_error))
        best_pick_index = results_error.index(candidates_pick[0])
        return search_yt[best_pick_index]
    except IndexError:
        search_yt = list(filter(lambda x: x['category'] == 'Videos', search_yt_raw))
        return search_yt[0] # returns the first yt pick if the duration filter fails




def file_handle(name, MUSIC_PATH):
    ''' for a given name, updates tags, artwork etc '''

    try:
        music_instance = MusicFile(name, MUSIC_PATH)
        reference = best_pick(music_instance)
        music_instance.adapt_tags(reference)
        new_name = f'{reference["title"]} - {reference["artists"][0]["name"]}.mp3'
        os.rename(f'{MUSIC_PATH}/{name}', f'{MUSIC_PATH}/filtered_files/{new_name}')
        print(f'SUCCESS {name}')
    except TypeError:
        print(f'{name} -- eyed 3 cannot load the file')
    except IndexError:
        print(f'{name}: no match')



def main(MUSIC_PATH):
    MUSIC_LIST = os.listdir(MUSIC_PATH)
    MUSIC_FILES = list(filter(lambda x: '.mp3' in x, MUSIC_LIST))
    os.makedirs(f'{MUSIC_PATH}/filtered_files', exist_ok=True)
    for music in MUSIC_FILES:
        try:
            file_handle(music, MUSIC_PATH)
        except:
            print(f'{music} -- Big fail')



# main(r'C:/Users/const/Music/Apollo/filtered_files')
