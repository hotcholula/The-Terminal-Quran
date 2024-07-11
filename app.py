import os
import xml.etree.ElementTree as ET
from termcolor import colored
from tabulate import tabulate

meta = []
quran = []
meaning = []
chapterList = []

def get_data_path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)

def chapters():
    read_data(list_chapters)

def info(chapter):
    read_data(lambda: get_chapter_info(chapter))

def read(chapter, verse, arabic):
    read_data(lambda: get_details(chapter, verse, arabic))

def search(keyword, arabic):
    read_data(lambda: search_translations(keyword, arabic))

def list_chapters():
    global chapterList
    table = []

    for i in range(0, 114):
        chapterList.append({
            'index': i + 1,
            'name': meta['sura'][i].attrib['tname'],
            'ename': meta['sura'][i].attrib['ename'],
            'ayas': meta['sura'][i].attrib['ayas'],
            'rukus': meta['sura'][i].attrib['rukus'],
            'start': meta['sura'][i].attrib['start'],
            'type': meta['sura'][i].attrib['type'],
            'order': meta['sura'][i].attrib['order']
        })

    for chapter in chapterList:
        table.append([colored(str(chapter['index']), 'green'), colored(chapter['name'], 'yellow')])

    print(tabulate(table, headers=[colored('Index', 'cyan'), colored('Chapter', 'cyan')]))

def get_chapter_info(chapter):
    global chapterList
    chapter_index = int(chapter) - 1

    if chapter_index < 0 or chapter_index >= len(chapterList):
        print(colored('Invalid chapter number.', 'red'))
        return

    chapter_info = chapterList[chapter_index]
    table_data.append([
        chapter_info['index'],
        chapter_info['name'],
        chapter_info['ename'],
        chapter_info['ayas'],
        chapter_info['rukus'],
        chapter_info['start'],
        chapter_info['type'],
        chapter_info['order']
    ])

    print(tabulate(table_data, headers='firstrow'))

def get_details(chapter, verse, arabic):
    global chapterList
    chapter_index = int(chapter) - 1

    if chapter_index < 0 or chapter_index >= len(chapterList):
        print(colored('Invalid chapter number.', 'red'))
        return

    if not verse or verse == '0':
        get_entire_chapter(chapter_index, arabic)
    else:
        get_chapter_verse(chapter_index, verse, arabic)

def get_entire_chapter(chapter, arabic):
    global chapterList, quran, meaning

    table_data = [
        [colored(chapterList[chapter]['index'] + ' : ' + chapterList[chapter]['name'] + ' (' + chapterList[chapter]['ename'] + ')', 'green')],
        [colored('Verse', 'cyan'), colored('Text', 'cyan')]
    ]

    verses = quran[chapter]['aya']
    table_data = set_verses(table_data, verses, arabic)

    print(tabulate(table_data))

def get_chapter_verse(chapter, verse, arabic):
    global chapterList, quran, meaning

    table_data = [
        [colored(chapterList[chapter]['index'] + ' : ' + chapterList[chapter]['name'] + ' (' + chapterList[chapter]['ename'] + ')', 'green')],
        [colored('Verse', 'cyan'), colored('Text', 'cyan')]
    ]

    is_range = ':' in verse

    if is_range:
        range_start, range_end = map(int, verse.split(':'))
        verses = quran[chapter]['aya'][range_start-1:range_end]
    else:
        verse_index = int(verse) - 1
        verses = [quran[chapter]['aya'][verse_index]]

    table_data = set_verses(table_data, verses, arabic)

    print(tabulate(table_data))

def read_data(callback):
    global meta, quran, meaning

    meta_tree = ET.parse(get_data_path('quran-data.xml'))
    meta_root = meta_tree.getroot()
    meta = meta_root.find('suras')

    quran_tree = ET.parse(get_data_path('ar.quran.xml'))
    quran_root = quran_tree.getroot()
    quran = quran_root.findall('sura')

    meaning_tree = ET.parse(get_data_path('en.sahih.xml'))
    meaning_root = meaning_tree.getroot()
    meaning = meaning_root.findall('sura')

    callback()

def set_verses(table_data, verses, arabic):
    global meaning

    for aya in verses:
        index = int(aya.attrib['index']) - 1

        if not arabic or arabic != '0':
            table_data.append([
                colored(aya.attrib['index'], 'yellow'),
                colored(aya.attrib['text'], 'yellow')
            ])

        table_data.append([
            meaning[index].attrib['index'],
            meaning[index].attrib['text']
        ])

    return table_data

def search_translations(keyword, arabic):
    global meta, quran, meaning

    results = []

    for index, chapter in enumerate(meaning):
        for aya in chapter.findall('aya'):
            verse_text = aya.attrib['text']
            verse_index = aya.attrib['index']
            chapter_name = meta[index].attrib['tname']
            chapter_name_english = meta[index].attrib['ename']
            arabic_text = ''

            if keyword.lower() in verse_text.lower():
                if arabic and arabic == '0':
                    arabic_text = quran[index].findall('aya')[int(verse_index)-1].attrib['text']

                results.append({
                    'chapter': chapter.attrib['index'] + ' - ' + chapter_name,
                    'verse': verse_index,
                    'arabic': arabic_text,
                    'text': verse_text
                })

    if not results:
        print(colored('Nothing found for given text.', 'red'))
        return

    table_data = [
        [colored('Chapter', 'cyan'), colored('Verse', 'cyan'), colored('Text', 'cyan')]
    ]

    for result in results:
        if arabic and arabic == '0':
            table_data.append([
                colored(result['chapter'], 'green'),
                colored(result['verse'], 'green'),
                colored(result['arabic'], 'yellow')
            ])
        else:
            table_data.append([
                colored(result['chapter'], 'green'),
                colored(result['verse'], 'green'),
                result['text']
            ])

    table_data.append([colored('Total Results: ' + str(len(results)), 'magenta')])

    print(tabulate(table_data))

if __name__ == '__main__':
    chapters()  # Default action if script is executed directly

