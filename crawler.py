import os

import flickrapi
import requests

# Not sure which image sizes the original dataset has chosen. Most likely not "Original" - too large.
_SIZE = "Original"


def _download_image(image_url, filename):
  img_data = requests.get(image_url).content
  with open(filename, 'wb') as f:
    f.write(img_data)


class Crawler(object):
  def __init__(self, class_file='all_data.txt', data_dir='data'):
    self._photo_ids = self._parse_metadata(class_file)
    self._data_dir = data_dir
    self._flickr = flickrapi.FlickrAPI(
      api_key='your_api_key',
      secret='your_secret_key',
    )

  def _parse_metadata(self, class_file):
    with open(class_file) as fid:
      lines = fid.readlines()
    photo_ids = [line.split(' ')[1] for line in lines]
    return photo_ids

  def _get_xml(self, photo_id):
    for retry_idx in range(10):
      try:
        root = self._flickr.photos.getSizes(photo_id=photo_id)
        break
      except flickrapi.exceptions.FlickrError as err:
        if "1: Photo not found" in repr(err):
          print(f"  Photo not found.")
          root = None
          break
        if "Status code 500 received" in repr(err):
          print(f"  Error code 500, retry {retry_idx + 1}.")
          continue
        else:
          raise err
    return root

  def crawl(self):
    idx_photo_pairs = list(zip(enumerate(self._photo_ids)))
    for (idx, photo_id), in idx_photo_pairs:
      filename = os.path.join(self._data_dir, f'{idx:05d}.jpg')
      print(f"Downloading file {filename}")
      root = self._get_xml(photo_id)
      if root is None:
        continue
      url = (root.find('sizes').findall(f"size[@label='{_SIZE}']")[0]
        .attrib['source'])
      print(f"  url: {url}")
      _download_image(image_url=url, filename=filename)


def main():
  crawler = Crawler()
  crawler.crawl()


if __name__ == "__main__":
  main()
