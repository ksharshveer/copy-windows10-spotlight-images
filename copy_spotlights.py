from os import path, makedirs, listdir, environ
from shutil import copy
from PIL import Image
from sys import argv, exit


def copy_spotlights_images(spotlights_dir, save_dir, split=True, filter_res=1920, img_ext=".png", dir_land="landscape", dir_port="portrait"):
  """
  For windows users, copies beautifull images stored on their machine, called 'Windows Spotlights' to a directory of their choice.

  Parameters:
    spotlights_dir (str): directory location where windows_spotlights are stored
    save_dir (str): directory location where the user wants to save spotlights images
    split (boolean): saves images inside save_dir in landscape and portrait folders. Default True
    filter_res (int): defautl resolution used to determine minimum width of an image to decide
      if it's a portrait image or landscape image. Ignores images with resolution less than defined
      resolution. Default 1920
    img_ext (str): the extension to use when saving images. Default ".png"
    dir_land (str): landscape directory name. Default "landscape"
    dir_port (str): portrait directory name. Default "portrait"
    
  """

  if not path.isdir(save_dir):
    raise Exception(f"'{save_dir}' does not seem to be a valid directory!")

  complete_landscape_path, complete_portrait_path = save_dir, save_dir

  if split:
    # complete paths to landscape and portrait directories inside the save location
    complete_landscape_path = path.join(save_dir, dir_land)
    complete_portrait_path = path.join(save_dir, dir_port)

    # make directories if they don't exist already
    makedirs(complete_landscape_path)
    makedirs(complete_portrait_path)

  for spotlight in listdir(spotlights_dir):
    sl = path.join(spotlights_dir, spotlight)
    
    im = Image.open(sl)

    if (int(im.size[0]) >= filter_res):
      copy(sl, path.join(complete_landscape_path, spotlight+img_ext))
    elif (int(im.size[1]) >= filter_res):
      copy(sl, path.join(complete_portrait_path, spotlight+img_ext))


if __name__ == "__main__":

  # Known directory location path where windows stores spotlight images
  HOME = environ.get("HOME")
  SPOTLIGHT_DIR = path.join(HOME, 'AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets')

  if len(argv) < 2:
    exit("No argument for a save directory was received. Exiting!")

  save_dir = argv[1]
  split = True
  
  if len(argv) == 3:
    split = False

  copy_spotlights_images(SPOTLIGHT_DIR, save_dir, split)
  