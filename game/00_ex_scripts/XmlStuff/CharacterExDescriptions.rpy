﻿init -999 python:
    import xml.etree.ElementTree as ET

    class CharacterExDescriptionTransform(store.object):
        #
        def __init__( self, aElementRoot, aId ):
            self.mId = aId
            self.mName = ""
            self.mParams = {}
            self._read( aElementRoot )

        #
        def _read( self, aElementRoot, aFolderBase, aOrderBase ):
            for child in aElementRoot:
                if child.tag == 'name':
                    self.mName = child.text
                else:
                    self.mParams[ child.tag ] = child.text


    class CharacterExDescriptionActionCondition(store.object):
        #
        def __init__( self, aElementRoot, aFolderBase, aOrderBase ):
            self.mType = ""
            self.mParams = []   # array of hashmaps (string-tupple(value,compare_method))
            # compare methods:
            # e - equal (default)
            # ne - not equal
            # le - lower or equal
            # ge - greater or equal
            # l - lower
            # g - greater
            # ne - not equal
            self._read( aElementRoot, aFolderBase, aOrderBase )

        #
        def _read( self, aElementRoot, aFolderBase, aOrderBase ):
            self.mType = aElementRoot.get('type')
            compPossible = [ 'e', 'ne', 'ge', 'le', 'g', 'l' ]
            for child in aElementRoot:
                if child.tag == 'params':
                    paramsMap = {}
                    for param in child:
                        compareMeth = param.get('c')
                        if compareMeth == None or ( compareMeth not in compPossible ):
                            compareMeth = 'e'
                        paramsMap[ param.tag ] = ( param.text, compareMeth )
                    self.mParams.append( paramsMap )


    class CharacterExDescriptionAction(store.object):
        #
        def __init__( self, aElementRoot, aFolderBase, aOrderBase ):
            self.mType = ""     # type of actions ( addItem, removeItem, showItem, hideItem )
            self.mEvent = ""    # type of events ( selfAdded, selfRemoved, itemAdded, itemRemoved, itemShown, itemHiden )
            self.mKeys = []   # array of strings ( keys where to add/remove etc. )
            self.mNames = []   # array of strings ( names of items/sets )
            self.mConditions = []   #array of condition descriptions
            self._read( aElementRoot, aFolderBase, aOrderBase )

        #
        def _read( self, aElementRoot, aFolderBase, aOrderBase ):
            self.mType = child.get('type')
            self.mEvent = child.get('event')
            for child in aElementRoot:
                if child.tag == 'body':
                    for condition in child:
                        self.mConditions.append( CharacterExDescriptionActionCondition( aElementRoot, aFolderBase, aOrderBase ) )
                if child.tag == 'key':
                    for key in child.text.split(','):
                        self.mKeys.append( key )
                if child.tag == 'name':
                    for name in child.text.split(','):
                        self.mNames.append( name )
            


    class CharacterExDescriptionStyle(store.object):
        #
        def __init__( self, aElementRoot, aItemName, aFolderBase, aOrderBase ):
            self.mName = aItemName
            self.mFrame = ""
            self.mFileFolder = ""
            self.mZOrder = 0
            self.mParent = ""
            self.mIsVisible = True
            self.mShift = Transform( pos = ( 0, 0 ) )
            self.mTransforms = {} # map of transform descriptions
            self.mHideList = [] # array of strings
            self.mActions = []  # array of actions descriptions

            self._read( aElementRoot, aFolderBase, aOrderBase )

        # read self from xml
        def _read( self, aElementRoot, aFolderBase, aOrderBase ):
            for child in aElementRoot:
                if child.tag == 'frame':
                    self.mFrame = child.text
                if child.tag == 'folder':
                    self.mFileFolder = aFolderBase.get( child.text )
                if child.tag == 'zorder':
                    self.mZOrder = aOrderBase.get( child.text )
                if child.tag == 'visible':
                    self.mIsVisible = bool( child.text )
                if child.tag == 'parent':
                    self.mParent = child.text
                if child.tag == 'shift':
                    if child.text != '':
                        posText = child.text
                        if posText != None:
                            positions = []
                            for pos in child.text.split( ',' ):
                                positions.append( int( pos ) )
                            self.mShift = Transform( pos = ( positions[0], positions[1] ) )
                
                if child.tag == 'transforms':
                    for trSingle in child:
                        trId = trSingle.get('id')
                        self.mTransforms[ trId ] = CharacterExDescriptionTransform( actSingle, trId )

                if child.tag == 'hidelist':
                    for hideItem in child:
                        self.mHideList.append( hideItem.text )

                if child.tag == 'actions':
                    for actSingle in child:
                        self.mActions.append( CharacterExDescriptionAction( actSingle, aFolderBase, aOrderBase ) )



    class CharacterExDescriptionItem(store.object):
        #
        def __init__( self, aXmlRoot, aFolderBase, aOrderBase ):
            self.mKey = ""
            self.mName = ""
            self.mStyles = {}
            self._read( aXmlRoot, aFolderBase, aOrderBase )


        # read self from xml
        def _read( self, aXmlRoot, aFolderBase, aOrderBase ):
            # first of all we should read this two items
            for child in aXmlRoot:
                if child.tag == 'key':
                    self.mKey = child.text
                if child.tag == 'name':
                    self.mName = child.text

            # and only then - styles
            for child in aXmlRoot:
                if child.tag == 'style':
                    styleKey = child.get('name')
                    self.mStyles[ styleKey ] = CharacterExDescriptionStyle( child, self.mName, aFolderBase, aOrderBase )
