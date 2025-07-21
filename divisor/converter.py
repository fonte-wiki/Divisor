import os
import re
import yaml

ASSET_REGEX = re.compile(r"(!?\[.*?\]\()((?!https?:\/\/|#|mailto:).*?)\)")

class Converter:
    def __init__(self, config):
        self.config = config

    def convert_file(self, source_path, dest_path, source_repo_dir):
        """
        Converts a single file.
        """
        with open(source_path, "r") as f:
            content = f.read()

        # Separate front matter from content
        match = re.search(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
        if match:
            front_matter_str = match.group(1)
            content_body = match.group(2)
            # Parse existing front matter
            try:
                front_matter = yaml.safe_load(front_matter_str)
            except yaml.YAMLError:
                front_matter = {}
        else:
            front_matter = {}
            content_body = content

        # Adapt front matter
        front_matter["layout"] = "default"
        if "title" not in front_matter:
            front_matter["title"] = self.get_title_from_content(content_body)

        pass

        # Rewrite internal links
        content_body = self.rewrite_internal_links(content_body)

        # Add description paragraph if it's the home page
        if dest_path.endswith("index.md") and self.config.site_metadata.description:
            content_body = f"***{self.config.site_metadata.description}***\n\n" + content_body

        # Re-assemble the file
        new_content = self.add_front_matter(content_body, front_matter)

        with open(dest_path, "w") as f:
            f.write(new_content)

        return content_body, front_matter, new_content

    def get_title_from_content(self, content):
        """
        Extracts the title from the first heading in the content.
        """
        match = re.search(r"^#\s+(.*)", content, re.MULTILINE)
        if match:
            return match.group(1)
        return "Untitled"

    def add_front_matter(self, content, front_matter):
        """
        Adds front matter to the beginning of the content.
        """
        fm_string = "---\n"
        for key, value in front_matter.items():
            fm_string += f"{key}: {value}\n"
        fm_string += "---\n\n"
        return fm_string + content

    def rewrite_internal_links(self, content):
        """
        Rewrites internal links to be compatible with Jekyll.
        """
        def replace_link(match):
            original_path_str = match.group(2)
            if not original_path_str.endswith(".md") and not any(original_path_str.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".mp3", ".mp4"]):
                # It's a page link without the .md extension
                subpages_folder = self.config.content_mapping.subpages_folder
                if original_path_str.startswith(f"/{subpages_folder}"):
                    path = original_path_str[len(subpages_folder) + 1:]
                else:
                    path = original_path_str
                new_path = path
                return f"{match.group(1)}{{{{ '{new_path}' | relative_url }}}})"
            elif original_path_str.endswith(".md"):
                # It's a page link
                subpages_folder = self.config.content_mapping.subpages_folder
                if original_path_str.startswith(f"/{subpages_folder}"):
                    path = original_path_str[len(subpages_folder) + 1:]
                else:
                    path = original_path_str
                new_path = path.replace(".md", "")
                return f"{match.group(1)}{{{{ '{new_path}' | relative_url }}}})"
            elif any(original_path_str.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".mp3", ".mp4"]):
                # It's a media link
                file_name = os.path.basename(original_path_str)
                new_path = f"/assets/media/{file_name}"
                return f"{match.group(1)}{{{{ '{new_path}' | relative_url }}}})"
            else:
                # Not a link we want to rewrite
                return match.group(0)

        return ASSET_REGEX.sub(replace_link, content)
