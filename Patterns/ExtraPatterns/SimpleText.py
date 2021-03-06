import Patterns.Pattern as P
import Patterns.Function as F
import letters
import copy


textRealHeight=5

@P.pattern("text")
@F.defaultArgsP(text='SPAACE', textHeight=1, textPos=0.5)
def textPattern(PatternInput):
    '''
    A simple text pattern, that uses letters that are 5 pixes tall.
    At textPos=0, the text is not on the screen; it is all the way tothe right.
    At text pos=1, it also exits the screen, and is all the way to the left.
    The height is normalized. Height=1 means that it uses the whole vertical span
    of the screen.
    '''
    text = str(PatternInput['text'])
    text=text.upper()
    textHeight = PatternInput['textHeight']
    textPos = PatternInput['textPos']

    canvasWidth = PatternInput['width']
    canvasHeight = PatternInput['height']

    epsilon=0.001
    conversionFactor = max(float(canvasHeight*textHeight/textRealHeight),epsilon)

    spaceWidth = letters.letters[' '].width+1
    realSpaceWidth = spaceWidth*conversionFactor
    spacePadding = int(canvasWidth/realSpaceWidth)+1

    paddedText = ' '*spacePadding+text+' '

    canvas = PatternInput['canvas']
    canvas = createScaledText(canvas, paddedText, textPos, conversionFactor)

    PatternInput['canvas']=canvas
    return PatternInput


def simpleCached(cacheSize):
    cache={}
    def cacheFunction(function):
        def cachedFunction(*args):
            tArgs=tuple(args)
            if tArgs in cache:
                return cache[tArgs]
            else:
                answer=function(*args)
                if len(cache)>cacheSize:
                    cache.popitem()
                    cache.popitem()
                cache[tArgs]=answer
                return answer
        return cachedFunction
    return cacheFunction

@simpleCached(4)
def getLetters(text):
    text= letters.sanitize_str(text)
    myletters = [letters.letters[c] for c in text]
    return myletters

def createScaledText(canvas, text, textPos, conversionFactor):
    myletters = getLetters(text)
    textWidth = sum(let.width + 1 for let in myletters)

    textWPos = textPos*textWidth
    indexBegin=0
    indexMax=len(myletters)
    pos = textWPos
    while pos >= 0 and indexBegin<indexMax:
        pos-= (myletters[indexBegin].width+1)
        indexBegin+=1
    indexBegin-=1
    pos+= myletters[indexBegin].width+1
    
    canvasWidth = canvas.width
    smallCanvasWidth = int(round(float(canvasWidth)/conversionFactor + pos))

    myRealLetters = myletters[indexBegin:]
    smallCanvas=createSmallTextCanvas(myRealLetters, smallCanvasWidth)

    red=(1,0,0)
    black=(0,0,0)
    maxY=5
    maxX=smallCanvasWidth
    def letterrizer(rgb,y,x):
        realX=int(float(x)/conversionFactor + pos)
        realY = int(float(y)/conversionFactor)
        if realY<maxY and realX<maxX and smallCanvas[realY][realX]:
            return red
        else:
            return black
    canvas.mapFunction(letterrizer)
    return canvas
    


def createSmallTextCanvas(myletters, smallCanvasWidth):
    canvas=[]
    for i in xrange(textRealHeight):
        canvas.append([0]*smallCanvasWidth)

    pos=0
    index=0
    maxIndex=len(myletters)
    while (pos<smallCanvasWidth and index<maxIndex):
        letter = myletters[index]
        pixels = letter.pixel_list
        for pixel in pixels:
            x,y=pixel
            if x+pos<smallCanvasWidth:
                canvas[y][x+pos]=1
        pos+=letter.width+1
        index+=1
    return canvas


