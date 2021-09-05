# -*- coding: utf-8 -*-
# Python script to open each file, read json input and copy to one text file for subsequent processing
import os, re, sys
import json

class clJsonDir2txt(object):
    '''
    @author Bogdan Babych, IÜD, Heidelberg University
    @email bogdan.babych@iued.uni-heidelberg.de
    a script for processing covid-19 corpus:
    @url https://www.semanticscholar.org/cord19 @url https://www.semanticscholar.org/cord19/download
        recursively reads files from a directory, and glues them together into a single corpus file

    @todo:
        working with sections - collect titles of all sections; frequent sections; select argumentative sections (e.g., discussion, analysis...)
        - to compare descriptive and argumentative parts of the corpus

        experimenting with different annotations (pos, parsing... ); MT quality evaluation...
    '''
    def __init__(self, SDirName, output_file = 'corpus_out.txt', include_title = True, include_refs = True, include_authors = True, tag='doc', id=1000000, split_by_docs = 0): # initialising by openning the directories
        self.SOutput_file = output_file
        self.BInclTitle = include_title # implemented
        self.BInclRefs = include_refs # not implemented yet
        self.BInclAuth = include_authors # not implemented yet
        self.STag = tag
        self.ID = id
        self.ISplitByDocs = int(split_by_docs)
        # print(self.ISplitByDocs)
        self.openDir(SDirName)
        return


    def openDir(self, path): # implementation of recursively openning directories from a given rule directory and reading each file recursively into a string
        i = 0
        if self.ISplitByDocs:
            SPartFile = "part1000000" + self.SOutput_file
            FOut = open(SPartFile, 'w')
        else:
            FOut = open(self.SOutput_file, 'w')

        for root,d_names,f_names in os.walk(path):
            for f in f_names:
                i+=1
                if i%1000==0: print(str(i) + '. Processing: ' + f)
                fullpath = os.path.join(root, f)
                # print(fullpath)
                try:
                    FIn = open(fullpath,'r')
                    SIn = FIn.read()
                    SText2Write = self.procFile(SIn,f,i)
                    if SText2Write: FOut.write(SText2Write) # if the string is not empty then write to file
                    FIn.close()
                except:
                    print(f'file {f} cannot be read or processed')

                # splitting output into chunks of "split_by_docs" size
                if self.ISplitByDocs and (i % self.ISplitByDocs == 0): # if self.ISplitByDocs == 0 then everything goes into one file; if this > 0 then
                    SPartFile = "part" + str(1000000 + i) + self.SOutput_file # generate new file name
                    FOut.flush()
                    FOut.close()
                    FOut = open(SPartFile, 'w')
        FOut.flush()
        FOut.close()

        return


    def procFile(self, SIn,SFNameIn,i): # sending each json string for extraction of text and attaching an correct tags to each output string output string
        STagOpen = '<' + self.STag + ' id="' + self.STag + str(self.ID + i)  + '">\n'
        STagClose = '\n</' + self.STag + '>\n\n'
        SText4Corpus = self.getJson(SIn, SFNameIn)
        if SText4Corpus:
            return STagOpen + SText4Corpus + STagClose
        else:
            print('\tNo data read from: ' + SFNameIn)
            return None


    def getJson(self, SIn, SFNameIn): # for each file-level string read from a file: managing internal structure of the covid-19 json file
        LOut = [] # collecting a list of strings
        try:
            DDoc = json.loads(SIn)
        except:
            print('\t\t' + SFNameIn + ' => error reading json2dictionary')
            return None
        # metadata:
        try:
            DMetaData = DDoc['metadata']
            if DMetaData:
                SMetaData = self.getJson_Metadata(DMetaData)
                if SMetaData: LOut.append(SMetaData)
        except:
            print('\t\t\t' + SFNameIn + ' ====> no metadata')
            DMetaData = None
        # body text
        try:
            LBodyText = DDoc['body_text']
            if LBodyText:
                SBodyText = self.getJson_BodyText(LBodyText)
                LOut.append(SBodyText)
        except:
            print('\t\t\t' + SFNameIn + ' ====> no body_text')
            LBodyText = None
        # further: to implement references

        SText = '\n\n'.join(LOut)
        return SText


    def getJson_Metadata(self, DIn): # converts interesting parts of metadata into a string
        SMetadata = ''
        LMetadata = []
        try: STitle = DIn["title"]
        except: STitle = None
        if STitle and self.BInclTitle:
            LMetadata.append(STitle)

        # to implement reading of authors' names

        if LMetadata: SMetadata = '\n\n'.join(LMetadata)
        return SMetadata


    def getJson_BodyText(self, LIn): # converts interesting parts of the body texts into a string
        SBodyText = ''
        LBodyText = []
        for DParagraph in LIn:
            try:
                ## DParagraphs[section] ## -- later on >> distinction between different sections....
                SParagraph = DParagraph["text"]
                LBodyText.append(SParagraph)
            except:
                print('!',)
                continue

        SBodyText = '\n\n'.join(LBodyText)
        return SBodyText



if __name__ == '__main__':
    OJsonDir2txt = clJsonDir2txt(sys.argv[1], output_file = 'covid19corpus.txt', include_title = True, include_refs = False, split_by_docs=0)
    # arguments:
    '''
        sys.argv[1], # obligatory: input directory name;
            other arguments optional:
            output_file = 'covid19corpus.txt',
            include_title = True, # include or exclude title
            include_refs = False, # not implemented yet: include or exclude references
            split_by_docs=0 # split by groups of n documents; if 0 then write to one file
    '''
