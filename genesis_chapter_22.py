from add_verse import add_verse
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("GENESIS CHAPTER 22 - SACRIFICE OF ISAAC - 24 VERSES")
print("="*60)

verses = [
    ("Genesis 22:1", "And it came to pass after these things, that God did tempt Abraham, and said unto him, Abraham: and he said, Behold, here I am.", "God Tests"),
    ("Genesis 22:2", "And he said, Take now thy son, thine only son Isaac, whom thou lovest, and get thee into the land of Moriah; and offer him there for a burnt offering upon one of the mountains which I will tell thee of.", "Offer Isaac"),
    ("Genesis 22:3", "And Abraham rose up early in the morning, and saddled his ass, and took two of his young men with him, and Isaac his son, and clave the wood for the burnt offering, and rose up, and went unto the place of which God had told him.", "Early Morning"),
    ("Genesis 22:4", "Then on the third day Abraham lifted up his eyes, and saw the place afar off.", "Third Day"),
    ("Genesis 22:5", "And Abraham said unto his young men, Abide ye here with the ass; and I and the lad will go yonder and worship, and come again to you.", "We Will Worship"),
    ("Genesis 22:6", "And Abraham took the wood of the burnt offering, and laid it upon Isaac his son; and he took the fire in his hand, and a knife; and they went both of them together.", "Both Together"),
    ("Genesis 22:7", "And Isaac spake unto Abraham his father, and said, My father: and he said, Here am I, my son. And he said, Behold the fire and the wood: but where is the lamb for a burnt offering?", "Where Lamb"),
    ("Genesis 22:8", "And Abraham said, My son, God will provide himself a lamb for a burnt offering: so they went both of them together.", "God Will Provide"),
    ("Genesis 22:9", "And they came to the place which God had told him of; and Abraham built an altar there, and laid the wood in order, and bound Isaac his son, and laid him on the altar upon the wood.", "Bound Isaac"),
    ("Genesis 22:10", "And Abraham stretched forth his hand, and took the knife to slay his son.", "Took Knife"),
    ("Genesis 22:11", "And the angel of the LORD called unto him out of heaven, and said, Abraham, Abraham: and he said, Here am I.", "Angel Calls"),
    ("Genesis 22:12", "And he said, Lay not thine hand upon the lad, neither do thou any thing unto him: for now I know that thou fearest God, seeing thou hast not withheld thy son, thine only son from me.", "Do Not Touch"),
    ("Genesis 22:13", "And Abraham lifted up his eyes, and looked, and behold behind him a ram caught in a thicket by his horns: and Abraham went and took the ram, and offered him up for a burnt offering in the stead of his son.", "Ram Provided"),
    ("Genesis 22:14", "And Abraham called the name of that place Jehovahjireh: as it is said to this day, In the mount of the LORD it shall be seen.", "Jehovah Jireh"),
    ("Genesis 22:15", "And the angel of the LORD called unto Abraham out of heaven the second time,", "Second Call"),
    ("Genesis 22:16", "And said, By myself have I sworn, saith the LORD, for because thou hast done this thing, and hast not withheld thy son, thine only son:", "God's Oath"),
    ("Genesis 22:17", "That in blessing I will bless thee, and in multiplying I will multiply thy seed as the stars of the heaven, and as the sand which is upon the sea shore; and thy seed shall possess the gate of his enemies;", "Stars and Sand"),
    ("Genesis 22:18", "And in thy seed shall all the nations of the earth be blessed; because thou hast obeyed my voice.", "Nations Blessed"),
    ("Genesis 22:19", "So Abraham returned unto his young men, and they rose up and went together to Beersheba; and Abraham dwelt at Beersheba.", "Return Beersheba"),
    ("Genesis 22:20", "And it came to pass after these things, that it was told Abraham, saying, Behold, Milcah, she hath also born children unto thy brother Nahor;", "Milcah's Children"),
    ("Genesis 22:21", "Huz his firstborn, and Buz his brother, and Kemuel the father of Aram,", "Huz Buz Kemuel"),
    ("Genesis 22:22", "And Chesed, and Hazo, and Pildash, and Jidlaph, and Bethuel.", "Five More"),
    ("Genesis 22:23", "And Bethuel begat Rebekah: these eight Milcah did bear to Nahor, Abraham's brother.", "Rebekah"),
    ("Genesis 22:24", "And his concubine, whose name was Reumah, she bare also Tebah, and Gaham, and Thahash, and Maachah.", "Reumah's Sons"),
]

for ref, text, title in verses:
    art = f'''
    ╔════════════════════════════════════════╗
    ║   {title.upper().center(42)} ║
    ╠════════════════════════════════════════╣
    ║                                        ║
    ║    Abraham's Ultimate Test             ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    '''
    add_verse(ref, text, title, art)

print("="*60)
print("GENESIS CHAPTER 22 COMPLETE - ALL 24 VERSES!")
print("="*60)
