import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class MetaShield:
    def __init__(self):
        # Configuration for automated paths
        self.raw_dir = os.path.join("data", "raw")
        self.processed_dir = os.path.join("data", "processed")
        self.supported_formats = (".jpg", ".jpeg", ".png")

        # Ensure directories exist
        for directory in [self.raw_dir, self.processed_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def get_decimal_from_dms(self, dms, ref):
        """Convert DMS coordinates to Decimal Degrees."""
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
        if ref in ["S", "W"]:
            return -(degrees + minutes + seconds)
        return degrees + minutes + seconds

    def process_images(self):
        """Scan data/raw and process all supported images automatically."""
        files = [
            f
            for f in os.listdir(self.raw_dir)
            if f.lower().endswith(self.supported_formats)
        ]

        if not files:
            print(
                f"[*] No images found in {self.raw_dir}. Please add files and try again."
            )
            return

        print(f"[*] Found {len(files)} image(s) in {self.raw_dir}\n")

        for filename in files:
            raw_path = os.path.join(self.raw_dir, filename)
            processed_path = os.path.join(self.processed_dir, f"cleaned_{filename}")

            print(f"--- Processing: {filename} ---")

            # 1. Extract and Analyze
            has_metadata = self.extract_metadata(raw_path)

            # 2. Automatically Sanitize if metadata exists
            if has_metadata:
                self.remove_metadata(raw_path, processed_path)
            else:
                print(f"    [i] Skipping sanitization for {filename} (Already clean).")
            print("-" * (16 + len(filename)))

    def extract_metadata(self, image_path):
        try:
            img = Image.open(image_path)
            exif_data = img._getexif()

            if not exif_data:
                print("    [-] No sensitive metadata found.")
                return False

            info = {}
            gps_info = {}

            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo":
                    for g_tag_id in value:
                        g_tag = GPSTAGS.get(g_tag_id, g_tag_id)
                        gps_info[g_tag] = value[g_tag_id]
                else:
                    info[tag] = value

            # Analysis Display
            sensitive_tags = ["Make", "Model", "Software", "DateTime"]
            for k in sensitive_tags:
                if k in info:
                    print(f"    > {k}: {info[k]}")

            if gps_info and "GPSLatitude" in gps_info:
                lat = self.get_decimal_from_dms(
                    gps_info["GPSLatitude"], gps_info["GPSLatitudeRef"]
                )
                lon = self.get_decimal_from_dms(
                    gps_info["GPSLongitude"], gps_info["GPSLongitudeRef"]
                )
                print(f"    [!] GPS DETECTED: {lat}, {lon}")
                print(f"    [!] Map: https://www.google.com/maps?q={lat},{lon}")

            return True
        except Exception as e:
            print(f"    [!] Extraction error: {e}")
            return False

    def remove_metadata(self, input_path, output_path):
        try:
            img = Image.open(input_path)
            data = list(img.getdata())
            img_clean = Image.new(img.mode, img.size)
            img_clean.putdata(data)
            img_clean.save(output_path)
            print(f"    [V] SANITIZED: Saved to {output_path}")
        except Exception as e:
            print(f"    [!] Sanitization failed: {e}")


if __name__ == "__main__":
    print("========================================")
    print("      METASHIELD - AUTO SCANNER        ")
    print("========================================")

    scanner = MetaShield()
    scanner.process_images()

    print("\n[V] All tasks completed.")
