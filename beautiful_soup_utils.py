import os
import copy
import re
import io_utils
import bs4  # needed to typecheck objects i.e. bs4.element.Tag
from bs4.dammit import EntitySubstitution  # for custom formatter for prettify
from bs4 import BeautifulSoup, Comment

ENC = 'utf-8-sig'


def has_text_content(tag):
    """
    check if a BeautifulSoup tag has text.

    :return: True if tag has text, False otherwise

    (@TODO: Ensure this is a Tag object?)
    see: https://stackoverflow.com/questions/61794102/how-to-remove-empty-p-tags-with-beautiful-soup-4
    """
    if len(tag.get_text(strip=True)) == 0:
        return False
    return True


def get_next_tag_sibling(soup_tag):
    """
    Returns nearset right sibling that is a Tag object
    (NOT a NavigableString object)
    If right siblings exhausted before it reaches
    a Tag, returns None

    Needed because for things like:

    <p>
      <br/>
      <hr class="inner anchor" id="inner-hr-1"/>
      <br/>
    </p>

    The left and right siblings of the <hr> Tag are
    actually \n chars that are NavigableStrings, not
    the <br> tags, as one might expect...
    """

    curr_tag = soup_tag
    next_sib = None
    while True:
        next_sib = curr_tag.next_sibling
        if isinstance(next_sib, bs4.element.Tag) or not next_sib:
            break
        curr_tag = next_sib
    return next_sib


def get_prev_tag_sibling(soup_tag):
    """
    see func doc for get_next_tag_sibling;
    this is reverse
    """
    curr_tag = soup_tag
    prev_sib = None
    while True:
        prev_sib = curr_tag.previous_sibling
        if isinstance(prev_sib, bs4.element.Tag) or not prev_sib:
            break
        curr_tag = prev_sib
    return prev_sib


def add_classes(tag, class_list):
    """
    add css classes to a BeautifulSoup tag.
    (if a class is already present, won't add it)
    This helper method is useful because a tag's 'class'
    attr can be either a String or a list; handles
    adding in either scenario.

    :param BeautifulSoup4 tag: tag to add classes to
    :param list class_list: css classes to add (as strings)
    :returns: None (Permenantly modifies tag)
    """

    if 'class' in tag.attrs:
        '''
        BeautifulSoup tag's 'class' attr
        can be str or list
        '''
        curr_classes = tag['class']
        if isinstance(curr_classes, str):
            # dont add dupes
            for new_class in class_list:
                if new_class not in curr_classes:
                    tag['class'] += " " + new_class
        elif isinstance(curr_classes, list):
            # don't add dupes
            final_list = curr_classes
            final_list.extend(x for x in class_list if x not in final_list)
            tag['class'] = final_list
        else:
            # use beautifulsoup4==4.11.1 if you use v 4.13.3 will hit this
            # because the types are different
            raise Exception("Can't identify type of tag's 'class' attr")
    else:
        tag['class'] = class_list


def get_classes(tag):
    """
    Return list of css classes in a BeautifulSoup tag

    :param BeautifulSoup4 tag: soup to get classes from
    :return: the list of css classes in tag (strings)
    """
    classes = []
    if 'class' in tag.attrs:
        '''
        BeautifulSoup tag's 'class' attr
        could be either String or list
        '''
        curr_classes = tag['class']
        if isinstance(curr_classes, str):
            # split existing class string to get a list
            classes = curr_classes.split(" ")
        elif isinstance(curr_classes, list):
            classes = curr_classes
        else:
            raise Exception("BeautifulSoupUtils: get_classes - class atr"
                            " is neither String nor list; can't parse it!")
    return classes


def remove_classes(tag, class_list):
    """
    Remove css classes from a BeautifulSoup tag

    :param BeautifulSoup. element to remove classes from
    :param list class_list: list of strings - the css
        classes to remove. (note: if a class isn't
        found in tag, it's ok)
    :returns: None. modifications to tag are permenant.
    """

    new_class_list = []
    if 'class' in tag.attrs:
        '''
        BeautifulSoup tag's 'class' attr
        could be either String or list
        '''
        curr_classes = tag['class']
        if isinstance(curr_classes, str):
            # split existing class string to get a list
            curr_classes_list = curr_classes.split(" ")
        elif isinstance(curr_classes, list):
            curr_classes_list = curr_classes
        else:
            raise Exception("BeautifulSoupUtils: remove_classes - class attr "
                            "is neither String nor list; can't parse it!")

        for myclass in curr_classes_list:
            if myclass not in class_list:
                new_class_list.append(myclass)
            tag['class'] = new_class_list


def find_replace_str(soup, string, content, allow_empty=False):
    """
    replaces first occurance of a string in a BeautifulSoup object
    with other content (either another string, or another beautifulsoup)

    use case:
    html doc with template vars %TITLE% or %MAIN-CONTENT%
    Generate that info elsewhere, then call this to swap it in
      beautiful_soup_utils.find_replace_str(my_soup, "%TITLE%, "my great title")
      beautiful_soup_utils.find_replace_str(my_soup, "%MAIN-CONTENT%", my_soup_div)

    :param BeautifulSoup4 soup: object to replace string in
    :param str string: string to replace
    :param content: what to replace with
    :type content: str or BeautifulSoup4
        (can be <class 'bs4.BeautifulSoup.tag'> or even
        <class 'bs4.BeautifulSoup'>)
    :param bolean allow_empty: optional. if True, don't
        raise Exception if string not found in soup
    :return: None (modified soup permenantly)

    WARNING! ::
    If content is BeauitulfSoup object,
    will convert it to str then back to BeautifulSoup object
    before adding to soup. This could permenantly modify the
    type of attributes in content: example, if you set a boolean
    attribute in content, it will be type String when it's done.
    """

    found = soup.find(string=re.compile(string))
    '''
    soup.find with string arg will return a NavigableString
    for the ENTIRE string of the tag that contains the string
    (i.e. suppose you have <h1>%TITLE% %NUMBER%</h1>
    soup.find(string=re.compile("%TITLE%"))
       --> returns "%TITLE% %NUMBER%")
    - if you were to directly replace_with on the find result,
    you'll be replacing the entire text of the tag, not just
    the part of the string that matches. Hence the loginc below:

    1. cast returned NavigableString to string
    2. cast content to replace with to string
    3. use standard string replace on 1.,
       to replace ONLY desired match text
       with 2.
    4. convert result of 3. to BeautifulSoup
    5. Finally, do the replace_with with 4.
    '''
    if found:
        found_string = str(copy.copy(found))
        found_replaced = found_string.replace(string, str(content))
        found_replaced = BeautifulSoup(found_replaced, 'html.parser')
        found.replace_with(found_replaced)
    elif not allow_empty:
        raise Exception("Can't find string {} in soup!".format(string))


'''
doesn't work yet
'''
def replace_all_occurances_in_doc(soup, find, replace_with):
    matches = soup.find_all(text=re.compile(find))
    for mmatch in matches:
        mmatch.replace_with(replace_with)


def js_tag(path):
    """
    returns a <script> tag (as BeautifulSoup object)
    for a path

    :param str path: path to put in the <script> tag
    :return: BeautifulSoup4 object of <script> tag
    """
    return BeautifulSoup('<script type="text/javascript" src="'
                         + path + '"></script>', "html.parser")


def css_tag(path):
    """
    returns a <link> tag (as BeautifulSoup object)
    for a path

    :param str path: path to put in the <link> tag
    :return: BeautifulSoup4 object of <link> tag
    """
    return BeautifulSoup('<link rel="stylesheet" href="' + path
                         + '" type="text/css">', "html.parser")

def add_js_tags(soup, paths, add_to_head=True):
    """
    add js script tags to soup

    :param BeautifulSoup4 soup: soup to add tags to
    :param list paths: strings of urls to the scripts
        (note: if rel paths, make sure rel the HTML
        doc you're adding to, for where its final
        location will be.
    :param boolean add_to_head: if true, append to <head>,
        else append to <body>

    ** Note - be mindful of js dependencies; if adding
    a scrip that uses jquery, you'd need jquery <script>
    to come before script which relies on it.
    """

    for path in paths:
        script_tag = js_tag(path)
        comment = Comment(' #script tag added via beautiful_soup_utils.py ')
        script_tag.script.insert_before(comment)
        if add_to_head:
            soup.head.append(script_tag)
        else:
            soup.body.append(script_tag)


def add_css_head_tags(soup, paths, startAt=None):
    """
    add css tags to <head> of a BeautifulSoup object

    :param BeautifulSoup4 soup: soup to add tags to
    :param list paths: list of Strings, of paths to
        the css files (if giving rel paths, ensure
        they're rel the HTML doc you'd be adding this
        to (where its final location will be)
    :param int startAt: optional. where to start
        inserting the new tags, among existing <link>
        tags in <head>. examples:
            0: adds paths at position 0 (i.e.,
                IN FRONT of all existing tags)
            5: inserts BEFORE the 5th existing tag
        (default behavior is to add after last existing
        <link> tag in <head>)
    :returns: None
    """

    soup_head = soup.find("head")
    if not soup_head:
        raise Exception("no 'head' tag in soup sent to add_css_head_tag")

    # make list of tags from list of paths
    new_paths = BeautifulSoup("", 'html.parser')
    for path in paths:
        link_tag = css_tag(path)
        comment = Comment(" #link tag added via beautiful_soup_utils.py ")
        link_tag.link.insert_before(comment)
        new_paths.append(link_tag)

    # find last <link> tag in <head> and insert the new
    # paths after that; if there aren't any <link> tags
    # in <head>, append the new paths to end of <head>

    link_tags = soup_head.find_all("link")
    if not link_tags:
        soup_head.append(new_paths)
    else:
        # default is insert after last <link> tag;
        # but if startAt arg given, insert after that point
        if startAt is not None:  # 0 is valid so don't do if startAt or it won't catch if it's 0
            if not 0 <= startAt <= len(link_tags):
                raise Exception("\nadd_css_head_tags: specified to start "
                                "adding your new tags at pos {} of existing "
                                "<link> tags, but there are only {} <link> "
                                "tags in this soup's <head>. You must specify "
                                "a number between 0 and {} (inclusive). (p.s. "
                                "if you give {}, that would insert them at the"
                                " end of the list of existing <link> tags, but"
                                " this is the default behavior without the "
                                "startAt args)"
                                .format(str(startAt), str(len(link_tags)),
                                        str(len(link_tags)),
                                        str(len(link_tags))))
            if startAt == len(link_tags):  # if they specified end of list, add at end of list
                link_tags[-1].insert_after(new_paths)
            else:  # anything else, start at that position.
                link_tags[startAt].insert_before(new_paths)
        else:
            link_tags[-1].insert_after(new_paths)


def make_soup(html_str):
    """
    convert a string to a BeautifulSoup4 object

    :param str html_str: string of (hopefully) valid HTML
    :return: BeautifulSoup4 object for the string
    """
    soup = BeautifulSoup(html_str.encode(ENC), 'html.parser')
    return soup


def make_soup_from_file(filepath):
    """
    convert a file to a beautifulSoup4 object

    :param str filepath: absolute path to file to read
    :return: BeautifulSoup4 object for data in the file
    """
    print(("\t\tbeautiful_soup_utils: Generate soup from file "
           "\n\t\t\t{}").format(filepath))
    if not os.path.abspath(filepath):
        raise Exception(
            ("ERROR (beautiful_soup_utils) filepath to get soup from is not "
             "absolute {}").format(filepath))
    if not os.path.exists(filepath):
        raise Exception(
            ("ERROR (beautiful_soup_utils) filepath to get soup from does "
             "not exist {}").format(filepath))
    file_str = io_utils.get_file_as_str(filepath)
    soup = make_soup(file_str)
    return soup


def preserve_nbsp_and_ru(string):
    """
    custom formatter for BeautifulSoup prettify.
    preserves both &nbsp and Cyrillic chars.
    When this function is passed as value to formatter
    arg (i.e. prettify(formatter=preserve_nbsp_and_ru))
    then every String and attribute value encountered
    will be passed to it; prettify will output
    whatever value it returns.

    necessary, because:
        - if you don't supply a formatter arg, &nbsp are removed
        - if you supply formatter='html', &nbsp are preserved, but
            Cyrillic gets mangled.
        - Note: prettify 'formatter' arg takes only 5 values:
            (1) "minimal" (removes &nbsp; preserves Cyrillic),
            (2) "html" (preserves &nbsp; mangles Cyrillic),
            (3) "html5" (not sure behavior)
            (4) None (removes &nbsp; preseves Cyrillic)
                [but docs warn it can generate bad HTML]
            (5) custom function.

    SO I posted about this:
    https://stackoverflow.com/questions/69790205/prettify-with-beautifulsoup-using-a-formatter-that-will-preserve-nbsp-and-cyril/69790637#69790637
    """

    newstr = ""
    # split on nbsp
    # (&nbsp are parsed in BS as \xa0)
    # (https://stackoverflow.com/questions/66895175/beautifulsoup-find-tag-with-text-containing-nbsp)
    split_str = string.split('\xa0')
    # (this will split a&nbsp;b&nsbp;&c --> [a,b,c])
    for i, space_between in enumerate(split_str):
        # space_between will be regular text
        newstr += space_between
        # add an &nbsp after it, unless you're on the last
        # item in the list, after which there would not be an &nbsp
        if i < len(split_str) - 1:
            # put the nbsp through the EntitySubstitution function
            # which will preserve it
            newstr += EntitySubstitution.substitute_html('\xa0')
    return newstr


def prettify_soup(soup, preserve_ru=True, preserve_nbsp=True):
    """
    prettify a BeautifulSoup4 object

    :param BeautifulSoup4 soup: BeautifulSoup object to prettify
    :param boolean preserve_ru: preserve Cyrillic when prettifying
    :param boolean preserve_bnsp: preserve &nbsp; chars
    :return: prettified STRING for soup
    """
    formatter = 'minimal'  # default formatter for prettify: preserves cyrillic but removes &nbsp;
    if preserve_ru and preserve_nbsp:
        formatter = preserve_nbsp_and_ru  # cust func that preserves both
    elif preserve_nbsp:
        formatter = 'html'  # preserves &nbsp; but mangles Cyrillic

    soup_str = soup.prettify(formatter=formatter)
    return soup_str


def write_soup_to_file(soup, output_filename, force, preserve_ru=False,
                       preserve_nbsp=True):
    """
    write a BeautifulSoup object to a file (prettified)

    :param BeautifulSoup4 soup: soup to write to file
    :param str output_filename: absolute path to file
        to write to.
    :param boolean force: Overwrite if files exists
    :param boolean preserve_ru: preserve Cyrillic while
        prettifying
    :param boolean preserve_nbsp: preserve &nbsp; chars
        while prettifying
    :return: None
    """
    print(("\t\tbeautiful_soup_utils: Prettify soup and write to\n\t\t\t{}")
          .format(output_filename))
    pretty_soup = prettify_soup(soup, preserve_ru, preserve_nbsp)
    io_utils.write_str_to_file(pretty_soup, output_filename, force)
