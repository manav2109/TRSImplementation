import itertools
import re
from autocorrect import Speller

def flatten_array(arr):
    return list(itertools.chain.from_iterable(arr))


def has_spaces_or_special_characters(s):
    # Regular expression to match any whitespace or special character
    pattern = re.compile(r'[\s\W]')
    # Search for the pattern in the string
    if pattern.search(s):
        return True
    else:
        return False

def remove_special_characters(s):
    # Regular expression to match any special character
    pattern = re.compile(r'[^A-Za-z0-9\s\-]')
    # Replace special characters with an empty string
    clean_string = pattern.sub('', s)
    return clean_string

def perform_spell_correction(sample):
    # sample = ['Fret-MOD sketch:', 'Description', 'Post-MOD sketch:', 'E_a.E. — Cable Loom', 'inst. drawings — Modify', 'harnesses insta‘llatiun', 'tor DHSC in Dimr', 'Zone D3 LH FWD', '(eel. G}', 'Legend', 'Extremity Delta:', 'Pawn“: Extremity Status', 'I Existing', 'MOR - (9291mm not involved}', 'Addedtmoclmed', 'I', 'FzF (929mm involved}', 'Removed', 'Floor', "' —' (gzgtnltlllllwolvea)", '- CILATiWoIMed', 'A330 — Harness PreeLtetlnltlon', 'TOOTVCBAD—B _ _', 'on 88—00 plate _ ‘—', 'Flight Direction', 'mowcaameA', 'on BBAOD plate', "2563VB-1MDJ'1 MDE", '_"—b', '1?13VB -', '1MDF1MDEF1MTI1MTE', '700 Né640~C', 'Y0 19V0660 —A']
    ret = []
    spell = Speller(lang='en')
    for s in sample:
        if has_spaces_or_special_characters(s):
            # print(f"Need to treat {s}")
            arr = s.split(' ')
            dump = []
            for a in arr:
                a = remove_special_characters(a)
                res = spell(a)
                if res != a:
                    dump.append(res)
                else:
                    dump.append(a)
            fin = ' '.join(dump)
            ret.append(fin)
            #print(f"Original {s} change to {fin}")
        else:
            ret.append(s)
    return ret
