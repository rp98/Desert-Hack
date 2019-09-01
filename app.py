from __future__ import unicode_literals
from summa import summarizer
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

#  Sum Pkg


@app.route('/')
def index():
    return render_template('index.html')


def stopword(text):
    text = text.split(' ')
    text2 = []
    for i in range(0, len(text)):
        if text[i] == "period":
            text2.append(".")
        elif text[i] == "pause":
            text2.append(",")
        elif text[i] == "question":
            text2.append("?")
        elif text[i] == '0':
            continue
        else:
            text2.append(text[i])

    s = " "
    s = s.join(text2)
    return(s)


def takenote(text):
    text = text.split(' ')
    text2 = []
    for i in range(0, len(text)):
        if ((text[i] == 'take' and text[i+1] == 'note') or (text[i-1] == 'kaya' and text[i] == 'take' and text[i+1] == 'note')):
            for j in range(i+2, len(text)):
                if text[j] == 'stop':
                    break
                text2.append(text[j])
                text[j] = '0'
    k = " "
    text = k.join(text)
    s = " "
    s = s.join(text2)
    return(s, text)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        text = request.form.get("text")
        ratio = float(request.form.get("slider"))
        highlights, processed_text = takenote(text)
        final_summary = summarizer.summarize(
            stopword(processed_text), ratio=ratio)

    return render_template('index.html', final_summary=final_summary, highlights=highlights, dummy=ratio)


if __name__ == '__main__':
    app.run(debug=True)
