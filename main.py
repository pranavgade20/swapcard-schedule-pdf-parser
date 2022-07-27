import PyPDF2
from dateutil.parser import parse
import ics

if __name__ == '__main__':
    pdf = PyPDF2.PdfFileReader(open('pdf.pdf', 'rb'))

    text = ''
    for page in pdf.pages:
        text += page.extractText() + '\n'

    events = []
    date = ''
    skip = 1
    split = text.split('\n')
    for i, l in enumerate(split):
        if skip > 0:
            skip -= 1
            continue
        if l.endswith(', 2022'):
            date = l
            continue
        elif l.endswith(' PM') or l.endswith(' AM'):
            events.append({'misc': '', 'loc': None})
            events[-1]['from'] = parse(f'{date} {l}')
            events[-1]['to'] = parse(f'{date} {split[i + 1][:7]}')
            events[-1]['title'] = split[i + 1][7:]
            skip = 1
            continue
        elif l.startswith('Meeting Points'):
            events[-1]['loc'] = l[17:]
        else:
            events[-1]['misc'] += l + ' '

    i = ics.Calendar(creator='pranav gade for eag sf 2022')
    for event in events:
        e = ics.Event(name=event['title'], begin=event['from'], end=event['to'], description=event['misc'], location=event['loc'])
        i.events.add(e)

    open('eag.ics', 'w+').write(i.serialize())