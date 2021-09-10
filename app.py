import os
import json
import random

import numpy as np

from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_cors import CORS, cross_origin

import pretty_midi
from pretty_midi import constants

SAMPLE_PATH = "static/samples_out"
SAMPLES = os.listdir(SAMPLE_PATH)

# Server Setup ###################################################################################################################
app = Flask(__name__)
CORS(app)
app.secret_key = str(random.random())

# Helpers ########################################################################################################################
def get_sample(sample_folder):
    original_midi_path_mixed = "{}/{}/mixed.mid".format(SAMPLE_PATH, sample_folder)
    original_midi_path_mel = "{}/{}/melody.mid".format(SAMPLE_PATH, sample_folder)
    original_midi_path_acc = "{}/{}/accompaniment_track.mid".format(SAMPLE_PATH, sample_folder)
    notedic_path = "{}/{}/{}_mixed.npy".format(SAMPLE_PATH, sample_folder, sample_folder)
    notedic_mel_path = "{}/{}/{}_mel.npy".format(SAMPLE_PATH, sample_folder, sample_folder)
    notedic_acc_path = "{}/{}/{}_acc.npy".format(SAMPLE_PATH, sample_folder, sample_folder)
    chord_path = "{}/{}/chord.npy".format(SAMPLE_PATH, sample_folder)
    json_path = "{}/{}/songData.json".format(SAMPLE_PATH, sample_folder)
    notedic = np.load(notedic_path, allow_pickle=True).item()
    notedic_mel = np.load(notedic_mel_path, allow_pickle=True).item()
    notedic_acc = np.load(notedic_acc_path, allow_pickle=True).item()
    chord = np.load(chord_path)
    root = np.zeros((16,12))
    bass = np.zeros((16,12))
    root[[i for i in range(16)],chord[:,0].astype(int)] = 1
    bass[[i for i in range(16)],chord[:,-1].astype(int)] = 1
    chord = np.concatenate((root,chord[:,1:-1],bass),axis=1)

    sustain_path = "static/sustain.npy"
    sustain = np.load(sustain_path)


    with open(json_path, 'r') as jsonFile:
            jsonData = json.load(jsonFile)
            name = jsonData['name']
            key = jsonData['key'][:-1]
            key = key.replace(':','')

    return original_midi_path_mixed, original_midi_path_mel, original_midi_path_acc, notedic, notedic_mel, notedic_acc, chord, sustain, key, name

def chd_to_str(c_mat):
    out = []
    pitches = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    for c in c_mat:
        root = np.argmax(c[:12])
        root_s = pitches[root]
        chroma = np.array([i for i in range(12)])[c[12:24]==1]
        chroma = (chroma - root) % 12
        bass = np.argmax(c[24:])
        if len(chroma) == 3:
            if 7 in chroma:
                if 4 in chroma:
                    c_type = ''
                if 3 in chroma:
                    c_type = 'm'
                if 1 in chroma or 2 in chroma:
                    c_type = 'sus2'
                if 5 in chroma or 6 in chroma:
                    c_type = 'sus4'
            else:
                c_type = '6'
        else:
            c_type = ''
        if bass == 0:
            bass_s = ''
        else:
            bass_s = '/' + pitches[(root + bass) % 12]
        out.append('{}{}{}'.format(root_s, c_type, bass_s))
    for i in range(len(out)-1, 0, -1):
        if out[i] == out[i-1]:
            out[i] = ''
    return out

def midi_to_noteseq(midi_path):
    midi = pretty_midi.PrettyMIDI(midi_path)
    note_seq = {'notes': [], 'totalTime':16}
    rescale = 4/3
    for note in midi.instruments[0].notes:
        note_seq['notes'].append({'pitch': note.pitch, 'startTime':note.start*rescale, 'endTime':note.end*rescale})
    return note_seq

def chd_to_deg(c_mat, key):
    out = []
    pitches = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    pitches_flat  = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
    deg = ['I', 'IIb', 'II', 'IIIb', 'III', 'IV', 'Vb', 'V', 'VIb', 'VI', 'VIIb', 'VI']

    key = key[:-3]
    if key in pitches:
        key = pitches.index(key)
    else:
        key = pitches_flat.index(key)

    for c in c_mat:
        root = np.argmax(c[:12])
        root_s = (root-key)%12
        chroma = np.array([i for i in range(12)])[c[12:24]==1]
        chroma = (chroma - root) % 12
        bass = np.argmax(c[24:])
        c_type = deg[root_s]
        if 3 in chroma:
            c_type = deg[root_s].lower()
        if 1 in chroma or 2 in chroma:
            c_type += 'sus2'
        if 5 in chroma or 6 in chroma:
            c_type += 'sus4'
        if bass != 0:
            c_type += '/' + deg[(root + bass - key) % 12]
        out.append(c_type)
    for i in range(len(out)-1, 0, -1):
        if out[i] == out[i-1]:
            out[i] = ''
    return out

def getSongData():
    # Progressions, keys, etc
    select_sample_folders = os.listdir(SAMPLE_PATH)
    songData = {}
    for folder in select_sample_folders:
        [song, segment] = folder.split("_")

        json_path = "{}/{}/songData.json".format(SAMPLE_PATH,folder)
        chord_path = "{}/{}/chord.npy".format(SAMPLE_PATH,folder)
        chord = np.load(chord_path)
        root = np.zeros((16,12))
        bass = np.zeros((16,12))
        root[[i for i in range(16)],chord[:,0].astype(int)] = 1
        bass[[i for i in range(16)],chord[:,-1].astype(int)] = 1
        chord = np.concatenate((root,chord[:,1:-1],bass),axis=1)

        with open(json_path, 'r') as jsonFile:
                jsonData = json.load(jsonFile)
                name = jsonData['name']
                key = jsonData['key'][:-1]
                key = key.replace(':','')

        songkey = "{}: {}".format(song, name)

        degs = chd_to_deg(chord, key)
        new_deg = []
        for deg in degs:
            if deg != '':
                new_deg.append(deg)

        if songkey not in songData.keys():
            songData[songkey] = {segment: '-'.join(new_deg), 'key': key}
        else:
            songData[songkey][segment] = '-'.join(new_deg)
    return songData

songData = getSongData()

# The Main Thing ##################################################################################################################
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/favicon.ico', methods=['GET'])
def serve_favicon():
    return app.send_static_file('favicon.ico')

@app.route('/js/<path>')
def serve_js(path):
    return app.send_static_file('js/'+path)

@app.route('/rnn_worker.js')
def serve_worker():
    return app.send_static_file('rnn_worker.js')

@app.route('/css/<path>')
def serve_css(path):
    return app.send_static_file('css/'+path)

@app.route('/get_songdata', methods=['GET'])
def get_songdata():
    out = {'songData': songData}
    return json.dumps(out)

@app.route('/get_data', methods=['GET'])
def get_data():
    songID = request.args.get("song")
    if songID == "000":
        sample_folder = random.choice(SAMPLES)
    else:
        sample_folder = songID
    original_midi_path_mixed, original_midi_path_mel, original_midi_path_acc, notedic, notedic_mel, notedic_acc, chord, sustain, key, name = get_sample(sample_folder)

    chord_str = chd_to_str(chord)
    chord_deg = chd_to_deg(chord, key)
    for idx, chd_str in enumerate(chord_str):
        if chord_deg[idx] != '':
            chord_str[idx] += " ({})".format(chord_deg[idx])

    out =  {'songID': sample_folder,
            'original_chd_str': chord_str,
            'original_chd_mat': chord.tolist(),
            'original_noteseq_mixed': midi_to_noteseq(original_midi_path_mixed),
            'original_noteseq_mel': midi_to_noteseq(original_midi_path_mel),
            'original_noteseq_acc': midi_to_noteseq(original_midi_path_acc),
            'notedic_mixed': notedic,
            'notedic_mel': notedic_mel,
            'notedic_acc': notedic_acc,
            'sustain': sustain.tolist(),
            'key': key,
            'name': name}
    return json.dumps(out)

if __name__ == '__main__':
    app.run(debug=False,port=os.getenv('PORT',5000))
