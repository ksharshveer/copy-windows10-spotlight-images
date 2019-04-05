from os import path, makedirs, listdir
# needed to import Path from pathlib because 'HOME' environment variable using os.path returned None on windows command line
from pathlib import Path
from shutil import copy
from argparse import ArgumentParser

from PIL import Image


def find_images(dir):
  """Given a directory, finds out which files in the root of the directory are images

  Arguments:
    dir {str} -- directory location to scan for image files

  Raises:
    AssertionError -- if given directory is not valid

  Returns:
    list -- list of filenames found in the given directory which are images
  """
  assert path.isdir(dir)==True
  
  im_files = []
  
  for item in listdir(dir):
    item_path = path.normpath(path.join(dir, item))

    if path.isfile(item_path):
      try:
        Image.open(item_path)
        im_files.append(item)
      except IOError:
        pass
    
  return im_files


def copy_spotlights_images(spotlights_dir, save_dir, split=True, min_res=1920, dir_land="landscape", dir_port="portrait", dir_other="other"):
  """For Windows 10 users, copies beautiful images stored on their machine, called 'Windows Spotlights' to a directory of their choice.
  
  Arguments:
    spotlights_dir {str} -- directory location where windows 10 stores spotlight images
    save_dir {str} -- directory location where spotlight images will be copied to
  
  Keyword Arguments:
    split {bool} -- split images into different folders based on types such as landscape and portrait (default: {True})
    min_res {int} -- ignore images with horizontal or vertical resolution lower than min_res value,  (default: {1920})
    dir_land {str} -- directory name in which to store landscape images (default: {"landscape"})
    dir_port {str} -- directory name in which to store portrait images (default: {"portrait"})
    dir_other {str} -- directory name in which to store images other than portrait or landscape type (default: {"other"})
  
  Raises:
    Exception -- raises exception if save_dir is not valid
  """
  if not path.isdir(save_dir):
    raise Exception(f"'{save_dir}' does not seem to be a valid directory!")

  complete_landscape_path, complete_portrait_path, complete_other_path = "", "", ""

  if split:
    # get complete paths to landscape, portrait, and other directories inside the save directory
    complete_landscape_path = path.normpath(path.join(save_dir, dir_land))
    complete_portrait_path = path.normpath(path.join(save_dir, dir_port))
    complete_other_path = path.normpath(path.join(save_dir, dir_other))

    # make required directories if they don't exist
    if not path.isdir(complete_landscape_path):
      makedirs(complete_landscape_path)
    if not path.isdir(complete_portrait_path):
      makedirs(complete_portrait_path) 
    if not path.isdir(complete_other_path):
      makedirs(complete_other_path) 

  else:
    # don't copy spotlight images into different folders
    complete_landscape_path, complete_portrait_path, complete_other_path = save_dir, save_dir, save_dir

  for image_file in find_images(spotlights_dir):
    image_file_full_path = path.normpath(path.join(spotlights_dir, image_file))

    im = Image.open(image_file_full_path)

    # save image with an extension as read by PIL.Image module
    save_image_file_name = image_file + "." + im.format
    where = None
    
    im_width, im_height = int(im.size[0]), int(im.size[1])

    if im_width >= min_res or im_height >= min_res:
      if (im_height < im_width):
        where = path.normpath(path.join(complete_landscape_path, save_image_file_name))

      elif (im_width < im_height):
        where = path.normpath(path.join(complete_portrait_path, save_image_file_name))
        
      else:
        where = path.normpath(path.join(complete_other_path, save_image_file_name))
    
    if where != None:
      copy(image_file_full_path, where)
    

if __name__ == "__main__":

  # Argument Parser to enable use of this program using bash terminal
  parser = ArgumentParser()
  parser.add_argument("save_dir", type=str, help="directory location where spotlight images will be copied to")
  parser.add_argument("--no-split", dest="no_split", action="store_true", help="portrait and landscape images will not be placed into separate folders")
  parser.add_argument("--min-res", dest="min_res", type=int, help="ignore images with horizontal or vertical resolution lower than min_res value, default:1920", default=1920)
  parser.add_argument("--dir-land", dest="dir_land", type=str, help="directory name in which to store landscape images, default:landscape", default="landscape")
  parser.add_argument("--dir-port", dest="dir_port", type=str, help="directory name in which to store portrait images, default:portrait", default="portrait")
  parser.add_argument("--dir-other", dest="dir_other", type=str, help="directory name in which to store images of equal resolution, default:other", default="other")
  args = parser.parse_args()

  # Known directory location path where windows stores spotlight images
  home = str(Path.home())
  spotlight_dir = path.join(home, 'AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets')

  save_dir = args.__getattribute__("save_dir")
  split = not args.__getattribute__("no_split")
  min_res = args.__getattribute__("min_res")
  dir_land = args.__getattribute__("dir_land")
  dir_port = args.__getattribute__("dir_port")
  dir_other = args.__getattribute__("dir_other")

  copy_spotlights_images(spotlight_dir, save_dir, split, min_res, dir_land, dir_port, dir_other)
  