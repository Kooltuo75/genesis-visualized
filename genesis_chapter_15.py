from add_verse import add_verse
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("GENESIS CHAPTER 15 - GOD'S COVENANT - 21 VERSES")
print("="*60)

verses = [
    ("Genesis 15:1", "After these things the word of the LORD came unto Abram in a vision, saying, Fear not, Abram: I am thy shield, and thy exceeding great reward.", "Fear Not"),
    ("Genesis 15:2", "And Abram said, Lord GOD, what wilt thou give me, seeing I go childless, and the steward of my house is this Eliezer of Damascus?", "Abram's Question"),
    ("Genesis 15:3", "And Abram said, Behold, to me thou hast given no seed: and, lo, one born in my house is mine heir.", "No Heir"),
    ("Genesis 15:4", "And, behold, the word of the LORD came unto him, saying, This shall not be thine heir; but he that shall come forth out of thine own bowels shall be thine heir.", "Your Own Son"),
    ("Genesis 15:5", "And he brought him forth abroad, and said, Look now toward heaven, and tell the stars, if thou be able to number them: and he said unto him, So shall thy seed be.", "Stars Promise"),
    ("Genesis 15:6", "And he believed in the LORD; and he counted it to him for righteousness.", "Faith Counted"),
    ("Genesis 15:7", "And he said unto him, I am the LORD that brought thee out of Ur of the Chaldees, to give thee this land to inherit it.", "Land Promise"),
    ("Genesis 15:8", "And he said, Lord GOD, whereby shall I know that I shall inherit it?", "How Know?"),
    ("Genesis 15:9", "And he said unto him, Take me an heifer of three years old, and a she goat of three years old, and a ram of three years old, and a turtledove, and a young pigeon.", "Covenant Animals"),
    ("Genesis 15:10", "And he took unto him all these, and divided them in the midst, and laid each piece one against another: but the birds divided he not.", "Animals Divided"),
    ("Genesis 15:11", "And when the fowls came down upon the carcases, Abram drove them away.", "Birds Driven Away"),
    ("Genesis 15:12", "And when the sun was going down, a deep sleep fell upon Abram; and, lo, an horror of great darkness fell upon him.", "Deep Sleep"),
    ("Genesis 15:13", "And he said unto Abram, Know of a surety that thy seed shall be a stranger in a land that is not theirs, and shall serve them; and they shall afflict them four hundred years;", "400 Years"),
    ("Genesis 15:14", "And also that nation, whom they shall serve, will I judge: and afterward shall they come out with great substance.", "God Will Judge"),
    ("Genesis 15:15", "And thou shalt go to thy fathers in peace; thou shalt be buried in a good old age.", "Die in Peace"),
    ("Genesis 15:16", "But in the fourth generation they shall come hither again: for the iniquity of the Amorites is not yet full.", "Fourth Generation"),
    ("Genesis 15:17", "And it came to pass, that, when the sun went down, and it was dark, behold a smoking furnace, and a burning lamp that passed between those pieces.", "Smoking Furnace"),
    ("Genesis 15:18", "In the same day the LORD made a covenant with Abram, saying, Unto thy seed have I given this land, from the river of Egypt unto the great river, the river Euphrates:", "Covenant Made"),
    ("Genesis 15:19", "The Kenites, and the Kenizzites, and the Kadmonites,", "Kenites Listed"),
    ("Genesis 15:20", "And the Hittites, and the Perizzites, and the Rephaims,", "Hittites Listed"),
    ("Genesis 15:21", "And the Amorites, and the Canaanites, and the Girgashites, and the Jebusites.", "All Peoples"),
]

for ref, text, title in verses:
    art = f'''
    ╔════════════════════════════════════════╗
    ║   {title.upper().center(42)} ║
    ╠════════════════════════════════════════╣
    ║                                        ║
    ║    God's Covenant with Abram           ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    '''
    add_verse(ref, text, title, art)

print("="*60)
print("GENESIS CHAPTER 15 COMPLETE - ALL 21 VERSES!")
print("="*60)
