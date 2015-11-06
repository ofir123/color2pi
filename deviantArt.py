import sys
import time
import math
import random
import logbook
import colorsys
import zmq
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException

# USE WITH FIREFOX & SELENIUM-0.46.0 ONLY!!!!!

# Server related constants.
DEFAULT_LISTENING_PORT = '5556'
STOP_MESSAGE = 'STOP'
OK_REPLY = 'OK'
COLORS_DELIMITER = ','

# A JS script which removes a given element.
REMOVE_SCRIPT = 'var element = document.querySelector("{0}");' \
                'if (element) element.parentNode.removeChild(element);'

# A JS script which modifies a specific value in all elements of a given class.
MODIFY_SCRIPT = 'var list = document.getElementsByClassName("{0}");' \
                'for (var i = 0; i < list.length; i++) {{ ' \
                'list[i].{1} = "{2}" }};'

# The size of one part of the color square.
COLOR_SQUARE_SIZE = 68
# Sliders settings.
MIN_OPACITY = 30
MAX_OPACITY = 118
MIN_SIZE = 30
MAX_SIZE = 60
COLORS_LIMIT = 120

log = logbook.Logger('DeviantArt')


def remove_class(driver, class_name):
    """
    Removes the element with the given class.
    """
    driver.execute_script(REMOVE_SCRIPT.format('.' + class_name))


def remove_id(driver, id_name):
    """
    Removes the element with the given ID.
    """
    driver.execute_script(REMOVE_SCRIPT.format('#' + id_name))


def change_canvas_size(driver, class_name, width, height, only_style=False):
    """
    Changes the size of a canvas, to the desired width and height.
    
    :param class_name: The canvas' class name.
    :param width: The desired width.
    :param height: The desired height.
    :param only_style: If True, the width and height will be changed in the style attribute only.
    """
    driver.execute_script(MODIFY_SCRIPT.format(class_name, 'style.width', str(width) + 'px'))
    driver.execute_script(MODIFY_SCRIPT.format(class_name, 'style.height', str(height) + 'px'))
    if not only_style:
        driver.execute_script(MODIFY_SCRIPT.format(class_name, 'width', str(width)))
        driver.execute_script(MODIFY_SCRIPT.format(class_name, 'height', str(height)))


def change_slider(driver, slider_element, value):
    """
    Changes one of the 3 option sliders.
    
    :param slider_element: The slider element to change.
    :param value: The desired value.
    """
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(slider_element, value, 0)
    action.click()
    action.perform()


def change_color(driver, r, g, b):
    """
    Changes the color according to the given RGB values.
    """
    h, s, v = colorsys.rgb_to_hsv(float(r), float(g), float(b))
    # Change hue.
    r = COLOR_SQUARE_SIZE / 2
    # The hue angle has an offset of 45 degrees.
    teta = math.radians(h * 360 - 45)
    # Add the center coordinates.
    x = r * math.cos(teta) + COLOR_SQUARE_SIZE / 2
    y = -r * math.sin(teta) + COLOR_SQUARE_SIZE / 2
    hue_element = driver.find_element_by_class_name('hueClick')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(hue_element, x, y)
    action.click()
    action.perform()
    # Change saturation and value.
    x = s * COLOR_SQUARE_SIZE
    y = COLOR_SQUARE_SIZE - (v / 255.0) * COLOR_SQUARE_SIZE
    saturation_element = driver.find_element_by_class_name('satval_area')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(saturation_element, x, y)
    action.click()
    action.perform()


def paint(driver, canvas_element, x, y):
    """
    Paint in the given coordinates.
    """
    try:
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(canvas_element, x, y)
        action.click_and_hold()
        for j in xrange(70):
            action.move_to_element_with_offset(canvas_element, x + (2 if j % 2 == 0 else -2), y)
        action.release()
        action.perform()
    except MoveTargetOutOfBoundsException:
        # If we accidentally stepped out of bounds,
        # stop the current paint action and release the mouse button.
        try:
            action = webdriver.common.action_chains.ActionChains(driver)
            action.release()
            action.perform()
        except Exception:
            pass


def setup():
    """
    Setup the browser window and painting canvas.

    :return: The newly created web driver.
    """
    # Set up the window.
    log.info('Loading the original website...')
    driver = webdriver.Firefox()
    driver.get('http://sta.sh/muro')
    driver.maximize_window()
    driver.find_element_by_tag_name('html').send_keys(Keys.F11)
    time.sleep(5)
    # Pick the right tool.
    log.info('Picking the splatter brush...')
    driver.find_element_by_class_name('iconSplatter').click()
    # Remove all unwanted side bars.
    log.info('Removing side bars...')
    remove_class(driver, 'sideBar')
    remove_class(driver, 'topArea')
    remove_id(driver, 'overhead-collect')
    # Set the density slider.
    log.info('Setting density value to 100%')
    sliders = driver.find_elements_by_class_name('sliderProgress')
    # Density.
    change_slider(driver, sliders[2], 120)
    # Maximize the canvas.
    log.info('Maximizing canvas size...')
    window_size = driver.get_window_size()
    canvas_width = window_size['width']
    canvas_height = window_size['height']
    change_canvas_size(driver, 'selectionCanvas', canvas_width, canvas_height)
    change_canvas_size(driver, 'drawPlzCanvas', canvas_width, canvas_height)
    change_canvas_size(driver, 'canvasBuffer', canvas_width, canvas_height)
    change_canvas_size(driver, 'stagingBuffer', canvas_width, canvas_height)
    change_canvas_size(driver, 'marchingAnts', canvas_width, canvas_height)
    change_canvas_size(driver, 'canvasPaint', canvas_width, canvas_height, only_style=True)
    # Modify specific styles and positions.
    driver.execute_script(MODIFY_SCRIPT.format('middleArea', 'style.paddingRight', '0px'))
    driver.execute_script(MODIFY_SCRIPT.format('middleArea', 'style.height', '100%'))
    driver.execute_script(MODIFY_SCRIPT.format('drawPlzCanvas', 'style.left', '0px'))
    driver.execute_script(MODIFY_SCRIPT.format('drawPlzCanvas', 'style.top', '0px'))
    driver.execute_script(MODIFY_SCRIPT.format('drawPlzCanvas', 'width', canvas_width))
    driver.execute_script('document.getElementsByClassName("canvasPaint")[1].width = %d;' % canvas_width)
    driver.execute_script('document.getElementsByClassName("canvasPaint")[1].height = %d;' % canvas_height)
    # Hide the mouse cursor.
    log.info('Hiding mouse reticule...')
    driver.execute_script(MODIFY_SCRIPT.format('cursorPreview', 'style.visibility', 'hidden'))
    return driver


def main():
    """
    Paints based on colors received from the server.
    Usage: deviantArt.py [PORT]
    """
    with logbook.StreamHandler(sys.stdout):
        # Validate input parameters.
        port = DEFAULT_LISTENING_PORT if len(sys.argv) == 1 else sys.argv[1]
        # Connect to the server.
        context = zmq.Context()
        log.info('Waiting for painting requests (port: {0})...'.format(port))
        socket = context.socket(zmq.REP)
        socket.bind('tcp://*:{0}'.format(port))
        # Initialize the website.
        driver = setup()
        # Find the canvas width and height.
        window_size = driver.get_window_size()
        canvas_width = window_size['width']
        canvas_height = window_size['height']
        # Find the main canvas element.
        canvas_element = driver.find_element_by_class_name('drawPlzCanvas')
        # Start painting!
        log.info('Let\'s paint!')
        colors_counter = 0
        while True:
            message = socket.recv()
            log.info('Received request: {0}'.format(message))
            socket.send(OK_REPLY)
            log.info('Sent {0} back'.format(OK_REPLY))
            if message == STOP_MESSAGE:
                log.info('Stopping!')
                break
            # Pick the requested color.
            r, g, b = message.split(COLORS_DELIMITER)
            # Don't get to close to the borders.
            x = random.randint(0, canvas_width - 90)
            y = random.randint(0, canvas_height - 90)
            log.info('Current RGB color - ({0}, {1}, {2})'.format(r, g, b))
            log.info('Current coordinates - ({0}, {1})'.format(x, y))
            change_color(driver, r, g, b)
            # Change opacity and size randomly.
            sliders = driver.find_elements_by_class_name('sliderProgress')
            # Opacity.
            opacity = random.randint(MIN_OPACITY, MAX_OPACITY)
            change_slider(driver, sliders[0], opacity)
            # Size.
            size = random.randint(MIN_SIZE, MAX_SIZE)
            change_slider(driver, sliders[1], size)
            log.info('Opacity: {0}, Size: {1}'.format(opacity, size))
            # Paint!
            paint(driver, canvas_element, x, y)
            x_button = driver.find_elements_by_class_name('x')
            if len(x_button) > 0:
                x_button[0].click()
                driver.execute_script('window.onbeforeunload = function(e){};')
            colors_counter += 1
            if colors_counter >= COLORS_LIMIT:
                colors_counter = 0
                driver.close()
                driver.execute_script('window.onbeforeunload = function(e){};')
                # Initialize the website.
                driver = setup()
                # Find the canvas width and height.
                window_size = driver.get_window_size()
                canvas_width = window_size['width']
                canvas_height = window_size['height']
                # Find the main canvas element.
                canvas_element = driver.find_element_by_class_name('drawPlzCanvas')


if __name__ == '__main__':
    main()
