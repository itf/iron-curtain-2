import time
from functools import wraps

'''
This file defines functions to be used for creating patterns, and
defines the PatternInput

Patterns are functions that take a PatternInput and returns a Canvas

'''


def intCache(intFunctionCondition):
    '''
    Takes a function that returns an int or boolean, and then a function
    to be cached and returns the cached function
    The cached function when called will evaluate the intFunction->N and then
    run the function N times (in case it has side effects),
    and return the result.
    If N <1, it will return the previous result and not run the function
    again.

    Example usage:
    @intCache(lambda x: x>1)
    def test(x):
			return x
      
    prints the previous value of x if x<=1

    '''
    def buildFunctionWithIntCache(function):
        cache=[None]
        @wraps(function) #preserves __name__ and __doc__
        def cachedFunction(*args, **kwargs):
            if cache[0]!=None:
                numberOfRuns=intFunctionCondition(*args, **kwargs)
                for i in xrange(numberOfRuns):
                    cache[0]=function(*args, **kwargs)
            else:
                cache[0]=function(*args, **kwargs)
            return cache[0]
        return cachedFunction
    return buildFunctionWithIntCache


def timedPattern(frameRate=30):
    '''
    Returns a pattern that will only be called on the determined frameRate
    Example usage:

    @timedPattern(30)
    def test(x):
	return x

    for i in xrange(1000):
	test(i)

    Will print 0 untill 1/30 of a second has passed
    and then will print the value of i right after 1/30 of a second.
    '''
    PREVIOUS_TIME = [None]
    miliseconds=1000
    def timeFrames(*args, **kwargs):
        thisTime=time.time()*miliseconds
        if(PREVIOUS_TIME[0]!=None):
            frames = int((thisTime - PREVIOUS_TIME[0])/miliseconds*frameRate)
            if(frames>0):
                PREVIOUS_TIME[0]=thisTime
        else:
            frames=0
            PREVIOUS_TIME[0]=time.time()*miliseconds
        return frames
    return lambda function:intCache(timeFrames)(function)


def framePattern(intFunction):
    '''
    Takes  a function to calculate the frame, 
    a frameGetter (a function that takes an int and returns
    a frame, and returns a pattern

    Example usage:
    @framePattern(lambda x:2*x)
    def frameGetter(x):
	return x

    frameGetter(2)->4
    '''
    def buildPatternFrame(frameGetter):
        @wraps(frameGetter)#preserves __name__ and __doc__
        def getFrame(*args, **kwargs):
            frame=intFunction(*args, **kwargs)
            return frameGetter(frame)
        return getFrame
    return buildPatternFrame

def timedFramePattern(frameRate=30):
    '''
    Takes a frame rate and a function that takes a frame;
    returns the result of the frameGetter for the particular frameRate
    in time

    Example:
    @timedFramePattern()
    def test(x):
	return x
    
    while(1):
	test(1)
    '''
    miliseconds=1000
    START_TIME = time.time()*miliseconds
    def timeFrames(*args, **kwargs):
        thisTime = time.time()*miliseconds
        return int((thisTime - START_TIME)/miliseconds*frameRate)
    return lambda frameGetter:framePattern(timeFrames)(frameGetter)


def staticPattern(pattern):
    '''
    Marker
    '''
    return pattern


'''
A pattern is a function that takes a PatternInput and returns a canvas
'''

class PaterrnInput(dict):
    def __init__(self, height, width, audioData=None, frame=None, params=None, canvas=None):
        self['width']=width
        self['height']=height
        self['audioData']=audioData
        self['frame']=frame
        self['params']=params
        self['canvas']=canvas
