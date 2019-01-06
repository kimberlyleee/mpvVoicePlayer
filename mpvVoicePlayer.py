import speech_recognition as sr
import pyttsx3
import os
import subprocess
import pafy
import pprint as pp



class VoicePlayer:
    def __init__(self):
        self.songList = {}
        self.songIndex = {}
        self.searchTerm = ''
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', "com.apple.speech.synthesis.voice.samantha")
        self.engine.setProperty('rate', 200)
        self.voiceRecognizer = sr.Recognizer()


    def removeNonAlphaNum(self, title):
        temp = ''
        for c in title:
            if (c.isalnum() or c.isspace()):
                temp += c
        return temp

    def search(self, query):
        qs = {
            'q': query,  # required
            'part': 'id,snippet',  # required
            'key': 'AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo',  # required
            'maxResults': 2,
            'type': 'video',
        }
        r = pafy.call_gdata('search', qs)
        #pp.pprint(r)
        items = r['items']
        itemsSize = len(items)
        for i in range(itemsSize):
            vidId = items[i]['id']['videoId']
            title = items[i]['snippet']['title']
            self.songList[vidId] = self.removeNonAlphaNum(title)
            self.songIndex[str(i + 1)] = vidId



    def play_with_mpv(self, video_id):
        sp = subprocess.Popen(['mpv', f'ytdl://{video_id}', '--no-video'])
        sp.communicate() # trigger command line to run mpv

    def sayTitles(self):
        counter = 1
        temp = "I've found " + str(len(self.songList)) + " songs"
        self.engine.say(temp)
        self.engine.runAndWait()

        for title in self.songList.values():
            self.engine.say(str(counter))
            self.engine.runAndWait()
            counter = counter + 1
            self.engine.say(title)
            self.engine.runAndWait()


    def askQuestion(self, sentence):
        print(sentence + '?')
        self.engine.say(sentence)
        self.engine.runAndWait()
        print("?")

        with sr.Microphone() as mp:
            audio = self.voiceRecognizer.listen(mp)

        try:
            userInput = self.voiceRecognizer.recognize_google(audio)
            return userInput

        except:
            pass


    def say(self, sentence):
        self.searchTerm = self.askQuestion(sentence)


def main():
    player = VoicePlayer()
    player.say("What song would you like to play")
    player.search(player.searchTerm)
    counter = 1
    for key,value in player.songList.items():
        print(str(counter) + ": " + value)
        counter = counter + 1
    player.sayTitles()
    songNumber = player.askQuestion("What song number would you like to play")
    print(songNumber)
    print(player.songIndex[songNumber ])
    player.play_with_mpv(player.songIndex[songNumber])

if __name__ == "__main__":
    main()










