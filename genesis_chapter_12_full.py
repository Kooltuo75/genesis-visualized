from add_verse import add_verse
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("GENESIS CHAPTER 12 - REMAINING VERSES 4-20")
print("="*60)

# Genesis 12:4-20 (verses 1-3 already done)
verses = [
    ("Genesis 12:4", "So Abram departed, as the LORD had spoken unto him; and Lot went with him: and Abram was seventy and five years old when he departed out of Haran.", "Abram Departs"),
    ("Genesis 12:5", "And Abram took Sarai his wife, and Lot his brother's son, and all their substance that they had gathered, and the souls that they had gotten in Haran; and they went forth to go into the land of Canaan; and into the land of Canaan they came.", "Journey to Canaan"),
    ("Genesis 12:6", "And Abram passed through the land unto the place of Sichem, unto the plain of Moreh. And the Canaanite was then in the land.", "At Sichem"),
    ("Genesis 12:7", "And the LORD appeared unto Abram, and said, Unto thy seed will I give this land: and there builded he an altar unto the LORD, who appeared unto him.", "Land Promise"),
    ("Genesis 12:8", "And he removed from thence unto a mountain on the east of Bethel, and pitched his tent, having Bethel on the west, and Hai on the east: and there he builded an altar unto the LORD, and called upon the name of the LORD.", "Altar at Bethel"),
    ("Genesis 12:9", "And Abram journeyed, going on still toward the south.", "Journey South"),
    ("Genesis 12:10", "And there was a famine in the land: and Abram went down into Egypt to sojourn there; for the famine was grievous in the land.", "Famine - To Egypt"),
    ("Genesis 12:11", "And it came to pass, when he was come near to enter into Egypt, that he said unto Sarai his wife, Behold now, I know that thou art a fair woman to look upon:", "Sarai's Beauty"),
    ("Genesis 12:12", "Therefore it shall come to pass, when the Egyptians shall see thee, that they shall say, This is his wife: and they will kill me, but they will save thee alive.", "Abram's Fear"),
    ("Genesis 12:13", "Say, I pray thee, thou art my sister: that it may be well with me for thy sake; and my soul shall live because of thee.", "Say You're My Sister"),
    ("Genesis 12:14", "And it came to pass, that, when Abram was come into Egypt, the Egyptians beheld the woman that she was very fair.", "Egyptians See"),
    ("Genesis 12:15", "The princes also of Pharaoh saw her, and commended her before Pharaoh: and the woman was taken into Pharaoh's house.", "Taken to Pharaoh"),
    ("Genesis 12:16", "And he entreated Abram well for her sake: and he had sheep, and oxen, and he asses, and menservants, and maidservants, and she asses, and camels.", "Abram Prospers"),
    ("Genesis 12:17", "And the LORD plagued Pharaoh and his house with great plagues because of Sarai Abram's wife.", "God Plagues Pharaoh"),
    ("Genesis 12:18", "And Pharaoh called Abram, and said, What is this that thou hast done unto me? why didst thou not tell me that she was thy wife?", "Pharaoh Questions"),
    ("Genesis 12:19", "Why saidst thou, She is my sister? so I might have taken her to me to wife: now therefore behold thy wife, take her, and go thy way.", "Return Sarai"),
    ("Genesis 12:20", "And Pharaoh commanded his men concerning him: and they sent him away, and his wife, and all that he had.", "Sent Away"),
]

for ref, text, title in verses:
    art = f'''
    ╔════════════════════════════════════════╗
    ║   {title.upper().center(42)} ║
    ╠════════════════════════════════════════╣
    ║                                        ║
    ║    Abraham's Story Continues...        ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    '''
    add_verse(ref, text, title, art)

print("="*60)
print("GENESIS CHAPTER 12 COMPLETE - ALL 20 VERSES!")
print("="*60)
