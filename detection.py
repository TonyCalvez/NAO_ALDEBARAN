import time
import cv2
import mss
import numpy


def median_color(img, kernel):
    median = cv2.medianBlur(img, kernel)
    return median


def segmentation_color(img, min_hsv, max_hsv):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # COLORPICKER = [105   8 192] [ 95  -2 152] [115  18 232]
    floor_low = min_hsv
    floor_high = max_hsv
    curr_mask = cv2.inRange(hsv_img, floor_low, floor_high)
    hsv_img[curr_mask > 0] = ([0, 0, 255])
    img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
    return img


def gray_converting(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img_gray


def thresholding_white_black(img):
    ret, thresh = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh


def drawing_contours(img, img_src):
    im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(img_src, contour, -1, (0, 255, 0), 3)
    return img, img_src

def edge_filtering(img):
    # Smoothing without removing edges.
    bilateral_images = cv2.bilateralFilter(img, 7, 50, 50)

    # Applying the canny filter
    canny_images = cv2.Canny(bilateral_images, 60, 120)
    return canny_images


def masking_top_screen(img, monitor):
    vertices = numpy.array(
        [[0, monitor["height"]], [0, monitor["height"] / 2], [monitor["width"] / 3, monitor["height"] / 3],
         [2 * monitor["width"] / 3, monitor["height"] / 3], [monitor["width"], monitor["height"] / 2],
         [monitor["width"], monitor["height"]],
         ], numpy.int32)
    mask = numpy.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, [vertices], 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked


def underlining(img, img_src, monitor):
    lines = cv2.HoughLinesP(img, 1, numpy.pi/180, 25, maxLineGap=255)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x1 < monitor["width"]/8 or x1 > monitor["width"] - monitor["width"]/8:
                cv2.line(img_src, (x1, y1), (x2, y2), (0, 255, 0), 10)
    return img_src


with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 120, "left": 60, "width": 800, "height": 400}
    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img_src = numpy.array(sct.grab(monitor))

        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)
        min_hsv = numpy.array([75, 250, 170])
        max_hsv = numpy.array([105, 270, 255])
        img = segmentation_color(img_src, min_hsv, max_hsv)
        img = median_color(img, 25)
        img = gray_converting(img)
        img = masking_top_screen(img, monitor)
        img = thresholding_white_black(img)
        img = edge_filtering(img)
        #img = underlining(img, img_src, monitor)

        cv2.imshow('DEEPDART Visual', img)

        # print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
