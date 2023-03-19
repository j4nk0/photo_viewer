#!/usr/bin/python3
# author: gajdijan@fit.cvut.cz

from PIL import Image
from io import BytesIO
import numpy as np
import string

def file2PPM6bytes(filename):
    try:
        ramFile = BytesIO()
        input_image = Image.open(filename)
        converted_image = input_image.convert('RGB')
        converted_image.save(ramFile, "PPM")
        return ramFile.getvalue()
    except:
        raise ValueError

class MyImage:

    """Internal image representation
        self.data   - bytes holding full PPM6 picture represemtation
        self.width  - integer - image width
        self.height - integer - image height
        self.colors - integer - describes number of colors (typically 255)
        self.begin  - header length"""

    def __init__(self, PPM6):
        self.data = PPM6
        self.width  = None
        self.height = None
        self.colors = None
        try:
            if PPM6[:2] != b'P6': raise ValueError
            i = 2
            while (PPM6[i] not in string.whitespace.encode('ascii')): i += 1
            while (PPM6[i] in string.whitespace.encode('ascii')): i += 1
            # skipping comments
            while (str(PPM6[i]) == b'#'):
                while (PPM6[i] not in string.whitespace.encode('ascii')): i += 1
                while (PPM6[i] in string.whitespace.encode('ascii')): i += 1
            # extracting data
            buffered_string = []
            while (PPM6[i] not in string.whitespace.encode('ascii')):
                # acii compatible encoding :
                buffered_string.append(bytes([PPM6[i]]).decode('utf-8'))
                i += 1
            self.width = int(''.join(buffered_string).strip())
            while (PPM6[i] in string.whitespace.encode('ascii')): i += 1
            buffered_string = []
            while (PPM6[i] not in string.whitespace.encode('ascii')):
                # acii compatible encoding :
                buffered_string.append(bytes([PPM6[i]]).decode('utf-8'))
                i += 1
            self.height = int(''.join(buffered_string).strip())
            while (PPM6[i] in string.whitespace.encode('ascii')): i += 1
            buffered_string = []
            while (PPM6[i] not in string.whitespace.encode('ascii')):
                # acii compatible encoding :
                buffered_string.append(bytes([PPM6[i]]).decode('utf-8'))
                i += 1
            while (PPM6[i] in string.whitespace.encode('ascii')): i += 1
            self.colors = int(''.join(buffered_string).strip())
        except: raise ValueError('P6 header parsing error')
        self.begin = i

    def swap(self, other):
        self.data   = other.data  
        self.width  = other.width 
        self.height = other.height
        self.colors = other.colors
        self.begin  = other.begin

    def getdata(self):
        return self.data

    def encode_header(self):
        """change data header so that it corresponds with attributes values"""
        newheader = 'P6\n'.encode('ascii')      \
            + str(self.width).encode('ascii')   \
            + ' '.encode('ascii')               \
            + str(self.height).encode('ascii')  \
            + '\n'.encode('ascii')              \
            + str(self.colors).encode('ascii') \
            + '\n'.encode('ascii')
        self.data = newheader + self.data[self.begin:] 
        self.begin = len(newheader)

    def getArray(self):
        return np.frombuffer(
            self.data[self.begin:],
            dtype=np.uint8,
            count=self.width * self.height * 3
        )

    def pixelateArray(self, arr):
        """changes shape of arr to allow pixel mapping by following formulae:
            arr [row][column][R/G/B]"""
        return arr.reshape((self.height, self.width, -3))

    def invert(self):
        arr = self.getArray()
        operation_array = np.array([255], dtype=np.uint8)
        arr = operation_array - arr
        self.data = self.data[:self.begin] + bytes(arr)

    def rotate_clockwise(self):
        arr = self.getArray()
        arr = self.pixelateArray(arr)
        arr = np.rot90(arr, 1, (1, 0))
        self.width, self.height = self.height, self.width
        self.encode_header()
        self.data = self.data[:self.begin] + bytes(arr)

    def rotate_counterclockwise(self):
        arr = self.getArray()
        arr = self.pixelateArray(arr)
        arr = np.rot90(arr, 1, (0, 1))
        self.width, self.height = self.height, self.width
        self.encode_header()
        self.data = self.data[:self.begin] + bytes(arr)

    def mirror(self):
        arr = self.getArray()
        arr = self.pixelateArray(arr)
        arr = np.fliplr(arr)
        self.data = self.data[:self.begin] + bytes(arr)
        
    def grayscale(self):
        arr = self.getArray()
        # gamma corrections:
        def gama1(x):
            if x <= 0.04045: return x / 12.92
            else: return ((x + 0.055) / 1.055) ** 2.4

        def gama2(x):
            if x <= 0.0031308: return  round(12.92 * x)
            else: return round(1.055 * x ** (1 / 2.4) - 0.055)
            
        g1 = np.vectorize(gama1, otypes=[np.float])
        g2 = np.vectorize(gama2, otypes=[np.uint8])
        arr = g1(arr)
        arr = self.pixelateArray(arr)
        operation_array = np.array([0.2126, 0.7152, 0.0722])
        arr = arr * operation_array
        arr = arr.sum(2)
        arr = arr.repeat(3)
        arr = self.pixelateArray(arr)
        arr = g2(arr)
        self.data = self.data[:self.begin] + bytes(arr)

    def sharpen(self):
        """applies Laplace operator:
            ( 0 -1  0)
            (-1  5 -1)
            ( 0 -1  0)"""
        arr = self.getArray()
        arr2 = self.getArray()
        arr = self.pixelateArray(arr)
        arr2 = self.pixelateArray(arr2)
        arr2.flags.writeable = True
        self.data = self.data[:self.begin] + bytes(arr)
        for row in range(1, self.height -1):
            for col in range(1, self.width -1):
                for rgb in range(3):
                    x = - int(arr[row -1][col][rgb])     \
                        - int(arr[row +1][col][rgb])     \
                        - int(arr[row][col -1][rgb])     \
                        - int(arr[row][col +1][rgb])     \
                        + 5 * arr[row][col][rgb]
                    if x > 255: x = 255
                    elif x < 0: x = 0
                    arr2[row][col][rgb] = x
        self.data = self.data[:self.begin] + bytes(arr2)

    def brighten(self):
        def brighten_pixel(x):
            x = 255 - x
            x = round(x * (4 / 5))
            return 255 - x

        arr = self.getArray()
        bp = np.vectorize(brighten_pixel, otypes=[np.uint8])
        arr = bp(arr)
        self.data = self.data[:self.begin] + bytes(arr)

    def darken(self):
        def darken_pixel(x):
            return round(x * (4 / 5))

        arr = self.getArray()
        dp = np.vectorize(darken_pixel, otypes=[np.uint8])
        arr = dp(arr)
        self.data = self.data[:self.begin] + bytes(arr)

if __name__ == '__main__':
    try:
        bts = file2PPM6bytes("Lenna.png")
        print('---')
        for i in range(20):
            print(bts[i])
        print('---')
        print(bts[:20])
        print('---')
        img = MyImage(bts)
        img.grayscale()
        #img.getdata()
    except ValueError:
        print("error")
        raise
