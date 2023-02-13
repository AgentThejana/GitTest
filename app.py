from TTS import speak
from pydub.audio_segment import AudioSegment
from math import floor
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
app.secret_key = 'Agent@Flask47'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tts', methods=['POST'])
def tts():
    story = request.form['tts']
    words = story.split(' ')
    phrase = ''
    global story_array
    story_array = []
    collection = []
    e = 0
    r = 0

#[['Once upon a time, ', 'in a land filled '], ['with talking animals, ', 'there was a lazy '], ['Mittens.']]
    for i in words:
        e += 1
        r += 1

        phrase += i+' '

        if len(words) == r:
                collection.append(phrase)
                story_array.append(collection)

        else:

            if e == 4 or  '.' in i or  ',' in i:
                collection.append(phrase)
                phrase = ''
                e = 0

            if len(collection) == 2:
                story_array.append(collection)
                collection = []

            
    return render_template('progress.html')


@app.route('/progress', methods=['POST'])
def progress():
    return tts_progress

@app.route('/generate', methods=['POST'])
def generate():
    
    print(story_array)

    silence = AudioSegment.from_file('silence.mp3',format='mp3')

    print('\nGenerating Audio...')
    global tts_progress
    tts_progress = str(floor(1/len(story_array)*100))
    print(tts_progress)


    mytext = speak(story_array[0][0])+silence+speak(story_array[0][1])+silence+speak(story_array[0][0])+speak(story_array[0][1])

    for index, item in enumerate(story_array[1:]):
        narration1 = speak(item[0])
        try:
            narration2 = speak(item[1])
            tts_progress = str(floor((index+2)/len(story_array)*100))
        except:
            mytext += silence+narration1
            tts_progress = str(floor((index+2)/len(story_array)*100))
            break
        
        mytext += narration1+silence+narration2+silence+narration1+narration2

    mytext.export('out.mp3',format='mp3')
    return "done"

@app.route('/download/audio')
def download():
    return send_file('out.mp3')
    


