#!/usr/bin/env python3
import os
import sys
import xml.etree.ElementTree as ET
import shutil
import textwrap
from termcolor import colored
import difflib
import re

def get_data_path(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(script_dir, 'data', filename)
    #print(f"DEBUG: Looking for file at {path}")  # Debug print
    return path

def load_quran_data():
    try:
        arabic_path = get_data_path('ar.quran.xml')
        arabic_tree = ET.parse(arabic_path)
    except FileNotFoundError:
        print(f"Error: Quran data file '{arabic_path}' not found.")
        sys.exit(1)

    try:
        english_path = get_data_path('en.quran.xml')
        english_tree = ET.parse(english_path)
    except FileNotFoundError:
        print(f"Error: Quran data file '{english_path}' not found.")
        sys.exit(1)

    arabic_root = arabic_tree.getroot()
    english_root = english_tree.getroot()

    return arabic_root, english_root

def alias_command(args):
    if args[0] == "-s":
        return ["search"] + args[1:]
    if args[0] == "-c":
        return ["count"] + args[1:]
    if args[0].startswith('/'):
        return ["search", args[0][1:]] + args[1:]
    return args

def highlight(text, word, no_highlight):
    if no_highlight:
        return text
    regex = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    return regex.sub(lambda match: colored(match.group(), 'cyan'), text)

def print_wrapped_verse(chapter_num, verse_num, text):
    width, _ = shutil.get_terminal_size()
    indent = ' ' * (len(f"{chapter_num}:{verse_num}") + 4)
    wrapper = textwrap.TextWrapper(width=width, initial_indent='', subsequent_indent=indent)
    wrapped_text = wrapper.fill(f"{chapter_num}:{verse_num}    {text}")
    print(wrapped_text)

def chapter_name_to_number(name):
    _, english_root = load_quran_data()
    chapters = {sura.get('ename').lower(): int(sura.get('index')) for sura in english_root.findall('./sura')}
    chapters.update({sura.get('tname').lower(): int(sura.get('index')) for sura in english_root.findall('./sura')})

    if name.lower() in chapters:
        return chapters[name.lower()]
    else:
        closest_match = difflib.get_close_matches(name.lower(), chapters.keys(), n=1)
        if closest_match:
            return chapters[closest_match[0]]
        else:
            print(f"Error: Invalid chapter name '{name}'.")
            sys.exit(1)

def parse_chapter_range(range_str):
    verse_pattern = re.compile(r"(\d+):(\d+)-(\d+):(\d+)")
    single_chapter_verse_pattern = re.compile(r"(\d+):(\d+)-(\d+)")
    single_chapter_pattern = re.compile(r"(\d+):(\d+)")

    if verse_pattern.match(range_str):
        start_chap, start_verse, end_chap, end_verse = map(int, verse_pattern.match(range_str).groups())
        return (start_chap, start_verse, end_chap, end_verse)
    elif single_chapter_verse_pattern.match(range_str):
        chapter, start_verse, end_verse = map(int, single_chapter_verse_pattern.match(range_str).groups())
        return (chapter, start_verse, chapter, end_verse)
    elif single_chapter_pattern.match(range_str):
        chapter, verse = map(int, single_chapter_pattern.match(range_str).groups())
        return (chapter, verse, chapter, verse)
    elif '-' in range_str:
        start, end = range_str.split('-')
        start_chap = chapter_name_to_number(start) if not start.isdigit() else int(start)
        end_chap = chapter_name_to_number(end) if not end.isdigit() else int(end)
        return (start_chap, None, end_chap, None)
    else:
        chap = chapter_name_to_number(range_str) if not range_str.isdigit() else int(range_str)
        return (chap, None, chap, None)

def read(chapter_num, verse_spec=None, lang="both", highlight_word=None, show_heading=True):
    arabic_root, english_root = load_quran_data()

    chapter_ar = arabic_root.find(f"./sura[@index='{chapter_num}']")
    chapter_en = english_root.find(f"./sura[@index='{chapter_num}']")
    if chapter_ar is None or chapter_en is None:
        print("Error: Invalid chapter number.")
        return

    if show_heading:
        if lang == "arabic":
            print(f"Chapter {chapter_num} - {chapter_ar.get('name')}:")
        elif lang == "english":
            print(f"Chapter {chapter_num} - {chapter_en.get('ename')}:")
        else:
            print(f"Chapter {chapter_num} - {chapter_en.get('ename')} ({chapter_en.get('tname')}) - {chapter_ar.get('name')}")
        if chapter_num not in [1, 9]:
            print("بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ")

    if verse_spec:
        if '-' in verse_spec:
            start, end = map(int, verse_spec.split('-'))
            for verse_num in range(start, end + 1):
                arabic_verse = arabic_root.find(f"./sura[@index='{chapter_num}']/aya[@index='{verse_num}']")
                english_verse = english_root.find(f"./sura[@index='{chapter_num}']/aya[@index='{verse_num}']")
                if arabic_verse is None or english_verse is None:
                    print(f"{chapter_num}:{verse_num}: Not found")
                else:
                    if lang in ("both", "arabic"):
                        text = arabic_verse.get('text')
                        if highlight_word:
                            text = highlight(text, highlight_word, False)
                        print_wrapped_verse(chapter_num, verse_num, text)
                    if lang in ("both", "english"):
                        text = english_verse.get('text')
                        if highlight_word:
                            text = highlight(text, highlight_word, False)
                        print_wrapped_verse(chapter_num, verse_num, text)
        else:
            verse_num = int(verse_spec)
            arabic_verse = arabic_root.find(f"./sura[@index='{chapter_num}']/aya[@index='{verse_num}']")
            english_verse = english_root.find(f"./sura[@index='{chapter_num}']/aya[@index='{verse_num}']")
            if arabic_verse is None or english_verse is None:
                print(f"{chapter_num}:{verse_num}: Not found")
            else:
                if lang in ("both", "arabic"):
                    text = arabic_verse.get('text')
                    if highlight_word:
                        text = highlight(text, highlight_word, False)
                    print_wrapped_verse(chapter_num, verse_num, text)
                if lang in ("both", "english"):
                    text = english_verse.get('text')
                    if highlight_word:
                        text = highlight(text, highlight_word, False)
                    print_wrapped_verse(chapter_num, verse_num, text)
    else:
        for aya in arabic_root.findall(f"./sura[@index='{chapter_num}']/aya"):
            if lang in ("both", "arabic"):
                text = aya.get('text')
                if highlight_word:
                    text = highlight(text, highlight_word, False)
                print_wrapped_verse(chapter_num, aya.get('index'), text)
            english_verse = english_root.find(f"./sura[@index='{chapter_num}']/aya[@index='{aya.get('index')}']")
            if english_verse is not None and lang in ("both", "english"):
                text = english_verse.get('text')
                if highlight_word:
                    text = highlight(text, highlight_word, False)
                print_wrapped_verse(chapter_num, aya.get('index'), text)

def read_range(range_spec, lang="both", highlight_word=None, no_chapter_headings=False):
    start_chap, start_verse, end_chap, end_verse = parse_chapter_range(range_spec)

    current_chap = start_chap
    first_pass = True

    if current_chap < 1 or current_chap > 114 or end_chap < 1 or end_chap > 115:
        print("Error: Chapter number must be between 1 and 114.")
        return

    while current_chap < end_chap or (current_chap == end_chap and (end_verse is None or start_verse <= end_verse)):
        if start_verse and end_verse and current_chap == start_chap:
            for verse_num in range(start_verse, end_verse + 1):
                read(current_chap, f"{verse_num}-{verse_num}", lang=lang, highlight_word=highlight_word, show_heading=first_pass and not no_chapter_headings)
        elif end_verse and current_chap == end_chap:
            for verse_num in range(1, end_verse + 1):
                read(current_chap, f"{verse_num}-{verse_num}", lang=lang, highlight_word=highlight_word, show_heading=first_pass and not no_chapter_headings)
        else:
            read(current_chap, lang=lang, highlight_word=highlight_word, show_heading=first_pass and not no_chapter_headings)
        
        first_pass = False
        current_chap += 1

def search(keyword, range_spec=None, output_file=None, no_chapter_headings=False, no_highlight=False):
    arabic_root, english_root = load_quran_data()
    found = False
    results = []
    count = 0

    keyword_regex = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)

    if range_spec:
        start_chap, start_verse, end_chap, end_verse = parse_chapter_range(range_spec)
        ranges = [(start_chap, start_verse, end_chap, end_verse)]
    else:
        ranges = [(1, None, 115, None)]

    for start_chap, start_verse, end_chap, end_verse in ranges:
        if int(start_chap) < 1 or int(end_chap) > 115:
            print("Error: Chapter number must be between 1 and 114.")
            return

        for chap_num in range(int(start_chap), int(end_chap) + 1):
            sura = english_root.find(f"./sura[@index='{chap_num}']")
            if sura is None:
                continue
            chapter_num = sura.get('index')
            chapter_name = sura.get('ename')
            chapter_results = []

            for aya in sura.findall('./aya'):
                verse_num = int(aya.get('index'))
                if start_verse and chap_num == int(start_chap) and verse_num < int(start_verse):
                    continue
                if end_verse and chap_num == int(end_chap) and verse_num > int(end_verse):
                    continue

                verse_text = aya.get('text')
                if keyword_regex.search(verse_text):
                    verse_text = highlight(verse_text, keyword, no_highlight)
                    count += 1
                    if not found:
                        results.append(f"Chapter {chapter_num} - {chapter_name}:")
                        found = True
                    chapter_results.append(f"{chapter_num}:{aya.get('index')}    {verse_text}")

            if chapter_results:
                if not no_chapter_headings:
                    results.append(f"Chapter {chapter_num} - {chapter_name}:")
                results.extend(chapter_results)

    if not found:
        results.append(f"There are no instances of '{keyword}' in the selected range.")
    else:
        results.insert(0, f"There were '{count}' occurrences of '{keyword}' in your selected range")
        results.insert(0, "In the Name of Allah, The Merciful, the Gracious")

    output = "\n".join(results)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"Results written to {output_file}")
    else:
        for result in results:
            print(result)

def search_info(info_type, range_spec, lang="both"):
    arabic_root, english_root = load_quran_data()
    start_chap, start_verse, end_chap, end_verse = parse_chapter_range(range_spec)

    if start_chap < 1 or end_chap > 115:
        print("Error: Chapter number must be between 1 and 114.")
        return

    if info_type not in ["verses", "rukus", "starts", "type", "order"]:
        print("Error: Invalid info type. Valid types are: verses, rukus, starts, type, order")
        return

    results = []
    for chap_num in range(start_chap, end_chap + 1):
        chapter_ar = arabic_root.find(f"./sura[@index='{chap_num}']")
        chapter_en = english_root.find(f"./sura[@index='{chap_num}']")
        if chapter_ar is None or chapter_en is None:
            continue

        if lang == "arabic":
            chapter_name = chapter_ar.get('name')
        elif lang == "english":
            chapter_name = chapter_en.get('ename')
        else:
            chapter_name = f"{chapter_en.get('ename')} ({chapter_en.get('tname')})"

        if info_type == "starts":
            chapter_info = chapter_en.get("start")
            results.append(f"{chap_num}. {chapter_name} - Starts at Verse: {chapter_info}")
        else:
            chapter_info = chapter_en.get(info_type)
            results.append(f"{chap_num}. {chapter_name} - {info_type.capitalize()}: {chapter_info}")

    for result in results:
        print(result)

def count(keyword, range_spec=None, output_file=None):
    _, english_root = load_quran_data()
    total_count = 0
    results = []

    keyword_regex = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)

    if range_spec:
        start_chap, start_verse, end_chap, end_verse = parse_chapter_range(range_spec)
        ranges = [(start_chap, start_verse, end_chap, end_verse)]
    else:
        ranges = [(1, None, 115, None)]

    for start_chap, start_verse, end_chap, end_verse in ranges:
        if int(start_chap) < 1 or int(end_chap) > 115:
            print("Error: Chapter number must be between 1 and 114.")
            return

        for chap_num in range(int(start_chap), int(end_chap) + 1):
            sura = english_root.find(f"./sura[@index='{chap_num}']")
            if sura is None:
                continue

            for aya in sura.findall('./aya'):
                verse_num = int(aya.get('index'))
                if start_verse and chap_num == int(start_chap) and verse_num < int(start_verse):
                    continue
                if end_verse and chap_num == int(end_chap) and verse_num > int(end_verse):
                    continue

                verse_text = aya.get('text')
                if keyword_regex.search(verse_text):
                    total_count += 1

    results.append(f"There were '{total_count}' occurrences of '{keyword}' in the selected range")
    output = "\n".join(results)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"Results written to {output_file}")
    else:
        print(output)

def info(chapter_range):
    arabic_root, english_root = load_quran_data()
    start_chap, start_verse, end_chap, end_verse = parse_chapter_range(chapter_range)

    if start_chap < 1 or end_chap > 115:
        print("Error: Chapter number must be between 1 and 114.")
        return

    for chap_num in range(start_chap, end_chap + 1):
        chapter_ar = arabic_root.find(f"./sura[@index='{chap_num}']")
        chapter_en = english_root.find(f"./sura[@index='{chap_num}']")
        if chapter_ar is None or chapter_en is None:
            continue

        print(f"Chapter {chap_num} Info:")
        print(f"Name (Arabic): {chapter_ar.get('name')}")
        print(f"Transliterated Name: {chapter_ar.get('tname')}")
        print(f"English Name: {chapter_en.get('ename')}")
        print(f"Verses: {chapter_ar.get('ayas')}")
        print(f"Rukus: {chapter_ar.get('rukus')}")
        print(f"Starts at Verse: {chapter_en.get('start')}")
        print(f"Type: {chapter_ar.get('type')}")
        print(f"Order: {chapter_ar.get('order')}")
        print()

def main():
    if len(sys.argv) < 2:
        print("Usage: quran <command> [<args>] [-a | -e] [-nc] [-nh]")
        sys.exit(1)

    command_args = sys.argv[1:]
    no_chapter_headings = False
    no_highlight = False

    if "-nc" in command_args:
        no_chapter_headings = True
        command_args.remove("-nc")
        
    if "-nh" in command_args:
        no_highlight = True
        command_args.remove("-nh")

    command_args = alias_command(command_args)
    command = command_args[0]

    lang = "both"
    highlight_word = None

    if "-a" in command_args:
        lang = "arabic"
        command_args.remove("-a")
    elif "-e" in command_args:
        lang = "english"
        command_args.remove("-e")
    if "-h" in command_args:
        highlight_index = command_args.index("-h")
        if highlight_index + 1 < len(command_args):
            highlight_word = command_args[highlight_index + 1]
            command_args = command_args[:highlight_index] + command_args[highlight_index + 2:]
        else:
            print("Usage: quran <command> [<args>] [-a | -e] [-h <word>]")
            sys.exit(1)

    specific_commands = {
        "chapters", "info", "rukus", "starts", "verses", "type", "order"
    }

    if command == "commands":
        print("Commands:")
        print("  chapters          List chapters in English")
        print("  chapters -a       List chapters in Arabic")
        print("  info              Show info for all chapters")
        print("  info <chapter>    Show info for a specific chapter")
        print("  info <start>-<end> Show info for a range of chapters")
        print("  <chapter>         Read full chapter")
        print("  <chapter>:<verse> Read specific verse")
        print("  <chapter>:<start>-<end> Read range of verses")
        print("  <chapter>:<verse> -e   Read specific verse in English")
        print("  <chapter>:<verse> -a   Read specific verse in Arabic")
        print("  <chapter>:<start>-<end> -e   Read range of verses in English")
        print("  <chapter>:<start>-<end> -a   Read range of verses in Arabic")
        print("  <chapter> -h <word> Highlight word in chapter")
        print("  <chapter>:<verse> -h <word> Highlight word in verse")
        print("  <chapter>:<start>-<end> -h <word> Highlight word in range of verses")
        print("  <chapter> <chapter>:<verse> -h <word> Highlight word in multiple chapters")
        print("  /<keyword>        Search keyword in entire Quran")
        print("  /<keyword> <range> Search keyword in specific range")
        print("  /<keyword> <range> -nc       Search keyword in specific range without chapter headings")
        print("  /<keyword> <range> -nh       Search keyword in specific range without highlighting")
        print("  count <keyword>   Count occurrences of keyword in entire Quran")
        print("  count <keyword> <range> Count occurrences of keyword in specific range")
        print("  <info_type> <range> [-a | -e] Search specific info in range (info_type can be: verses, rukus, starts, type, order)")
    elif command == "chapters":
        output_file = command_args[1] if len(command_args) > 1 and command_args[1].startswith(">") else None
        chapters(lang=lang, output_file=output_file)
    elif command == "info":
        chapter_range = command_args[1] if len(command_args) > 1 else "1-114"
        info(chapter_range)
    elif command == "search":
        if len(command_args) < 2:
            print("Usage: quran search <keyword> [range] [-nh]")
            sys.exit(1)
        keyword = command_args[1]
        range_spec = command_args[2] if len(command_args) > 2 else None
        output_file = command_args[3] if len(command_args) > 3 and command_args[3].startswith(">") else None
        search(keyword, range_spec, output_file, no_chapter_headings, no_highlight)
    elif command == "count":
        if len(command_args) < 2:
            print("Usage: quran count <keyword> [range]")
            sys.exit(1)
        range_spec = command_args[2] if len(command_args) > 2 else None
        output_file = command_args[3] if len(command_args) > 3 and command_args[3].startswith(">") else None
        count(command_args[1], range_spec, output_file)
    elif command in specific_commands:
        if len(command_args) < 2:
            print(f"Usage: quran {command} <range> [-a | -e]")
            sys.exit(1)
        range_spec = command_args[1]
        search_info(command, range_spec, lang=lang)
    else:
        if ":" in command and "-" in command:
            read_range(command, lang=lang, highlight_word=None if no_highlight else highlight_word, no_chapter_headings=no_chapter_headings)
        elif ":" in command:
            parts = command.split(':')
            chapter_num = parts[0]
            verse_spec = parts[1] if len(parts) > 1 else None
            chapter_num = chapter_name_to_number(chapter_num) if not chapter_num.isdigit() else int(chapter_num)
            read(chapter_num, verse_spec, lang=lang, highlight_word=None if no_highlight else highlight_word, show_heading=not no_chapter_headings)
        elif '-' in command:
            read_range(command, lang=lang, highlight_word=None if no_highlight else highlight_word, no_chapter_headings=no_chapter_headings)
        else:
            chapter_num = chapter_name_to_number(command) if not command.isdigit() else int(command)
            read(chapter_num, lang=lang, highlight_word=None if no_highlight else highlight_word, show_heading=not no_chapter_headings)

if __name__ == "__main__":
    main()
