from add_verse import add_verse
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("GENESIS CHAPTER 23 - SARAH'S DEATH - 20 VERSES")
print("="*60)

verses = [
    ("Genesis 23:1", "And Sarah was an hundred and seven and twenty years old: these were the years of the life of Sarah.", "Sarah's Age"),
    ("Genesis 23:2", "And Sarah died in Kirjatharba; the same is Hebron in the land of Canaan: and Abraham came to mourn for Sarah, and to weep for her.", "Sarah Died"),
    ("Genesis 23:3", "And Abraham stood up from before his dead, and spake unto the sons of Heth, saying,", "Spoke to Heth"),
    ("Genesis 23:4", "I am a stranger and a sojourner with you: give me a possession of a buryingplace with you, that I may bury my dead out of my sight.", "Need Burial Place"),
    ("Genesis 23:5", "And the children of Heth answered Abraham, saying unto him,", "Heth Answered"),
    ("Genesis 23:6", "Hear us, my lord: thou art a mighty prince among us: in the choice of our sepulchres bury thy dead; none of us shall withhold from thee his sepulchre, but that thou mayest bury thy dead.", "Mighty Prince"),
    ("Genesis 23:7", "And Abraham stood up, and bowed himself to the people of the land, even to the children of Heth.", "Abraham Bowed"),
    ("Genesis 23:8", "And he communed with them, saying, If it be your mind that I should bury my dead out of my sight; hear me, and intreat for me to Ephron the son of Zohar,", "Ask Ephron"),
    ("Genesis 23:9", "That he may give me the cave of Machpelah, which he hath, which is in the end of his field; for as much money as it is worth he shall give it me for a possession of a buryingplace amongst you.", "Cave Machpelah"),
    ("Genesis 23:10", "And Ephron dwelt among the children of Heth: and Ephron the Hittite answered Abraham in the audience of the children of Heth, even of all that went in at the gate of his city, saying,", "Ephron Answered"),
    ("Genesis 23:11", "Nay, my lord, hear me: the field give I thee, and the cave that is therein, I give it thee; in the presence of the sons of my people give I it thee: bury thy dead.", "I Give It"),
    ("Genesis 23:12", "And Abraham bowed down himself before the people of the land.", "Bowed Again"),
    ("Genesis 23:13", "And he spake unto Ephron in the audience of the people of the land, saying, But if thou wilt give it, I pray thee, hear me: I will give thee money for the field; take it of me, and I will bury my dead there.", "Will Pay"),
    ("Genesis 23:14", "And Ephron answered Abraham, saying unto him,", "Ephron's Answer"),
    ("Genesis 23:15", "My lord, hearken unto me: the land is worth four hundred shekels of silver; what is that betwixt me and thee? bury therefore thy dead.", "400 Shekels"),
    ("Genesis 23:16", "And Abraham hearkened unto Ephron; and Abraham weighed to Ephron the silver, which he had named in the audience of the sons of Heth, four hundred shekels of silver, current money with the merchant.", "Paid Silver"),
    ("Genesis 23:17", "And the field of Ephron, which was in Machpelah, which was before Mamre, the field, and the cave which was therein, and all the trees that were in the field, that were in all the borders round about, were made sure", "Field Made Sure"),
    ("Genesis 23:18", "Unto Abraham for a possession in the presence of the children of Heth, before all that went in at the gate of his city.", "Abraham's Possession"),
    ("Genesis 23:19", "And after this, Abraham buried Sarah his wife in the cave of the field of Machpelah before Mamre: the same is Hebron in the land of Canaan.", "Buried Sarah"),
    ("Genesis 23:20", "And the field, and the cave that is therein, were made sure unto Abraham for a possession of a buryingplace by the sons of Heth.", "Made Sure"),
]

for ref, text, title in verses:
    art = f'''
    ╔════════════════════════════════════════╗
    ║   {title.upper().center(42)} ║
    ╠════════════════════════════════════════╣
    ║                                        ║
    ║    Sarah's Death and Burial            ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    '''
    add_verse(ref, text, title, art)

print("="*60)
print("GENESIS CHAPTER 23 COMPLETE - ALL 20 VERSES!")
print("="*60)
