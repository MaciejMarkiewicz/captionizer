# Captionizer

Captionizer enables you to create transcriptions of lectures, online meetings or videos with a help of speech recognition engines.


## Usage

- Install packages from requirements.txt - `pip install -r reguirements.txt`
- Enable stereo mix on windows -> right click on the sound icon on the taskbar -> sounds -> recording -> stereo mix -> enable
- Get an api key for azure cognitive services (preferred) or google speech api (you can use the default google key, but it is very limited)
- Run the app, go to preferences and set the engine, key and language. Set stereo mix as the input device, if you want to transcribe the sounds you hear.
- Press record to start recording
- Press stop to stop
- Transcription is stored to the specified path
- Be aware that changing your default recording device might result in changing your current online meeting software default settings

## App architecture

The app was build using the MVVM pattern, with view being the user entry point, and the viewmodel serving as a data source and updating the model.
The other-way communication is performed using decorator-like callbacks (expanding on top of each other) and asynchronous coroutines,
e.g. the document writer. Speech recognition engines use the strategy pattern, inheriting from the abstract Engine class.


## Tests and accuracy

The Azure engine performs much better than the Google one, so I will use it for the most part.
Mistake ratio is described as: (wrong words + 0.5 * correct words, but in a wrong form) / all words.
Punctuation accuracy is not measured, although it's worth noting, that only Azure engine provides it 
(it has a solid accuracy in English, and acceptable in Polish)

AZURE / ENG:

- [World politics, Yale University lecture](https://youtu.be/BDqvzFY72mg?t=717) - 11:58-14:28 - see 
  [transcription fragment](https://github.com/MaciejMarkiewicz/captionizer/tree/master/src/examples/eng-azure.docx) - 0% mistakes -
  perfectly transcribed and with perfect (reflecting speaker's intention) punctuation

AZURE / PL

- [Prof. Jerzy Bralczyk: "Jak mówić, żeby nas słuchano"](https://youtu.be/TG4ZAGnlPOY?t=775) - 12:56-14:10 - see 
  [transcription fragment](https://github.com/MaciejMarkiewicz/captionizer/tree/master/src/examples/pl-azure.docx) - 4% mistakes -
  mostly small, understandable mistakes, one serious - punctuation is not great, but still better, than plain text

GOOGLE / ENG
- [World politics, Yale University lecture](https://youtu.be/BDqvzFY72mg?t=717) - 11:58-12:25 - see 
  [transcription fragment](https://github.com/MaciejMarkiewicz/captionizer/tree/master/src/examples/eng-google.docx) - 9% mistakes - 
  perfect for the most part, high mistake ratio due to one missing expression in the end (was probably classified as mumbling)

GOOGLE / PL

- [Prof. Jerzy Bralczyk: "Jak mówić, żeby nas słuchano"](https://youtu.be/TG4ZAGnlPOY?t=775) - 12:56-13:22 - see 
  [transcription fragment](https://github.com/MaciejMarkiewicz/captionizer/tree/master/src/examples/pl-azure.docx) - 5% mistakes -
  surprisingly good, mistakes are understandable