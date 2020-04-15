from sys import stdout, path
path.append("..")

from wordcloud import WordCloud, ImageColorGenerator
from config.config_file import baseDir
import os
import json
from functools import reduce
import matplotlib.pyplot as plt  
from PIL import Image
import numpy as np

baseDir += "/Data/OtherChains"

def constructCorpus(chainName, channelName):
    fn = os.path.join(baseDir, chainName, "Telegram", channelName+".json")
    with open(fn) as f:
        data = json.load(f)
    corp = ""
    for msg in data:
        if msg["Body"] != None:
            corp += msg["Body"]
    return corp.lower()
        
def createCloud(corpus, chainName, channelName):
    wc = WordCloud(background_color="white", max_words=100, width=500, height=500, random_state=1).generate(corpus)# to recolour the image
    
    mask = np.array(Image.open("bw.jpg"))    
    colors = ImageColorGenerator(mask)
    
    img = plt.imshow(wc.recolor(color_func=colors))
    plt.axis("off")
    outputPath = os.path.join(baseDir, chainName, "Telegram", channelName+"_wordcloud.png")
    plt.savefig(outputPath)

def main():
    with open("telegram_channels.json") as f:
        channelNames = json.load(f)

    for chain,names in channelNames.items():
        for name in names:
            print("generating word cloud for channel %s" % name)
            corp = constructCorpus(chain, name)
            createCloud(corp, chain, name)

if __name__ == "__main__":
    main()