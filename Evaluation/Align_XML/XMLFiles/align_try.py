# <book lang="fr">
#   <article n="0">
#     <div> FR </div>
#     <div> FR </div>
#     <pb>1</pb>
#
#   </article>
#   <article n="1">
#     <div heading="article">FR TITEL 1</div>
#     <div> FR </div>
#     <pb>2</pb>
#     <pb>3</pb>
#
#   </article>
#   <article n="2">
#     <div heading="article"> FR TITEL 2</div>
#     <div> FR </div>
#     <pb>4</pb>
#     <pb>5</pb>
#
#   </article>
#     <article n="3">
#     <div heading="article"> FR TITEL 3</div>
#     <div> FR </div>
#     <pb>6</pb>
#   </article>
#
#   </article>
#     <article n="4">
#     <div heading="article"> FR TITEL 3</div>
#     <div> FR </div>
#     <pb>6</pb>
#   </article>
# </book>

# for each article: save the <pb> child node FR {pb1: a0, pb2:a1, pb3:a1, pb4:a2, pb5:a2, pb6:a3
#import sys
from lxml import etree
from collections import defaultdict
my_dict = defaultdict(list)

frxml = open("/Users/dona/structurexml/Evaluation/Align_XML/XMLFiles/bulletin_1998_5_Kleider_fr.xml", 'r')
tree = etree.parse(frxml)
root = tree.getroot()
for element in root.iter("article", "pb"):
    if element.tag == "article":
        articlenr = element.get("n")
        articlenr =  "a"+articlenr
    if element.tag == "pb":
        pbnumber = "pb"+element.text
        my_dict[pbnumber] +=[articlenr]
        #print "%s - %s" % (element.tag, element.text)
#print my_dict

for key in sorted(my_dict, reverse=False):
    print key, my_dict[key]