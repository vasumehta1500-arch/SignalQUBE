from pathlib import Path
import requests
import zipfile


FDA_PAGE = (
    "https://fis.fda.gov/extensions/"
    "FPD-QDE-FAERS/FPD-QDE-FAERS.html"
)


class FAERSDownloader:

    def __init__(self, year=2025, quarter="Q4"):

        self.year = str(year)
        self.quarter = quarter.upper()

        self.output_path = Path(
            f"data/raw/{self.year}{self.quarter}"
        )

        self.output_path.mkdir(
            parents=True,
            exist_ok=True
        )

    def get_page(self):

        print("=" * 60)
        print("CONNECTING TO FDA")
        print("=" * 60)

        response = requests.get(
            FDA_PAGE,
            timeout=60
        )

        response.raise_for_status()

        return response.text

    def find_download_url(self):

        html = self.get_page()

        # The FDA page contains the quarterly
        # download links directly in the HTML.
        #
        # We search for the 2025 Q4 ASCII ZIP.
        search_terms = [
            "2025Q4",
            "2025_Q4",
            "2025-q4",
            "2025%20q4"
        ]

        for line in html.splitlines():

            lower_line = line.lower()

            if (
                "ascii" in lower_line
                and "zip" in lower_line
                and "2025" in lower_line
            ):

                # Try to extract href
                if 'href="' in lower_line:

                    start = line.find('href="') + 6
                    end = line.find('"', start)

                    href = line[start:end]

                    if href.startswith("//"):
                        href = "https:" + href

                    elif href.startswith("/"):
                        href = (
                            "https://fis.fda.gov"
                            + href
                        )

                    elif href.startswith("./"):
                        href = (
                            "https://fis.fda.gov/"
                            + href[2:]
                        )

                    if href.startswith("http"):

                        print(
                            "\nFDA download URL found:"
                        )
                        print(href)

                        return href

        raise RuntimeError(
            "Could not find the 2025 Q4 ASCII "
            "download link on the FDA page."
        )

    def download(self):

        url = self.find_download_url()

        zip_path = (
            self.output_path
            / f"FAERS_{self.year}_{self.quarter}.zip"
        )

        print("=" * 60)
        print("DOWNLOADING FDA FAERS DATA")
        print("=" * 60)

        print(f"Year      : {self.year}")
        print(f"Quarter   : {self.quarter}")
        print(f"Destination: {zip_path}")

        response = requests.get(
            url,
            stream=True,
            timeout=300
        )

        response.raise_for_status()

        total_bytes = 0

        with open(zip_path, "wb") as file:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:
                    file.write(chunk)
                    total_bytes += len(chunk)

        size_mb = (
            total_bytes / (1024 * 1024)
        )

        print(
            f"\nDownloaded: {size_mb:.2f} MB"
        )

        return zip_path

    def extract(self, zip_path):

        print("\nExtracting FDA files...")

        with zipfile.ZipFile(
            zip_path,
            "r"
        ) as zip_file:

            zip_file.extractall(
                self.output_path
            )

        print(
            "\nFiles extracted to:"
        )
        print(self.output_path)

        return self.output_path


def main():

    downloader = FAERSDownloader(
        year=2025,
        quarter="Q4"
    )

    zip_path = downloader.download()

    downloader.extract(zip_path)

    print("\n" + "=" * 60)
    print("FDA FAERS DOWNLOAD COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()