
from requests import get, post
from pydub import AudioSegment
from io import BytesIO


def speak(text):

    payload = r"""[{"voiceId":"Amazon British English (Amy)","ssml":"<speak version=\"1.0\" xml:lang=\"en-GB\">"""+text+r"""</speak>"}]"""
    #<prosody rate='medium' pitch='low'><break time='0s'/>hello i am going to take over the world.</prosody>
        
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "referer": "https://ttstool.com/",
        "content-type": "application/json",
        "accept": "*/*"
    }

    res = post('https://support.readaloud.app/ttstool/createParts',data=payload,headers=headers)
    mp3 = get('https://support.readaloud.app/ttstool/getParts', params={"q": res.json()[0]})
    audio = AudioSegment.from_file(BytesIO(mp3.content), format="mp3")

    return audio
    
   

    

