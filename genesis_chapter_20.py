from add_verse import add_verse
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("GENESIS CHAPTER 20 - ABRAHAM AND ABIMELECH - 18 VERSES")
print("="*60)

verses = [
    ("Genesis 20:1", "And Abraham journeyed from thence toward the south country, and dwelled between Kadesh and Shur, and sojourned in Gerar.", "Journey to Gerar"),
    ("Genesis 20:2", "And Abraham said of Sarah his wife, She is my sister: and Abimelech king of Gerar sent, and took Sarah.", "Sister Again"),
    ("Genesis 20:3", "But God came to Abimelech in a dream by night, and said to him, Behold, thou art but a dead man, for the woman which thou hast taken; for she is a man's wife.", "God's Dream"),
    ("Genesis 20:4", "But Abimelech had not come near her: and he said, Lord, wilt thou slay also a righteous nation?", "Righteous Nation"),
    ("Genesis 20:5", "Said he not unto me, She is my sister? and she, even she herself said, He is my brother: in the integrity of my heart and innocency of my hands have I done this.", "Integrity Defense"),
    ("Genesis 20:6", "And God said unto him in a dream, Yea, I know that thou didst this in the integrity of thy heart; for I also withheld thee from sinning against me: therefore suffered I thee not to touch her.", "Withheld from Sin"),
    ("Genesis 20:7", "Now therefore restore the man his wife; for he is a prophet, and he shall pray for thee, and thou shalt live: and if thou restore her not, know thou that thou shalt surely die, thou, and all that are thine.", "Restore Her"),
    ("Genesis 20:8", "Therefore Abimelech rose early in the morning, and called all his servants, and told all these things in their ears: and the men were sore afraid.", "Men Afraid"),
    ("Genesis 20:9", "Then Abimelech called Abraham, and said unto him, What hast thou done unto us? and what have I offended thee, that thou hast brought on me and on my kingdom a great sin? thou hast done deeds unto me that ought not to be done.", "What Have You Done"),
    ("Genesis 20:10", "And Abimelech said unto Abraham, What sawest thou, that thou hast done this thing?", "Why This"),
    ("Genesis 20:11", "And Abraham said, Because I thought, Surely the fear of God is not in this place; and they will slay me for my wife's sake.", "Fear of God"),
    ("Genesis 20:12", "And yet indeed she is my sister; she is the daughter of my father, but not the daughter of my mother; and she became my wife.", "Half Sister"),
    ("Genesis 20:13", "And it came to pass, when God caused me to wander from my father's house, that I said unto her, This is thy kindness which thou shalt shew unto me; at every place whither we shall come, say of me, He is my brother.", "Wandering Agreement"),
    ("Genesis 20:14", "And Abimelech took sheep, and oxen, and menservants, and womenservants, and gave them unto Abraham, and restored him Sarah his wife.", "Gifts Given"),
    ("Genesis 20:15", "And Abimelech said, Behold, my land is before thee: dwell where it pleaseth thee.", "Dwell Here"),
    ("Genesis 20:16", "And unto Sarah he said, Behold, I have given thy brother a thousand pieces of silver: behold, he is to thee a covering of the eyes, unto all that are with thee, and with all other: thus she was reproved.", "Silver Given"),
    ("Genesis 20:17", "So Abraham prayed unto God: and God healed Abimelech, and his wife, and his maidservants; and they bare children.", "Abraham Prayed"),
    ("Genesis 20:18", "For the LORD had fast closed up all the wombs of the house of Abimelech, because of Sarah Abraham's wife.", "Wombs Closed"),
]

for ref, text, title in verses:
    art = f'''
    ╔════════════════════════════════════════╗
    ║   {title.upper().center(42)} ║
    ╠════════════════════════════════════════╣
    ║                                        ║
    ║    Abraham and Abimelech               ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    '''
    add_verse(ref, text, title, art)

print("="*60)
print("GENESIS CHAPTER 20 COMPLETE - ALL 18 VERSES!")
print("="*60)
