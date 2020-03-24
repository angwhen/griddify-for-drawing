import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import sys
import argparse
try:
    from PIL import Image
except ImportError:
    import Image

def sizeCanvas(imageHeight,imageWidth,canvasHeight,canvasWidth):
    if imageHeight < imageWidth:
        imageRatio = imageHeight/imageWidth
        canvasRatio = canvasHeight/canvasWidth
        if (imageRatio<canvasRatio):
            return canvasWidth*imageRatio,canvasWidth
        else:
            return canvasHeight,canvasHeight/imageRatio
    else:
        imageRatio = imageWidth/imageHeight
        canvasRatio = canvasWidth/canvasHeight
        if (imageRatio<canvasRatio):
            return canvasHeight,canvasHeight*imageRatio
        else:
            return canvasWidth/imageRatio,canvasWidth
# references
# https://stackoverflow.com/questions/44816682/drawing-grid-lines-across-the-image-uisng-opencv-python

def griddify(filename,canvasWidth,canvasHeight):
    # Open image file
    image = Image.open(filename)
    my_dpi=200.

    # Set up figure
    imageWidth = image.size[0]
    imageHeight = image.size[1]
    fig=plt.figure(figsize=(float(image.size[0])/my_dpi,float(image.size[1])/my_dpi),dpi=my_dpi)
    ax=fig.add_subplot(111)

    # Remove whitespace from around the image
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

    # Set the gridding interval: here we use the major tick interval
    myInterval=imageHeight/8
    heightPieces = 8
    if (imageHeight < imageWidth):
        myInterval = imageHeight/5
        heightPieces = 5
    loc = plticker.MultipleLocator(base=myInterval)
    locMinor = plticker.MultipleLocator(base=myInterval/2)
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)
    ax.xaxis.set_minor_locator(locMinor)
    ax.yaxis.set_minor_locator(locMinor)

    # Add the grid
    ax.grid(which='minor', axis='both', linestyle=':', linewidth=0.4,color='w')
    ax.grid(which='major', axis='both', linestyle='-', linewidth=1,color='g')

    # Add the image
    ax.imshow(image)

    # Find number of gridsquares in x and y direction
    nx=abs(int(float(ax.get_xlim()[1]-ax.get_xlim()[0])/float(myInterval)))
    ny=abs(int(float(ax.get_ylim()[1]-ax.get_ylim()[0])/float(myInterval)))

    if (not ((canvasWidth <= canvasHeight and imageWidth <=imageHeight) or (canvasWidth > canvasHeight and imageWidth > imageHeight))):
        heightHold = canvasHeight
        canvasHeight=canvasWidth
        canvasWidth=heightHold

    # Save the figure
    fig.savefig('gridded_image.jpg')

    newCanvasHeight,newCanvasWidth=sizeCanvas(imageHeight,imageWidth,canvasHeight,canvasWidth)
    print("Modify your canvas to have dimensions: %.2f by %.2f cm"%(newCanvasHeight,newCanvasWidth))
    print("Divide the canvas into major pieces of size %.2f cm"%(newCanvasHeight/heightPieces))
    for x in range(1,8):
        print(newCanvasHeight/heightPieces*x, end ="cm ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #required.add_argument('--required_arg', required=True)
    parser.add_argument('filename', nargs='?', default=None)
    parser.add_argument("-w","--width", type=float, default = 60, help="enter the width of your canvas in cm")
    parser.add_argument("-t","--height", type=float, default = 45,help="enter the height of your canvas in cm")
    args = parser.parse_args()
    griddify(args.filename,args.width,args.height)