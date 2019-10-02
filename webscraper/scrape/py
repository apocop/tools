#python3
"""Scrapes text from a single webpage to the terminal.

Example Usage:

python3 scrape.py --url=https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D1%88%D0%BA%D0%B0
"""

from absl import app
from absl import flags
from bs4 import BeautifulSoup
import urllib3

FLAGS = flags.FLAGS

flags.DEFINE_string('url', None, "URL to scrape.")
flags.mark_flag_as_required("url")


def main(argv):
    del argv # Unused.

    url = FLAGS.url
    headers = {
      'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
    }

    http = urllib3.PoolManager()
    request = http.request('GET', url, headers=headers)
    source = request.data

    # Remove HTML.
    soup = BeautifulSoup(source, 'lxml')

    # Remove Scripts.
    for script in soup(['script', 'style']):
        script.extract()

    text = soup.get_text()

    # Remove blank lines.
    clean_text = "".join([line for line in text.strip().splitlines(True) if line.strip()])
    print(clean_text)


if __name__ == '__main__':
    app.run(main)
