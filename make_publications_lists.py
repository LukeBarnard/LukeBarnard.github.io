from pybtex.database import parse_file
from pybtex.richtext import Text, Tag, HRef
import numpy as np


def make_website_publications_list():
    """
    Make a HTML publications list from a bib file of my references. 
    """
    
    
    bib_data = parse_file('my_references.bib')

    # Sort the list by years
    years = []
    keys = []
    for i, e in enumerate(bib_data.entries):
        years.append(bib_data.entries[e].fields['year'])
        keys.append(e)

    years = np.array(years).astype('int32')
    sorted_id = np.argsort(years)[::-1]
    keys = np.array(keys)
    sorted_keys = keys[sorted_id]

    tab = "    "
    with open("publications.html", "w", encoding="utf-8") as f:
        f.write("<ol reversed>\n")

        for i, e in enumerate(sorted_keys):

            # Only print out articles, no thesis or unpublished work.
            if bib_data.entries[e].type != "article":
                continue

            authors = bib_data.entries[e].persons["author"]
            # Get rid of initials.
            names = [a.last_names[0] for a in authors]

            # Make my name bold, because, ego.
            names = [Tag("b", n) if n=="Barnard" else Text(n) for n in names]

            # Form author list dependent on number of authors.
            if len(names)==1:
                name_str =  Text(names[0], ", ")
            elif len(names) == 2:
                name_str =  Text(names[0], " and ", names[1], ", ")
            else:
                name_str = Text(names[0] + " et al., ")

            yr_str = Text(" (" + bib_data.entries[e].fields["year"], "), ")
            ttl = bib_data.entries[e].fields["title"]
            ttl = ttl.replace('{', '')
            ttl = ttl.replace('}', '')
            title_str = Text(ttl, ", ")

            jrnl = bib_data.entries[e].fields["journal"]
            jrnl = jrnl.replace("\&", '&')
            jrnl_str = Text(" ", jrnl, ", ")

            doi_url = "https://doi.org/" + bib_data.entries[e].fields["doi"]
            doi_str = Text(" DOI:", HRef(doi_url, bib_data.entries[e].fields["doi"]))


            f.write(tab+"<li>\n")
            f.write(tab+tab+ Tag('b', title_str).render_as("html")+ "<br>\n")
            f.write(tab+tab+Text(name_str, yr_str, jrnl_str, doi_str).render_as("html"))            
            f.write(tab+ "</li><br>\n")
        f.write("</ol>")
    return


def make_cv_publications_list():
    """
    Make a HTML publications list from a bib file of my references, but formatted so it copies nicely to my CV. 
    """
    
    bib_data = parse_file('my_references.bib')

    # Sort the list by years
    years = []
    keys = []
    for i, e in enumerate(bib_data.entries):
        years.append(bib_data.entries[e].fields['year'])
        keys.append(e)

    years = np.array(years).astype('int32')
    sorted_id = np.argsort(years)[::-1]
    keys = np.array(keys)
    sorted_keys = keys[sorted_id]

    total_count = 1
    for e in sorted_keys:
        if bib_data.entries[e].type == "article":
            total_count += 1

    article_count = 0

    with open("cv_publications.html", "w", encoding="utf-8") as f:

        for i, e in enumerate(sorted_keys):

            # Only print out articles, no thesis or unpublished work.
            if bib_data.entries[e].type != "article":
                continue

            article_count = article_count + 1

            authors = bib_data.entries[e].persons["author"]
            # Get rid of initials.
            names = [a.last_names[0] for a in authors]

            # Make my name bold, because, ego.
            names = [Tag("b", n) if n=="Barnard" else Text(n) for n in names]

            # Form author list dependent on number of authors.
            name_str = Text('')
            for j, n in enumerate(names):

                if j == 0:
                    name_str = name_str + n
                elif (j > 0) & (j < len(names)-1):
                    name_str = name_str + ", " + n
                elif j == len(names)-1:
                    name_str = name_str + " and " + n

            name_str = Text(name_str)
            yr_str = Text(" (" + bib_data.entries[e].fields["year"], "), ")
            ttl = bib_data.entries[e].fields["title"]
            ttl = ttl.replace('{', '')
            ttl = ttl.replace('}', '')
            title_str = Text(ttl, ", ")

            jrnl = bib_data.entries[e].fields["journal"]
            jrnl = jrnl.replace("\&", '&')
            jrnl_str = Text(" ", jrnl, ", ")

            doi_url = "https://doi.org/" + bib_data.entries[e].fields["doi"]
            doi_str = Text(" DOI:", HRef(doi_url, bib_data.entries[e].fields["doi"]))
            count_str = Text("{:02d}. ".format(total_count - article_count))

            f.write(Tag('b', count_str, title_str).render_as("html")+ "<br>\n")
            f.write(Text(name_str, yr_str, jrnl_str, doi_str).render_as("html"))
            f.write('<br><br>')
        return

if __name__ == "__main__":
    make_website_publications_list()
    make_cv_publications_list()
    
