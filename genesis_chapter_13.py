from add_verse import add_verse
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("GENESIS CHAPTER 13 - ABRAM AND LOT SEPARATE - 18 VERSES")
print("="*60)

verses = [
    ("Genesis 13:1", "And Abram went up out of Egypt, he, and his wife, and all that he had, and Lot with him, into the south.", "Return from Egypt"),
    ("Genesis 13:2", "And Abram was very rich in cattle, in silver, and in gold.", "Abram's Wealth"),
    ("Genesis 13:3", "And he went on his journeys from the south even to Bethel, unto the place where his tent had been at the beginning, between Bethel and Hai;", "Journey to Bethel"),
    ("Genesis 13:4", "Unto the place of the altar, which he had made there at the first: and there Abram called on the name of the LORD.", "Return to Altar"),
    ("Genesis 13:5", "And Lot also, which went with Abram, had flocks, and herds, and tents.", "Lot's Possessions"),
    ("Genesis 13:6", "And the land was not able to bear them, that they might dwell together: for their substance was great, so that they could not dwell together.", "Land Too Small"),
    ("Genesis 13:7", "And there was a strife between the herdmen of Abram's cattle and the herdmen of Lot's cattle: and the Canaanite and the Perizzite dwelled then in the land.", "Strife Between Herdmen"),
    ("Genesis 13:8", "And Abram said unto Lot, Let there be no strife, I pray thee, between me and thee, and between my herdmen and thy herdmen; for we be brethren.", "No Strife"),
    ("Genesis 13:9", "Is not the whole land before thee? separate thyself, I pray thee, from me: if thou wilt take the left hand, then I will go to the right; or if thou depart to the right hand, then I will go to the left.", "Choose Your Land"),
    ("Genesis 13:10", "And Lot lifted up his eyes, and beheld all the plain of Jordan, that it was well watered every where, before the LORD destroyed Sodom and Gomorrah, even as the garden of the LORD, like the land of Egypt, as thou comest unto Zoar.", "Lot Sees Jordan"),
    ("Genesis 13:11", "Then Lot chose him all the plain of Jordan; and Lot journeyed east: and they separated themselves the one from the other.", "Lot Chooses Jordan"),
    ("Genesis 13:12", "Abram dwelled in the land of Canaan, and Lot dwelled in the cities of the plain, and pitched his tent toward Sodom.", "Separation Complete"),
    ("Genesis 13:13", "But the men of Sodom were wicked and sinners before the LORD exceedingly.", "Wicked Sodom"),
    ("Genesis 13:14", "And the LORD said unto Abram, after that Lot was separated from him, Lift up now thine eyes, and look from the place where thou art northward, and southward, and eastward, and westward:", "God Speaks to Abram"),
    ("Genesis 13:15", "For all the land which thou seest, to thee will I give it, and to thy seed for ever.", "Land Promise Forever"),
    ("Genesis 13:16", "And I will make thy seed as the dust of the earth: so that if a man can number the dust of the earth, then shall thy seed also be numbered.", "Seed as Dust"),
    ("Genesis 13:17", "Arise, walk through the land in the length of it and in the breadth of it; for I will give it unto thee.", "Walk the Land"),
    ("Genesis 13:18", "Then Abram removed his tent, and came and dwelt in the plain of Mamre, which is in Hebron, and built there an altar unto the LORD.", "Altar at Mamre"),
]

for ref, text, title in verses:
    art = f'''
    ╔════════════════════════════════════════╗
    ║   {title.upper().center(42)} ║
    ╠════════════════════════════════════════╣
    ║                                        ║
    ║    Abram and Lot's Journey             ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    '''
    add_verse(ref, text, title, art)

print("="*60)
print("GENESIS CHAPTER 13 COMPLETE - ALL 18 VERSES!")
print("="*60)
