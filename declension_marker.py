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

    from declension_marker import DeclensionMarker

    marker = DeclensionMarker(
        "*", "[", "]", "[[", "]]",
        "{", "}", ["c1, c2"], ["e1"],
        ["ex"])

    to_mark = "[Иван*а] сын."
    marked = marker.mark_sentence(to_mark, False, True, True)
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


class DeclensionMarker:

    def __init__(
            self, delim_declension="*",
            delim_noun_open="[", delim_noun_close="]",
            delim_nom_noun_open="[[", delim_nom_noun_close="]]",
            delim_sentence_open="{", delim_sentence_close="}",
            base_classes=["base"], declension_classes=["end"],
            example_sentence_classes=["example"]):

        """
        :param Str delim_declension: delimeter to split nouns on
            (i.e. * in Иван*а)
        :param Str delim_noun_open: left delimeter that encapsulates nouns
            (i.e. [ in [Иван*а])
        :param Str delim_noun_close: right delimeter that encapsulates nouns
            (i.e. ] in [Иван*а])
        :param Str delim_nom_noun_open: left delimeter that encapsulates
            nouns in the nominative case (no declension)
            (i.e. [[ in [[Иван]])
        :param Str delim_noun_close: right delimeter that encapsulates
            nouns in the nominative case (no declension)
            (i.e. ]] in [[Иван]])
        :param Str delim_sentence_open: left delimeter that encapsulates
            entire example sentences
            (i.e. { in {[Иван*а] сын.})
        :param Str delim_sentence_close: right delimeter that encapsulates
            entire example sentences
            (i.e. } in {[Иван*а] сын.})
        :param list<String> base_classes: css classes to add to
            <span> of base parts of nouns (part prior to declension)
            (i.e. <span class="base">Иван</span><span>а</span>)
        :param list<String> declension_classes: sets css classes to add
            to <span> of declined parts of nouns
            (i.e. <span>Иван</span><span class="end">а</span>)
        """

        self.delim_declension = delim_declension
        self.delim_noun_open = delim_noun_open
        self.delim_noun_close = delim_noun_close
        self.delim_nom_noun_open = delim_nom_noun_open
        self.delim_nom_noun_close = delim_nom_noun_close
        self.delim_sentence_open = delim_sentence_open
        self.delim_sentence_close = delim_sentence_close
        self.base_classes = base_classes
        self.declension_classes = declension_classes
        self.example_sentence_classes = example_sentence_classes

    def mark_noun(self, noun, dictionary_form=False, add_lang_attr=True):
        """
        takes an example noun that's been marked for declension
        and returns a string of HTML seperating the root and
        declined portion in <span> tags.

        Example (assuming default DeclensionMarker delims and css classes):
            mark_noun("Иван*а")

        returns:
            "<span class="base">Иван</span><span class="end">а</span>"

        :param String noun: noun to mark up
        :param boolean dictionary_form: if True, noun should be in
            dictionary form (this way can err if there's
            no delim on a non-nom noun)
        :param boolean add_lang_attr: if True, adds lang="ru" to
            <span> tags
        :return Str: the noun marked up in HTML
        """

        lang_attr = None
        if add_lang_attr:
            lang_attr = "ru"

        markup = []
        parsed = noun.split(self.delim_declension)
        # wrap base (noun up to delined portion) in <span>
        markup.append(
                wrap_in_tag(parsed[0], "span", self.base_classes, lang_attr))
        if len(parsed) > 1:
            if dictionary_form:
                raise Exception(
                        "Example noun ({}) indicated as ditionary form "
                        "but has declension delimeter "
                        "({})".format(noun, self.delim_declension))
            else:
                if len(parsed) == 2:
                    if not parsed[0]:
                        raise Exception(
                                "Delimeter at beginning of noun ({}): "
                                "{} is used to mark declined "
                                "ending".format(noun, self.delim_declension))
                    if not parsed[1]:
                        # 0-ending noun i.e. not nom, but no ending
                        print("Zero-ending... figure this out later...")
                    else:
                        # wrap declined ending in <span>
                        markup.append(wrap_in_tag(
                            parsed[1], "span",
                            self.declension_classes, lang_attr))
                else:
                    raise Exception(
                            "Multiple delimeters in noun! {}".format(noun))
        else:
            if not dictionary_form:
                raise Exception(
                        "No delimeter ({}) in example noun, yet not indicated"
                        "to be in nominative form: "
                        "{}".format(self.delim_declension, noun))

        marked = "".join(markup)
        return marked

    def mark_sentence(self, sentence, wrap_sentence_in_spans=False,
                      convert_space_to_nbsp=True, add_lang_attr=False,
                      encapsulation_tag=None):
        """
        Returns HTML markup for an example sentence

        Example (assuming default DeclensionMarker delims and css classes):
            mark_sentence("[Иван*а] cын.")

        returns:
            "<span class='base'>Иван</span><span class='end'>а</span> сын."

        :param Str sentence: sentence to makeup
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
        :return Str: String of marked up HTMl for sentence
        """
        marked = ""
        dictionary_form = False

        if convert_space_to_nbsp:
            sentence = sentence.replace(" ", "&nbsp;")

        # determine which delimeters noun is encapsulated in
        open_delim = None
        close_delim = None
        if self.delim_noun_open and self.delim_noun_close in sentence:
            open_delim = self.delim_noun_open
            close_delim = self.delim_noun_close
        if self.delim_nom_noun_open and self.delim_nom_noun_close in sentence:
            open_delim = self.delim_nom_noun_open
            close_delim = self.delim_nom_noun_close
            dictionary_form = True
        if not open_delim or not close_delim:
            raise Exception("not formed correctly")

        # parse the sentence into left, noun section, right
        left, noun, right = None, None, None
        parsed = sentence.split(open_delim)
        if len(parsed) > 1:
            left = parsed[0]
            rest = parsed[1].split(close_delim)
            if len(rest) > 1:
                noun = rest[0]
                right = rest[1]
            else:
                raise Exception("not formed correctly")

        # markup noun
        noun_markup = self.mark_noun(noun, dictionary_form, add_lang_attr)

        # wrap remaining parts of sentence in <span> tags if requested
        if wrap_sentence_in_spans:
            lang_attr = None
            if add_lang_attr:
                lang_attr = "ru"
            left = wrap_in_tag(
                    left, "span", self.example_sentence_classes, lang_attr)
            right = wrap_in_tag(
                    right, "span", self.example_sentence_classes, lang_attr)

        marked = left + noun_markup + right

        # wrap entire marked up sentence in a tag if requrested
        if encapsulation_tag:
            marked = wrap_in_tag(marked, encapsulation_tag)

        return marked

    def mark_string(self, string):
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
        :return String: string with all example sentences replaced with
            their marked up version
        """

        escaped_delim_sentence_open = escape_string(self.delim_sentence_open)
        escaped_delim_sentence_close = escape_string(self.delim_sentence_close)

        res = re.findall(
                r"({}(.*?){})".format(
                    escaped_delim_sentence_open, escaped_delim_sentence_close),
                string)
        for (enclosed_sentence, sentence) in res:
            string = string.replace(
                    enclosed_sentence, self.mark_sentence(sentence))

        return string
