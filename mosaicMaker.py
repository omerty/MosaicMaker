import argparse
import os
from PIL import Image
import math
import sys
import pickle
import warnings
import concurrent.futures
from ImageScrapper import GoogleImageScraper
from patch import webdriver_executable
import shutil

def color_distance(c1, c2):
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def get_average_color(image):
    input_image = image.resize((1, 1))
    return input_image.getpixel((0, 0))

def find_file(target_color, average_colors, files):
    min_index = 0
    min_distance = sys.maxsize
    for i in range(len(average_colors)):
        curr_color = average_colors[i]
        distance = color_distance(target_color, curr_color)
        if distance < min_distance:
            min_index = i
            min_distance = distance
    return files[min_index]

def resize_target_image(input_image):
    warnings.filterwarnings("ignore")
    w, h = input_image.size
    SCALE = int(math.sqrt(25000000) // max(w, h))  # with tile size of 35, under 8mb for disc
    input_image = input_image.resize((w * SCALE, h * SCALE)).convert("RGB")
    w, h = input_image.size
    input_image = input_image.crop((0, 0, w - w % TILE_SIZE, h - h % TILE_SIZE))
    return input_image

TILE_SIZE = 50

def create_mosaic(user, server_dir, image_path, avatars_path):
    print(avatars_path)
    tiles_dir = avatars_path
    input_image = resize_target_image(Image.open(image_path).copy())
    w, h = input_image.size
    output_image = Image.new("RGB", (w, h))
    data_dir = os.path.join(server_dir, "data")

    files = []
    average_colors = []
    PIK_files = os.path.join(data_dir, "files.dat")
    PIK_average_colors = os.path.join(data_dir, "average_colors.dat")

    if os.path.exists(data_dir) and os.path.exists(PIK_files) and os.path.exists(PIK_average_colors):
        with open(PIK_files, "rb") as f:
            files = pickle.load(f)
        with open(PIK_average_colors, "rb") as f:
            average_colors = pickle.load(f)
        print(f'Loaded {len(files)} images and {len(average_colors)} average colors.')
    else:
        for root, subFolders, xfiles in os.walk(tiles_dir):
            for filename in xfiles:
                lower_name = filename.lower()
                if lower_name.endswith(".jpg") or lower_name.endswith(".jpeg") or lower_name.endswith(".png"):
                    image = Image.open(os.path.join(root, filename)).resize((TILE_SIZE, TILE_SIZE)).convert("RGB")
                    average_color = get_average_color(image)
                    average_colors.append(average_color)
                    files.append(image)
                    print(f'Reading {filename:40.40}', flush=True, end='\r')
        print(f'Read {len(files)} images and computed their average colors.')

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        with open(PIK_files, "wb") as f:
            pickle.dump(files, f)
        with open(PIK_average_colors, "wb") as f:
            pickle.dump(average_colors, f)
        print(f'Saved {len(files)} images and {len(average_colors)} average colors.')

    num_r, num_c = h // TILE_SIZE, w // TILE_SIZE

    count = 0
    total = num_r * num_c
    for r in range(num_r):  
        for c in range(num_c):
            x = c * TILE_SIZE
            y = r * TILE_SIZE
            curr_image = input_image.crop((x, y, x + TILE_SIZE, y + TILE_SIZE))
            average_color = get_average_color(curr_image)
            file = find_file(average_color, average_colors, files)
            output_image.paste(file, (x, y, x + TILE_SIZE, y + TILE_SIZE))
            count += 1
            print(f'Generating image: {round(count / total * 100, 2)}%', flush=True, end='\r')
    output_dir = os.path.join(server_dir, "output_images")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_image_path = os.path.join(output_dir, f'output_{user.id}.jpeg')
    output_image.save(output_image_path, "jpeg")
    return output_image_path

def main():
    parser = argparse.ArgumentParser(description="Create a mosaic image.")
    parser.add_argument('user_id', type=int, help='User ID for the mosaic image')
    parser.add_argument('image_path', type=str, help='Path to the target image')
    parser.add_argument('avatars_path', type=str, help='Path to the avatars directory')

    args = parser.parse_args()

    user = type('User', (object,), {'id': args.user_id})()  # Creating a dummy user object with an ID attribute
    server_dir = os.getcwd()  # Use current working directory for server_dir

    output_image_path = create_mosaic(user, server_dir, args.image_path, args.avatars_path)
    print(f"Mosaic image created at: {output_image_path}")


def delete_directory(directory):
    try:
        shutil.rmtree(directory)
        print(f"The directory {directory} has been deleted.")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")


def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        webdriver_path, 
        image_path, 
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed)
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)

    # Release resources
    del image_scraper

if __name__ == "__main__":
    # Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'C:/Users/mdome/anaconda3/Lib/site-packages/selenium', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'avatars'))

    directory_to_delete = os.path.normpath(os.path.join(os.getcwd(), 'data'))
    delete_directory(directory_to_delete)

    directory_to_delete = os.path.normpath(os.path.join(os.getcwd(), 'output_images'))
    delete_directory(directory_to_delete)

    directory_to_delete = os.path.normpath(os.path.join(os.getcwd(), 'avatars'))
    delete_directory(directory_to_delete)

    # Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys = list(set(["Cats"]))

    # Parameters
    number_of_images = 100               # Desired number of images
    headless = True                      # True = No Chrome GUI
    min_resolution = (0, 0)              # Minimum desired image resolution
    max_resolution = (9999, 9999)        # Maximum desired image resolution
    max_missed = 10                      # Max number of failed images before exit
    number_of_workers = 1                # Number of "workers" used
    keep_filenames = False               # Keep original URL image filenames

    # Run each search_key in a separate thread
    # Automatically waits for all threads to finish
    # Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)

    main()
