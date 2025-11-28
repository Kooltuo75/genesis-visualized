from add_verse import add_verse
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("GENESIS CHAPTER 11 - PART 2 - VERSES 11-32")
print("="*60)

# Continue with remaining genealogy verses
# These follow a similar pattern - showing ages, births, and deaths

verses_data = [
    ("Genesis 11:11", "And Shem lived after he begat Arphaxad five hundred years, and begat sons and daughters."),
    ("Genesis 11:12", "And Arphaxad lived five and thirty years, and begat Salah:"),
    ("Genesis 11:13", "And Arphaxad lived after he begat Salah four hundred and three years, and begat sons and daughters."),
    ("Genesis 11:14", "And Salah lived thirty years, and begat Eber:"),
    ("Genesis 11:15", "And Salah lived after he begat Eber four hundred and three years, and begat sons and daughters."),
    ("Genesis 11:16", "And Eber lived four and thirty years, and begat Peleg:"),
    ("Genesis 11:17", "And Eber lived after he begat Peleg four hundred and thirty years, and begat sons and daughters."),
    ("Genesis 11:18", "And Peleg lived thirty years, and begat Reu:"),
    ("Genesis 11:19", "And Peleg lived after he begat Reu two hundred and nine years, and begat sons and daughters."),
    ("Genesis 11:20", "And Reu lived two and thirty years, and begat Serug:"),
    ("Genesis 11:21", "And Reu lived after he begat Serug two hundred and seven years, and begat sons and daughters."),
    ("Genesis 11:22", "And Serug lived thirty years, and begat Nahor:"),
    ("Genesis 11:23", "And Serug lived after he begat Nahor two hundred years, and begat sons and daughters."),
    ("Genesis 11:24", "And Nahor lived nine and twenty years, and begat Terah:"),
    ("Genesis 11:25", "And Nahor lived after he begat Terah an hundred and nineteen years, and begat sons and daughters."),
    ("Genesis 11:26", "And Terah lived seventy years, and begat Abram, Nahor, and Haran."),
    ("Genesis 11:27", "Now these are the generations of Terah: Terah begat Abram, Nahor, and Haran; and Haran begat Lot."),
    ("Genesis 11:28", "And Haran died before his father Terah in the land of his nativity, in Ur of the Chaldees."),
    ("Genesis 11:29", "And Abram and Nahor took them wives: the name of Abram's wife was Sarai; and the name of Nahor's wife, Milcah, the daughter of Haran, the father of Milcah, and the father of Iscah."),
    ("Genesis 11:30", "But Sarai was barren; she had no child."),
    ("Genesis 11:31", "And Terah took Abram his son, and Lot the son of Haran his son's son, and Sarai his daughter in law, his son Abram's wife; and they went forth with them from Ur of the Chaldees, to go into the land of Canaan; and they came unto Haran, and dwelt there."),
    ("Genesis 11:32", "And the days of Terah were two hundred and five years: and Terah died in Haran.")
]

for i, (ref, text) in enumerate(verses_data, start=11):
    # Extract person's name from verse
    name = ref.split()[-1].replace(":", "")
    if "Shem" in text:
        name = "Shem"
    elif "Arphaxad" in text and "begat" in text and i == 12:
        name = "Arphaxad"
    elif "Salah" in text and "begat" in text and i == 14:
        name = "Salah"
    elif "Eber" in text and "begat" in text and i == 16:
        name = "Eber"
    elif "Peleg" in text and "begat" in text and i == 18:
        name = "Peleg"
    elif "Reu" in text and "begat" in text and i == 20:
        name = "Reu"
    elif "Serug" in text and "begat" in text and i == 22:
        name = "Serug"
    elif "Nahor" in text and "begat" in text and i == 24:
        name = "Nahor"
    elif "Terah" in text and "begat Abram" in text:
        name = "Terah"
    elif "generations of Terah" in text:
        name = "Terah's Line"
    elif "Haran died" in text:
        name = "Haran's Death"
    elif "took them wives" in text:
        name = "Marriages"
    elif "Sarai was barren" in text:
        name = "Sarai Barren"
    elif "went forth" in text:
        name = "Journey Begins"
    elif "Terah died" in text:
        name = "Death of Terah"

    title = f"{name} - Verse {i}"

    ascii_art = f"""
    ╔════════════════════════════════════════╗
    ║      📜 {name.upper()} 📜
    ╠════════════════════════════════════════╣
    ║                                        ║
    ║         👨 {name}
    ║                                        ║
    ║    Genealogy continues...              ║
    ║    Line to Abraham                     ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    """

    add_verse(ref, text, title, ascii_art)

print("="*60)
print("GENESIS CHAPTER 11 PART 2 COMPLETE - VERSES 11-32!")
print("="*60)
