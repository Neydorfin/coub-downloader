import requests
import json
import videoMaker


def download_video(permalink, url_video, url_audio):
    print(f'Start downloading file {permalink}...')
    try:
        # Save Video
        r = requests.get(url=url_video)
        with open(f'Download/{permalink}.mp4', 'wb') as file:
            file.write(r.content)
        print('Successful downloaded video!')

        # Save audio
        r = requests.get(url=url_audio)
        with open(f'Download/{permalink}.mp3', 'wb') as file:
            file.write(r.content)
        print('Successful downloaded audio!')
        print('Done downloading resources')
        return "Done downloading resources"
    except Exception as _ex:
        return _ex


def pars(url):
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'aaaaaemai123@mail.com'  # This is another valid field
        }
        response = requests.get(url=url, headers=headers)
        file_json = str(response.text)
        data = json.loads(file_json)
    except Exception as _ex:
        return 'Request error'
    data = data['coubs']
    files = dict()
    for el in data:
        try:
            url_video = el['file_versions']['html5']['video']['higher']['url']
            url_audio = el['file_versions']['html5']['audio']['high']['url']
            permalink = el['permalink']
            arr = (url_video, url_audio)
            files[str(permalink)] = arr
        except Exception as _ex:
            return "error parsing"
    return files


def main():
    full_dict = dict()
    # set after explore category what you want
    catalog = 'animals-pets'
    # on one page exist 10 coub video
    starting_page = 0
    number_of_page = 2
    for i in range(starting_page, number_of_page):
        print(f"Parsing {i + 1} page...")
        url = f'https://coub.com/api/v2/timeline/explore/{catalog}?page={i + 1}'
        data = pars(url=url)
        if data == 'Request error':
            print("Something came wrong, request error!!!")
        elif data == "error parsing":
            print("Something came wrong, parsing error!!!")
        else:
            print(f"Dowloading {i + 1} page...")
            for permalink, value in data.items():
                if download_video(permalink, value[0], value[1]) == "Done downloading resources":
                    videoMaker.make_video(permalink=permalink)
            full_dict.update(data)
    full_dict = json.dumps(full_dict)
    with open('new.json', 'w') as file:
        file.write(full_dict)
    # videoMaker.concatenate_full_video(full_dict)


if __name__ == '__main__':
    main()
