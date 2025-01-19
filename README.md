# IELTS Speaking Test Simulator

Real-time Conversational Practice with AI-Powered IELTS Speaking Test Simulation


## Table of contents
* [1. Project Overview]
* [2. Features]
* [3. Environment Variables]
* [4. Technologies Used]


  

## 1. Project Overview <a class="anchor" id="project-description"></a>
This project is a real-time IELTS Speaking Test Simulator designed to help users practice their English speaking skills. It provides AI-driven feedback on fluency, grammar, vocabulary, and pronunciation, simulating a real IELTS examiner.

The tool supports real-time speech-to-text conversion, automated assessment, and custom feedback, allowing users to track their progress and improve their speaking skills.


## 2. Features <a class="anchor" id="dataset"></a>
- Upload and process audio files (MP3, WAV, etc.)
- Automatic speech-to-text transcription
- Text analysis and evaluation
- User-friendly web interface with Streamlit
  

## 3. Environment <a class="anchor" id="environment"></a>

It's highly recommended to use a virtual environment for your projects, there are many ways to do this; we've outlined one such method below. Make sure to regularly update this section. This way, anyone who clones your repository will know exactly what steps to follow to prepare the necessary environment. The instructions provided here should enable a person to clone your repo and quickly get started.

### Create the new evironment 

python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows

### This is how you activate the virtual environment in a terminal and install the project dependencies

```bash
# activate the virtual environment
conda activate <env>
# install the pip package
conda install pip
# install the requirements for this project
pip install -r requirements.txt
```
## 4. Technologies used<a class="anchor" id="mlflow"></a>

Python
- OpenAI Whisper
- Streamlit
- Pydub (for audio processing)
- FFmpeg (for file conversion)



### What is Streamlit?

[Streamlit](https://www.streamlit.io/)  is a framework that acts as a web server with dynamic visuals, multiple responsive pages, and robust deployment of your models.

In its own words:
> Streamlit ... is the easiest way for data scientists and machine learning engineers to create beautiful, performant apps in only a few hours!  All in pure Python. All for free.

> It’s a simple and powerful app model that lets you build rich UIs incredibly quickly.

[Streamlit](https://www.streamlit.io/)  takes away much of the background work needed in order to get a platform which can deploy your models to clients and end users. Meaning that you get to focus on the important stuff (related to the data), and can largely ignore the rest. This will allow you to become a lot more productive.  

