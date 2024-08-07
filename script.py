import json
import re
import os

manifest_path = '/Users/sairaakhter/Downloads/testManuscript/index.json'
updated_manifest_path = '/Users/sairaakhter/Downloads/testManuscript/updated_index.json'


with open(manifest_path, 'r') as f:
    manifest = json.load(f)

def update_urls(manifest):
    for item in manifest['items']:
        for annotation_page in item['items']:
            for annotation in annotation_page['items']:
                # Update to convert TIFF to JPEG
                if 'body' in annotation and 'id' in annotation['body']:
                    original_url = annotation['body']['id']
                    new_url = re.sub(r"/iiif/3/(.*)\.tif", r"/iiif/2/\1/full/full/0/default.jpg", original_url)
                    annotation['body']['id'] = new_url

                # Update or add the thumbnail URL
                body_id = annotation['body']['id']
                base_filename = re.search(r'/iiif/2/(.*)/full/full/0/default.jpg', body_id).group(1)
                thumb_url = f"http://localhost:8182/iiif/2/{base_filename}/full/90,/0/default.jpg"

                if 'thumbnail' in item:
                    for thumbnail in item['thumbnail']:
                        if 'id' in thumbnail and thumbnail['id'].endswith("thumb.jpg"):
                            thumbnail['id'] = thumb_url
                else:
                    item['thumbnail'] = [{
                        "id": thumb_url,
                        "type": "Image"
                    }]
    return manifest

# Update URLs in the manifest
updated_manifest = update_urls(manifest)

# Save updated manifest
with open(updated_manifest_path, 'w') as f:
    json.dump(updated_manifest, f, indent=2)

print("Manifest updated successfully.")
print(f"Updated manifest saved at: {updated_manifest_path}")
