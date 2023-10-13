from PIL import Image
import time

def getExampleImage(path: str):
    """ließt das Beispiel Bild als png am relativen Pfand ein

    :param path: Der relative pfad von dem Bild des Beispiels
    :returns: eine liste von Zeilen des Beispiels
    """
    return Image.open(path).convert("RGB")

def main():
    for x in range(5,6):

        #Input
        rawData = getExampleImage(f"bild{x+1}.png")
        img = rawData.load()

        width, height = rawData.size

        #print(f"Beispiel {x+1}:")


        r,g,b = img[0,0]
        Pos = [0,0]

        msg = chr(img[0,0][0])

        while not (g == 0 and b == 0):

            Pos[0] += g
            Pos[1] += b

            r,g,b = img[Pos[0]%width,Pos[1]%height]

            msg += chr(r)

        print(msg)

        rawData.close()

        print()

if __name__ == "__main__":
    main()