from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd



def u(i):
    try:
        return chr(int(i, 16))    #int(i, 16) converts the hex string to an integer, and chr returns the representation in unicode
    except:
        return i         #if something fails, returns the input
    

def create_df_unicode():
    """
    Parses unicode names list into pandas dataframe
    Data downloaded from https://www.unicode.org/Public/UCD/latest/ucd/
    """
    with open('data/unicode_names_list.txt','r', encoding = "utf8") as f:   #added "encoding = 'utf8'" since it wasn't running on mine
        unicode = f.read()

    unicode = unicode.split('\n')    #splits the text at every new line and creates a list of lines
    df_unicode = pd.DataFrame([k.split('\t') for k in unicode if len(k)>0 and k[0] not in '\t;@'], columns=['code','note'])
    
    #splits the text at every tab (\t) EXCEPt if the line has no values in it (length of the line is 0) and except if it starts with \t ; @ since some of the introductory lines start with these -- only want the characters we care about. Also, turns it into a Dataframe with columns 'code' and 'note'
    
    #changed 'u' to 'k' in order to avoid confusion with the function
  
    df_unicode = df_unicode[df_unicode.note.apply(lambda x: x[0]!='<')].reset_index(drop=True)  #drops any row that has the start of the 'note' column as '<' -- there are a series of lines that are '<control>' and not needed so this drops those
    
    df_unicode.note.apply(lambda x: x.split()[0]).value_counts().index.tolist()  #this just prints the first 'word' in note which tends to be the language? not affecting df_unicode, so likely just a check
    
    df_unicode['rep'] = df_unicode.code.apply(u)     #creates column for representation

    return df_unicode



def code_type(code):
    """
    Determines code type of unicode code.
    """
    h = '0x'+code
    for a,b,c in [('0x1F600', '0x1F64F', 'Emoticons'),    
                  ('0x1F300', '0x1F5FF', 'Misc Symbols and Pictographs'),
                  ('0x1F680', '0x1F6FF', 'Transport and Map'),
                  ('0x2600', '0x26FF', 'Misc symbols'),
                  ('0x2700', '0x27BF', 'Dingbats'),
                  ('0xFE00', '0xFE0F', 'Variation Selectors'),
                  ('0x1F900', '0x1F9FF', 'Supplemental Symbols and Pictographs'),
                  ('0x1F1E6', '0x1F1FF', 'Flags')]:
        if a <= h <= b:      #checks if the unicode that you want to check ('h') is between a and b, if so, is assigned  appropriate label
            return c
    return 'Writing Symbol'    #if it doesn't fit any of the above categories



def get_language(note):
    """
    Extracts language from unicode note.
    Assumes first word of note is the language.
    """
    return note.split()[0]      #splits note and takes first word

    
def make_picture(code, ttf):
    """
    Creates picture of character
    Inputs:
        code: hex representation of unicode character
        ttf: location of .ttf file for a font
    Outputs:
        picture: 2d numpy array
    """
    image = Image.new('RGB', (100,100))

    draw = ImageDraw.Draw(image) 
    draw.text((50,50), 
              u(code), 
              font = ImageFont.truetype(ttf, 11))
    picture = np.mean(255-np.array(image),axis=-1)/255
    return picture
