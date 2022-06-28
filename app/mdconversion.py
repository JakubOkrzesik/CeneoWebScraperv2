import re
import markdown

def mdconvert():
    with open('README.md', 'r') as f:
        text = f.read()
    
    template = markdown.markdown(text, extensions=['tables'])

    return re.sub('<table>', '<table class="table table-striped">', template)