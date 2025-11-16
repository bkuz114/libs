"""
Utility for generating marked up HTML for Russian
sentences indicating noun declensions.
(Made for my various Ru language learning tools
for teaching noun declensions.)

Use this class if you have multiple HTML files (or
.txt/.json, etc. that you're using pythong to
convert into HTML), which have example sentences
demonstrating noun declension patterns; this will
give an easy way to add the example sentences straight
into those files, rather than having to add the
markup within the files. This makes for cleaner/easier
to read files, and also easier to handle if global
changes need to be handled (changing css classes,
tags, lang attrs, etc.)

usage:

    import declension_utils as marker

    to_mark = "[Иван*а] сын."
    marked = marker.mark_sentence(
                        to_mark, "[", "]",
                        "[[", "]]", "*",
                        False, True, True)
    print(to_mark)
    print(marked)

    "[Иван*а] сын."
    "<span class="c1 c2">Иавн</span><span class="e1">а</span>&nbsp;сын."

"""

import re


def is_regex_char(string):
    """checks if a string is a reserved regex char"""
    regex_chars = [
            "^", "$", ".", "*", "+", "?", "{", "}",
            "[", "]", "(", ")", "|", "\\"]
    if string in regex_chars:
        return True
    return False


def escape_string(string):
    """escapes regex chars within a string"""
    newstr = ""
    for char in string:
        if is_regex_char(char):
            char = "\\" + char
        newstr += char
    return newstr


def wrap_in_tag(html_str, tag_name, classes=[], lang_attr=None):
    """
    Wraps String in HTML tag specified. Optional class list.
    Example: wrap_in_tag("my text", "div", ["a", "b", "c"])
    Returns: "<div class="a b c">my text</div>"

    :param Str html_str: string of HTML to wrap in a tag
    :param Str tag_name: type of tag (e.g. "span", "div")
    :param list<Str> classes: css classes to add to tag.
    :param Str lang_attr: if supplied, adds lang attr
        to the tag, with this value i.e. <span lang="ru">
    """

    wrap = "<" + tag_name
    if classes:
        class_list = " ".join(classes)
        wrap += " class='" + class_list + "'"
    if lang_attr:
        wrap += " lang='" + lang_attr + "'"
    wrap += ">" + html_str + "</" + tag_name + ">"
    return wrap


def mark_noun(noun, delim, dictionary_form=False, add_lang_attr=True,
              base_classes=[], declension_classes=[],
              add_space_start=False, add_space_end=False):
    """
    takes an example noun that's been marked for declension
    and returns a string of HTML seperating the root and
    declined portion in <span> tags.

    Example (assuming default DeclensionMarker delims and css classes):
        mark_noun("Иван*а")

    returns:
        "<span class="base">Иван</span><span class="end">а</span>"

    :param String noun: noun to mark up
    :param Str delim: delimeter separating noun base from declined end
        (i.e. * in Иван*а)
    :param boolean dictionary_form: if True, noun should be in
        dictionary form (this way can err if there's
        no delim on a non-nom noun)
    :param boolean add_lang_attr: if True, adds lang="ru" to
        <span> tags
    :param list<Str> base_classes: css classes to add to <span> for
        base of noun
    :param list<Str> declension_classes: css classes to add to <span>
        for declined ending
    :param boolean add_space_start: if True, adds <span>&nbsp;</span>
        before opening/base <span> (used when noun is preceeded by
        a space in the sentence, and font-size=0 on parent tag --
        a strategry for removing defualt spacing around <span> tags)
    :param boolean add_space_end: if True, adds <span>&nbsp;</span>
        after last/declension <span> (used when noun is followed by
        a space in the sentence, and font-size=0 on parent tag --
        a strategy for removing default spacing around <span> tags)
    :return Str: the noun marked up in HTML
    """

    marked = ""

    lang_attr = None
    if add_lang_attr:
        lang_attr = "ru"

    split_noun = noun.split(delim)
    if len(split_noun) == 1:  # no * char; no change, such as acc masc inan
        marked += wrap_in_tag(
                split_noun[0], "span", base_classes, lang_attr)
    elif len(split_noun) == 2:  # regular stuff
        if dictionary_form:
            raise Exception(
                    "Example noun ({}) indicated as ditionary form "
                    "but has declension delimeter "
                    "({})".format(noun, delim))
        if not split_noun[0]:
            raise Exception(
                    "Delimeter at beginning of noun ({}): "
                    "{} is used to mark declined "
                    "ending".format(noun, delim))
        else:
            # wrap portion of noun up to declension
            marked += wrap_in_tag(
                    split_noun[0], "span", base_classes, lang_attr)
        if not split_noun[1]:
            # zero ending noun, i.e. not nom, but no ending
            print("Zero-ending... figure this out later...")
        else:
            # wrap declined ending in <span>
            marked += wrap_in_tag(
                split_noun[1], "span",
                declension_classes, lang_attr)
    else:
        raise Exception("Noun has more than one {} char".format(delim))

    # add spaces to front or end of span
    # &nbsp; must be in a <span>, else it will get
    # font-size:0 of the parent and it won't show up
    SPACE = "<span>&nbsp;</span>"
    if add_space_start:
        marked = SPACE + marked
    if add_space_end:
        marked = marked + SPACE
    return marked


def mark_sentence(sentence,
                  open_delim_non_nom, close_delim_non_nom,
                  open_delim_nom, close_delim_nom, noun_delim,
                  wrap_sentence_in_spans=False,
                  convert_space_to_nbsp=True, add_lang_attr=False,
                  encapsulation_tag=None,
                  base_classes=[],
                  declension_classes=[],
                  sentence_classes=[],
                  pad_spans=False):
    """
    Returns HTML markup for an example sentence

    Example (assuming default DeclensionMarker delims and css classes):
        mark_sentence("[Иван*а] cын.")

    returns:
        "<span class='base'>Иван</span><span class='end'>а</span> сын."

    :param Str sentence: sentence to makeup
    :param Str open_delim_non_nom: left delimeter that encapsulates
        declined nouns (i.e. [ in [Иван*а])
    :param Str close_delim_non_nom: right delimeter that encapsulates
        declined nouns (i.e. ] in [Иван*а])
    :param Str open_delim_nom: left delimeter that encapsulates
        nouns in the nominative case (no declension)
        (i.e. [[ in [[Иван]])
    :param Str close_delim_nom: right delimeter that encapsulates
        nouns in the nominative case (no declension)
        (i.e. ]] in [[Иван]])
    :param Str noun_delim: delimeter to split nouns on
        (i.e. * in Иван*а)
    :param boolean wrap_sentence_in_spans: if True, then
        non-noun part of sentence gets wrapped in <span> tags
        as well (i.e.
            <span>Иван</span><span>а</span><span> сын.</span>)
    :paran boolean convert_space_to_nbsp: if True, convert
        returned HTML should have &nbsp; in place of space
        chars. This can be necessary depending on the
        css on parent classes, as space chars might be eliminated,
        resulting in <span> tags with no spacing between them.
    :param boolean add_lang_attr: if True, adds lang="ru" to
        <span> tags
    :param String encapsulation_tag: a tag to wrap the entire
        marked up sentence in ("span", "div", etc.)
    :param list<Str> base_classes: css classes for <span>
        capturing noun UP to declined part (in addition
    :param list<Str> declension_classes: css classes for <span>
        capturing declined part of a noun
    :param list<Str> sentence_classes: css classes for <span>
        for non-noun part of sentences
        (only used if wrap_sentence_in_spans=True)
    :paran boolean pad_spans: if True, then:
        1. adds <span>&nbsp;</span> BEFORE noun <span>s if noun
           preceeded by space (i.e. "Папа [Борис*а]")
        2. adds <span>&nbspl</span> AFTER noun <span>s if noun
           is followed by space (i.e. "[Иван*а] сын")
        (This is needed for cases where font-size=0 on parent tag,
        which is a strategy for removing automatic spacing around
        <span> tags; in such scenarios, the space prior to that noun
        <span> will NOT render in the browser, and would end up with
        "ПапаБориса", hence the need for this option)
    :return Str: String of marked up HTMl for sentence
    """

    noun_section = ""
    before_noun = ""
    after_noun = ""
    dictionary_form = False
    noun_starts_sentence = False
    noun_ends_sentence = False

    if convert_space_to_nbsp:
        sentence = sentence.replace(" ", "&nbsp;")

    # determine which delimeters noun is encapsulated in
    open_delim = None
    close_delim = None
    if open_delim_non_nom and close_delim_non_nom in sentence:
        open_delim = open_delim_non_nom
        close_delim = close_delim_non_nom
    if open_delim_nom and close_delim_nom in sentence:
        open_delim = open_delim_nom
        close_delim = close_delim_nom
        dictionary_form = True
    if not open_delim or not close_delim:
        raise Exception(
                "Can't find delimeter set in sentence. Sets:"
                "{} {} (for nouns which decline in the sentence "
                "or {} {} (for nominative examples"
                ")".format(
                    open_delim_non_nom, close_delim_non_nom,
                    open_delim_nom, close_delim_nom))

    # section to left of noun
    sentence_split = sentence.split(open_delim)
    if len(sentence_split) == 2:
        before_noun = sentence_split[0]
        if not before_noun:
            # open delim first char in sentence
            noun_starts_sentence = True
        rest = sentence_split[1]
    elif len(sentence_split) < 2:
        raise Exception(
            "No {} char (noun not encapsulated in "
            "{} {})".format(open_delim, open_delim, close_delim))
    if len(sentence_split) > 2:
        raise Exception(
            "Too many {} chars (noun should be encapsulated in "
            "{} {})".format(open_delim, open_delim, close_delim))

    # noun section + section to right
    sentence_split = rest.split(close_delim)
    if len(sentence_split) == 2:
        noun_section = sentence_split[0]
        after_noun = sentence_split[1]
        if not noun_section:
            raise Exception(
                    "{} {} delimeters, but no noun "
                    "inside".format(open_delim, close_delim))
        if after_noun == after_noun.lstrip():
            # no space follows the noun
            # (either it ends sentence, or
            # punctunation immediately follows,
            # i.e. [Борис*а].)
            noun_ends_sentence = True
    elif len(sentence_split) < 2:
        raise Exception(
                "No {} char (noun not encapsulated in "
                "{} {}".format(close_delim, open_delim, close_delim))
    elif len(sentence_split) > 2:
        raise Exception(
            "Too many {} chars (noun should be encapsulated in "
            "{} {})".format(close_delim, open_delim, close_delim))

    # markup noun
    add_space_start = False
    add_space_end = False
    if pad_spans and not noun_starts_sentence:
        add_space_start = True
    if pad_spans and not noun_ends_sentence:
        add_space_end = True
    noun_markup = mark_noun(
            noun_section, noun_delim,
            dictionary_form, add_lang_attr,
            base_classes,
            declension_classes,
            add_space_start, add_space_end)

    # wrap remaining parts of sentence in <span> tags if requested
    if wrap_sentence_in_spans:
        lang_attr = None
        if add_lang_attr:
            lang_attr = "ru"
        if before_noun:
            before_noun = wrap_in_tag(
                    before_noun, "span", sentence_classes, lang_attr)
        if after_noun:
            after_noun = wrap_in_tag(
                    after_noun, "span", sentence_classes, lang_attr)

    marked = before_noun + noun_markup + after_noun

    # wrap entire marked up sentence in a tag if requrested
    if encapsulation_tag:
        marked = wrap_in_tag(marked, encapsulation_tag)

    return marked


def mark_string(string,
                open_delim_sentence, close_delim_sentence,
                open_delim_non_nom, close_delim_non_nom,
                open_delim_nom, close_delim_nom,
                noun_delim,
                wrap_sentence_parts_in_spans=False,
                convert_spaces_to_nbsp=False, add_lang_attr=False,
                base_classes=[],
                declension_classes=[],
                sentence_classes=[],
                pad_spans=False):

    """
    finds all example sentences in a String and marks them

    example (assuming default DeclensionMarker delims and css classes):

    "<html>
        <head></head>
        <body>
            {[Иван*а] сын.}
            <br>
            {Папа [Бор*и].}
        </body>
    </html>"

    returns:

    "<html>
        <head></head>
        <body>
        <span class="base">Иван</span><span class="end">а</span>&nbsp;сын
        <br>
        Папа&nbsp;<span class="base">Бор</span><span class="end">и</span>.
        </body>
    </html>"

    :param String string: the string to find example sentences in
    :param Str open_delim_sentence: left delimeter that encapsulates
        entire example sentences
        (i.e. { in {[Иван*а] сын.})
    :param Str close_delim_sentence: right delimeter that encapsulates
        entire example sentences
        (i.e. } in {[Иван*а] сын.})
    :param Str open_delim_non_nom: left delimeter that encapsulates
        declined nouns (i.e. [ in [Иван*а])
    :param Str close_delim_non_nom: right delimeter that encapsulates
        declined nouns (i.e. ] in [Иван*а])
    :param Str open_delim_nom: left delimeter that encapsulates
        nouns in the nominative case (no declension)
        (i.e. [[ in [[Иван]])
    :param Str close_delim_nom: right delimeter that encapsulates
        nouns in the nominative case (no declension)
        (i.e. ]] in [[Иван]])
    :param Str noun_delim: delimeter to split nouns on
        (i.e. * in Иван*а)
    :param boolean wrap_sentence_parts_in_spans: if True, then
        non-noun parts of sentence gets wrapped in <span> tags
        as well (i.e.
            <span>Иван</span><span>а</span><span> сын.</span>)
    :paran boolean convert_space_to_nbsp: if True, converts
        space chars in example sentences to &nbsp;
        (Necessary depending on css on parent classes, as space
        chars might be eliminated, resulting in <span> tags with
        no spacing between them.)
    :param boolean add_lang_attr: if True, adds lang="ru" to
        <span> tags
    :param list<Str> base_classes: css classes for <span>
        capturing nouns UP to declined part
    :param list<Str> declension_classes: css classes for <span>
        capturing declined parts of noun
    :param list<Str> sentence_classes: css classes for <span>
        tags encapsulating non-noun parts of example sentences
        (only used if wrap_sentence_parts_in_spans=True)
    :paran boolean pad_spans: if True, then:
        1. adds <span>&nbsp;</span> BEFORE noun <span>s if noun
           preceeded by space (i.e. "Папа [Борис*а]")
        2. adds <span>&nbspl</span> AFTER noun <span>s if noun
           is followed by space (i.e. "[Иван*а] сын")
        (This is needed for cases where font-size=0 on parent tag,
        which is a strategy for removing automatic spacing around
        <span> tags; in such scenarios, the space prior to that noun
        <span> will NOT render in the browser, and would end up with
        "ПапаБориса", hence the need for this option)
    :return String: string with all example sentences replaced with
        their marked up version
    """

    escaped_delim_sentence_open = escape_string(open_delim_sentence)
    escaped_delim_sentence_close = escape_string(close_delim_sentence)

    res = re.findall(
            r"({}(.*?){})".format(
                escaped_delim_sentence_open, escaped_delim_sentence_close),
            string)
    for (enclosed_sentence, sentence) in res:
        string = string.replace(
                enclosed_sentence,
                mark_sentence(
                    sentence,
                    open_delim_non_nom, close_delim_non_nom,
                    open_delim_nom, close_delim_nom,
                    noun_delim,
                    wrap_sentence_parts_in_spans,
                    convert_spaces_to_nbsp, add_lang_attr,
                    base_classes,
                    declension_classes,
                    sentence_classes,
                    pad_spans))
    return string
