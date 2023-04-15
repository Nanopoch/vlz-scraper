from enum import Enum
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os.path


# class that represents a page of the VectorZoneLogo website
class AlphabeticPage:
    class SVGType(Enum):
        LOGO = "logo"
        RECTANGLE = "rectangle"
        HORIZONTAL = "horizontal"
        VERTICAL = "vertical"
        WORDMARK = "wordmark"
        TILE = "tile"
        OFFICIAL = "official"

    def __init__(self, category: str):
        self.category = category

        self.numb_icons = 0
        self.numb_icons_skipped = 0

        self.numb_rectangles = 0
        self.numb_rectangles_skipped = 0

        self.numb_horizontals = 0
        self.numb_horizontals_skipped = 0

        self.numb_verticals = 0
        self.numb_verticals_skipped = 0

        self.numb_wordmarks = 0
        self.numb_wordmarks_skipped = 0

        self.numb_tiles = 0
        self.numb_tiles_skipped = 0

        self.numb_official = 0
        self.numb_official_skipped = 0

    def increase_counter_by(self, counter: SVGType, value: int):
        if value > 0:
            if counter == self.SVGType.LOGO:
                self.numb_icons += value
            elif counter == self.SVGType.RECTANGLE:
                self.numb_rectangles += value
            elif counter == self.SVGType.HORIZONTAL:
                self.numb_horizontals += value
            elif counter == self.SVGType.VERTICAL:
                self.numb_verticals += value
            elif counter == self.SVGType.WORDMARK:
                self.numb_wordmarks += value
            elif counter == self.SVGType.TILE:
                self.numb_tiles += value
            elif counter == self.SVGType.OFFICIAL:
                self.numb_official += value
        elif value == -1:
            if counter == self.SVGType.LOGO:
                self.numb_icons_skipped += 1
            elif counter == self.SVGType.RECTANGLE:
                self.numb_rectangles_skipped += 1
            elif counter == self.SVGType.HORIZONTAL:
                self.numb_horizontals_skipped += 1
            elif counter == self.SVGType.VERTICAL:
                self.numb_verticals_skipped += 1
            elif counter == self.SVGType.WORDMARK:
                self.numb_wordmarks_skipped += 1
            elif counter == self.SVGType.TILE:
                self.numb_tiles_skipped += 1
            elif counter == self.SVGType.OFFICIAL:
                self.numb_official_skipped += 1

    def get_numb_downloaded(self):
        return self.numb_icons + self.numb_rectangles + self.numb_wordmarks + self.numb_tiles + self.numb_official + self.numb_horizontals + self.numb_verticals

    def get_numb_skipped(self):
        return self.numb_icons_skipped + self.numb_rectangles_skipped + self.numb_wordmarks_skipped + self.numb_tiles_skipped + self.numb_official_skipped + self.numb_horizontals_skipped + self.numb_verticals_skipped


# downloads and saves an SVG file from a given URL and name
def download_and_save_svg(url: str, name: str):
    if os.path.isfile("svg/" + name + ".svg"):
        print("Logo already exists: " + name)
        return -1

    svg_response = requests.get(url)

    if svg_response.status_code != 200:
        error_explanation = " (does not exist)" if svg_response.status_code == 404 else f" (status code: {svg_response.status_code})"
        print(f"Error downloading logo: {name} {error_explanation}")
        return 0

    with open("svg/" + name + ".svg", "w", encoding="utf8") as f:
        f.write(svg_response.text)

    return 1


# prints a full report of the scraping by AlphabeticPage in a pretty format
def print_report(pages_map: list[AlphabeticPage]):
    print("Scraping report:\n")

    total_icons = 0
    total_icons_skipped = 0
    total_rectangles = 0
    total_rectangles_skipped = 0
    total_horizontal = 0
    total_horizontal_skipped = 0
    total_vertical = 0
    total_vertical_skipped = 0
    total_wordmarks = 0
    total_wordmarks_skipped = 0
    total_tiles = 0
    total_tiles_skipped = 0
    total_official = 0
    total_official_skipped = 0

    total_downloaded = 0
    total_skipped = 0

    for page in pages_map:
        total_icons += page.numb_icons
        total_icons_skipped += page.numb_icons_skipped

        total_rectangles += page.numb_rectangles
        total_rectangles_skipped += page.numb_rectangles_skipped

        total_horizontal += page.numb_horizontals
        total_horizontal_skipped += page.numb_horizontals_skipped

        total_vertical += page.numb_verticals
        total_vertical_skipped += page.numb_verticals_skipped

        total_wordmarks += page.numb_wordmarks
        total_wordmarks_skipped += page.numb_wordmarks_skipped

        total_tiles += page.numb_tiles
        total_tiles_skipped += page.numb_tiles_skipped

        total_official += page.numb_official
        total_official_skipped += page.numb_official_skipped

        total_downloaded += page.get_numb_downloaded()
        total_skipped += page.get_numb_skipped()

        print(f"Page {page.category}:")
        print(
            f"Number of logos: {str(page.numb_icons)} (skipped: {str(page.numb_icons_skipped)})")
        print(
            f"Number of rectangles: {str(page.numb_rectangles)} (skipped: {str(page.numb_rectangles_skipped)})")
        print(
            f"Number of horizontals: {str(page.numb_horizontals)} (skipped: {str(page.numb_horizontals_skipped)})")
        print(
            f"Number of verticals: {str(page.numb_verticals)} (skipped: {str(page.numb_verticals_skipped)})")
        print(
            f"Number of wordmarks: {str(page.numb_wordmarks)} (skipped: {str(page.numb_wordmarks_skipped)})")
        print(
            f"Number of tiles: {str(page.numb_tiles)} (skipped: {str(page.numb_tiles_skipped)})")
        print(
            f"Number of official: {str(page.numb_official)} (skipped: {str(page.numb_official_skipped)})")

        print(f"Number of all: {str(page.get_numb_downloaded())}\n")

    print(f"Total logos: {total_icons} (skipped: {total_icons_skipped})")
    print(
        f"Total rectangles: {total_rectangles} (skipped: {total_rectangles_skipped})")
    print(
        f"Total horizontals: {total_horizontal} (skipped: {total_horizontal_skipped})")
    print(
        f"Total verticals: {total_vertical} (skipped: {total_vertical_skipped})")
    print(
        f"Total wordmarks: {total_wordmarks} (skipped: {total_wordmarks_skipped})")
    print(f"Total tiles: {total_tiles} (skipped: {total_tiles_skipped})")
    print(
        f"Total official: {total_official} (skipped: {total_official_skipped})")

    print(f"Total: {total_downloaded} (skipped: {total_skipped})")


if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    # list of all pages to scrape
    pages_map = [AlphabeticPage('abc'), AlphabeticPage('def'), AlphabeticPage('ghi'),
                 AlphabeticPage('jkl'), AlphabeticPage('mno'), AlphabeticPage('pgrs'), AlphabeticPage('tuv'), AlphabeticPage('wxyz'), AlphabeticPage('0123456789')]

    driver.get("https://www.vectorlogo.zone/logos/index.html")

    try:
        # iterate over all pages and get all SVG links
        for i, page in enumerate(pages_map):
            print(
                f"\n\nScraping page {i + 1} of {len(pages_map)} ({page.category})\n\n")

            svg_links = [svg_element.get_property(
                "href") for svg_element in driver.find_elements(By.CSS_SELECTOR, f"#vector{page.category} > a")]

            # iterate over all SVG links and download them
            for link in svg_links:
                link = str(link)

                logo_name = link.split("/")[-2]

                icon_file_name = logo_name + "-icon.svg"

                rectangle_file_name = logo_name + "-ar21.svg"
                rectangle_local_file_name = logo_name + "-rectangle.svg"

                horizontal_file_name = logo_name + "-horizontal.svg"

                vertical_file_name = logo_name + "-vertical.svg"

                wordmark_file_name = logo_name + "-wordmark.svg"

                tile_file_name = logo_name + "-tile.svg"

                official_file_name = logo_name + "-official.svg"

                print(f"\nDownloading logo collection for: { logo_name }")

                page.increase_counter_by(AlphabeticPage.SVGType.LOGO, download_and_save_svg(
                    "https://www.vectorlogo.zone/logos/" + logo_name + "/" + icon_file_name, icon_file_name))
                page.increase_counter_by(AlphabeticPage.SVGType.RECTANGLE, download_and_save_svg("https://www.vectorlogo.zone/logos/" +
                                                                                                 logo_name + "/" + rectangle_file_name, rectangle_local_file_name))
                page.increase_counter_by(AlphabeticPage.SVGType.HORIZONTAL, download_and_save_svg(
                    "https://www.vectorlogo.zone/logos/" + logo_name + "/" + horizontal_file_name, horizontal_file_name))
                page.increase_counter_by(AlphabeticPage.SVGType.VERTICAL, download_and_save_svg(
                    "https://www.vectorlogo.zone/logos/" + logo_name + "/" + vertical_file_name, vertical_file_name))
                page.increase_counter_by(AlphabeticPage.SVGType.WORDMARK, download_and_save_svg(
                    "https://www.vectorlogo.zone/logos/" + logo_name + "/" + wordmark_file_name, wordmark_file_name))
                page.increase_counter_by(AlphabeticPage.SVGType.TILE, download_and_save_svg(
                    "https://www.vectorlogo.zone/logos/" + logo_name + "/" + tile_file_name, tile_file_name))
                page.increase_counter_by(AlphabeticPage.SVGType.OFFICIAL, download_and_save_svg(
                    "https://www.vectorlogo.zone/logos/" + logo_name + "/" + official_file_name, official_file_name))

    # in case of an error (or user interruption), print the report and exit
    finally:
        print_report(pages_map)

        print('\nPlease wait while the browser is closing... (this may take a few seconds)')

        driver.quit()

        sys.exit(0)
