# Mosaic Image Generator

This project generates a mosaic image by using smaller images (avatars) to recreate a target image. It includes functionalities to scrape images from Google, process and store average colors, and create the mosaic image.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Notes](#notes)
- [License](#license)

## Requirements

Ensure you have the following libraries installed:

```bash
pip install argparse
pip install Pillow
pip install requests
pip install selenium
pip install concurrent.futures
pip install pickle-mixin
```

Additionally, download the required NLTK data if you haven't already:

```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
```

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/mosaic-image-generator.git
cd mosaic-image-generator
```

2. **Download ChromeDriver**:

Download the ChromeDriver that matches your version of Chrome from [here](https://sites.google.com/chromium.org/driver/). Place the `chromedriver` executable in the directory specified in the `webdriver_executable` path within your code.

## Usage

1. **Scrape Images**:

To scrape images from Google and save them in the specified directory, run the script with the following command:

```bash
python mosaic_image_generator.py
```

2. **Create Mosaic Image**:

To create a mosaic image using the scraped avatars, run the following command:

```bash
python mosaic_image_generator.py <user_id> <image_path> <avatars_path>
```

- `<user_id>`: A unique user ID.
- `<image_path>`: Path to the target image you want to convert into a mosaic.
- `<avatars_path>`: Path to the directory containing the avatars.

### Example

```bash
python mosaic_image_generator.py 1 "path/to/target/image.jpg" "path/to/avatars"
```

## Notes

- The script will automatically handle the resizing and processing of images.
- You can customize the `TILE_SIZE` and other parameters in the script to adjust the mosaic output.
- The `data` and `output_images` directories will be created in the current working directory to store processed data and output images, respectively.
